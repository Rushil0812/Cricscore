import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.utils.timezone import now
from django.http import HttpResponseForbidden
from score_app.models import Match, Score, Commentary
from score_app.forms import MatchForm, ScoreUpdateForm, TossDecisionForm

@login_required
def create_match(request):
    """ Admin can create a new match with automatic start time """
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to create matches.")
    if request.method == 'POST':
        form = MatchForm(request.POST)
        if form.is_valid():
            match = form.save(commit=False)
            match.start_time = now()  
            match.save()
            return redirect('toss_decision', match_id=match.id)  
    else:
        form = MatchForm()
    return render(request, 'score_app/create_match.html', {'form': form})

@login_required
def delete_match(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    match.delete()
    return redirect('live_scores')

@login_required
def live_scores(request):
    matches = Match.objects.filter(winner__isnull=True).order_by('-start_time')
    context = {'matches': matches} 
    return render(request, 'score_app/live_scores.html', context)

@login_required
def toss_decision_view(request, match_id):
    match = get_object_or_404(Match, id=match_id)

    if request.method == "POST":
        form = TossDecisionForm(request.POST, instance=match)
        if form.is_valid():
            match = form.save(commit=False)
            match.decide_batting_team() 
            return redirect('match_detail', match_id=match.id)
    else:
        form = TossDecisionForm(instance=match)
    return render(request, "score_app/toss_decision.html", {"form": form, "match": match})

@login_required
def match_detail(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    return render(request, 'score_app/match_detail.html', {'match': match})

@login_required
def update_score(request, match_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to update matches.")
    match = get_object_or_404(Match, id=match_id)
    score, created = Score.objects.get_or_create(match=match)
    commentary_text = ""
    
    # Ensure current_innings exists (default to 1)
    if not hasattr(score, 'current_innings'):
        score.current_innings = 1
        score.save()
    
    # Define the two teams based on toss decision.
    first_innings_team = match.batting_first
    second_innings_team = match.team1 if match.batting_first == match.team2 else match.team2
    
    # Determine current batting team and corresponding score fields.
    if score.current_innings == 1:
        current_team = first_innings_team
        current_runs_field = 'team1_runs' if current_team == match.team1 else 'team2_runs'
        current_wickets_field = 'team1_wickets' if current_team == match.team1 else 'team2_wickets'
    else:
        current_team = second_innings_team
        current_runs_field = 'team1_runs' if current_team == match.team1 else 'team2_runs'
        current_wickets_field = 'team1_wickets' if current_team == match.team1 else 'team2_wickets'
    
    def increment_overs(overs):
        """
        Increment the overs value by one ball.
        The overs value is represented as a float:
            e.g. 5.3 means 5 overs and 3 balls.
        When 6 balls are completed, it rolls over to the next whole number.
        """
        whole = int(overs)
        current_ball = int(round((overs - whole) * 10))
        if current_ball < 5:
            new_overs = whole + (current_ball + 1) / 10
        else:
            new_overs = whole + 1.0
        return new_overs

    # In the first innings, check if the innings should end.
    if score.current_innings == 1:
        if getattr(score, current_wickets_field) >= 10 or score.overs >= 20:
            if first_innings_team == match.team1:
                target = score.team1_runs + 1
            else:
                target = score.team2_runs + 1
            Commentary.objects.create(match=match, text=f"{current_team} has given target of {target}!")
            # Transition to second innings; record first innings score as the target.
            score.current_innings = 2
            score.overs = 0  # Reset overs for the second innings.
            score.save()
            return redirect('live_scores')
    else:
        # In second innings, calculate the target from the first innings.
        if first_innings_team == match.team1:
            target = score.team1_runs + 1
        else:
            target = score.team2_runs + 1

        second_innings_runs = getattr(score, current_runs_field)
        second_innings_wickets = getattr(score, current_wickets_field)
        
        # Check if the chasing team has reached or surpassed the target.
        if second_innings_runs >= target:
            Commentary.objects.create(match=match, text=f"{current_team} have chased down the target! {current_team} wins!")
            match.winner = current_team  # Record the winner.
            match.save()
            return redirect('live_scores')
        
        # Check if the chasing team is all out before reaching the target.
        if second_innings_wickets >= 10:
            Commentary.objects.create(match=match, text=f"{current_team} are all out. {first_innings_team} wins!")
            match.winner = first_innings_team  # Record the winner.
            match.save()
            return redirect('live_scores')
        
        # Check if 20 overs have been completed in the second innings.
        if score.overs >= 20:
            if second_innings_runs < target:
                run_diff = target - second_innings_runs - 1  # runs short of target
                Commentary.objects.create(match=match, text=f"Second innings over. {first_innings_team} wins by {run_diff} runs!")
                match.winner = first_innings_team  # Record the winner.
            else:
                Commentary.objects.create(match=match, text=f"Second innings complete and target chased. {current_team} wins!")
                match.winner = current_team  # Record the winner.
            match.save()
            return redirect('live_scores')
    
    if request.method == 'POST':
        if request.POST.get('update_type') == 'random':
            run_options = [0, 1, 2, 3, 4, 6]
            run_weights = [15, 40, 30, 5, 5, 5]
            run_scored = random.choices(run_options, weights=run_weights, k=1)[0]
            
            # Set wicket chance in percent.
            wicket_chance_percent = 50
            wicket_taken = random.random() < (wicket_chance_percent / 100)
            
            if wicket_taken:
                run_scored = random.choice([0, 1])
                setattr(score, current_wickets_field, getattr(score, current_wickets_field) + 1)
                commentary_text = f"WICKET! {current_team} lost a wicket."
            else:
                commentary_text = f"{run_scored} runs scored!" 
            
            setattr(score, current_runs_field, getattr(score, current_runs_field) + run_scored)
            score.overs = min(increment_overs(score.overs), 20)
            score.save()
            Commentary.objects.create(match=match, text=commentary_text)
            
            # In second innings, re-check win conditions after the update.
            if score.current_innings == 2:
                if first_innings_team == match.team1:
                    target = score.team1_runs + 1
                else:
                    target = score.team2_runs + 1

                second_innings_runs = getattr(score, current_runs_field)
                second_innings_wickets = getattr(score, current_wickets_field)
                
                if second_innings_runs >= target:
                    Commentary.objects.create(match=match, text=f"{current_team} have chased down the target! {current_team} wins!")
                    match.winner = current_team
                    match.save()
                    return redirect('live_scores')
                if second_innings_wickets >= 10:
                    Commentary.objects.create(match=match, text=f"{current_team} are all out. {first_innings_team} wins!")
                    match.winner = first_innings_team
                    match.save()
                    return redirect('live_scores')
                if score.overs >= 20:
                    if second_innings_runs < target:
                        run_diff = target - second_innings_runs - 1
                        Commentary.objects.create(match=match, text=f"Second innings over. {first_innings_team} wins by {run_diff} runs!")
                        match.winner = first_innings_team
                    else:
                        Commentary.objects.create(match=match, text=f"Second innings complete and target chased. {current_team} wins!")
                        match.winner = current_team
                    match.save()
                    return redirect('live_scores')
        else:
            form = ScoreUpdateForm(request.POST, instance=score)
            if form.is_valid():
                form.save()
        
        # Prepare score data for broadcasting.
        score_data = {
            "match_id": match.id,
            "team1": match.team1,
            "team2": match.team2,
            "team1_runs": score.team1_runs,
            "team2_runs": score.team2_runs,
            "team1_wickets": score.team1_wickets,
            "team2_wickets": score.team2_wickets,
            "overs": score.overs,
            "commentary": commentary_text,
        }
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "live_scores",
            {
                "type": "send_update",
                "message": score_data,
            }
        )
        return redirect('live_scores')
    else:
        form = ScoreUpdateForm(instance=score)
    
    context = {
        'form': form,
        'match': match,
        'current_team': current_team,
        'current_innings': score.current_innings,
    }
    return render(request, 'score_app/update_score.html', context)

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('live_scores')
        else:
            return render(request, 'score_app/login.html', {'error': 'Invalid username or password'})
    return render(request, 'score_app/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def previous_matches(request):
    prev_matches = Match.objects.filter(winner__isnull=False).order_by('-start_time')
    context = {'prev_matches': prev_matches}
    return render(request, 'score_app/previous_matches.html', context)

@login_required
def match_commentary(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    commentary_list = match.commentary.all().order_by('-timestamp')
    context = {'match':match, 'commentary_list':commentary_list}
    return render(request, 'score_app/match_commentary.html', context)