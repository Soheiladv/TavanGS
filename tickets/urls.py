"""
Tickets App URLs - Support System
"""

from django.urls import path
from . import views

app_name = 'tickets'

urlpatterns = [
    # Ticket management
    path('', views.TicketListView.as_view(), name='list'),
    path('create/', views.TicketCreateView.as_view(), name='create'),
    path('<uuid:ticket_id>/', views.TicketDetailView.as_view(), name='detail'),
    path('<uuid:ticket_id>/update/', views.TicketUpdateView.as_view(), name='update'),
    path('<uuid:ticket_id>/reply/', views.TicketReplyView.as_view(), name='reply'),
    
    # Dashboard and categories
    path('dashboard/', views.SupportDashboardView.as_view(), name='dashboard'),
    path('categories/', views.TicketCategoryListView.as_view(), name='category_list'),
    path('categories/create/', views.TicketCategoryCreateView.as_view(), name='category_create'),
    path('categories/<slug:slug>/edit/', views.TicketCategoryUpdateView.as_view(), name='category_edit'),
    path('categories/<slug:slug>/delete/', views.TicketCategoryDeleteView.as_view(), name='category_delete'),
    
    # AJAX endpoints
    path('ajax/create/', views.ticket_create_ajax, name='create_ajax'),
    path('ajax/<uuid:ticket_id>/reply/', views.ticket_reply_ajax, name='reply_ajax'),
    path('ajax/<uuid:ticket_id>/status/', views.ticket_status_update_ajax, name='status_update_ajax'),
]
