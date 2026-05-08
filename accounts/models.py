from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar_initial = models.CharField(max_length=2, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.avatar_initial and self.user:
            name = self.user.first_name or self.user.username
            self.avatar_initial = name[:2].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}'s profile"
