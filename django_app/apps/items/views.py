from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Item, Category, Location, Resolution
from .forms import ItemForm, ResolutionForm
from .serializers import ItemSerializer, CategorySerializer, LocationSerializer
from rest_framework import viewsets, permissions

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class LocationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all().order_by('-created_at')
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@login_required
def report_item_view(request, status):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.status = status.upper()
            item.save()
            return redirect('items:index')
    else:
        form = ItemForm()
    
    context = {
        'form': form,
        'status': status.capitalize(),
        'title': f'Report {status.capitalize()} Item'
    }
    return render(request, 'items/report_item.html', context)

def item_detail_view(request, pk):
    item = get_object_or_404(Item, pk=pk)
    resolve_form = ResolutionForm()
    return render(request, 'items/item_detail.html', {
        'item': item,
        'resolve_form': resolve_form,
    })

@login_required
def contact_info_view(request, pk):
    """Return the reporter's contact info as JSON."""
    item = get_object_or_404(Item, pk=pk)
    user = item.user
    return JsonResponse({
        'username': user.username,
        'email': user.email or 'Not provided',
        'phone': getattr(user, 'phone_number', '') or 'Not provided',
    })

@login_required
def resolve_item_view(request, pk):
    """Mark an item as resolved and save receiver details."""
    item = get_object_or_404(Item, pk=pk)
    
    if request.method == 'POST':
        form = ResolutionForm(request.POST)
        if form.is_valid():
            resolution = form.save(commit=False)
            resolution.item = item
            resolution.resolved_by = request.user
            resolution.save()
            item.status = 'RESOLVED'
            item.save()
            messages.success(request, f'"{item.title}" has been marked as resolved. Record will be cleared in 1 week.')
            return redirect('items:index')
        else:
            messages.error(request, 'Please fill in all required fields.')
            return redirect('items:item_detail', pk=pk)
    
    return redirect('items:item_detail', pk=pk)

def index_view(request):
    items = Item.objects.exclude(status='RESOLVED').order_by('-created_at')[:12]
    return render(request, 'items/index.html', {'items': items})

def seed_data_view(request):
    """Temporary tool to seed categories and locations."""
    from django.http import HttpResponse
    if not request.user.is_superuser:
        return HttpResponse("Unauthorized", status=401)
        
    categories = ['Electronics', 'Bags & Wallets', 'Keys', 'Documents', 'Clothing', 'Others']
    locations = ['Main Lobby', 'Cafeteria', 'Library', 'Sports Complex', 'Boys Hostel', 'Girls Hostel', 'Academic Block']
    
    # Clear existing to avoid duplicates if user runs it multiple times
    Category.objects.all().delete()
    Location.objects.all().delete()
    
    for cat in categories:
        Category.objects.get_or_create(name=cat)
        
    for loc in locations:
        Location.objects.get_or_create(name=loc)
        
    return HttpResponse("<h1>Success!</h1><p>Categories and Locations have been seeded.</p><p>You can now go back and report items.</p>")
