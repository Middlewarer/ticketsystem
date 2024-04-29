from django.db import models
from django.contrib.auth.models import User, AbstractUser

class UserProfile(AbstractUser):
    class Roles(models.TextChoices):
        CUSTOMER = 'CUSTOMER'
        AGENT = 'AGENT'
        ADMINISTRATOR = 'ADMINISTRATOR'

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(Roles.choices, max_length=50, default=Roles.CUSTOMER)


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
    seeker = models.ForeignKey(User, on_delete=models.CASCADE)
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.PENDING)
    priority = models.IntegerField(choices=Priority.choices, default=Priority.NORMAL)
    resolved = models.BooleanField(default=False)

# Create your models here.
