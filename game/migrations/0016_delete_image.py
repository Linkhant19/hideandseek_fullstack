# Generated by Django 5.1.3 on 2024-12-04 21:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0015_uploadcard_image_file'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Image',
        ),
    ]
