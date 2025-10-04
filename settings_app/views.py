"""
Settings App Views - Dynamic CSS, Control Panel, and Font/SEO Management
"""

from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.core.cache import cache
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib import messages

from .models import SiteSettings, SiteTemplate, FeatureFlag, FontSettings
from news.models import News, NewsCategory, NewsTag


class DynamicCSSView(TemplateView):
    template_name = 'settings_app/dynamic_css.html'
    content_type = 'text/css'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cache_key = 'site_settings_css'
        settings_data = cache.get(cache_key)
        if settings_data is None:
            try:
                site_settings = SiteSettings.load()
                settings_data = {
                    'primary_color': site_settings.primary_color,
                    'secondary_color': site_settings.secondary_color,
                    'accent_color': site_settings.accent_color,
                    'font_family': site_settings.font_family,
                    'layout_direction': site_settings.layout_direction,
                    'template_theme': site_settings.template_theme,
                    'header_style': site_settings.header_style,
                    'footer_style': site_settings.footer_style,
                    'custom_css': site_settings.custom_css,
                }
                cache.set(cache_key, settings_data, 3600)
            except Exception:
                settings_data = {
                    'primary_color': '#2563eb',
                    'secondary_color': '#7c3aed',
                    'accent_color': '#f59e0b',
                    'font_family': 'Vazir, Tahoma, sans-serif',
                    'layout_direction': 'rtl',
                    'template_theme': 'modern',
                    'header_style': 'fixed',
                    'footer_style': 'full',
                    'custom_css': '',
                }
        context.update(settings_data)
        return context


def clear_css_cache(request):
    if request.user.is_staff:
        cache.delete('site_settings_css')
        return HttpResponse('CSS cache cleared', content_type='text/plain')
    return HttpResponse('Unauthorized', status=401)


# =========================
# Staff Control Panel Views
# =========================

User = get_user_model()


@method_decorator(staff_member_required, name='dispatch')
class ControlPanelDashboardView(TemplateView):
    template_name = 'settings_app/control_panel/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = SiteSettings.load()
        context['templates_count'] = SiteTemplate.objects.count()
        context['active_templates'] = SiteTemplate.objects.filter(is_active=True).count()
        context['feature_flags'] = FeatureFlag.objects.order_by('-updated_at')[:10]
        context['users_count'] = User.objects.count()
        context['staff_count'] = User.objects.filter(is_staff=True).count()
        context['fonts_count'] = FontSettings.objects.count()
        return context


@method_decorator(staff_member_required, name='dispatch')
class TemplatesManageView(TemplateView):
    template_name = 'settings_app/control_panel/templates.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['templates'] = SiteTemplate.objects.order_by('-is_default', 'template_type', 'name')
        return context


@method_decorator(staff_member_required, name='dispatch')
class FeatureFlagsManageView(TemplateView):
    template_name = 'settings_app/control_panel/features.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['flags'] = FeatureFlag.objects.all().order_by('name')
        return context


@method_decorator(staff_member_required, name='dispatch')
class UsersManageView(TemplateView):
    template_name = 'settings_app/control_panel/users.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all().order_by('-date_joined')[:50]
        context['staff'] = User.objects.filter(is_staff=True).order_by('-date_joined')[:50]
        return context


# ============
# Fonts CRUD
# ============

@method_decorator(staff_member_required, name='dispatch')
class FontListView(ListView):
    model = FontSettings
    template_name = 'settings_app/control_panel/fonts_list.html'
    context_object_name = 'fonts'
    paginate_by = 20


@method_decorator(staff_member_required, name='dispatch')
class FontCreateView(CreateView):
    model = FontSettings
    fields = ['name','family_name','font_file','font_format','font_weight','is_active','is_default','is_rtl_support','description']
    template_name = 'settings_app/control_panel/fonts_form.html'
    success_url = reverse_lazy('settings_app:fonts_list')

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.uploaded_by = self.request.user
        return super().form_valid(form)


@method_decorator(staff_member_required, name='dispatch')
class FontUpdateView(UpdateView):
    model = FontSettings
    fields = ['name','family_name','font_file','font_format','font_weight','is_active','is_default','is_rtl_support','description']
    template_name = 'settings_app/control_panel/fonts_form.html'
    success_url = reverse_lazy('settings_app:fonts_list')


@method_decorator(staff_member_required, name='dispatch')
class FontDeleteView(DeleteView):
    model = FontSettings
    template_name = 'settings_app/control_panel/fonts_confirm_delete.html'
    success_url = reverse_lazy('settings_app:fonts_list')


