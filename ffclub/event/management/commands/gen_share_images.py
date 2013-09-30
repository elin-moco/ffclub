# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import NoArgsCommand, BaseCommand
from ffclub.event.models import Campaign
from ffclub.upload.models import ImageUpload
from ffclub.upload.utils import generate_share_image


class Command(BaseCommand):
    help = 'Generate share images'
    option_list = NoArgsCommand.option_list

    def handle(self, *args, **options):
        self.options = options
        campaignSlug = args[0]
        contentTypeId = ContentType.objects.get(model='campaign').id
        entityId = Campaign.objects.get(slug=campaignSlug).id
        for upload in ImageUpload.objects.filter(content_type=contentTypeId, entity_id=entityId):
            generate_share_image(upload, campaignSlug)

    def push_image_stack(self, background, foreground, offset=(0, 0)):
        background.paste(foreground, offset, foreground)
        return background
