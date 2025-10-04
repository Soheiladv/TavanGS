"""
TakoTech Website URL Configuration
Main routing for all apps and features
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from django.views.i18n import set_language
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# Import sitemaps (will create later)
# from .sitemaps import sitemaps

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Authentication
    path('auth/', include('allauth.urls')),
    path('users/', include('users.urls')),
    path('accounts/', include('accounts.urls')),
    
    # Main Apps
    path('', include('products.urls')),
    path('services/', include('services.urls')),
    path('sales/', include('sales.urls')),
    path('tickets/', include('tickets.urls')),
    path('compute/', include('computation_engine.urls')),
    path('settings/', include('settings_app.urls')),
    path('news/', include('news.urls')),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # Language and Internationalization
    path('i18n/setlang/', set_language, name='set_language'),
    
    # SEO and Utilities
    # path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    
    # Health check
    path('health/', TemplateView.as_view(template_name='health.html'), name='health_check'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    # Add debug toolbar
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns

# Custom error handlers
handler400 = 'takotech_website.views.bad_request'
handler403 = 'takotech_website.views.permission_denied'
handler404 = 'takotech_website.views.page_not_found'
handler500 = 'takotech_website.views.server_error'