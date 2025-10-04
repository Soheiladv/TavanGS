"""
Settings App URLs - Dynamic CSS and Configuration
"""

from django.urls import path
from . import views

app_name = 'settings_app'

urlpatterns = [
    # Dynamic CSS generation
    path('css/dynamic.css', views.DynamicCSSView.as_view(), name='dynamic_css'),

    # Cache
    path('cache/clear-css/', views.clear_css_cache, name='clear_css_cache'),

    # Staff Control Panel
    path('control/', views.ControlPanelDashboardView.as_view(), name='control_dashboard'),
    path('control/templates/', views.TemplatesManageView.as_view(), name='control_templates'),
    path('control/features/', views.FeatureFlagsManageView.as_view(), name='control_features'),
    path('control/users/', views.UsersManageView.as_view(), name='control_users'),

    # Fonts CRUD
    path('control/fonts/', views.FontListView.as_view(), name='fonts_list'),
    path('control/fonts/create/', views.FontCreateView.as_view(), name='fonts_create'),
    path('control/fonts/<int:pk>/edit/', views.FontUpdateView.as_view(), name='fonts_edit'),
    path('control/fonts/<int:pk>/delete/', views.FontDeleteView.as_view(), name='fonts_delete'),

    # Site Templates CRUD
    path('control/templates/', views.SiteTemplateListView.as_view(), name='template_list'),
    path('control/templates/create/', views.SiteTemplateCreateView.as_view(), name='template_create'),
    path('control/templates/<int:pk>/edit/', views.SiteTemplateUpdateView.as_view(), name='template_edit'),
    path('control/templates/<int:pk>/delete/', views.SiteTemplateDeleteView.as_view(), name='template_delete'),

    # Feature Flags CRUD
    path('control/features/', views.FeatureFlagListView.as_view(), name='feature_flag_list'),
    path('control/features/create/', views.FeatureFlagCreateView.as_view(), name='feature_flag_create'),
    path('control/features/<int:pk>/edit/', views.FeatureFlagUpdateView.as_view(), name='feature_flag_edit'),
    path('control/features/<int:pk>/delete/', views.FeatureFlagDeleteView.as_view(), name='feature_flag_delete'),

    # SEO
    path('control/seo/', views.SeoManageView.as_view(), name='control_seo'),
]
