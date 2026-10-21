"""R05: compare two HLS media playlists without fetching any network content."""
from urllib.parse import urlsplit


def segment_signature(playlist):
    if not isinstance(playlist, str):
        raise ValueError("HLS playlist must be text")
    lines = [line.strip() for line in playlist.splitlines() if line.strip()]
    if not lines or lines[0] != "#EXTM3U":
        raise ValueError("Invalid HLS playlist")
    if any(line.startswith("#EXT-X-KEY") for line in lines):
        raise ValueError("Encrypted playlist requires separate rights/device evidence")
    segments = [line for line in lines if not line.startswith("#")]
    if not segments or not any(line.startswith("#EXTINF:") for line in lines):
        raise ValueError("No media segments")
    for segment in segments:
        parts = urlsplit(segment)
        if parts.scheme and parts.scheme not in ("http", "https"):
            raise ValueError("Unsupported segment URL scheme")
        if segment.startswith("//"):
            raise ValueError("Protocol-relative segment URL not accepted")
    return tuple(segments)


def changed_segment_window(first, second):
    """A changed segment window is evidence of playlist rotation, not playback."""
    before, after = segment_signature(first), segment_signature(second)
    return {"changed": before != after, "first_segments": len(before),
            "second_segments": len(after), "video_audio_verified": False,
            "channel_identity_verified": False, "production_ready": False}
