# Generated by Django 5.0.4 on 2024-11-29 19:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_player_playing_hand_alter_user_geo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='blade',
            field=models.CharField(blank=True, help_text="Player's Blade", max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='playing_hand',
            field=models.IntegerField(blank=True, choices=[(0, 'RIGHT_HAND'), (1, 'LEFT_HAND'), (2, 'BOTH')], help_text='By which hand player prefer to play, or both', null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='rating',
            field=models.PositiveBigIntegerField(blank=True, default=100, help_text='Rating of player in club rating system'),
        ),
        migrations.AlterField(
            model_name='player',
            name='rubber_backhand',
            field=models.CharField(blank=True, help_text="Player's Ruber Backhand", max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='rubber_forehand',
            field=models.CharField(blank=True, help_text="Player's Ruber Forehand", max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
