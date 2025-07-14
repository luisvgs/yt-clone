from django.db import models
from django.contrib.auth.models import User

class Video(models.Model):
    title = models.CharField(max_length=255)
    youtube_embed_url = models.URLField()
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def popularity_score(self):
        likes = self.likes.count()
        dislikes = self.dislikes.count()
        comments = self.comments.count()
        # return (likes + 10) - (dislikes + 5) + comments
        return (likes * 10) - (dislikes * 5) + comments

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, related_name="likes", on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'video')


class Dislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, related_name="dislikes", on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'video')


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='video_comments')
    video = models.ForeignKey(Video, related_name="comments", on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class ViewHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='video_view_history')
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    watched_at = models.DateTimeField(auto_now_add=True)