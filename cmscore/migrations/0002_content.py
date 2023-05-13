# Generated by Django 4.1.6 on 2023-05-06 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmscore', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('content_type', models.CharField(choices=[('expert', 'expert'), ('farm', 'farm'), ('support', 'support')], max_length=255)),
                ('content_detail', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
