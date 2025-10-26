from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']



PRIORITY_CHOICES = [
    ('Low', 'Low'),
    ('Medium', 'Medium'),
    ('High', 'High'),
]

STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Completed', 'Completed'),
]

class Task(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    completed_at = models.DateTimeField(null=True, blank=True)

    def clean(self):
        # ✅ Ensure due date is in the future
        if self.due_date < timezone.now():
            raise ValidationError('Due date must be in the future.')

        # ✅ Prevent editing completed tasks (unless reverted)
        if self.pk:
            existing = Task.objects.filter(pk=self.pk).first()
            if existing and existing.status == 'Completed' and self.status != 'Completed':
                raise ValidationError('Cannot edit a completed task unless reverted to incomplete.')

    def save(self, *args, **kwargs):
        # ✅ Add completion timestamp when marked as completed
        if self.status == 'Completed' and self.completed_at is None:
            self.completed_at = timezone.now()

        # ✅ Reset timestamp if reverted to incomplete
        elif self.status == 'Pending' and self.completed_at is not None:
            self.completed_at = None

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.status})"
