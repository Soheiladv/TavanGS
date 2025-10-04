"""
News App URLs - News Management URLs
"""

from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    # Public URLs
    path('', views.NewsListView.as_view(), name='news_list'),
    path('<slug:slug>/', views.NewsDetailView.as_view(), name='news_detail'),
    path('<slug:news_slug>/comment/', views.add_comment, name='add_comment'),
    path('<slug:news_slug>/like/', views.NewsLikeView.as_view(), name='news_like'),
    path('rss/', views.news_rss_feed, name='rss_feed'),
    
    # Staff URLs - News Management
    path('create/', views.NewsCreateView.as_view(), name='news_create'),
    path('<int:pk>/edit/', views.NewsUpdateView.as_view(), name='news_edit'),
    path('<int:pk>/delete/', views.NewsDeleteView.as_view(), name='news_delete'),
    path('dashboard/', views.NewsDashboardView.as_view(), name='dashboard'),
    
    # Staff URLs - Category Management
    path('categories/', views.NewsCategoryListView.as_view(), name='category_list'),
    path('categories/create/', views.NewsCategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/edit/', views.NewsCategoryUpdateView.as_view(), name='category_edit'),
    path('categories/<int:pk>/delete/', views.NewsCategoryDeleteView.as_view(), name='category_delete'),
]
