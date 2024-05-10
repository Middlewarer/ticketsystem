from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return self.user.username


# ----> TICKET MODEL
class Ticket(models.Model):

    class Status(models.TextChoices):
        CLOSED = 'Closed'
        PENDING = 'Pending'
        APPROVED = 'Approved'
        REJECTED = 'Rejected'

    class Priority(models.IntegerChoices):
        LOW = 1
        NORMAL = 2
        HIGH = 3
        CRITICAL = 4

    title = models.CharField(max_length=100)
    description = models.TextField()
    #category = models.ForeignKey('Category', on_delete=models.CASCADE)
    seeker = models.ForeignKey(User, related_name='tickets_as_agent', on_delete=models.CASCADE, null=True)
    agent = models.ForeignKey(User, related_name='tickets_as_seeker', on_delete=models.CASCADE, default=None, null=True)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.PENDING)
    priority = models.IntegerField(choices=Priority.choices, default=Priority.NORMAL)
    resolved = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.seeker = self.seeker  # Установите seaker при создании билета
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# Create your models here.
