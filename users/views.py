"""
Users App Views - User Profile Management and Dashboard
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import View as GenericView
from django.views.generic import TemplateView, UpdateView, ListView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy, reverse
from django.db.models import Count
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import json
import logging

from accounts.models import CustomUser as User
from .forms import UserProfileForm, UserPreferencesForm
from tickets.models import Ticket
from sales.models import DemoRequest, PricingRequest, SalesLead

logger = logging.getLogger(__name__)


class StaffRequiredMixin(UserPassesTestMixin):
    """میکسین برای دسترسی محدود به staff"""
    def test_func(self):
        return self.request.user.is_staff


class UserDashboardView(LoginRequiredMixin, TemplateView):
    """User dashboard with overview of activities"""
    template_name = 'users/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Ticket statistics
        context['total_tickets'] = Ticket.objects.filter(user=user).count()
        context['open_tickets'] = Ticket.objects.filter(user=user, status='open').count()
        context['resolved_tickets'] = Ticket.objects.filter(user=user, status='resolved').count()
        context['recent_tickets'] = Ticket.objects.filter(user=user).order_by('-created_at')[:5]
        
        # Sales requests
        context['demo_requests'] = DemoRequest.objects.filter(user=user).count()
        context['pricing_requests'] = PricingRequest.objects.filter(user=user).count()
        context['recent_demos'] = DemoRequest.objects.filter(user=user).order_by('-created_at')[:3]
        context['recent_pricing'] = PricingRequest.objects.filter(user=user).order_by('-created_at')[:3]
        
        # Sales leads (if user has any)
        context['sales_leads'] = SalesLead.objects.filter(email=user.email).count()
        
        # User activity summary
        context['account_age_days'] = (timezone.now() - user.created_at).days
        context['last_login'] = user.last_login
        
        return context


class ProfileView(LoginRequiredMixin, TemplateView):
    """User profile view"""
    template_name = 'users/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """Edit user profile"""
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('users:profile')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'پروفایل شما با موفقیت بروزرسانی شد.')
        return response


class UserPreferencesView(LoginRequiredMixin, UpdateView):
    """User preferences and settings"""
    model = User
    form_class = UserPreferencesForm
    template_name = 'users/preferences.html'
    success_url = reverse_lazy('users:preferences')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'تنظیمات شما با موفقیت ذخیره شد.')
        return response


class UserTicketsView(LoginRequiredMixin, ListView):
    """User's tickets list"""
    model = Ticket
    template_name = 'users/tickets.html'
    context_object_name = 'tickets'
    paginate_by = 10
    
    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_tickets'] = Ticket.objects.filter(user=self.request.user).count()
        context['open_tickets'] = Ticket.objects.filter(user=self.request.user, status='open').count()
        context['resolved_tickets'] = Ticket.objects.filter(user=self.request.user, status='resolved').count()
        return context


class UserRequestsView(LoginRequiredMixin, TemplateView):
    """User's demo and pricing requests"""
    template_name = 'users/requests.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        context['demo_requests'] = DemoRequest.objects.filter(user=user).order_by('-created_at')
        context['pricing_requests'] = PricingRequest.objects.filter(user=user).order_by('-created_at')
        context['total_demos'] = context['demo_requests'].count()
        context['total_pricing'] = context['pricing_requests'].count()
        
        return context


class UserActivityView(LoginRequiredMixin, TemplateView):
    """User activity log and statistics"""
    template_name = 'users/activity.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Activity statistics
        context['account_created'] = user.created_at
        context['last_login'] = user.last_login
        context['account_age_days'] = (timezone.now() - user.created_at).days
        
        # Recent activity
        context['recent_tickets'] = Ticket.objects.filter(user=user).order_by('-created_at')[:10]
        context['recent_demos'] = DemoRequest.objects.filter(user=user).order_by('-created_at')[:5]
        context['recent_pricing'] = PricingRequest.objects.filter(user=user).order_by('-created_at')[:5]
        
        # Monthly activity
        from django.db.models import Count
        from django.db.models.functions import TruncMonth
        
        context['monthly_tickets'] = Ticket.objects.filter(user=user).annotate(
            month=TruncMonth('created_at')
        ).values('month').annotate(count=Count('id')).order_by('month')
        
        return context


