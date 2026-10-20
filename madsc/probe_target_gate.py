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
