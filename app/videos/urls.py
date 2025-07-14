from django.urls import path
from . import views

app_name = "videos"

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_video, name='upload_video'),
    path('video/<int:video_id>/', views.video_detail, name='video_detail'),
    path('video/<int:video_id>/like/', views.like_video, name='like_video'),
    path('video/<int:video_id>/dislike/', views.dislike_video, name='dislike_video'),
    path('video/<int:video_id>/comment/', views.add_comment, name='add_comment'),
    path('popular/', views.popular, name='popular'),
    path('history/', views.history, name='watch_history'),
]
