from rest_framework import serializers
from .models import Item, Category, Location

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    location_name = serializers.ReadOnlyField(source='location.name')
    author_name = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Item
        fields = [
            'id', 'title', 'description', 'status', 'category', 'category_name',
            'location', 'location_name', 'date', 'image', 'user', 'author_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']
