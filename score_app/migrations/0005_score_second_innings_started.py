# Generated by Django 5.1 on 2025-02-05 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('score_app', '0004_remove_match_toss_decision_match_batting_first_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='score',
            name='second_innings_started',
            field=models.BooleanField(default=False),
        ),
    ]
