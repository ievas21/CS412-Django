# Generated by Django 5.1.1 on 2024-10-01 14:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='test',
            new_name='text',
        ),
    ]