# API Views
class UserProfileAPIView(APIView):
    """API endpoint for user profile data"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'full_name': user.full_name,
            'user_type': user.user_type,
            'company_name': user.company_name,
            'job_title': user.job_title,
            'phone_number': user.phone_number,
            'is_email_verified': user.is_email_verified,
            'is_phone_verified': user.is_phone_verified,
            'two_factor_enabled': user.two_factor_enabled,
            'language': user.language,
            'timezone': user.timezone,
            'theme': user.theme,
            'created_at': user.created_at,
            'last_login': user.last_login,
        })
    
    def patch(self, request):
        user = request.user
        data = request.data
        
        # Update allowed fields
        allowed_fields = [
            'first_name', 'last_name', 'company_name', 'job_title', 
            'phone_number', 'language', 'timezone', 'theme'
        ]
        
        for field in allowed_fields:
            if field in data:
                setattr(user, field, data[field])
        
        user.save()
        
        return Response({
            'success': True,
            'message': 'پروفایل بروزرسانی شد'
        })


class UserPreferencesAPIView(APIView):
    """API endpoint for user preferences"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        return Response({
            'language': user.language,
            'timezone': user.timezone,
            'theme': user.theme,
            'email_notifications': user.email_notifications,
            'sms_notifications': user.sms_notifications,
            'marketing_emails': user.marketing_emails,
        })
    
    def patch(self, request):
        user = request.user
        data = request.data
        
        # Update preferences
        preferences_fields = [
            'language', 'timezone', 'theme', 'email_notifications',
            'sms_notifications', 'marketing_emails'
        ]
        
        for field in preferences_fields:
            if field in data:
                setattr(user, field, data[field])
        
        user.save()
        
        return Response({
            'success': True,
            'message': 'تنظیمات ذخیره شد'
        })


class UserStatsAPIView(APIView):
    """API endpoint for user statistics"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        # Calculate statistics
        total_tickets = Ticket.objects.filter(user=user).count()
        open_tickets = Ticket.objects.filter(user=user, status='open').count()
        resolved_tickets = Ticket.objects.filter(user=user, status='resolved').count()
        
        demo_requests = DemoRequest.objects.filter(user=user).count()
        pricing_requests = PricingRequest.objects.filter(user=user).count()
        
        return Response({
            'tickets': {
                'total': total_tickets,
                'open': open_tickets,
                'resolved': resolved_tickets,
            },
            'requests': {
                'demo': demo_requests,
                'pricing': pricing_requests,
            },
            'account_age_days': (timezone.now() - user.created_at).days,
            'last_login': user.last_login,
        })


# AJAX Views
@login_required
def update_profile_ajax(request):
    """Update user profile via AJAX"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = request.user
            
            # Update allowed fields
            allowed_fields = [
                'first_name', 'last_name', 'company_name', 'job_title', 
                'phone_number', 'bio'
            ]
            
            for field in allowed_fields:
                if field in data:
                    setattr(user, field, data[field])
            
            user.save()
            
            return JsonResponse({
                'success': True,
                'message': 'پروفایل بروزرسانی شد'
            })
        except Exception as e:
            logger.error(f"AJAX profile update error: {e}")
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid method'})


