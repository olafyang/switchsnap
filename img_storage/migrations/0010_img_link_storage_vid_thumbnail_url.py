# Generated by Django 3.1.2 on 2020-11-04 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('img_storage', '0009_auto_20201103_2231'),
    ]

    operations = [
        migrations.AddField(
            model_name='img_link_storage',
            name='vid_thumbnail_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
