"""
Computation Engine Views - Calculation API
"""

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

from .models import ComputationSession, ComputationTemplate, ComputationResult, ComputationMetrics
from .forms import ComputationTemplateForm, ComputationSessionForm, ComputationResultForm, ComputationMetricsForm
from .services import BudgetCalculationService, SecurityAnalysisService, AIInferenceService


class StaffRequiredMixin(UserPassesTestMixin):
    """میکسین برای دسترسی محدود به staff"""
    def test_func(self):
        return self.request.user.is_staff


@method_decorator(csrf_exempt, name='dispatch')
class BudgetCalculationView(LoginRequiredMixin, TemplateView):
    """Budget calculation endpoint"""
    template_name = 'computation_engine/budget_calculation.html'
    
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            
            service = BudgetCalculationService(user=request.user)
            result = service.execute_with_session(data)
            
            return JsonResponse({
                'success': True,
                'result': result,
                'session_id': str(service.session.session_id)
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })


@method_decorator(csrf_exempt, name='dispatch')
class SecurityAnalysisView(LoginRequiredMixin, TemplateView):
    """Security analysis endpoint"""
    template_name = 'computation_engine/security_analysis.html'
    
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            
            service = SecurityAnalysisService(user=request.user)
            result = service.execute_with_session(data)
            
            return JsonResponse({
                'success': True,
                'result': result,
                'session_id': str(service.session.session_id)
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })


@method_decorator(csrf_exempt, name='dispatch')
class AIInferenceView(LoginRequiredMixin, TemplateView):
    """AI inference endpoint"""
    template_name = 'computation_engine/ai_inference.html'
    
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            
            service = AIInferenceService(user=request.user)
            result = service.execute_with_session(data)
            
            return JsonResponse({
                'success': True,
                'result': result,
                'session_id': str(service.session.session_id)
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })


class SessionDetailView(LoginRequiredMixin, DetailView):
    """Computation session detail"""
    model = ComputationSession
    template_name = 'computation_engine/session_detail.html'
    context_object_name = 'session'
    slug_field = 'session_id'
    slug_url_kwarg = 'session_id'
    
    def get_queryset(self):
        return ComputationSession.objects.filter(user=self.request.user)


class TemplateListView(TemplateView):
    """Available computation templates"""
    template_name = 'computation_engine/template_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['templates'] = ComputationTemplate.objects.filter(is_active=True)
        return context


class TemplateDetailView(DetailView):
    """Computation template detail"""
    model = ComputationTemplate
    template_name = 'computation_engine/template_detail.html'
    context_object_name = 'template'