@login_required
def update_preferences_ajax(request):
    """Update user preferences via AJAX"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = request.user
            
            # Update preferences
            preferences_fields = [
                'language', 'timezone', 'theme', 'email_notifications',
                'sms_notifications', 'marketing_emails'
            ]
            
            for field in preferences_fields:
                if field in data:
                    setattr(user, field, data[field])
            
            user.save()
            
            return JsonResponse({
                'success': True,
                'message': 'تنظیمات ذخیره شد'
            })
        except Exception as e:
            logger.error(f"AJAX preferences update error: {e}")
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid method'})


@login_required
def delete_account_ajax(request):
    """Delete user account via AJAX"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            password = data.get('password')
            
            # Verify password
            if not request.user.check_password(password):
                return JsonResponse({
                    'success': False,
                    'error': 'رمز عبور اشتباه است'
                })
            
            # Delete user account
            user_email = request.user.email
            request.user.delete()
            
            # Send confirmation email
            try:
                send_mail(
                    'حذف حساب کاربری',
                    f'حساب کاربری {user_email} با موفقیت حذف شد.',
                    settings.DEFAULT_FROM_EMAIL,
                    [user_email],
                    fail_silently=True,
                )
            except Exception as e:
                logger.error(f"Failed to send account deletion email: {e}")
            
            return JsonResponse({
                'success': True,
                'message': 'حساب کاربری با موفقیت حذف شد',
                'redirect_url': reverse('products:home')
            })
        except Exception as e:
            logger.error(f"AJAX account deletion error: {e}")
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid method'})


# CRUD Views برای مدیریت کاربران (Staff Only)
class UserListView(StaffRequiredMixin, ListView):
    """فهرست کاربران (Staff)"""
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = User.objects.all().order_by('-created_at')
        
        # فیلتر بر اساس نوع کاربر
        user_type = self.request.GET.get('user_type')
        if user_type:
            queryset = queryset.filter(user_type=user_type)
            
        # فیلتر بر اساس وضعیت
        is_active = self.request.GET.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active == 'true')
            
        return queryset


class UserCreateView(StaffRequiredMixin, CreateView):
    """ایجاد کاربر جدید (Staff)"""
    model = User
    template_name = 'users/user_form.html'
    fields = ['email', 'first_name', 'last_name', 'user_type', 'is_active', 'is_staff']
    success_url = reverse_lazy('users:user_list')
    
    def form_valid(self, form):
        # تولید رمز عبور موقت
        import secrets
        import string
        temp_password = ''.join(secrets.choices(string.ascii_letters + string.digits, k=12))
        form.instance.set_password(temp_password)
        
        messages.success(self.request, f'کاربر جدید با موفقیت ایجاد شد. رمز عبور موقت: {temp_password}')
        return super().form_valid(form)


