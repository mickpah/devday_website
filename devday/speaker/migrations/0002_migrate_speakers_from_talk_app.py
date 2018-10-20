# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-10 20:31
from __future__ import unicode_literals

import os

from django.db import migrations
from django.utils.text import slugify


def copy_image_field(source, target):
    if source:
        target.save(
            os.path.basename(source.name),
            source.file, save=False)


def migrate_existing_speakers(apps, schema_manager):
    OldSpeaker = apps.get_model('talk', 'Speaker')
    Speaker = apps.get_model('speaker', 'Speaker')
    PublishedSpeaker = apps.get_model('speaker', 'PublishedSpeaker')
    Talk = apps.get_model('talk', 'Talk')
    for old_speaker in OldSpeaker.objects.order_by('-user__event__start_time'):
        attendee = old_speaker.user
        event = attendee.event
        user = attendee.user

        speaker_name = '{0} {1}'.format(
            user.first_name, user.last_name).strip()
        if not speaker_name:  # we have speakers with no name
            speaker_name = user.email
        slug = slugify(speaker_name)
        if not Speaker.objects.filter(user=user).exists():
            speaker = Speaker(
                name=speaker_name,
                slug=slug,
                twitter_handle=user.twitter_handle,
                phone=user.phone,
                position=user.position,
                organization=user.organization,
                video_permission=old_speaker.videopermission,
                short_biography=old_speaker.shortbio,
                user=user,
                date_registered=user.date_joined,
                shirt_size=old_speaker.shirt_size,
            )
            copy_image_field(old_speaker.portrait, speaker.portrait)
            copy_image_field(old_speaker.thumbnail, speaker.thumbnail)
            copy_image_field(old_speaker.public_image, speaker.public_image)
            speaker.save()
        else:
            speaker = Speaker.objects.get(user=user)
        if (Talk.objects.filter(speaker=old_speaker).exists() and
                not PublishedSpeaker.objects.filter(
                    speaker=speaker.id).exists()):
            published = PublishedSpeaker(
                name=speaker_name,
                slug=slug,
                twitter_handle=user.twitter_handle,
                phone=user.phone,
                position=user.position,
                organization=user.organization,
                video_permission=old_speaker.videopermission,
                short_biography=old_speaker.shortbio,
                speaker=speaker,
                date_published=event.start_time,
                event=event,
                email=user.email,
            )
            copy_image_field(old_speaker.portrait, published.portrait)
            copy_image_field(old_speaker.thumbnail, published.thumbnail)
            copy_image_field(old_speaker.public_image, published.public_image)
            published.save()


class Migration(migrations.Migration):
    dependencies = [
        ('speaker', '0001_initial'),
        ('attendee', '0007_auto_20180410_1540'),
        ('talk', '0030_fill_session_slugs_from_titles'),
    ]

    run_before = [
        ('attendee', '0009_auto_20181020_0802'),
    ]

    operations = [
        migrations.RunPython(migrate_existing_speakers)
    ]
