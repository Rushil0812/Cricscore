from django.contrib import admin
from score_app.models import Match, Score

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['id', 'team1', 'team2', 'is_live']

@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ['match', 'team1_runs', 'team2_runs', 'team1_wickets', 'team2_wickets', 'overs']