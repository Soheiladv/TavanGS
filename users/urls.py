"""
Users App URLs - User Management and Profile
"""

from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Dashboard and profile
    path('dashboard/', views.UserDashboardView.as_view(), name='dashboard'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    path('preferences/', views.UserPreferencesView.as_view(), name='preferences'),
    
    # User activities
    path('tickets/', views.UserTicketsView.as_view(), name='tickets'),
    path('requests/', views.UserRequestsView.as_view(), name='requests'),
    path('activity/', views.UserActivityView.as_view(), name='activity'),
    
    # API endpoints
    path('api/profile/', views.UserProfileAPIView.as_view(), name='api_profile'),
    path('api/preferences/', views.UserPreferencesAPIView.as_view(), name='api_preferences'),
    path('api/stats/', views.UserStatsAPIView.as_view(), name='api_stats'),
    
    # AJAX endpoints
    path('ajax/profile/update/', views.update_profile_ajax, name='ajax_profile_update'),
    path('ajax/preferences/update/', views.update_preferences_ajax, name='ajax_preferences_update'),
    path('ajax/account/delete/', views.delete_account_ajax, name='ajax_account_delete'),
    
    # CRUD Management (Staff Only)
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/create/', views.UserCreateView.as_view(), name='user_create'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    path('users/<int:pk>/edit/', views.UserUpdateView.as_view(), name='user_edit'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
    
    # Advanced User Panel
    path('advanced-dashboard/', views.AdvancedDashboardView.as_view(), name='advanced_dashboard'),
    path('advanced-profile/', views.AdvancedProfileView.as_view(), name='advanced_profile'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('enable-2fa/', views.Enable2FAView.as_view(), name='enable_2fa'),
    path('disable-2fa/', views.Disable2FAView.as_view(), name='disable_2fa'),
    path('create-api-key/', views.CreateAPIKeyView.as_view(), name='create_api_key'),
    path('delete-api-key/<int:pk>/', views.DeleteAPIKeyView.as_view(), name='delete_api_key'),
]