class UserUpdateView(StaffRequiredMixin, UpdateView):
    """ویرایش کاربر (Staff)"""
    model = User
    template_name = 'users/user_form.html'
    fields = ['email', 'first_name', 'last_name', 'user_type', 'is_active', 'is_staff', 'is_superuser']
    success_url = reverse_lazy('users:user_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'کاربر با موفقیت به‌روزرسانی شد.')
        return super().form_valid(form)


class UserDeleteView(StaffRequiredMixin, DeleteView):
    """حذف کاربر (Staff)"""
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('users:user_list')
    
    def get_success_url(self):
        messages.success(self.request, 'کاربر با موفقیت حذف شد.')
        return super().get_success_url()


class UserDetailView(StaffRequiredMixin, TemplateView):
    """جزئیات کاربر (Staff)"""
    template_name = 'users/user_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, pk=kwargs['pk'])
        context['user'] = user
        
        # آمار فعالیت‌های کاربر
        context['ticket_count'] = Ticket.objects.filter(user=user).count()
        context['demo_requests'] = DemoRequest.objects.filter(user=user).count()
        context['pricing_requests'] = PricingRequest.objects.filter(user=user).count()
        
        return context


# Advanced User Panel Views
class AdvancedDashboardView(LoginRequiredMixin, TemplateView):
    """داشبورد پیشرفته کاربری"""
    template_name = 'users/advanced_dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # User statistics
        context['active_tickets'] = Ticket.objects.filter(user=user, status__in=['open', 'in_progress']).count()
        context['total_downloads'] = getattr(user, 'downloads_count', 0)
        context['computation_sessions'] = getattr(user, 'computation_sessions_count', 0)
        context['user_score'] = getattr(user, 'user_score', 0)
        
        # Recent activities (mock data for now)
        from datetime import timedelta
        from django.utils import timezone
        context['recent_activities'] = [
            {
                'icon': 'ticket-alt',
                'description': 'تیکت جدید ایجاد شد',
                'timestamp': timezone.now() - timedelta(hours=2)
            },
            {
                'icon': 'download',
                'description': 'محصول BudgetPro دانلود شد',
                'timestamp': timezone.now() - timedelta(hours=5)
            },
            {
                'icon': 'calculator',
                'description': 'محاسبه بودجه انجام شد',
                'timestamp': timezone.now() - timedelta(days=1)
            }
        ]
        
        # Notifications (mock data for now)
        context['notifications'] = [
            {
                'icon': 'info-circle',
                'color': 'blue',
                'message': 'نسخه جدید BudgetPro منتشر شد',
                'timestamp': timezone.now() - timedelta(hours=1)
            },
            {
                'icon': 'check-circle',
                'color': 'green',
                'message': 'تیکت شما حل شد',
                'timestamp': timezone.now() - timedelta(hours=3)
            }
        ]
        
        # System status
        api_calls = getattr(user, 'api_calls_count', 0) or 0
        api_limit = getattr(user, 'api_rate_limit', 1000) or 1000
        context['api_usage_percentage'] = (api_calls / api_limit) * 100 if api_limit > 0 else 0
        context['storage_used'] = getattr(user, 'storage_used_mb', 0)
        
        return context

class AdvancedProfileView(LoginRequiredMixin, TemplateView):
    """پروفایل پیشرفته کاربری"""
    template_name = 'users/advanced_profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Add user's API keys
        context['api_keys'] = getattr(user, 'api_keys', [])
        context['two_factor_enabled'] = getattr(user, 'two_factor_enabled', False)
        
        return context

class ChangePasswordView(LoginRequiredMixin, View):
    """تغییر رمز عبور"""
    def post(self, request):
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        
        if not old_password or not new_password:
            messages.error(request, 'لطفاً تمام فیلدها را پر کنید')
            return redirect('users:advanced_profile')
        
        if not request.user.check_password(old_password):
            messages.error(request, 'رمز عبور فعلی اشتباه است')
            return redirect('users:advanced_profile')
        
        request.user.set_password(new_password)
        request.user.save()
        
        messages.success(request, 'رمز عبور با موفقیت تغییر کرد')
        return redirect('users:advanced_profile')

class Enable2FAView(LoginRequiredMixin, TemplateView):
    """فعال‌سازی احراز هویت دو مرحله‌ای"""
    template_name = 'users/enable_2fa.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Generate QR code for 2FA setup
        context['qr_code'] = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=='
        return context

class Disable2FAView(LoginRequiredMixin, View):
    """غیرفعال‌سازی احراز هویت دو مرحله‌ای"""
    def post(self, request):
        # Disable 2FA for user
        user = request.user
        user.two_factor_enabled = False
        user.save()
        
        messages.success(request, 'احراز هویت دو مرحله‌ای غیرفعال شد')
        return redirect('users:advanced_profile')

class CreateAPIKeyView(LoginRequiredMixin, TemplateView):
    """ایجاد کلید API"""
    template_name = 'users/create_api_key.html'
    
    def post(self, request):
        import secrets
        name = request.POST.get('name')
        if not name:
            messages.error(request, 'نام کلید API الزامی است')
            return redirect('users:create_api_key')
        
        # Create API key (mock implementation)
        api_key = f"takotech_{secrets.token_urlsafe(32)}"
        
        # Save to user's API keys (mock)
        messages.success(request, f'کلید API ایجاد شد: {api_key}')
        return redirect('users:advanced_profile')

class DeleteAPIKeyView(LoginRequiredMixin, View):
    """حذف کلید API"""
    def post(self, request, pk):
        # Delete API key (mock implementation)
        messages.success(request, 'کلید API حذف شد')
        return redirect('users:advanced_profile')