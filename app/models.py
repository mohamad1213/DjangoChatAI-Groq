from django.db import models
from django.contrib.auth.models import User

class AIResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    prompt = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        username = self.user.username if self.user else "Anonymous"
        return f"{username} - {self.created_at.date()}"

    class Meta:
        ordering = ['-created_at']
