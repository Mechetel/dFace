# Generated by Django 4.1.1 on 2022-09-26 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai_camera', '0006_person_image_nd_array'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='image',
            field=models.FileField(null=True, upload_to='images/'),
        ),
    ]