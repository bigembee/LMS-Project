from __future__ import annotations

from django.core.management.base import BaseCommand

from allauth.idp.oidc.models import Token


class Command(BaseCommand):
    help = "Deletes expired OpenID Connect tokens."

    def handle(self, *args, **options) -> None:
        count, _ = Token.objects.expired().delete()
        self.stdout.write(f"{count} expired token(s) deleted.")
