from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fields_of_interest = models.ManyToManyField('FieldOfInterest', blank=True)

    def __str__(self):
        return self.user.username


class FieldOfInterest(models.Model):
    name = models.CharField(max_length=100)
    challenges = models.ManyToManyField('Challenge', blank=True)  # Keep this as 'challenges'

    def __str__(self):
        return self.name
    
class Challenge(models.Model):
    name = models.CharField(max_length=100)
    total_days = models.IntegerField()
    field_of_interest = models.ForeignKey(
        'FieldOfInterest',
        on_delete=models.CASCADE,
        related_name='challenge_set',
        null=True,  # Allow NULL values
        blank=True  # Allow blank values in forms
    )
    def __str__(self):
        return self.name

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.message}"
    
class UploadedFile(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    challenge = models.ForeignKey('Challenge', on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')  # Generic file field
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.challenge.name}"


class Badge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    awarded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.challenge.name} Badge"