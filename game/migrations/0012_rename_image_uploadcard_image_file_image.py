# Generated by Django 5.1.3 on 2024-12-04 20:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0011_uploadcard'),
    ]

    operations = [
        migrations.RenameField(
            model_name='uploadcard',
            old_name='image',
            new_name='image_file',
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_file', models.ImageField(upload_to='')),
                ('upload_card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.uploadcard')),
            ],
        ),
    ]
