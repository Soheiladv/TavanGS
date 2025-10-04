"""
Services App URLs - Service Showcase
"""

from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    # Service listing and details
    path('', views.ServiceListView.as_view(), name='list'),
    path('<slug:slug>/', views.ServiceDetailView.as_view(), name='detail'),
    path('create/new/', views.ServiceCreateView.as_view(), name='create'),
    path('<slug:slug>/edit/', views.ServiceUpdateView.as_view(), name='edit'),
    path('<slug:slug>/delete/', views.ServiceDeleteView.as_view(), name='delete'),
    
    # Service categories
    path('category/<slug:slug>/', views.ServiceCategoryView.as_view(), name='category'),
    path('categories/', views.ServiceCategoryListView.as_view(), name='category_list'),
    path('categories/create/', views.ServiceCategoryCreateView.as_view(), name='category_create'),
    path('categories/<slug:slug>/edit/', views.ServiceCategoryUpdateView.as_view(), name='category_edit'),
    path('categories/<slug:slug>/delete/', views.ServiceCategoryDeleteView.as_view(), name='category_delete'),
    
    # Interactive features
    path('consultation/request/', views.ConsultationRequestView.as_view(), name='consultation_request'),
    path('quote/request/', views.QuoteRequestView.as_view(), name='quote_request'),
    
    # AJAX endpoints
    path('ajax/contact/', views.service_contact_ajax, name='contact_ajax'),
]
