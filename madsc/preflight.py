from pathlib import Path
from madsc.playlist import inspect_playlist
from madsc.epg import check_epg_mapping

def preflight(playlist: Path, epg: Path) -> dict:
    if playlist.name != 'playlist.m3u8' or epg.name != 'xmltv.xml':
        raise ValueError('Invalid filenames')
    p = inspect_playlist(playlist)
    e = check_epg_mapping(playlist, epg)
    return {'playlist_channels': p['channel_count'], 'ready_for_device_test': bool(e['matching_verified']), 'production_approved': False, 'read_only': True}
