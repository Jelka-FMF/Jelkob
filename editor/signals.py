import logging
from urllib.parse import urljoin

import requests
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext as _

from .models import Submission


@receiver(post_save, sender=Submission)
def submission_post_save(sender, instance, created, **kwargs):
    if not created or not settings.DISCORD_WEBHOOK:
        return

    fields = []

    if instance.name:
        fields.append({"name": _("Name"), "value": instance.name})

    if instance.author:
        fields.append({"name": _("Author"), "value": instance.author})

    if instance.school:
        fields.append({"name": _("School"), "value": instance.school})

    try:
        requests.post(
            settings.DISCORD_WEBHOOK,
            json={
                "embeds": [
                    {
                        "title": _("New pattern has been submitted!"),
                        "url": urljoin(
                            settings.ROOT_URL,
                            reverse("admin:editor_submission_change", args=[instance.pk]),
                        ),
                        "fields": fields,
                        "color": 5814783,
                    }
                ],
                "username": settings.DISCORD_USERNAME,
                "avatar_url": settings.DISCORD_AVATAR,
            },
        )

    except requests.RequestException as error:
        logger = logging.getLogger(__name__)
        logger.exception(error)
