"""
Sales App URLs - Sales and Version Management
"""

from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    # Product versions
    path('versions/', views.ProductVersionListView.as_view(), name='version_list'),
    path('versions/<slug:product_slug>/', views.ProductVersionsView.as_view(), name='product_versions'),
    path('version/<slug:product_slug>/<str:version>/', views.VersionDetailView.as_view(), name='version_detail'),
    
    # Downloads
    path('download/<slug:product_slug>/', views.ProductDownloadView.as_view(), name='product_download'),
    path('trial/<slug:product_slug>/', views.TrialDownloadView.as_view(), name='trial_download'),
    
    # Lead generation
    path('demo-request/', views.DemoRequestView.as_view(), name='demo_request'),
    path('demo-request/success/', views.DemoRequestSuccessView.as_view(), name='demo_request_success'),
    path('pricing-request/', views.PricingRequestView.as_view(), name='pricing_request'),
    path('pricing-request/success/', views.PricingRequestSuccessView.as_view(), name='pricing_request_success'),
    
    # Sales dashboard
    path('dashboard/', views.SalesDashboardView.as_view(), name='dashboard'),
    
    # CRUD Management (Staff Only)
    # Product Versions CRUD
    path('versions/create/', views.ProductVersionCreateView.as_view(), name='version_create'),
    path('versions/<int:pk>/edit/', views.ProductVersionUpdateView.as_view(), name='version_edit'),
    path('versions/<int:pk>/delete/', views.ProductVersionDeleteView.as_view(), name='version_delete'),
    
    # Demo Requests Management (Staff)
    path('demos/', views.DemoRequestListView.as_view(), name='demo_request_list'),
    path('demos/<int:pk>/edit/', views.DemoRequestUpdateView.as_view(), name='demo_request_edit'),
    
    # Pricing Requests Management (Staff)
    path('pricing/', views.PricingRequestListView.as_view(), name='pricing_request_list'),
    path('pricing/<int:pk>/edit/', views.PricingRequestUpdateView.as_view(), name='pricing_request_edit'),
    
    # Sales Leads Management (Staff)
    path('leads/', views.SalesLeadListView.as_view(), name='sales_lead_list'),
    path('leads/create/', views.SalesLeadCreateView.as_view(), name='sales_lead_create'),
    path('leads/<int:pk>/edit/', views.SalesLeadUpdateView.as_view(), name='sales_lead_edit'),
    
    # AJAX endpoints
    path('ajax/product/<slug:product_slug>/versions/', views.get_product_versions, name='ajax_product_versions'),
    path('ajax/download/<uuid:session_id>/complete/', views.track_download_completion, name='ajax_download_complete'),
]
