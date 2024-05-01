from django.db import models
from django.contrib.auth.models import User


# ----> TICKET MODEL
class Ticket(models.Model):

    class Status(models.TextChoices):
        CLOSED = 'CLOSED'
        PENDING = 'PENDING'
        APPROVED = 'APPROVED'
        REJECTED = 'REJECTED'

    class Priority(models.IntegerChoices):
        LOW = 1
        NORMAL = 2
        HIGH = 3
        CRITICAL = 4

    title = models.CharField(max_length=100)
    description = models.TextField()
    #category = models.ForeignKey('Category', on_delete=models.CASCADE)
    seeker = models.ForeignKey(User, related_name='tickets_as_agent', on_delete=models.CASCADE, default=None, null=True)
    agent = models.ForeignKey(User, related_name='tickets_as_seeker', on_delete=models.CASCADE, default=None, null=True)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.PENDING)
    priority = models.IntegerField(choices=Priority.choices, default=Priority.NORMAL)
    resolved = models.BooleanField(default=False)


# Create your models here.
