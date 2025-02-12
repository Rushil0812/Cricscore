from django.urls import re_path
from score_app import consumers

websocket_urlpatterns = [
    re_path(r'ws/live_scores/', consumers.LiveScoreConsumer.as_asgi()),
]