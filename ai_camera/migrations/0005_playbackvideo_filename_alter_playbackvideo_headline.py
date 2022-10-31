# Generated by Django 4.1.2 on 2022-10-31 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai_camera', '0004_playbackvideo_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='playbackvideo',
            name='filename',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='playbackvideo',
            name='headline',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
