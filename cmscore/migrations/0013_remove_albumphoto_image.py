# Generated by Django 4.1.6 on 2023-05-15 06:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmscore', '0012_alter_albumphoto_image_alter_albumphotoimages_images'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='albumphoto',
            name='image',
        ),
    ]