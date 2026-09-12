from django.contrib.auth.models import User
from django.db import models


class Explanation(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="explanations",
    )
    code = models.TextField()
    language = models.CharField(max_length=30)
    explanation = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.language}"