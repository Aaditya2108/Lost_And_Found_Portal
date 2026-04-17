from django.db import models
from django.conf import settings
from apps.items.models import Item

class ContactRequest(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='contact_requests')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_requests')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request for {self.item.title} from {self.sender.username}"
