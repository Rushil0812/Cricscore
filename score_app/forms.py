from django import forms
from score_app.models import Score, Match

class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['team1', 'team2', 'is_live']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['team1'].widget.attrs.update({'class': 'form-control'})
        self.fields['team2'].widget.attrs.update({'class': 'form-control'})
        self.fields['is_live'].widget.attrs.update({'class': 'form-check-input'})

class ScoreUpdateForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ['team1_runs', 'team2_runs', 'team1_wickets', 'team2_wickets', 'overs']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['team1_runs'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter Team 1 Runs'})
        self.fields['team2_runs'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter Team 2 Runs'})
        self.fields['team1_wickets'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter Team 1 Wickets'})
        self.fields['team2_wickets'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter Team 2 Wickets'})
        self.fields['overs'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter Overs'})

class TossDecisionForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['toss_winner', 'toss_decision']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            teams = [(self.instance.team1, self.instance.team1), (self.instance.team2, self.instance.team2)]
            self.fields['toss_winner'].widget = forms.Select(choices=teams, attrs={'class': 'form-control'})
        self.fields['toss_decision'].widget.attrs.update({'class': 'form-control'})
