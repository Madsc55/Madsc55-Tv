"""Shared credential-safe HTTPS redirect policy for GitHub read-only clients."""
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, build_opener


class GitHubRedirectHandler(HTTPRedirectHandler):
    def __init__(self, *, allow_storage=False):
        super().__init__()
        self.allow_storage = allow_storage

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        parsed = urlsplit(newurl)
        if (parsed.scheme != "https" or not parsed.hostname
                or parsed.username is not None or parsed.password is not None):
            raise ValueError("Unsafe GitHub redirect")
        same_api = parsed.netloc == "api.github.com"
        if not self.allow_storage and not same_api:
            raise ValueError("GitHub API redirect left approved origin")
        redirected = super().redirect_request(req, fp, code, msg, headers, newurl)
        if redirected is not None and not same_api:
            redirected.remove_header("Authorization")
        return redirected


def github_opener(*, allow_storage=False):
    return build_opener(GitHubRedirectHandler(allow_storage=allow_storage))
