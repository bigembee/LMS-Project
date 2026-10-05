from __future__ import annotations

from allauth.socialaccount import providers
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.klaviyo.views import KlaviyoOAuth2Adapter
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class KlaviyoAccount(ProviderAccount):
    def to_str(self):
        if name := self.account.extra_data.get("contact_information", {}).get(
            "organization_name"
        ):
            return name
        return super().to_str()


class KlaviyoProvider(OAuth2Provider):
    id = "klaviyo"
    name = "Klaviyo"
    account_class = KlaviyoAccount
    oauth2_adapter_class = KlaviyoOAuth2Adapter

    def extract_uid(self, data):
        return data["data"][0]["id"]

    def extract_common_fields(self, data: dict) -> dict:
        ret: dict = {}
        contact_information = self.extract_extra_data(data).get(
            "contact_information", {}
        )
        if email := contact_information.get("default_sender_email"):
            ret["email"] = email
        if name := contact_information.get("organization_name"):
            ret["name"] = name
        return ret

    def extract_extra_data(self, data: dict) -> dict:
        return data["data"][0]["attributes"]

    def get_default_scope(self):
        return ["accounts:read"]


provider_classes = [KlaviyoProvider]
providers.registry.register(KlaviyoProvider)
