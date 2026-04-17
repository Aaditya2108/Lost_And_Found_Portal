from django.db import models
from django.conf import settings
from datetime import timedelta
from django.utils import timezone

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
    image = models.ImageField(upload_to='items/', blank=True, null=True)
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
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Resolution for {self.item.title}"

