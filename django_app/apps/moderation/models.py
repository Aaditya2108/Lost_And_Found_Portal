from django.db import models
from django.conf import settings
from apps.items.models import Item

class Report(models.Model):
    REPORT_REASONS = (
        ('SPAM', 'Spam'),
        ('INAPPROPRIATE', 'Inappropriate Content'),
        ('FAKE', 'Fake Item'),
        ('OTHER', 'Other'),
    )
    
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='reports')
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reason = models.CharField(max_length=20, choices=REPORT_REASONS)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Report for {self.item.title} by {self.reported_by.username}"
