import logging
from urllib.parse import urljoin

import httpx
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import translation
from django.utils.translation import gettext as _

from .models import Submission


@receiver(post_save, sender=Submission)
async def submission_post_save(sender, instance, created, **kwargs):
    if not created or not settings.DISCORD_WEBHOOK:
        return

    fields = []

    with translation.override(settings.LANGUAGE_CODE):
        if instance.name:
            fields.append({"name": _("Name"), "value": instance.name})

        if instance.author:
            fields.append({"name": _("Author"), "value": instance.author})

        if instance.school:
            fields.append({"name": _("School"), "value": instance.school})

        title = _("New pattern has been submitted!")

        view_label = _("View Submission")
        manage_label = _("Manage Submission")

    view_url = urljoin(settings.ROOT_URL, reverse("project-share-longid", args=[instance.project.longid]))
    manage_url = urljoin(settings.ROOT_URL, reverse("admin:editor_submission_change", args=[instance.pk]))

    try:
        async with httpx.AsyncClient() as client:
            await client.post(
                settings.DISCORD_WEBHOOK,
                json={
                    "embeds": [
                        {
                            "title": title,
                            "fields": fields,
                            "color": settings.DISCORD_COLOR,
                        },
                        {
                            "description": f"**[{view_label}]({view_url}) | [{manage_label}]({manage_url})**",
                            "color": settings.DISCORD_COLOR,
                        },
                    ],
                    "username": settings.DISCORD_USERNAME,
                    "avatar_url": settings.DISCORD_AVATAR,
                },
            )

    except httpx.RequestError as error:
        logger = logging.getLogger(__name__)
        logger.exception(error)
