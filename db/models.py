from django.db import models
from manage import init_django

init_django()

class Model(models.Model):
    id = models.AutoField(primary_key=True)


    class Meta:
        abstract = True

# define models here
# class Post(Model):
#    pass

class ClubsNamesM(Model):
    league_name = models.CharField(max_length=255, null=False)
    club_name = models.CharField(max_length=255, null=False)

class TimetableM(Model):
    league_name = models.CharField(max_length=255, null=False)
    round_number = models.IntegerField(null=True, default=None)
    date_round = models.CharField(max_length=255, default=None)
    home_team = models.ForeignKey(ClubsNamesM, on_delete=models.CASCADE, related_name="home_team")
    home_team_goals = models.IntegerField(null=True, default=None)
    away_team = models.ForeignKey(ClubsNamesM, on_delete=models.CASCADE, related_name="away_team")
    away_team_goals = models.IntegerField(null=True, default=None)
    home_team_win = models.BooleanField()
    draw = models.BooleanField()
    away_team_win = models.BooleanField()
