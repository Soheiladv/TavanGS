"""
Products App Serializers - API Serialization
"""

from rest_framework import serializers
from .models import Product, ProductCategory


class ProductCategorySerializer(serializers.ModelSerializer):
    """Serializer for product categories"""
    
    class Meta:
        model = ProductCategory
        fields = [
            'id', 'name', 'slug', 'description', 'icon', 
            'color', 'is_active', 'created_at'
        ]
        read_only_fields = ['created_at']


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for products"""
    
    category = ProductCategorySerializer(read_only=True)
    full_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'full_name', 'slug', 'brand_prefix',
            'tagline', 'description', 'short_description',
            'category', 'status', 'logo', 'banner_image',
            'features', 'technical_specs', 'has_free_version',
            'has_trial', 'trial_days', 'view_count', 'download_count',
            'is_featured', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'view_count', 'download_count', 'created_at', 'updated_at'
        ]


class ProductSummarySerializer(serializers.ModelSerializer):
    """Lightweight serializer for product summaries"""
    
    category_name = serializers.CharField(source='category.name', read_only=True)
    full_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'full_name', 'slug', 'short_description',
            'category_name', 'logo', 'is_featured'
        ]
