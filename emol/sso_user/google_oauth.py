import os
from authlib.integrations.django_client import OAuth
import logging

logger = logging.getLogger("cards")


class GoogleOAuth:
    def __init__(self):
        self.oauth = OAuth()

        if os.getenv("EMOL_DEV") == "1":
            provider_url = os.getenv("OAUTH_PROVIDER_URL", "http://oauth-mock:8081")
            logger.debug("Using mock OAuth provider at %s", provider_url)

            self.google = self.oauth.register(
                name="google",
                server_metadata_url=f"{provider_url}/.well-known/oauth-authorization-server",
                client_id="mock-client-id",  # Will be overridden by SSM
                client_secret="mock-client-secret",  # Will be overridden by SSM
                client_kwargs={"scope": "openid email profile"},
            )
        else:
            logger.debug("Using production Google OAuth")
            self.google = self.oauth.register(
                name="google",
                server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
                client_kwargs={"scope": "openid email profile"},
            )
