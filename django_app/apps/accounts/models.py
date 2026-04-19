from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.security_utils import encrypt_data, decrypt_data

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('STUDENT', 'Student'),
        ('STAFF', 'Staff'),
        ('ADMIN', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='STUDENT')
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.phone_number and not self.phone_number.startswith('gAAAA'):
            self.phone_number = encrypt_data(self.phone_number)
        super().save(*args, **kwargs)

    @property
    def decripted_phone(self):
        return decrypt_data(self.phone_number)

    def __str__(self):
        return self.username
