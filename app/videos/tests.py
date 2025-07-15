from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Video, ViewHistory
from django.utils import timezone

from datetime import timedelta

class VideoViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test', password='1234')
        self.video = Video.objects.create(title="Video testeo", youtube_embed_url="url", uploaded_by=self.user)

    def test_popular_view_status(self):
        response = self.client.get(reverse('videos:popular'))
        self.assertEqual(response.status_code, 200)

    def test_popular_template_used(self):
        response = self.client.get(reverse('videos:popular'))
        self.assertTemplateUsed(response, 'videos/popular.html')

    def test_history_requires_auth(self):
        response = self.client.get(reverse('videos:watch_history'))
        self.assertEqual(response.status_code, 302)

    def test_history_logged_in_works(self):
        self.client.login(username='test', password='1234')
        ViewHistory.objects.create(user=self.user, video=self.video, watched_at=timezone.now())
        response = self.client.get(reverse('videos:watch_history'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'videos/watch_history.html')

    def test_video_appears_once_in_history(self):
        self.client.login(username='test', password='1234')
        now = timezone.now()
        ViewHistory.objects.create(user=self.user, video=self.video, watched_at=now - timedelta(minutes=2))
        ViewHistory.objects.create(user=self.user, video=self.video, watched_at=now)
        response = self.client.get(reverse('videos:watch_history'))
        self.assertContains(response, self.video.title, count=1)

    def test_history_only_for_logged_user(self):
        other_user = User.objects.create_user(username='other', password='abcd')
        ViewHistory.objects.create(user=other_user, video=self.video, watched_at=timezone.now())
        self.client.login(username='test', password='1234')
        response = self.client.get(reverse('videos:watch_history'))
        self.assertNotContains(response, self.video.title)