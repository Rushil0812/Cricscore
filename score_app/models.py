from django.db import models
from django.contrib.auth.models import User

class Match(models.Model):
    team1 = models.CharField(max_length=100)
    team2 = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    is_live = models.BooleanField(default=False) 
    toss_winner = models.CharField(max_length=100, blank=True, null=True)  
    toss_decision = models.CharField(max_length=10, choices=[('bat', 'Bat First'), ('bowl', 'Bowl First')], blank=True, null=True)
    batting_first = models.CharField(max_length=100, blank=True, null=True)
    winner = models.CharField(max_length=100, blank=True, null=True)
    
    def decide_batting_team(self):
        """Determine which team bats first based on toss decision."""
        if self.toss_winner and self.toss_decision:
            if self.toss_decision == "bat":
                self.batting_first = self.toss_winner
            else:
                self.batting_first = self.team1 if self.toss_winner == self.team2 else self.team2
        self.save()
     
    def __str__(self):  
        return f"{self.team1} vs {self.team2}"
    
class Score(models.Model):
    match = models.OneToOneField(Match, on_delete=models.CASCADE, related_name='score')
    team1_runs = models.IntegerField(default=0)
    team2_runs = models.IntegerField(default=0)
    team1_wickets = models.IntegerField(default=0)
    team2_wickets = models.IntegerField(default=0)
    overs = models.FloatField(default=0.0)
    current_innings = models.IntegerField(default=1)
    
    def __str__(self):
        return f"{self.match} - Score"
    
class Commentary(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='commentary')
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commentary for {self.match} - {self.text[:50]}"
