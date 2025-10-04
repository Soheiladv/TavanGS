"""
Products App Admin Configuration
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Product, ProductCategory


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    """Admin interface for product categories"""
    
    list_display = ['name', 'slug', 'icon_preview', 'color_preview', 'product_count', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Visual Elements', {
            'fields': ('icon', 'color')
        }),
        ('Settings', {
            'fields': ('is_active',)
        }),
    )
    
    def icon_preview(self, obj):
        """Show icon preview"""
        if obj.icon:
            return format_html(
                '<i class="fa fa-{}" style="font-size: 16px;"></i>',
                obj.icon
            )
        return '-'
    icon_preview.short_description = 'Icon'
    
    def color_preview(self, obj):
        """Show color preview"""
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border: 1px solid #ccc; border-radius: 3px;"></div>',
            obj.color
        )
    color_preview.short_description = 'Color'
    
    def product_count(self, obj):
        """Show number of products in category"""
        count = obj.products.count()
        if count > 0:
            url = reverse('admin:products_product_changelist') + f'?category__id__exact={obj.id}'
            return format_html('<a href="{}">{} محصول</a>', url, count)
        return '0 محصول'
    product_count.short_description = 'Products'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin interface for products"""
    
    list_display = [
        'full_name', 'category', 'status', 'logo_preview', 
        'view_count', 'download_count', 'is_featured', 'is_active'
    ]
    list_filter = [
        'category', 'status', 'is_featured', 'is_active', 
        'has_free_version', 'has_trial', 'created_at'
    ]
    search_fields = ['name', 'brand_prefix', 'description', 'short_description']
    prepopulated_fields = {'slug': ('brand_prefix', 'name')}
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                ('name', 'brand_prefix'),
                'slug',
                ('tagline',),
                'description',
                'short_description',
            )
        }),
        ('Classification', {
            'fields': (
                ('category', 'status'),
            )
        }),
        ('Visual Elements', {
            'fields': (
                'logo',
                'banner_image',
            ),
            'classes': ('collapse',)
        }),
        ('Features & Specifications', {
            'fields': (
                'features',
                'technical_specs',
            ),
            'classes': ('collapse',)
        }),
        ('Pricing & Trial', {
            'fields': (
                ('has_free_version', 'has_trial'),
                'trial_days',
            )
        }),
        ('Analytics', {
            'fields': (
                ('view_count', 'download_count'),
            ),
            'classes': ('collapse',)
        }),
        ('Admin Settings', {
            'fields': (
                ('is_featured', 'is_active'),
            )
        }),
    )
    
    readonly_fields = ['view_count', 'download_count', 'created_at', 'updated_at']
    
    def logo_preview(self, obj):
        """Show logo preview"""
        if obj.logo:
            return format_html(
                '<img src="{}" style="max-height: 30px; max-width: 50px;" />',
                obj.logo.url
            )
        return '-'
    logo_preview.short_description = 'Logo'
    
    def get_queryset(self, request):
        """Optimize queryset"""
        return super().get_queryset(request).select_related('category')
    
    actions = ['make_featured', 'remove_featured', 'activate_products', 'deactivate_products']
    
    def make_featured(self, request, queryset):
        """Mark products as featured"""
        count = queryset.update(is_featured=True)
        self.message_user(request, f'{count} محصول به عنوان ویژه انتخاب شد.')
    make_featured.short_description = 'انتخاب به عنوان محصول ویژه'
    
    def remove_featured(self, request, queryset):
        """Remove featured status"""
        count = queryset.update(is_featured=False)
        self.message_user(request, f'{count} محصول از حالت ویژه خارج شد.')
    remove_featured.short_description = 'حذف از محصولات ویژه'
    
    def activate_products(self, request, queryset):
        """Activate products"""
        count = queryset.update(is_active=True)
        self.message_user(request, f'{count} محصول فعال شد.')
    activate_products.short_description = 'فعال‌سازی محصولات'
    
    def deactivate_products(self, request, queryset):
        """Deactivate products"""
        count = queryset.update(is_active=False)
        self.message_user(request, f'{count} محصول غیرفعال شد.')
    deactivate_products.short_description = 'غیرفعال‌سازی محصولات'
    
    class Media:
        css = {
            'all': ('admin/css/products.css',)
        }
        js = ('admin/js/products.js',)