# =========
# SEO Page
# =========

@method_decorator(staff_member_required, name='dispatch')
class SeoManageView(TemplateView):
    template_name = 'settings_app/control_panel/seo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Placeholder context; can be bound to SiteSettings fields if present
        context['meta_defaults'] = {
            'title': 'TakoTech - پلتفرم راهکارهای هوشمند',
            'description': 'راهکارهای نرم‌افزاری، امنیتی و هوش مصنوعی',
            'keywords': 'هوش مصنوعی, امنیت, نرم‌افزار, SaaS',
        }
        return context


# CRUD Views for SiteTemplate
@method_decorator(staff_member_required, name='dispatch')
class SiteTemplateListView(ListView):
    """فهرست تمپلیت‌های سایت (Staff)"""
    model = SiteTemplate
    template_name = 'settings_app/control_panel/template_list.html'
    context_object_name = 'templates'
    paginate_by = 20
    
    def get_queryset(self):
        return SiteTemplate.objects.all().order_by('name')


@method_decorator(staff_member_required, name='dispatch')
class SiteTemplateCreateView(CreateView):
    """ایجاد تمپلیت سایت جدید (Staff)"""
    model = SiteTemplate
    template_name = 'settings_app/control_panel/template_form.html'
    fields = ['name', 'description', 'template_type', 'content', 'is_active', 'is_default']
    success_url = reverse_lazy('settings_app:template_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'تمپلیت سایت جدید با موفقیت ایجاد شد.')
        return super().form_valid(form)


@method_decorator(staff_member_required, name='dispatch')
class SiteTemplateUpdateView(UpdateView):
    """ویرایش تمپلیت سایت (Staff)"""
    model = SiteTemplate
    template_name = 'settings_app/control_panel/template_form.html'
    fields = ['name', 'description', 'template_type', 'content', 'is_active', 'is_default']
    success_url = reverse_lazy('settings_app:template_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'تمپلیت سایت با موفقیت به‌روزرسانی شد.')
        return super().form_valid(form)


@method_decorator(staff_member_required, name='dispatch')
class SiteTemplateDeleteView(DeleteView):
    """حذف تمپلیت سایت (Staff)"""
    model = SiteTemplate
    template_name = 'settings_app/control_panel/template_confirm_delete.html'
    success_url = reverse_lazy('settings_app:template_list')
    
    def get_success_url(self):
        messages.success(self.request, 'تمپلیت سایت با موفقیت حذف شد.')
        return super().get_success_url()


# CRUD Views for FeatureFlag
@method_decorator(staff_member_required, name='dispatch')
class FeatureFlagListView(ListView):
    """فهرست فیچر فلگ‌ها (Staff)"""
    model = FeatureFlag
    template_name = 'settings_app/control_panel/feature_flag_list.html'
    context_object_name = 'feature_flags'
    paginate_by = 20
    
    def get_queryset(self):
        return FeatureFlag.objects.all().order_by('name')


@method_decorator(staff_member_required, name='dispatch')
class FeatureFlagCreateView(CreateView):
    """ایجاد فیچر فلگ جدید (Staff)"""
    model = FeatureFlag
    template_name = 'settings_app/control_panel/feature_flag_form.html'
    fields = ['name', 'description', 'is_enabled', 'target_users', 'rollout_percentage', 'start_date', 'end_date']
    success_url = reverse_lazy('settings_app:feature_flag_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'فیچر فلگ جدید با موفقیت ایجاد شد.')
        return super().form_valid(form)


@method_decorator(staff_member_required, name='dispatch')
class FeatureFlagUpdateView(UpdateView):
    """ویرایش فیچر فلگ (Staff)"""
    model = FeatureFlag
    template_name = 'settings_app/control_panel/feature_flag_form.html'
    fields = ['name', 'description', 'is_enabled', 'target_users', 'rollout_percentage', 'start_date', 'end_date']
    success_url = reverse_lazy('settings_app:feature_flag_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'فیچر فلگ با موفقیت به‌روزرسانی شد.')
        return super().form_valid(form)


@method_decorator(staff_member_required, name='dispatch')
class FeatureFlagDeleteView(DeleteView):
    """حذف فیچر فلگ (Staff)"""
    model = FeatureFlag
    template_name = 'settings_app/control_panel/feature_flag_confirm_delete.html'
    success_url = reverse_lazy('settings_app:feature_flag_list')
    
    def get_success_url(self):
        messages.success(self.request, 'فیچر فلگ با موفقیت حذف شد.')
        return super().get_success_url()