# Generated by Django 5.1.3 on 2024-11-08 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voter_analytics', '0002_alter_voter_dob_alter_voter_precinct_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voter',
            name='apartment_number',
            field=models.TextField(blank=True, null=True),
        ),
    ]
