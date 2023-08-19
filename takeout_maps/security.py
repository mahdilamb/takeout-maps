"""Module containing security definitions."""
import typing
import urllib.parse

from fastapi import Request
from fastapi.security import OAuth2AuthorizationCodeBearer
from fitbit_web import auth, client

from takeout_maps import exceptions


class FitbitAuth(OAuth2AuthorizationCodeBearer):
    """Fitbit Authentication object."""

    def __init__(
        self,
    ) -> None:
        super().__init__(
            authorizationUrl=f"https://www.fitbit.com/oauth2/authorize?response_type=code&code_challenge={auth.code_challenge(auth.CODE_VERIFIER)}&code_challenge_method=S256&redirect_uri={urllib.parse.quote(auth.REDIRECT_URL)}",
            tokenUrl="https://api.fitbit.com/oauth2/token?grant_type=authorization_code",
            refreshUrl=auth.REFRESH_URL,
            scopes={k: k for k in typing.get_args(auth.Scope)},
        )
        self.__client = None
        self.__redirect_path = urllib.parse.urlparse(auth.REDIRECT_URL).path

    def __call__(self, request: Request):
        if request.url.path == self.__redirect_path:
            self.__client = client.Client(
                tokens=auth.token_from_code(
                    urllib.parse.parse_qs(request.url.query)["code"][0]
                )
            )
        if self.__client is None:
            raise exceptions.NoFitbitAuthorizationError()
        return self.__client
