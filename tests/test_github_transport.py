"""Exercise real urllib redirect dispatch offline across all authenticated clients."""
import hashlib
import io
import tempfile
import unittest
from email.message import Message
from pathlib import Path
from unittest.mock import patch
from urllib.request import HTTPSHandler, Request, build_opener
from urllib.response import addinfourl

from madsc.github_transport import GitHubRedirectHandler
from madsc.github_history_client import github_json
from madsc.github_legacy_pair_client import download_execution_artifact
from madsc.history_artifact_download import download_verified_history_artifact
from madsc.legacy_99_bulk_audit import github
from tests.test_history_artifact_download import FILES, archive


class FakeHTTPS(HTTPSHandler):
    def __init__(self, payload, destination='https://storage.example/signed.zip'):
        super().__init__()
        self.payload, self.destination, self.requests = payload, destination, []

    def https_open(self, request):
        self.requests.append(request)
        headers = Message()
        first = len(self.requests) == 1
        if first:
            headers['Location'] = self.destination
        response = addinfourl(io.BytesIO(b'' if first else self.payload), headers,
                              request.full_url, 302 if first else 200)
        response.msg = 'Found' if first else 'OK'
        return response

    def install(self):
        return patch('madsc.github_transport.build_opener',
                     side_effect=lambda handler: build_opener(self, handler))


class GitHubTransportTests(unittest.TestCase):
    def test_both_artifact_clients_strip_token_on_actual_redirect_dispatch(self):
        for client in ('history', 'parity'):
            fake = FakeHTTPS(archive(FILES))
            with self.subTest(client=client), tempfile.TemporaryDirectory() as tmp, fake.install():
                if client == 'history':
                    result = download_verified_history_artifact(
                        repository='Madsc55/Madsc55-Tv', artifact_id=123, token='fixture',
                        expected_hashes={k: hashlib.sha256(v).hexdigest() for k, v in FILES.items()},
                        destination=Path(tmp) / 'history')
                    self.assertEqual(set(result), set(FILES))
                else:
                    self.assertEqual(download_execution_artifact(
                        {'repository': 'Madsc55/Madsc55-Tv', 'artifact': {'id': 123}},
                        token='fixture'), archive(FILES))
            self.assertEqual(len(fake.requests), 2)
            self.assertEqual(fake.requests[0].get_header('Authorization'), 'Bearer fixture')
            self.assertIsNone(fake.requests[1].get_header('Authorization'))

    def test_both_json_clients_reject_off_origin_before_second_request(self):
        for client in (github_json, github):
            fake = FakeHTTPS(b'{}')
            with self.subTest(client=client.__name__), fake.install(), self.assertRaises(ValueError):
                client('https://api.github.com/repos/Madsc55/Madsc55-Tv', token='fixture')
            self.assertEqual(len(fake.requests), 1)

    def test_api_same_origin_redirect_preserves_auth(self):
        fake = FakeHTTPS(b'{"ok":true}', 'https://api.github.com/repos/renamed/repo')
        with fake.install():
            self.assertEqual(github_json('https://api.github.com/repos/example/repo',
                                         token='fixture'), {'ok': True})
        self.assertEqual(fake.requests[1].get_header('Authorization'), 'Bearer fixture')

    def test_unsafe_redirects_rejected_before_connection(self):
        for target in ('http://storage.example/a', 'https://user@storage.example/a',
                       'https://user:pass@storage.example/a', 'https:///missing-host'):
            with self.subTest(target=target), self.assertRaises(ValueError):
                GitHubRedirectHandler(allow_storage=True).redirect_request(
                    Request('https://api.github.com/a'), None, 302, '', {}, target)

    def test_token_never_restored_after_storage_hop(self):
        handler = GitHubRedirectHandler(allow_storage=True)
        first = Request('https://api.github.com/a', headers={'Authorization': 'Bearer fixture'})
        second = handler.redirect_request(first, None, 302, '', {}, 'https://storage.example/a')
        third = handler.redirect_request(second, None, 302, '', {}, 'https://api.github.com/a')
        self.assertIsNone(third.get_header('Authorization'))
        for target in ('https://api.github.com.evil/a', 'https://api.github.com:444/a'):
            redirected = handler.redirect_request(first, None, 302, '', {}, target)
            self.assertIsNone(redirected.get_header('Authorization'))

    def test_audit_rejects_unbounded_json(self):
        fake = FakeHTTPS(b' ' * (2 * 1024 * 1024 + 1), 'https://api.github.com/large')
        with fake.install(), self.assertRaisesRegex(ValueError, 'Oversized'):
            github('https://api.github.com/start', token='fixture')

    def test_audit_rejects_external_initial_url(self):
        fake = FakeHTTPS(b'{}')
        with fake.install(), self.assertRaises(ValueError):
            github('https://other.example/', token='fixture')
        self.assertEqual(fake.requests, [])
