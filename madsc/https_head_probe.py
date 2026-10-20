"""Explicit opt-in, read-only HTTPS header probe with pinned public DNS answers.

Never follows redirects, never sends URL credentials, never writes playlist data.
This is a single HTTP header observation, NOT an ffprobe or live stream test.
"""
import ipaddress
import time
import socket
import ssl
from urllib.parse import urlsplit

from madsc.probe_target_gate import validate_probe_handoff, validate_resolved_addresses


def observe_https_headers(url: str, envelope: dict, run_id: str, commit_sha: str,
                          *, authorized: bool = False, timeout: float = 5.0) -> dict:
    if authorized is not True:
        raise PermissionError("Explicit probe authorization required")
    if type(timeout) not in (float, int) or not 0 < timeout <= 5:
        raise ValueError("Unsafe network timeout")
    started = time.monotonic()
    deadline = started + timeout
    gate = validate_probe_handoff(url, envelope, run_id, commit_sha, authorized=True)
    parts = urlsplit(url)
    host = parts.hostname
    # Validate every DNS answer before selecting an address. Re-resolution inside
    # the TLS connection is forbidden: connect only to the selected numeric IP.
    try:
        answers = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM,
                                     proto=socket.IPPROTO_TCP)
        ips = validate_resolved_addresses([entry[4][0] for entry in answers])
    except (socket.gaierror, OSError) as exc:
        raise ValueError("DNS resolution failed") from exc
    if not ips:
        raise ValueError("No safe DNS address")
    address = ipaddress.ip_address(ips[0])
    family = socket.AF_INET6 if address.version == 6 else socket.AF_INET
    target = (str(address), 443, 0, 0) if address.version == 6 else (str(address), 443)
    path = parts.path or "/"
    if parts.query:
        path += "?" + parts.query
    if any(ch in path for ch in "\r\n"):
        raise ValueError("Unsafe request target")
    try:
        path.encode("ascii")
    except UnicodeEncodeError as exc:
        raise ValueError("Non-ASCII request target must be percent-encoded") from exc
    request = ("HEAD " + path + " HTTP/1.1\r\nHost: " + host +
               "\r\nConnection: close\r\nAccept: */*\r\n\r\n").encode("ascii")
    context = ssl.create_default_context()
    def remaining():
        seconds = deadline - time.monotonic()
        if seconds <= 0:
            raise TimeoutError("HTTPS observation deadline exceeded")
        return seconds

    with socket.socket(family, socket.SOCK_STREAM) as raw:
        raw.settimeout(remaining())
        raw.connect(target)
        raw.settimeout(remaining())
        with context.wrap_socket(raw, server_hostname=host) as conn:
            conn.settimeout(remaining())
            conn.sendall(request)
            header = bytearray()
            while b"\r\n\r\n" not in header:
                conn.settimeout(remaining())
                block = conn.recv(1024)
                if not block:
                    raise ValueError("Incomplete HTTP response")
                header.extend(block)
                if len(header) > 8192:
                    raise ValueError("Oversized HTTP response headers")
    status_line = bytes(header).split(b"\r\n", 1)[0]
    tokens = status_line.split(b" ")
    if len(tokens) < 2 or tokens[0] not in (b"HTTP/1.1", b"HTTP/1.0") or\
            len(tokens[1]) != 3 or not tokens[1].isdigit():
        raise ValueError("Invalid HTTP response")
    status = int(tokens[1])
    if 300 <= status < 400:
        raise ValueError("HTTP redirects prohibited")
    return {"schema": "madsc-k3-https-head-observation-v1",
            "url_sha256": gate["url_sha256"], "k2_source_digest": gate["k2_source_digest"],
            "run_id": run_id, "commit_sha": commit_sha, "http_status": status,
            "tls_verified": True, "dns_pinned": True, "redirects_followed": False,
            "network_probed": True, "stream_continuity_verified": False,
            "ibo_device_verified": False, "production_writes": False,
            "production_ready": False}
