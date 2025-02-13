# Generated by Django 5.1.5 on 2025-02-10 04:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('score_app', '0007_player'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commentary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commentary', to='score_app.match')),
            ],
        ),
        migrations.DeleteModel(
            name='Player',
        ),
    ]
