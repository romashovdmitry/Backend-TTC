# Generated by Django 5.0.4 on 2024-12-09 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_alter_user_birth_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='geo',
            field=models.IntegerField(choices=[(1, 'Dubai'), (2, 'Abu Dhabi'), (3, 'Sharjah'), (4, 'Other Emirate')], help_text='User can choose 1 from 4 variants', null=True, verbose_name="User's geo"),
        ),
    ]