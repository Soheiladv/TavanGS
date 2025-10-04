"""
Products App Views - Product Catalog and Showcase
"""

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Product, ProductCategory
from .forms import ProductForm, ProductCategoryForm
from django.urls import reverse_lazy
from .serializers import ProductSerializer, ProductCategorySerializer


class StaffRequiredMixin(UserPassesTestMixin):
    """میکسین برای دسترسی محدود به staff"""
    def test_func(self):
        return self.request.user.is_staff


class HomeView(TemplateView):
    """Homepage with hero section and featured products"""
    template_name = 'products/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_products'] = Product.objects.filter(is_featured=True, is_active=True)[:6]
        context['categories'] = ProductCategory.objects.filter(is_active=True)[:8]
        return context


class ProductListView(ListView):
    """Product catalog with filtering and search"""
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)
        
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        return queryset.order_by('-is_featured', '-created_at')


class ProductDetailView(DetailView):
    """Detailed product page"""
    model = Product
    template_name = 'products/detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.increment_view_count()
        return obj


class ProductCreateView(StaffRequiredMixin, CreateView):
    """ایجاد محصول جدید"""
    model = Product
    form_class = ProductForm
    template_name = 'products/form.html'
    success_url = reverse_lazy('products:list')
    
    def form_valid(self, form):
        messages.success(self.request, 'محصول جدید با موفقیت ایجاد شد.')
        return super().form_valid(form)


class ProductUpdateView(StaffRequiredMixin, UpdateView):
    """ویرایش محصول"""
    model = Product
    form_class = ProductForm
    template_name = 'products/form.html'
    slug_field = 'slug'
    success_url = reverse_lazy('products:list')
    
    def form_valid(self, form):
        messages.success(self.request, 'محصول با موفقیت به‌روزرسانی شد.')
        return super().form_valid(form)


class ProductDeleteView(StaffRequiredMixin, DeleteView):
    """حذف محصول"""
    model = Product
    template_name = 'products/confirm_delete.html'
    slug_field = 'slug'
    success_url = reverse_lazy('products:list')
    
    def get_success_url(self):
        messages.success(self.request, 'محصول با موفقیت حذف شد.')
        return super().get_success_url()


class ProductDemoView(DetailView):
    model = Product
    template_name = 'products/demo.html'
    context_object_name = 'product'
    slug_field = 'slug'


class ProductTrialView(DetailView):
    model = Product
    template_name = 'products/trial.html'
    context_object_name = 'product'
    slug_field = 'slug'


class ProductCompareView(ListView):
    model = Product
    template_name = 'products/compare.html'
    context_object_name = 'products'


class SandboxView(TemplateView):
    template_name = 'products/sandbox.html'


class ProductSandboxView(DetailView):
    model = Product
    template_name = 'products/product_sandbox.html'
    context_object_name = 'product'
    slug_field = 'slug'


class ProductShowcaseView(TemplateView):
    template_name = 'products/showcase.html'


class FeaturedProductsView(ListView):
    model = Product
    template_name = 'products/featured.html'
    context_object_name = 'products'


class HeroQuizView(TemplateView):
    template_name = 'products/hero_quiz.html'

    def post(self, request, *args, **kwargs):
        answers = {
            'industry': request.POST.get('industry'),
            'priority': request.POST.get('priority'),
            'team_size': request.POST.get('team_size'),
        }
        qs = Product.objects.filter(is_active=True)
        if answers['priority'] == 'security':
            qs = qs.filter(Q(name__icontains='Secure') | Q(description__icontains='امنیت'))
        elif answers['priority'] == 'budgeting':
            qs = qs.filter(Q(name__icontains='Budget') | Q(description__icontains='بودجه'))
        recommended = list(qs[:3])
        return render(request, 'products/hero_quiz_result.html', {
            'answers': answers,
            'recommended': recommended,
        })


def product_search_ajax(request):
    """AJAX endpoint for product search"""
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse({'results': []})
    
    products = Product.objects.filter(
        Q(name__icontains=query) | Q(short_description__icontains=query),
        is_active=True
    )[:10]
    
    results = [
        {
            'name': product.full_name,
            'slug': product.slug,
            'category': product.category.name,
        }
        for product in products
    ]
    
    return JsonResponse({'results': results})


# AJAX endpoints to update counters
def increment_product_view(request, slug):
    if request.method == 'POST':
        try:
            product = get_object_or_404(Product, slug=slug)
            product.increment_view_count()
            return JsonResponse({'success': True, 'view_count': product.view_count})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Method not allowed'})


def increment_product_download(request, slug):
    if request.method == 'POST':
        try:
            product = get_object_or_404(Product, slug=slug)
            product.increment_download_count()
            return JsonResponse({'success': True, 'download_count': product.download_count})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Method not allowed'})

# Category page
class ProductCategoryView(ListView):
    model = Product
    template_name = 'products/category.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        self.category = get_object_or_404(ProductCategory, slug=self.kwargs['slug'])
        return Product.objects.filter(category=self.category, is_active=True).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class CategoryListView(StaffRequiredMixin, ListView):
    """فهرست دسته‌بندی‌های محصول"""
    model = ProductCategory
    template_name = 'products/category_list.html'
    context_object_name = 'categories'
    paginate_by = 20
    
    def get_queryset(self):
        return ProductCategory.objects.all().order_by('name')


class CategoryCreateView(StaffRequiredMixin, CreateView):
    """ایجاد دسته‌بندی محصول جدید"""
    model = ProductCategory
    form_class = ProductCategoryForm
    template_name = 'products/category_form.html'
    success_url = reverse_lazy('products:category_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'دسته‌بندی محصول جدید با موفقیت ایجاد شد.')
        return super().form_valid(form)


class CategoryUpdateView(StaffRequiredMixin, UpdateView):
    """ویرایش دسته‌بندی محصول"""
    model = ProductCategory
    form_class = ProductCategoryForm
    template_name = 'products/category_form.html'
    slug_field = 'slug'
    success_url = reverse_lazy('products:category_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'دسته‌بندی محصول با موفقیت به‌روزرسانی شد.')
        return super().form_valid(form)


class CategoryDeleteView(StaffRequiredMixin, DeleteView):
    """حذف دسته‌بندی محصول"""
    model = ProductCategory
    template_name = 'products/category_confirm_delete.html'
    slug_field = 'slug'
    success_url = reverse_lazy('products:category_list')
    
    def get_success_url(self):
        messages.success(self.request, 'دسته‌بندی محصول با موفقیت حذف شد.')
        return super().get_success_url()


# API ViewSets (for router in products/urls.py)
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'short_description']
    ordering_fields = ['name', 'created_at', 'view_count']
    ordering = ['-created_at']


class ProductCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductCategory.objects.filter(is_active=True)
    serializer_class = ProductCategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
