import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from django.utils import timezone
from apps.items.models import Item, Category, Location
from apps.accounts.models import CustomUser

def populate():
    # Create superuser if not exists
    if not CustomUser.objects.filter(username='admin').exists():
        CustomUser.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    
    user = CustomUser.objects.get(username='admin')
    
    # Categories
    cats = ['Electronics', 'Documents', 'Keys', 'Wallets', 'Clothing']
    for cat_name in cats:
        Category.objects.get_or_create(name=cat_name)
    
    # Locations
    locs = ['Main Library', 'Cafeteria', 'CS Building', 'Student Center', 'Sports Complex']
    for loc_name in locs:
        Location.objects.get_or_create(name=loc_name)
        
    categories = list(Category.objects.all())
    locations = list(Location.objects.all())
    
    # Items
    items_data = [
        ('Blue Laptop Bag', 'Lost a navy blue Dell laptop bag with chargers.', 'LOST'),
        ('iPhone 15 Pro', 'Found near the library entrance, silver color.', 'FOUND'),
        ('Silver Keychain', 'Keys with a silver keychain found in the cafeteria.', 'FOUND'),
        ('Brown Leather Wallet', 'Lost my wallet containing student ID.', 'LOST'),
        ('Black Umbrella', 'Found a large black umbrella in the CS building.', 'FOUND'),
    ]
    
    for title, desc, status in items_data:
        Item.objects.create(
            title=title,
            description=desc,
            status=status,
            category=random.choice(categories),
            location=random.choice(locations),
            date=timezone.now().date(),
            user=user
        )
    print("Populated dummy data.")

if __name__ == '__main__':
    populate()
