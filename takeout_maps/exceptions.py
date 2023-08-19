"""Custom exceptions."""
from fastapi import HTTPException


class NoFitbitAuthorizationError(HTTPException):
    def __init__(self, headers: dict[str, str] | None = None) -> None:
        super().__init__(
            401, "Fitbit authorization is required for this path.", headers
        )
