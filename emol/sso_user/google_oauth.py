import logging
import os
from typing import Any, Dict

from authlib.integrations.django_client import OAuth
from django.http import HttpResponseRedirect
from django.urls import reverse

logger = logging.getLogger("cards")


class MockOAuthClient:
    """
    A mock OAuth client for development purposes.

    Provides a simplified OAuth flow for local development without requiring
    actual Google OAuth credentials.
    """

    def __init__(self) -> None:
        """Initialize with default test user info."""
        self.user_info = {
            "sub": "mock-user-id",
            "email": "admin@emol.ca",
            "name": "Development User",
            "given_name": "Development",
            "family_name": "User",
        }

    def authorize_redirect(
        self, request: Any, redirect_uri: str, **kwargs: Any
    ) -> HttpResponseRedirect:
        """Simulate OAuth redirect by going straight to mock callback."""
        return HttpResponseRedirect(reverse("mock_oauth_callback"))

    def authorize_access_token(self, request: Any) -> Dict[str, Any]:
        """Return mock token response with userinfo included."""
        return {
            "access_token": "mock-token",
            "token_type": "Bearer",
            "expires_in": 3600,
            "scope": "openid email profile",
            "userinfo": self.user_info,
        }


class GoogleOAuth:
    """
    Handles Google OAuth integration with mock support for development.

    In development (EMOL_DEV=1), uses MockOAuthClient.
    In production, uses real Google OAuth.
    """

    def __init__(self) -> None:
        self.oauth = OAuth()

        if os.getenv("EMOL_DEV") == "1":
            logger.info("Using MockOAuthClient for development")
            self.google = MockOAuthClient()
        else:
            logger.info("Using production Google OAuth")
            self.google = self.oauth.register(
                name="google",
                server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
                client_kwargs={"scope": "openid email profile"},
            )