def session_status_ajax(request, session_id):
    """AJAX endpoint for session status"""
    try:
        session = get_object_or_404(ComputationSession, session_id=session_id)
        
        return JsonResponse({
            'status': session.status,
            'progress': session.progress_percentage,
            'result': session.output_data if session.status == 'completed' else None,
            'error': session.error_message if session.status == 'failed' else None
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


# CRUD Views برای مدیریت (Staff Only)
class ComputationTemplateListView(StaffRequiredMixin, ListView):
    """فهرست قالب‌های محاسباتی (Staff)"""
    model = ComputationTemplate
    template_name = 'computation_engine/template_list.html'
    context_object_name = 'templates'
    paginate_by = 20
    
    def get_queryset(self):
        return ComputationTemplate.objects.all().order_by('name')


class ComputationTemplateCreateView(StaffRequiredMixin, CreateView):
    """ایجاد قالب محاسباتی جدید (Staff)"""
    model = ComputationTemplate
    form_class = ComputationTemplateForm
    template_name = 'computation_engine/template_form.html'
    success_url = reverse_lazy('computation_engine:template_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'قالب محاسباتی جدید با موفقیت ایجاد شد.')
        return super().form_valid(form)


class ComputationTemplateUpdateView(StaffRequiredMixin, UpdateView):
    """ویرایش قالب محاسباتی (Staff)"""
    model = ComputationTemplate
    form_class = ComputationTemplateForm
    template_name = 'computation_engine/template_form.html'
    success_url = reverse_lazy('computation_engine:template_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'قالب محاسباتی با موفقیت به‌روزرسانی شد.')
        return super().form_valid(form)


class ComputationTemplateDeleteView(StaffRequiredMixin, DeleteView):
    """حذف قالب محاسباتی (Staff)"""
    model = ComputationTemplate
    template_name = 'computation_engine/template_confirm_delete.html'
    success_url = reverse_lazy('computation_engine:template_list')
    
    def get_success_url(self):
        messages.success(self.request, 'قالب محاسباتی با موفقیت حذف شد.')
        return super().get_success_url()


class ComputationSessionListView(StaffRequiredMixin, ListView):
    """فهرست جلسات محاسباتی (Staff)"""
    model = ComputationSession
    template_name = 'computation_engine/session_list.html'
    context_object_name = 'sessions'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = ComputationSession.objects.all().order_by('-created_at')
        
        # فیلتر بر اساس وضعیت
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
            
        return queryset


class ComputationSessionCreateView(StaffRequiredMixin, CreateView):
    """ایجاد جلسه محاسباتی جدید (Staff)"""
    model = ComputationSession
    form_class = ComputationSessionForm
    template_name = 'computation_engine/session_form.html'
    success_url = reverse_lazy('computation_engine:session_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'جلسه محاسباتی جدید ایجاد شد.')
        return super().form_valid(form)


class ComputationSessionUpdateView(StaffRequiredMixin, UpdateView):
    """ویرایش جلسه محاسباتی (Staff)"""
    model = ComputationSession
    form_class = ComputationSessionForm
    template_name = 'computation_engine/session_form.html'
    success_url = reverse_lazy('computation_engine:session_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'جلسه محاسباتی به‌روزرسانی شد.')
        return super().form_valid(form)


class ComputationResultListView(StaffRequiredMixin, ListView):
    """فهرست نتایج محاسباتی (Staff)"""
    model = ComputationResult
    template_name = 'computation_engine/result_list.html'
    context_object_name = 'results'
    paginate_by = 20
    
    def get_queryset(self):
        return ComputationResult.objects.all().order_by('-created_at')


class ComputationResultUpdateView(StaffRequiredMixin, UpdateView):
    """ویرایش نتیجه محاسباتی (Staff)"""
    model = ComputationResult
    form_class = ComputationResultForm
    template_name = 'computation_engine/result_form.html'
    success_url = reverse_lazy('computation_engine:result_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'نتیجه محاسباتی به‌روزرسانی شد.')
        return super().form_valid(form)


class ComputationResultDeleteView(StaffRequiredMixin, DeleteView):
    """حذف نتیجه محاسباتی (Staff)"""
    model = ComputationResult
    template_name = 'computation_engine/result_confirm_delete.html'
    success_url = reverse_lazy('computation_engine:result_list')
    
    def get_success_url(self):
        messages.success(self.request, 'نتیجه محاسباتی حذف شد.')
        return super().get_success_url()


class ComputationMetricsListView(StaffRequiredMixin, ListView):
    """فهرست متریک‌های محاسباتی (Staff)"""
    model = ComputationMetrics
    template_name = 'computation_engine/metrics_list.html'
    context_object_name = 'metrics'
    paginate_by = 20
    
    def get_queryset(self):
        return ComputationMetrics.objects.all().order_by('-date')


class ComputationMetricsCreateView(StaffRequiredMixin, CreateView):
    """ایجاد متریک محاسباتی جدید (Staff)"""
    model = ComputationMetrics
    form_class = ComputationMetricsForm
    template_name = 'computation_engine/metrics_form.html'
    success_url = reverse_lazy('computation_engine:metrics_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'متریک محاسباتی جدید ایجاد شد.')
        return super().form_valid(form)


class ComputationMetricsUpdateView(StaffRequiredMixin, UpdateView):
    """ویرایش متریک محاسباتی (Staff)"""
    model = ComputationMetrics
    form_class = ComputationMetricsForm
    template_name = 'computation_engine/metrics_form.html'
    success_url = reverse_lazy('computation_engine:metrics_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'متریک محاسباتی به‌روزرسانی شد.')
        return super().form_valid(form)