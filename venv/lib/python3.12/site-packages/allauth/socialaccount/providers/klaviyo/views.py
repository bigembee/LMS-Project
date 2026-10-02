from __future__ import annotations

from allauth.socialaccount.adapter import get_adapter
from allauth.socialaccount.models import SocialToken
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)


KLAVIYO_API_VERSION = "2026-01-15"


class KlaviyoOAuth2Adapter(OAuth2Adapter):
    provider_id = "klaviyo"
    basic_auth = True

    access_token_url = "https://a.klaviyo.com/oauth/token"  # nosec
    authorize_url = "https://www.klaviyo.com/oauth/authorize"  # nosec
    accounts_url = "https://a.klaviyo.com/api/accounts/"

    def complete_login(self, request, app, token: SocialToken, **kwargs):
        with get_adapter().get_requests_session() as sess:
            r = sess.get(
                self.accounts_url,
                headers={
                    "accept": "application/vnd.api+json",
                    "content-type": "application/vnd.api+json",
                    "revision": KLAVIYO_API_VERSION,
                    "Authorization": f"Bearer {token.token}",
                },
            )
            r.raise_for_status()
            extra_data = r.json()
        return self.get_provider().sociallogin_from_response(request, extra_data)


oauth2_login = OAuth2LoginView.adapter_view(KlaviyoOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(KlaviyoOAuth2Adapter)
