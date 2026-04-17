from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.items.models import Resolution

class Command(BaseCommand):
    help = 'Deletes resolved items older than their delete_after date'

    def handle(self, *args, **options):
        expired = Resolution.objects.filter(delete_after__lte=timezone.now())
        count = expired.count()
        
        for resolution in expired:
            item = resolution.item
            self.stdout.write(f'Deleting resolved item: {item.title}')
            item.delete()  # This cascades and deletes the Resolution too
        
        self.stdout.write(self.style.SUCCESS(f'Successfully cleaned up {count} resolved items.'))
