"""
Computation Engine URLs - Calculation API
"""

from django.urls import path
from . import views

app_name = 'computation_engine'

urlpatterns = [
    # Computation endpoints
    path('budget/', views.BudgetCalculationView.as_view(), name='budget_calculation'),
    path('security/', views.SecurityAnalysisView.as_view(), name='security_analysis'),
    path('ai/', views.AIInferenceView.as_view(), name='ai_inference'),
    
    # Session management
    path('session/<uuid:session_id>/', views.SessionDetailView.as_view(), name='session_detail'),
    path('session/<uuid:session_id>/status/', views.session_status_ajax, name='session_status'),
    
    # Templates
    path('templates/', views.TemplateListView.as_view(), name='templates'),
    
    # CRUD Management (Staff Only)
    # Templates CRUD
    path('templates/', views.ComputationTemplateListView.as_view(), name='template_list'),
    path('templates/create/', views.ComputationTemplateCreateView.as_view(), name='template_create'),
    path('templates/<int:pk>/edit/', views.ComputationTemplateUpdateView.as_view(), name='template_edit'),
    path('templates/<int:pk>/delete/', views.ComputationTemplateDeleteView.as_view(), name='template_delete'),
    
    # Sessions CRUD
    path('sessions/', views.ComputationSessionListView.as_view(), name='session_list'),
    path('sessions/create/', views.ComputationSessionCreateView.as_view(), name='session_create'),
    path('sessions/<int:pk>/edit/', views.ComputationSessionUpdateView.as_view(), name='session_edit'),
    
    # Results CRUD
    path('results/', views.ComputationResultListView.as_view(), name='result_list'),
    path('results/<int:pk>/edit/', views.ComputationResultUpdateView.as_view(), name='result_edit'),
    path('results/<int:pk>/delete/', views.ComputationResultDeleteView.as_view(), name='result_delete'),
    
    # Metrics CRUD
    path('metrics/', views.ComputationMetricsListView.as_view(), name='metrics_list'),
    path('metrics/create/', views.ComputationMetricsCreateView.as_view(), name='metrics_create'),
    path('metrics/<int:pk>/edit/', views.ComputationMetricsUpdateView.as_view(), name='metrics_edit'),
]
