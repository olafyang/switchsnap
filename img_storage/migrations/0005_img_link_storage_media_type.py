# Generated by Django 3.1.2 on 2020-11-02 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('img_storage', '0004_auto_20201017_1733'),
    ]

    operations = [
        migrations.AddField(
            model_name='img_link_storage',
            name='media_type',
            field=models.CharField(default='photo', max_length=5),
            preserve_default=False,
        ),
    ]
