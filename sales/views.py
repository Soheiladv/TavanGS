"""
Sales App Views - Product Versions, Downloads, and Lead Generation
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.db.models import Q, Count, Subquery, OuterRef
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
import uuid
import logging

from .models import ProductVersion, DownloadSession, DemoRequest, PricingRequest, SalesLead
from .forms import ProductVersionForm, DemoRequestForm, PricingRequestForm, SalesLeadAdminForm
from products.models import Product

logger = logging.getLogger(__name__)


class StaffRequiredMixin(UserPassesTestMixin):
    """میکسین برای دسترسی محدود به staff"""
    def test_func(self):
        return self.request.user.is_staff


class ProductVersionListView(ListView):
    """List all product versions across all products"""
    model = ProductVersion
    template_name = 'sales/version_list.html'
    context_object_name = 'versions'
    paginate_by = 20
    
    def get_queryset(self):
        return ProductVersion.objects.filter(is_active=True).select_related('product')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(is_active=True)
        # DB-agnostic latest version per product (avoids DISTINCT ON)
        latest_versions = []
        for p in context['products']:
            v = ProductVersion.objects.filter(product=p, is_active=True).order_by('-release_date').first()
            if v:
                latest_versions.append(v)
        context['latest_versions'] = latest_versions
        return context


class ProductVersionsView(ListView):
    """List versions for a specific product"""
    model = ProductVersion
    template_name = 'sales/product_versions.html'
    context_object_name = 'versions'
    paginate_by = 15
    
    def get_queryset(self):
        self.product = get_object_or_404(Product, slug=self.kwargs['product_slug'])
        return ProductVersion.objects.filter(
            product=self.product, 
            is_active=True
        ).order_by('-release_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.product
        context['latest_version'] = self.get_queryset().first()
        return context


class VersionDetailView(DetailView):
    """Detailed view of a specific product version"""
    model = ProductVersion
    template_name = 'sales/version_detail.html'
    context_object_name = 'version'
    
    def get_object(self):
        product = get_object_or_404(Product, slug=self.kwargs['product_slug'])
        return get_object_or_404(
            ProductVersion,
            product=product,
            version_number=self.kwargs['version'],
            is_active=True
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.object.product
        context['other_versions'] = ProductVersion.objects.filter(
            product=self.object.product,
            is_active=True
        ).exclude(id=self.object.id).order_by('-release_date')[:5]
        return context


class ProductDownloadView(DetailView):
    """Handle product downloads with tracking"""
    model = ProductVersion
    template_name = 'sales/product_download.html'
    
    def get_object(self):
        product = get_object_or_404(Product, slug=self.kwargs['product_slug'])
        return get_object_or_404(
            ProductVersion,
            product=product,
            is_active=True
        ).order_by('-release_date').first()  # Get latest version
    
    def get(self, request, *args, **kwargs):
        version = self.get_object()
        
        # Create download session
        download_session = DownloadSession.objects.create(
            user=request.user if request.user.is_authenticated else None,
            product_version=version,
            download_type='full',
            ip_address=self.get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        # Increment download count
        version.download_count += 1
        version.save(update_fields=['download_count'])
        
        # Log the download
        logger.info(f"Download initiated: {version.full_version_name} by {download_session.ip_address}")
        
        context = {
            'version': version,
            'download_session': download_session,
        }
        return render(request, self.template_name, context)
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class TrialDownloadView(DetailView):
    """Handle trial downloads with tracking"""
    model = ProductVersion
    template_name = 'sales/trial_download.html'
    
    def get_object(self):
        product = get_object_or_404(Product, slug=self.kwargs['product_slug'])
        return get_object_or_404(
            ProductVersion,
            product=product,
            has_trial=True,
            is_active=True
        ).order_by('-release_date').first()
    
    def get(self, request, *args, **kwargs):
        version = self.get_object()
        
        # Create download session
        download_session = DownloadSession.objects.create(
            user=request.user if request.user.is_authenticated else None,
            product_version=version,
            download_type='trial',
            ip_address=self.get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        # Increment trial count
        version.trial_count += 1
        version.save(update_fields=['trial_count'])
        
        # Create sales lead if user is not authenticated
        if not request.user.is_authenticated:
            SalesLead.objects.create(
                source='trial_download',
                full_name='Anonymous User',
                email='anonymous@example.com',
                product_interest=version.product,
                notes=f'Trial download of {version.full_version_name}'
            )
        
        context = {
            'version': version,
            'download_session': download_session,
            'trial_days': version.trial_days,
        }
        return render(request, self.template_name, context)
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class DemoRequestView(CreateView):
    """Handle demo requests"""
    model = DemoRequest
    form_class = DemoRequestForm
    template_name = 'sales/demo_request.html'
    success_url = reverse_lazy('sales:demo_request_success')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(is_active=True)
        return context
    
    def form_valid(self, form):
        # Set user if authenticated
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
            form.instance.email = self.request.user.email
            form.instance.full_name = self.request.user.full_name
        
        response = super().form_valid(form)
        
        # Create sales lead
        SalesLead.objects.create(
            source='demo_request',
            full_name=form.instance.full_name,
            email=form.instance.email,
            phone=form.instance.phone,
            company=form.instance.company,
            job_title=form.instance.job_title,
            product_interest=form.instance.product,
            notes=f'Demo request for {form.instance.product.full_name}'
        )
        
        # Send notification email (if configured)
        try:
            send_mail(
                f'Demo Request: {form.instance.product.full_name}',
                f'A new demo request has been submitted by {form.instance.full_name}',
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently=True,
            )
        except Exception as e:
            logger.error(f"Failed to send demo request email: {e}")
        
        messages.success(
            self.request, 
            'درخواست دمو شما با موفقیت ثبت شد. تیم فروش به زودی با شما تماس خواهد گرفت.'
        )
        
        return response


class PricingRequestView(CreateView):
    """Handle pricing requests"""
    model = PricingRequest
    form_class = PricingRequestForm
    template_name = 'sales/pricing_request.html'
    success_url = reverse_lazy('sales:pricing_request_success')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(is_active=True)
        return context
    
    def form_valid(self, form):
        # Set user if authenticated
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
            form.instance.email = self.request.user.email
            form.instance.full_name = self.request.user.full_name
        
        response = super().form_valid(form)
        
        # Create sales lead
        SalesLead.objects.create(
            source='pricing_request',
            full_name=form.instance.full_name,
            email=form.instance.email,
            phone=form.instance.phone,
            company=form.instance.company,
            job_title=form.instance.job_title,
            product_interest=form.instance.product,
            notes=f'Pricing request for {form.instance.product.full_name}'
        )
        
        # Send notification email (if configured)
        try:
            send_mail(
                f'Pricing Request: {form.instance.product.full_name}',
                f'A new pricing request has been submitted by {form.instance.full_name}',
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently=True,
            )
        except Exception as e:
            logger.error(f"Failed to send pricing request email: {e}")
        
        messages.success(
            self.request, 
            'درخواست قیمت شما با موفقیت ثبت شد. تیم فروش به زودی با شما تماس خواهد گرفت.'
        )
        
        return response


class DemoRequestSuccessView(TemplateView):
    """Success page for demo requests"""
    template_name = 'sales/demo_request_success.html'


class PricingRequestSuccessView(TemplateView):
    """Success page for pricing requests"""
    template_name = 'sales/pricing_request_success.html'


class SalesDashboardView(LoginRequiredMixin, TemplateView):
    """Sales dashboard for staff members"""
    template_name = 'sales/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Only allow staff members
        if not self.request.user.is_staff:
            return context
        
        # Sales statistics
        context['total_leads'] = SalesLead.objects.count()
        context['new_leads'] = SalesLead.objects.filter(status='new').count()
        context['demo_requests'] = DemoRequest.objects.filter(status='pending').count()
        context['pricing_requests'] = PricingRequest.objects.filter(status='pending').count()
        
        # Recent activity
        context['recent_leads'] = SalesLead.objects.order_by('-created_at')[:10]
        context['recent_demos'] = DemoRequest.objects.order_by('-created_at')[:5]
        context['recent_pricing'] = PricingRequest.objects.order_by('-created_at')[:5]
        
        # Download statistics
        context['total_downloads'] = DownloadSession.objects.filter(is_completed=True).count()
        context['trial_downloads'] = DownloadSession.objects.filter(
            download_type='trial', 
            is_completed=True
        ).count()
        
        return context


# AJAX Views for dynamic content
def get_product_versions(request, product_slug):
    """AJAX endpoint to get versions for a product"""
    try:
        product = get_object_or_404(Product, slug=product_slug)
        versions = ProductVersion.objects.filter(
            product=product, 
            is_active=True
        ).order_by('-release_date')
        
        data = {
            'versions': [
                {
                    'version_number': v.version_number,
                    'version_type': v.get_version_type_display(),
                    'release_date': v.release_date.strftime('%Y-%m-%d'),
                    'changelog': v.changelog[:200] + '...' if len(v.changelog) > 200 else v.changelog,
                    'download_url': v.download_url,
                    'is_free': v.is_free,
                    'price': str(v.price) if v.price else None,
                }
                for v in versions
            ]
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def track_download_completion(request, session_id):
    """AJAX endpoint to track download completion"""
    try:
        session = get_object_or_404(DownloadSession, session_id=session_id)
        session.is_completed = True
        session.completed_at = timezone.now()
        session.save()
        
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# CRUD Views برای مدیریت (Staff Only)
class ProductVersionCreateView(StaffRequiredMixin, CreateView):
    """ایجاد نسخه محصول جدید"""
    model = ProductVersion
    form_class = ProductVersionForm
    template_name = 'sales/version_form.html'
    success_url = reverse_lazy('sales:version_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'نسخه محصول جدید با موفقیت ایجاد شد.')
        return super().form_valid(form)


class ProductVersionUpdateView(StaffRequiredMixin, UpdateView):
    """ویرایش نسخه محصول"""
    model = ProductVersion
    form_class = ProductVersionForm
    template_name = 'sales/version_form.html'
    success_url = reverse_lazy('sales:version_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'نسخه محصول با موفقیت به‌روزرسانی شد.')
        return super().form_valid(form)


class ProductVersionDeleteView(StaffRequiredMixin, DeleteView):
    """حذف نسخه محصول"""
    model = ProductVersion
    template_name = 'sales/version_confirm_delete.html'
    success_url = reverse_lazy('sales:version_list')
    
    def get_success_url(self):
        messages.success(self.request, 'نسخه محصول با موفقیت حذف شد.')
        return super().get_success_url()


class DemoRequestListView(StaffRequiredMixin, ListView):
    """فهرست درخواست‌های دمو (Staff)"""
    model = DemoRequest
    template_name = 'sales/demo_request_list.html'
    context_object_name = 'demo_requests'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = DemoRequest.objects.all().order_by('-created_at')
        
        # فیلتر بر اساس وضعیت
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
            
        return queryset


class DemoRequestUpdateView(StaffRequiredMixin, UpdateView):
    """ویرایش درخواست دمو (مدیریت وضعیت توسط Staff)"""
    model = DemoRequest
    template_name = 'sales/demo_request_form.html'
    fields = ['status', 'assigned_to', 'notes', 'scheduled_at']
    success_url = reverse_lazy('sales:demo_request_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'وضعیت درخواست دمو به‌روزرسانی شد.')
        return super().form_valid(form)


class PricingRequestListView(StaffRequiredMixin, ListView):
    """فهرست درخواست‌های قیمت (Staff)"""
    model = PricingRequest
    template_name = 'sales/pricing_request_list.html'
    context_object_name = 'pricing_requests'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = PricingRequest.objects.all().order_by('-created_at')
        
        # فیلتر بر اساس وضعیت
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
            
        return queryset


class PricingRequestUpdateView(StaffRequiredMixin, UpdateView):
    """ویرایش درخواست قیمت (مدیریت پاسخ توسط Staff)"""
    model = PricingRequest
    template_name = 'sales/pricing_request_admin_form.html'
    fields = ['status', 'quoted_price', 'currency', 'assigned_to', 'response_notes', 'responded_at']
    success_url = reverse_lazy('sales:pricing_request_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'پاسخ درخواست قیمت بع‌روزرسانی شد.')
        return super().form_valid(form)


class SalesLeadListView(StaffRequiredMixin, ListView):
    """فهرست سرنخ‌های فروش (Staff)"""
    model = SalesLead
    template_name = 'sales/sales_lead_list.html'
    context_object_name = 'sales_leads'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = SalesLead.objects.all().order_by('-created_at')
        
        # فیلتر بر اساس وضعیت
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
            
        return queryset


class SalesLeadUpdateView(StaffRequiredMixin, UpdateView):
    """ویرایش سرنخ فروش"""
    model = SalesLead
    form_class = SalesLeadAdminForm
    template_name = 'sales/sales_lead_form.html'
    success_url = reverse_lazy('sales:sales_lead_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'سرنخ فروش به‌روزرسانی شد.')
        return super().form_valid(form)


class SalesLeadCreateView(StaffRequiredMixin, CreateView):
    """ایجاد سرنخ فروش جدید"""
    model = SalesLead
    form_class = SalesLeadAdminForm
    template_name = 'sales/sales_lead_form.html'
    success_url = reverse_lazy('sales:sales_lead_list')
    
    def form_valid(self, form):
        form.instance.lead_id = uuid.uuid4()
        messages.success(self.request, 'سرنخ فروش جدید ایجاد شد.')
        return super().form_valid(form)