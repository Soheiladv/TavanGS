"""
Services App Views - Service Showcase
"""

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from .models import Service, ServiceCategory, ServiceInquiry
from .forms import ServiceForm, ServiceCategoryForm


class StaffRequiredMixin(UserPassesTestMixin):
    """میکسین برای دسترسی محدود به staff"""
    def test_func(self):
        return self.request.user.is_staff


class ServiceListView(ListView):
    """Service listing page"""
    model = Service
    template_name = 'services/list.html'
    context_object_name = 'services'
    paginate_by = 12
    
    def get_queryset(self):
        return Service.objects.filter(is_active=True).order_by('-is_featured', 'name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ServiceCategory.objects.filter(is_active=True)
        return context


class ServiceDetailView(DetailView):
    """Detailed service page"""
    model = Service
    template_name = 'services/detail.html'
    context_object_name = 'service'
    slug_field = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = self.object
        
        # Related services
        context['related_services'] = Service.objects.filter(
            category=service.category,
            is_active=True
        ).exclude(id=service.id)[:3]
        
        return context


class ServiceCategoryView(ListView):
    """Services filtered by category"""
    model = Service
    template_name = 'services/category.html'
    context_object_name = 'services'
    paginate_by = 12
    
    def get_queryset(self):
        self.category = get_object_or_404(ServiceCategory, slug=self.kwargs['slug'])
        return Service.objects.filter(
            category=self.category,
            is_active=True
        ).order_by('-is_featured', 'name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class ConsultationRequestView(CreateView):
    """Consultation request form"""
    model = ServiceInquiry
    template_name = 'services/consultation_request.html'
    fields = ['service', 'name', 'email', 'phone', 'company', 'subject', 'message', 'budget_range', 'timeline']
    success_url = reverse_lazy('services:list')
    
    def form_valid(self, form):
        form.instance.inquiry_type = 'consultation'
        messages.success(self.request, 'درخواست مشاوره شما با موفقیت ثبت شد. به زودی با شما تماس خواهیم گرفت.')
        return super().form_valid(form)


class QuoteRequestView(CreateView):
    """Quote request form"""
    model = ServiceInquiry
    template_name = 'services/quote_request.html'
    fields = ['service', 'name', 'email', 'phone', 'company', 'subject', 'message', 'budget_range', 'timeline']
    success_url = reverse_lazy('services:list')
    
    def form_valid(self, form):
        form.instance.inquiry_type = 'quote'
        messages.success(self.request, 'درخواست قیمت شما ثبت شد. پیشنهاد قیمت به زودی ارسال خواهد شد.')
        return super().form_valid(form)


def service_contact_ajax(request):
    """AJAX endpoint for service contact"""
    if request.method == 'POST':
        try:
            # Process contact form data
            data = {
                'name': request.POST.get('name'),
                'email': request.POST.get('email'),
                'message': request.POST.get('message'),
                'service_id': request.POST.get('service_id'),
            }
            
            # Create inquiry (simplified)
            if data['service_id']:
                service = Service.objects.get(id=data['service_id'])
                ServiceInquiry.objects.create(
                    service=service,
                    name=data['name'],
                    email=data['email'],
                    subject='تماس از وب‌سایت',
                    message=data['message'],
                    inquiry_type='general'
                )
            
            return JsonResponse({'success': True, 'message': 'پیام شما ارسال شد.'})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Method not allowed'})


# CRUD for Services
class ServiceCreateView(StaffRequiredMixin, CreateView):
    """ایجاد سرویس جدید"""
    model = Service
    form_class = ServiceForm
    template_name = 'services/form.html'
    success_url = reverse_lazy('services:list')
    
    def form_valid(self, form):
        messages.success(self.request, 'سرویس جدید با موفقیت ایجاد شد.')
        return super().form_valid(form)


class ServiceUpdateView(StaffRequiredMixin, UpdateView):
    """ویرایش سرویس"""
    model = Service
    form_class = ServiceForm
    template_name = 'services/form.html'
    slug_field = 'slug'
    success_url = reverse_lazy('services:list')
    
    def form_valid(self, form):
        messages.success(self.request, 'سرویس با موفقیت به‌روزرسانی شد.')
        return super().form_valid(form)


class ServiceDeleteView(StaffRequiredMixin, DeleteView):
    """حذف سرویس"""
    model = Service
    template_name = 'services/confirm_delete.html'
    slug_field = 'slug'
    success_url = reverse_lazy('services:list')
    
    def get_success_url(self):
        messages.success(self.request, 'سرویس با موفقیت حذف شد.')
        return super().get_success_url()


# CRUD for Service Categories
class ServiceCategoryListView(StaffRequiredMixin, ListView):
    """فهرست دسته‌بندی‌های سرویس"""
    model = ServiceCategory
    template_name = 'services/category_list.html'
    context_object_name = 'categories'
    paginate_by = 20
    
    def get_queryset(self):
        return ServiceCategory.objects.all().order_by('name')


class ServiceCategoryCreateView(StaffRequiredMixin, CreateView):
    """ایجاد دسته‌بندی سرویس جدید"""
    model = ServiceCategory
    form_class = ServiceCategoryForm
    template_name = 'services/category_form.html'
    success_url = reverse_lazy('services:category_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'دسته‌بندی سرویس جدید با موفقیت ایجاد شد.')
        return super().form_valid(form)


class ServiceCategoryUpdateView(StaffRequiredMixin, UpdateView):
    """ویرایش دسته‌بندی سرویس"""
    model = ServiceCategory
    form_class = ServiceCategoryForm
    template_name = 'services/category_form.html'
    slug_field = 'slug'
    success_url = reverse_lazy('services:category_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'دسته‌بندی سرویس با موفقیت به‌روزرسانی شد.')
        return super().form_valid(form)


class ServiceCategoryDeleteView(StaffRequiredMixin, DeleteView):
    """حذف دسته‌بندی سرویس"""
    model = ServiceCategory
    template_name = 'services/category_confirm_delete.html'
    slug_field = 'slug'
    success_url = reverse_lazy('services:category_list')
    
    def get_success_url(self):
        messages.success(self.request, 'دسته‌بندی سرویس با موفقیت حذف شد.')
        return super().get_success_url()