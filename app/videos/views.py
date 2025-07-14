from django.shortcuts import render, redirect, get_object_or_404
from .models import Video, Like, Dislike, Comment, ViewHistory
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count, F, Q, IntegerField, ExpressionWrapper, Max
from django.core.paginator import Paginator

import random

def home(request):
    videos = list(Video.objects.all())
    random.shuffle(videos)
    return render(request, 'videos/home.html', {'videos': videos})

@login_required
def upload_video(request):
    if request.method == 'POST':
        title = request.POST['title']
        embed_url = request.POST['youtube_embed_url']
        Video.objects.create(
            title=title,
            youtube_embed_url=embed_url,
            uploaded_by=request.user
        )
        return redirect('videos:home')
    return render(request, 'videos/upload.html')

@login_required
def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)

    ViewHistory.objects.create(user=request.user, video=video, watched_at=timezone.now())

    user_liked = Like.objects.filter(user=request.user, video=video).exists()
    user_disliked = Dislike.objects.filter(user=request.user, video=video).exists()
    comments = video.comments.order_by('-created_at')

    return render(request, 'videos/video_detail.html', {
        'video': video,
        'user_liked': user_liked,
        'user_disliked': user_disliked,
        'comments': comments,
    })


@login_required
def like_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    Like.objects.get_or_create(user=request.user, video=video)
    Dislike.objects.filter(user=request.user, video=video).delete()
    return redirect('videos:video_detail', video_id=video_id)


@login_required
def dislike_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    Dislike.objects.get_or_create(user=request.user, video=video)
    Like.objects.filter(user=request.user, video=video).delete()
    return redirect('videos:video_detail', video_id=video_id)


@login_required
def add_comment(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    text = request.POST.get("text", "").strip()
    if text:
        Comment.objects.create(user=request.user, video=video, text=text)
    return redirect('videos:video_detail', video_id=video_id)

def popular(request):
    videos = Video.objects.annotate(
        likes_count=Count('likes', distinct=True),
        dislikes_count=Count('dislikes', distinct=True),
        comments_count=Count('comments', distinct=True),
    ).annotate(
        popularity=ExpressionWrapper(
            F('likes_count') * 10 - F('dislikes_count') * 5 + F('comments_count'),
            output_field=IntegerField()
        )
    ).order_by('-popularity')[:5]

    return render(request, 'videos/popular.html', {'videos': videos})

@login_required
def history(request):
    latest_views = (
        ViewHistory.objects
        .filter(user=request.user)
        .values('video')
        .annotate(last_seen=Max('watched_at'))
    )

    video_to_timestamp = {
        entry['video']: entry['last_seen'] for entry in latest_views
    }

    view_histories = (
        ViewHistory.objects
        .filter(user=request.user, watched_at__in=video_to_timestamp.values())
        .select_related('video')
        .order_by('-watched_at')
    )

    paginator = Paginator(view_histories, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'videos/watch_history.html', {'page_obj': page_obj})