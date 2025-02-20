from django.test import TestCase
from score_app.models import Match, Score, Commentary

class MatchModelTest(TestCase):
    def setUp(self):
        self.match = Match.objects.create(
            team1='India',
            team2='Australia',
            start_time='2025-02-20T14:30:00Z',
            is_live=True,
            toss_winner='India',
            toss_decision='bat',
        )
        
    def test_match_creation(self):
        self.assertEqual(self.match.team1, 'India')
        self.assertEqual(self.match.team2, 'Australia')
        self.assertTrue(self.match.is_live)
        
    def test_decide_batting_team(self):
        self.match.decide_batting_team()
        self.assertEqual(self.match.batting_first, 'India')
        
class ScoreModelTest(TestCase):
    def setUp(self):
        self.match = Match.objects.create(team1='India', team2='Australia', start_time='2025-02-20T14:30:00Z')
        self.score = Score.objects.create(
            match=self.match,
            team1_runs=190,
            team2_runs=167,
            team1_wickets=5,
            team2_wickets=10,
            overs=20.0,
            current_innings=2 
        )
        
    def test_score_creation(self):
        self.assertEqual(self.score.match, self.match)
        self.assertEqual(self.score.team1_runs, 190)
        self.assertEqual(self.score.team2_runs, 167)
        self.assertEqual(self.score.team1_wickets, 5)
        self.assertEqual(self.score.team2_wickets, 10)
        self.assertEqual(self.score.overs, 20.0)
        self.assertEqual(self.score.current_innings, 2)
        
class CommentaryModelTet(TestCase):
    def setUp(self):
        self.match = Match.objects.create(team1='India', team2='Australia', start_time='2025-02-20T14:30:00Z')
        self.commentary = Commentary.objects.create(match=self.match, text="India wins by 23 runs!")
        
    def test_commentary_creation(self):
        self.assertEqual(self.commentary.match, self.match)
        self.assertEqual(self.commentary.text, "India wins by 23 runs!")