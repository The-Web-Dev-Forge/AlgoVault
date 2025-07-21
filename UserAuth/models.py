from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_used = models.BooleanField(default=False)
    
    def is_expired(self):
        # Token expires after 1 hour
        return timezone.now() > self.created_at + timezone.timedelta(hours=1)
    
    def __str__(self):
        return f"Password reset token for {self.user.username}"
