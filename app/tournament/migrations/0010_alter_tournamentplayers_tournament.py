# Generated by Django 5.0.4 on 2024-11-23 00:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0009_knockoutgame'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournamentplayers',
            name='tournament',
            field=models.ForeignKey(help_text='Проводимый клубом туринр.', on_delete=django.db.models.deletion.CASCADE, related_name='tournament_players', to='tournament.tournament', verbose_name='Проводимый клубом туринр.'),
        ),
    ]