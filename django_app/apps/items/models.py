from django.db import models
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from apps.security_utils import validate_image_file, encrypt_data, decrypt_data

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    STATUS_CHOICES = (
        ('LOST', 'Lost'),
        ('FOUND', 'Found'),
        ('RESOLVED', 'Resolved'),
    )

    title = models.CharField(max_length=200, db_index=True)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, db_index=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    image = models.ImageField(upload_to='items/', blank=True, null=True, validators=[validate_image_file])
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='items')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.status})"

class Resolution(models.Model):
    """Tracks resolved items. Auto-deleted 1 week after creation."""
    item = models.OneToOneField(Item, on_delete=models.CASCADE, related_name='resolution')
    resolved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    receiver_username = models.CharField(max_length=150)
    receiver_contact = models.CharField(max_length=100)
    notes = models.TextField(blank=True, default='')
    resolved_at = models.DateTimeField(auto_now_add=True)
    delete_after = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.delete_after:
            self.delete_after = timezone.now() + timedelta(weeks=1)
        
        # Encrypt the contact info before saving if it's not already encrypted
        # We check if it looks like an encrypted string (Fernet strings start with gAAAA)
        if self.receiver_contact and not self.receiver_contact.startswith('gAAAA'):
            self.receiver_contact = encrypt_data(self.receiver_contact)
            
        super().save(*args, **kwargs)

    @property
    def decripted_contact(self):
        return decrypt_data(self.receiver_contact)

    def __str__(self):
        return f"Resolution for {self.item.title}"

