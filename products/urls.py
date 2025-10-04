"""
Products App URLs - Product Catalog and Showcase
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# API Router for REST endpoints
router = DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'categories', views.ProductCategoryViewSet)

app_name = 'products'

urlpatterns = [
    # Homepage
    path('', views.HomeView.as_view(), name='home'),
    
    # Product Catalog
    path('products/', views.ProductListView.as_view(), name='list'),
    path('products/create/', views.ProductCreateView.as_view(), name='create'),
    path('products/<slug:slug>/edit/', views.ProductUpdateView.as_view(), name='edit'),
    path('products/<slug:slug>/delete/', views.ProductDeleteView.as_view(), name='delete'),
    path('products/category/<slug:slug>/', views.ProductCategoryView.as_view(), name='category'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('categories/<slug:slug>/edit/', views.CategoryUpdateView.as_view(), name='category_edit'),
    path('categories/<slug:slug>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),
    path('products/<slug:slug>/', views.ProductDetailView.as_view(), name='detail'),
    
    # Product Features
    path('products/<slug:slug>/demo/', views.ProductDemoView.as_view(), name='demo'),
    path('products/<slug:slug>/trial/', views.ProductTrialView.as_view(), name='trial'),
    path('products/<slug:slug>/compare/', views.ProductCompareView.as_view(), name='compare'),
    
    # Interactive Features
    path('sandbox/', views.SandboxView.as_view(), name='sandbox'),
    path('sandbox/<slug:product_slug>/', views.ProductSandboxView.as_view(), name='product_sandbox'),
    
    # AJAX Endpoints
    path('ajax/product/<slug:slug>/view/', views.increment_product_view, name='increment_view'),
    path('ajax/product/<slug:slug>/download/', views.increment_product_download, name='increment_download'),
    path('ajax/search/', views.product_search_ajax, name='search_ajax'),
    
    # API Endpoints
    path('api/v1/', include(router.urls)),
    
    # Special Pages
    path('showcase/', views.ProductShowcaseView.as_view(), name='showcase'),
    path('featured/', views.FeaturedProductsView.as_view(), name='featured'),
    path('quiz/', views.HeroQuizView.as_view(), name='hero_quiz'),
]
