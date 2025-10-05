"""
News App Views - News Management System
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.db.models import Q, Count, F
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import logging

from .models import News, NewsCategory, NewsComment, NewsTag, NewsTagRelation
from .forms import NewsForm, NewsCategoryForm, NewsCommentForm

logger = logging.getLogger(__name__)


class StaffRequiredMixin(UserPassesTestMixin):
    """میکسین برای دسترسی محدود به staff"""
    def test_func(self):
        return self.request.user.is_staff


class NewsListView(ListView):
    """فهرست اخبار"""
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = News.objects.filter(status='published').order_by('-is_pinned', '-published_at')
        
        # فیلتر بر اساس دسته‌بندی
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # فیلتر بر اساس تگ
        tag_slug = self.request.GET.get('tag')
        if tag_slug:
            queryset = queryset.filter(newstagrelation__tag__slug=tag_slug)
        
        # جستجو
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(summary__icontains=search) |
                Q(content__icontains=search)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = NewsCategory.objects.filter(is_active=True)
        context['featured_news'] = News.objects.filter(
            status='published', 
            is_featured=True
        ).order_by('-published_at')[:3]
        context['recent_news'] = News.objects.filter(
            status='published'
        ).order_by('-published_at')[:5]
        return context


class NewsDetailView(DetailView):
    """جزئیات خبر"""
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return News.objects.filter(status='published')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # افزایش تعداد بازدید
        self.object.increment_view_count()
        
        # اخبار مرتبط
        context['related_news'] = News.objects.filter(
            status='published',
            category=self.object.category
        ).exclude(pk=self.object.pk).order_by('-published_at')[:4]
        
        # نظرات
        context['comments'] = NewsComment.objects.filter(
            news=self.object,
            is_approved=True,
            parent__isnull=True
        ).order_by('-created_at')
        
        # فرم نظر
        context['comment_form'] = NewsCommentForm()
        
        return context


class NewsCreateView(StaffRequiredMixin, CreateView):
    """ایجاد خبر جدید"""
    model = News
    form_class = NewsForm
    template_name = 'news/news_form.html'
    success_url = reverse_lazy('news:news_list')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        if form.instance.status == 'published':
            form.instance.published_at = timezone.now()
        messages.success(self.request, 'خبر با موفقیت ایجاد شد.')
        return super().form_valid(form)


class NewsUpdateView(StaffRequiredMixin, UpdateView):
    """ویرایش خبر"""
    model = News
    form_class = NewsForm
    template_name = 'news/news_form.html'
    success_url = reverse_lazy('news:news_list')
    
    def form_valid(self, form):
        if form.instance.status == 'published' and not form.instance.published_at:
            form.instance.published_at = timezone.now()
        messages.success(self.request, 'خبر با موفقیت به‌روزرسانی شد.')
        return super().form_valid(form)


class NewsDeleteView(StaffRequiredMixin, DeleteView):
    """حذف خبر"""
    model = News
    template_name = 'news/news_confirm_delete.html'
    success_url = reverse_lazy('news:news_list')
    
    def get_success_url(self):
        messages.success(self.request, 'خبر با موفقیت حذف شد.')
        return super().get_success_url()


class NewsCategoryListView(StaffRequiredMixin, ListView):
    """فهرست دسته‌بندی‌های اخبار"""
    model = NewsCategory
    template_name = 'news/category_list.html'
    context_object_name = 'categories'
    paginate_by = 20
    
    def get_queryset(self):
        return NewsCategory.objects.annotate(
            news_count=Count('news')
        ).order_by('-created_at')


class NewsCategoryCreateView(StaffRequiredMixin, CreateView):
    """ایجاد دسته‌بندی جدید"""
    model = NewsCategory
    form_class = NewsCategoryForm
    template_name = 'news/category_form.html'
    success_url = reverse_lazy('news:category_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'دسته‌بندی با موفقیت ایجاد شد.')
        return super().form_valid(form)


class NewsCategoryUpdateView(StaffRequiredMixin, UpdateView):
    """ویرایش دسته‌بندی"""
    model = NewsCategory
    form_class = NewsCategoryForm
    template_name = 'news/category_form.html'
    success_url = reverse_lazy('news:category_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'دسته‌بندی با موفقیت به‌روزرسانی شد.')
        return super().form_valid(form)


class NewsCategoryDeleteView(StaffRequiredMixin, DeleteView):
    """حذف دسته‌بندی"""
    model = NewsCategory
    template_name = 'news/category_confirm_delete.html'
    success_url = reverse_lazy('news:category_list')
    
    def get_success_url(self):
        messages.success(self.request, 'دسته‌بندی با موفقیت حذف شد.')
        return super().get_success_url()


@login_required
def add_comment(request, news_slug):
    """افزودن نظر"""
    news = get_object_or_404(News, slug=news_slug, status='published')
    
    if request.method == 'POST':
        form = NewsCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.news = news
            comment.user = request.user
            comment.save()
            messages.success(request, 'نظر شما با موفقیت ثبت شد.')
        else:
            messages.error(request, 'خطا در ثبت نظر.')
    
    return redirect('news:news_detail', slug=news_slug)


@method_decorator(csrf_exempt, name='dispatch')
class NewsLikeView(LoginRequiredMixin, TemplateView):
    """لایک کردن خبر"""
    
    def post(self, request, news_slug):
        news = get_object_or_404(News, slug=news_slug, status='published')
        
        # اینجا می‌توانید منطق لایک را پیاده‌سازی کنید
        # برای مثال، استفاده از مدل Like یا session
        
        return JsonResponse({
            'success': True,
            'like_count': news.like_count + 1
        })


class NewsDashboardView(StaffRequiredMixin, TemplateView):
    """داشبورد مدیریت اخبار"""
    template_name = 'news/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # آمار کلی
        context['total_news'] = News.objects.count()
        context['published_news'] = News.objects.filter(status='published').count()
        context['draft_news'] = News.objects.filter(status='draft').count()
        context['total_views'] = News.objects.aggregate(
            total_views=models.Sum('view_count')
        )['total_views'] or 0
        
        # اخبار اخیر
        context['recent_news'] = News.objects.order_by('-created_at')[:10]
        
        # دسته‌بندی‌های محبوب
        context['popular_categories'] = NewsCategory.objects.annotate(
            news_count=Count('news')
        ).order_by('-news_count')[:5]
        
        return context


def news_rss_feed(request):
    """فید RSS اخبار"""
    from django.http import HttpResponse
    from django.template.loader import render_to_string
    
    news = News.objects.filter(status='published').order_by('-published_at')[:20]
    
    rss_content = render_to_string('news/rss_feed.xml', {
        'news': news,
        'site_url': request.build_absolute_uri('/')
    })
    
    return HttpResponse(rss_content, content_type='application/rss+xml')


# =========================
# Tag Management Views
# =========================

class NewsTagListView(StaffRequiredMixin, ListView):
    """فهرست تگ‌های اخبار"""
    model = NewsTag
    template_name = 'news/tag_list.html'
    context_object_name = 'tags'
    paginate_by = 20
    
    def get_queryset(self):
        return NewsTag.objects.annotate(
            news_count=Count('newstagrelation')
        ).order_by('-created_at')


class NewsTagCreateView(StaffRequiredMixin, CreateView):
    """ایجاد تگ جدید"""
    model = NewsTag
    template_name = 'news/tag_form.html'
    fields = ['name', 'description', 'color']
    success_url = reverse_lazy('news:tag_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'تگ جدید با موفقیت ایجاد شد.')
        return super().form_valid(form)


class NewsTagUpdateView(StaffRequiredMixin, UpdateView):
    """ویرایش تگ"""
    model = NewsTag
    template_name = 'news/tag_form.html'
    fields = ['name', 'description', 'color']
    success_url = reverse_lazy('news:tag_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'تگ با موفقیت بروزرسانی شد.')
        return super().form_valid(form)


class NewsTagDeleteView(StaffRequiredMixin, DeleteView):
    """حذف تگ"""
    model = NewsTag
    template_name = 'news/tag_confirm_delete.html'
    success_url = reverse_lazy('news:tag_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'تگ با موفقیت حذف شد.')
        return super().delete(request, *args, **kwargs)
