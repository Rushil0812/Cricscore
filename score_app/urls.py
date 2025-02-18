from django.urls import path
from score_app import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('live_scores/', views.live_scores, name='live_scores'),
    path('previous_matches/', views.previous_matches, name='previous_matches'),
    path('previous-matches/<int:match_id>/commentary/', views.match_commentary, name='match_commentary'),
    path('update_score/<int:match_id>/', views.update_score, name='update_score'),
    path('create_match/', views.create_match, name='create_match'),
    path('delete_match/<int:match_id>/', views.delete_match, name='delete_match'),
    path('match/<int:match_id>/toss/', views.toss_decision_view, name='toss_decision'),
    path('match/<int:match_id>/', views.match_detail, name='match_detail'),  
    path('logout/', views.user_logout, name='logout'),
]
