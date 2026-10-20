"""Opt-in K3 network target preflight. Pure validation: never performs a request.

A URL is not permission to probe it. Network execution requires separate explicit
authorization, DNS/IP validation at connect time, and redirect rejection.
"""
import hashlib
import ipaddress
from urllib.parse import urlsplit


def validate_probe_target(url: str, *, authorized: bool = False) -> dict:
    if authorized is not True:
        raise PermissionError("Explicit probe authorization required")
    if not isinstance(url, str) or len(url) > 2048 or any(ord(c) < 33 or ord(c) == 127 for c in url):
        raise ValueError("Invalid probe URL")
    try:
        parts = urlsplit(url)
        host = parts.hostname
        port = parts.port
    except ValueError as exc:
        raise ValueError("Invalid probe URL") from exc
    if (parts.scheme != "https" or not host or not parts.netloc or
            parts.username is not None or parts.password is not None or
            parts.fragment or port not in (None, 443) or
            not host.isascii() or host.endswith(".") or
            host.lower() in ("localhost", "localhost.localdomain") or
            host.lower().endswith((".local", ".localhost", ".internal", ".test"))):
        raise ValueError("Unsafe probe target")
    # Hostnames need a separate DNS resolution/pinning gate before any socket is opened.
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        if not all(label and len(label) <= 63 and
                   label[0].isalnum() and label[-1].isalnum() and
                   all(ch.isascii() and (ch.isalnum() or ch == "-") for ch in label)
                   for label in host.split(".")):
            raise ValueError("Invalid hostname")
        if "." not in host:
            raise ValueError("Unqualified hostname")
        kind = "DNS_REQUIRES_CONNECT_TIME_PINNING"
    else:
        if not address.is_global:
            raise ValueError("Non-public IP target")
        kind = "PUBLIC_IP_REQUIRES_CONNECT_TIME_CHECK"
    return {"url_sha256": hashlib.sha256(url.encode("utf-8")).hexdigest(),
            "target_kind": kind, "preflight_only": True,
            "network_probed": False, "production_writes": False,
            "production_ready": False}



def validate_resolved_addresses(addresses: list[str]) -> tuple[str, ...]:
    """Reject mixed public/private DNS answers; caller must pin IP at connection."""
    if not isinstance(addresses, list) or not addresses:
        raise ValueError("Missing resolved addresses")
    validated = []
    for value in addresses:
        if not isinstance(value, str):
            raise ValueError("Invalid DNS answer")
        try:
            address = ipaddress.ip_address(value)
        except ValueError as exc:
            raise ValueError("Invalid DNS answer") from exc
        if not address.is_global or (
                isinstance(address, ipaddress.IPv6Address) and address.ipv4_mapped is not None):
            raise ValueError("Non-public DNS answer")
        validated.append(str(address))
    if len(set(validated)) != len(validated):
        raise ValueError("Duplicate DNS answer")
    return tuple(validated)


def validate_probe_handoff(url: str, envelope: dict, run_id: str,
                           commit_sha: str, *, authorized: bool = False) -> dict:
    """Require a candidate fingerprint in the verified K2 envelope before any probe."""
    from madsc.artifact_handoff import unpack
    target = validate_probe_target(url, authorized=authorized)
    discovery = unpack(envelope, run_id, commit_sha)
    matches = [item for item in discovery["candidates"]
               if item["url_sha256"] == target["url_sha256"]]
    if len(matches) != 1:
        raise ValueError("Probe target is not a verified K2 candidate")
    return {**target, "k2_source_digest": envelope["digest"],
            "run_id": run_id, "commit_sha": commit_sha,
            "redirects_allowed": False, "max_runtime_seconds": 15,
            "dns_pinning_required": True}
