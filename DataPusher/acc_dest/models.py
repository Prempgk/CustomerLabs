from django.db import models
import uuid
from django.utils import timezone
from django_password_validators.password_character_requirements.password_validation import PasswordCharacterValidator
from django.contrib.auth.password_validation import MinimumLengthValidator


# Create your models here.

class Accounts(models.Model):  # Accounts model
    account_id = models.AutoField(primary_key=True)
    email_id = models.EmailField(null=False, blank=False, unique=True)
    password = models.CharField(max_length=20, null=False, blank=False)
    account_name = models.CharField(max_length=150, null=False, blank=False)
    acc_secret = models.UUIDField(default=uuid.uuid4().hex, null=False, blank=False, unique=True, editable=False)
    website = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(null=False, blank=False, default=timezone.now)
    updated_at = models.DateTimeField(null=True, blank=True)


class Destinations(models.Model):   # Destination model
    id = models.AutoField(primary_key=True)
    account = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    url = models.URLField(null=False, blank=False)
    http_method = models.CharField(choices=[('POST', "POST"), ('GET', "GET")], max_length=20, null=False, blank=False)
    headers = models.JSONField(null=False, blank=False)
    created_at = models.DateTimeField(null=False, blank=False, default=timezone.now)
    updated_at = models.DateTimeField(null=True, blank=True)
