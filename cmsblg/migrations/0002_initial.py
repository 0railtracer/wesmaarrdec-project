# Generated by Django 4.1.6 on 2023-05-23 13:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cmscore', '0001_initial'),
        ('cmsblg', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='postimages',
            name='albumphoto',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='cmscore.albumphoto'),
        ),
        migrations.AddField(
            model_name='postimages',
            name='post',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='cmsblg.post'),
        ),
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='cmsblg.category'),
        ),
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ManyToManyField(blank=True, related_name='postimg', to='cmsblg.postimages'),
        ),
        migrations.AddField(
            model_name='fact',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='cmsblg.category'),
        ),
        migrations.AddField(
            model_name='comment',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='cmsblg.comment'),
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='cmsblg.post'),
        ),
    ]
