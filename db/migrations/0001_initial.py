# Generated by Django 5.1.3 on 2024-11-26 19:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClubsNamesM',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('league_name', models.CharField(max_length=255)),
                ('club_name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TimetableM',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('league_name', models.CharField(max_length=255)),
                ('round_number', models.IntegerField(default=None, null=True)),
                ('date_round', models.CharField(default=None, max_length=255)),
                ('home_team_goals', models.IntegerField(default=None, null=True)),
                ('away_team_goals', models.IntegerField(default=None, null=True)),
                ('home_team_win', models.BooleanField()),
                ('draw', models.BooleanField()),
                ('away_team_win', models.BooleanField()),
                ('away_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='away_team', to='db.clubsnamesm')),
                ('home_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home_team', to='db.clubsnamesm')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
