"""
Tickets App Views - Advanced Support System
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.db.models import Q, Count
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import logging

from .models import Ticket, TicketCategory, TicketReply, TicketAttachment
from .forms import TicketCreateForm, TicketReplyForm

logger = logging.getLogger(__name__)


class StaffRequiredMixin(UserPassesTestMixin):
    """میکسین برای دسترسی محدود به staff"""
    def test_func(self):
        return self.request.user.is_staff


class TicketListView(LoginRequiredMixin, ListView):
    """فهرست تیکت‌های کاربر"""
    model = Ticket
    template_name = 'tickets/list.html'
    context_object_name = 'tickets'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Ticket.objects.filter(user=self.request.user)
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Filter by category
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        
        # Filter by priority
        priority = self.request.GET.get('priority')
        if priority:
            queryset = queryset.filter(priority=priority)
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = TicketCategory.objects.filter(is_active=True)
        context['status_choices'] = Ticket.STATUS_CHOICES
        context['priority_choices'] = Ticket.PRIORITY_CHOICES
        
        # Statistics
        context['total_tickets'] = Ticket.objects.filter(user=self.request.user).count()
        context['open_tickets'] = Ticket.objects.filter(user=self.request.user, status='open').count()
        context['in_progress_tickets'] = Ticket.objects.filter(user=self.request.user, status='in_progress').count()
        context['resolved_tickets'] = Ticket.objects.filter(user=self.request.user, status='resolved').count()
        
        return context


class TicketDetailView(LoginRequiredMixin, DetailView):
    """جزئیات تیکت"""
    model = Ticket
    template_name = 'tickets/detail.html'
    context_object_name = 'ticket'
    slug_field = 'ticket_id'
    slug_url_kwarg = 'ticket_id'
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Ticket.objects.all()
        return Ticket.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['replies'] = self.object.replies.filter(is_private=False).order_by('created_at')
        context['reply_form'] = TicketReplyForm()
        context['can_reply'] = self.object.status not in ['closed', 'cancelled']
        return context


class TicketCreateView(LoginRequiredMixin, CreateView):
    """ایجاد تیکت جدید"""
    model = Ticket
    form_class = TicketCreateForm
    template_name = 'tickets/create.html'
    success_url = reverse_lazy('tickets:list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = TicketCategory.objects.filter(is_active=True)
        return context
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.ip_address = self.get_client_ip()
        form.instance.user_agent = self.request.META.get('HTTP_USER_AGENT', '')
        
        # Auto-assign if category has auto-assignment
        if form.instance.category.auto_assign_to:
            form.instance.assigned_to = form.instance.category.auto_assign_to
        
        response = super().form_valid(form)
        
        # Send notification email
        try:
            send_micket_notification(self.object)
        except Exception as e:
            logger.error(f"Failed to send ticket notification: {e}")
        
        messages.success(self.request, 'تیکت شما با موفقیت ایجاد شد. تیم پشتیبانی به زودی با شما تماس خواهد گرفت.')
        return response
    
    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip


class TicketUpdateView(LoginRequiredMixin, UpdateView):
    """ویرایش تیکت (فقط برای کارکنان)"""
    model = Ticket
    template_name = 'tickets/update.html'
    fields = ['status', 'priority', 'assigned_to']
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Ticket.objects.all()
        return Ticket.objects.none()
    
    def get_success_url(self):
        return reverse('tickets:detail', kwargs={'ticket_id': self.object.ticket_id})


class TicketReplyView(LoginRequiredMixin, CreateView):
    """پاسخ به تیکت"""
    model = TicketReply
    form_class = TicketReplyForm
    template_name = 'tickets/reply.html'
    
    def dispatch(self, request, *args, **kwargs):
        self.ticket = get_object_or_404(Ticket, ticket_id=kwargs['ticket_id'])
        
        # Check permissions
        if not request.user.is_staff and self.ticket.user != request.user:
            messages.error(request, 'شما مجاز به مشاهده این تیکت نیستید.')
            return redirect('tickets:list')
        
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.ticket = self.ticket
        form.instance.user = self.request.user
        
        # Determine reply type
        if self.request.user.is_staff:
            form.instance.reply_type = 'staff'
        else:
            form.instance.reply_type = 'customer'
        
        response = super().form_valid(form)
        
        # Update ticket status and timestamps
        if self.request.user.is_staff and self.ticket.status == 'open':
            self.ticket.status = 'in_progress'
            self.ticket.first_response_at = timezone.now()
            self.ticket.save()
        
        # Send notification email
        try:
            send_reply_notification(self.object)
        except Exception as e:
            logger.error(f"Failed to send reply notification: {e}")
        
        messages.success(self.request, 'پاسخ شما با موفقیت ارسال شد.')
        return HttpResponseRedirect(reverse('tickets:detail', kwargs={'ticket_id': self.ticket.ticket_id}))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ticket'] = self.ticket
        return context


class SupportDashboardView(LoginRequiredMixin, TemplateView):
    """داشبورد پشتیبانی برای کارکنان"""
    template_name = 'tickets/dashboard.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, 'شما مجاز به دسترسی به این صفحه نیستید.')
            return redirect('tickets:list')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Statistics
        context['total_tickets'] = Ticket.objects.count()
        context['open_tickets'] = Ticket.objects.filter(status='open').count()
        context['in_progress_tickets'] = Ticket.objects.filter(status='in_progress').count()
        context['pending_tickets'] = Ticket.objects.filter(status='pending').count()
        context['resolved_tickets'] = Ticket.objects.filter(status='resolved').count()
        context['overdue_tickets'] = Ticket.objects.filter(sla_breached=True).count()
        
        # Recent tickets
        context['recent_tickets'] = Ticket.objects.order_by('-created_at')[:10]
        context['overdue_tickets_list'] = Ticket.objects.filter(sla_breached=True).order_by('-created_at')[:5]
        
        # Category statistics
        context['category_stats'] = TicketCategory.objects.annotate(
            ticket_count=Count('tickets')
        ).order_by('-ticket_count')
        
        # Priority statistics
        context['priority_stats'] = Ticket.objects.values('priority').annotate(
            count=Count('priority')
        ).order_by('priority')
        
        return context


class TicketCategoryListView(StaffRequiredMixin, ListView):
    """فهرست دسته‌بندی‌های تیکت (Staff)"""
    model = TicketCategory
    template_name = 'tickets/category_list.html'
    context_object_name = 'categories'
    paginate_by = 20
    
    def get_queryset(self):
        return TicketCategory.objects.all().order_by('name')


class TicketCategoryCreateView(StaffRequiredMixin, CreateView):
    """ایجاد دسته‌بندی تیکت جدید (Staff)"""
    model = TicketCategory
    template_name = 'tickets/category_form.html'
    fields = ['name', 'slug', 'description', 'icon', 'color', 'response_time_hours', 'resolution_time_hours', 'is_active']
    success_url = reverse_lazy('tickets:category_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'دسته‌بندی تیکت جدید با موفقیت ایجاد شد.')
        return super().form_valid(form)


class TicketCategoryUpdateView(StaffRequiredMixin, UpdateView):
    """ویرایش دسته‌بندی تیکت (Staff)"""
    model = TicketCategory
    template_name = 'tickets/category_form.html'
    fields = ['name', 'slug', 'description', 'icon', 'color', 'response_time_hours', 'resolution_time_hours', 'is_active']
    success_url = reverse_lazy('tickets:category_list')
    slug_field = 'slug'
    
    def form_valid(self, form):
        messages.success(self.request, 'دسته‌بندی تیکت با موفقیت به‌روزرسانی شد.')
        return super().form_valid(form)


class TicketCategoryDeleteView(StaffRequiredMixin, DeleteView):
    """حذف دسته‌بندی تیکت (Staff)"""
    model = TicketCategory
    template_name = 'tickets/category_confirm_delete.html'
    success_url = reverse_lazy('tickets:category_list')
    slug_field = 'slug'
    
    def get_success_url(self):
        messages.success(self.request, 'دسته‌بندی تیکت با موفقیت حذف شد.')
        return super().get_success_url()


# AJAX Views
@login_required
def ticket_create_ajax(request):
    """ایجاد تیکت از طریق AJAX"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Create ticket
            ticket = Ticket.objects.create(
                title=data.get('title'),
                description=data.get('description'),
                category_id=data.get('category'),
                priority=data.get('priority', 2),
                user=request.user,
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            
            return JsonResponse({
                'success': True, 
                'message': 'تیکت با موفقیت ایجاد شد',
                'ticket_id': str(ticket.ticket_id),
                'redirect_url': reverse('tickets:detail', kwargs={'ticket_id': ticket.ticket_id})
            })
        except Exception as e:
            logger.error(f"AJAX ticket creation error: {e}")
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid method'})


@login_required
def ticket_reply_ajax(request, ticket_id):
    """پاسخ به تیکت از طریق AJAX"""
    if request.method == 'POST':
        try:
            ticket = get_object_or_404(Ticket, ticket_id=ticket_id)
            
            # Check permissions
            if not request.user.is_staff and ticket.user != request.user:
                return JsonResponse({'success': False, 'error': 'Permission denied'})
            
            data = json.loads(request.body)
            
            # Create reply
            reply = TicketReply.objects.create(
                ticket=ticket,
                user=request.user,
                content=data.get('content'),
                reply_type='staff' if request.user.is_staff else 'customer'
            )
            
            # Update ticket status
            if request.user.is_staff and ticket.status == 'open':
                ticket.status = 'in_progress'
                ticket.first_response_at = timezone.now()
                ticket.save()
            
            return JsonResponse({
                'success': True, 
                'message': 'پاسخ با موفقیت ارسال شد',
                'reply_id': reply.id
            })
        except Exception as e:
            logger.error(f"AJAX reply error: {e}")
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid method'})


@login_required
def ticket_status_update_ajax(request, ticket_id):
    """بروزرسانی وضعیت تیکت از طریق AJAX"""
    if request.method == 'POST':
        try:
            ticket = get_object_or_404(Ticket, ticket_id=ticket_id)
            
            # Check permissions (only staff can update status)
            if not request.user.is_staff:
                return JsonResponse({'success': False, 'error': 'Permission denied'})
            
            data = json.loads(request.body)
            new_status = data.get('status')
            
            if new_status in [choice[0] for choice in Ticket.STATUS_CHOICES]:
                ticket.status = new_status
                
                # Update timestamps
                if new_status == 'resolved' and not ticket.resolved_at:
                    ticket.resolved_at = timezone.now()
                elif new_status == 'closed' and not ticket.closed_at:
                    ticket.closed_at = timezone.now()
                
                ticket.save()
                
                return JsonResponse({
                    'success': True, 
                    'message': 'وضعیت تیکت بروزرسانی شد'
                })
            else:
                return JsonResponse({'success': False, 'error': 'Invalid status'})
                
        except Exception as e:
            logger.error(f"AJAX status update error: {e}")
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid method'})


# Helper functions
def get_client_ip(request):
    """Get client IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def send_ticket_notification(ticket):
    """Send email notification for new ticket"""
    if not settings.EMAIL_HOST:
        return
    
    subject = f'تیکت جدید: {ticket.title}'
    message = f"""
تیکت جدیدی با شناسه {ticket.ticket_id} ایجاد شده است.

عنوان: {ticket.title}
دسته‌بندی: {ticket.category.name}
اولویت: {ticket.get_priority_display()}
کاربر: {ticket.user.get_full_name()}

شرح مسئله:
{ticket.description}

برای مشاهده تیکت، به پنل مدیریت مراجعه کنید.
"""
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [settings.DEFAULT_FROM_EMAIL],
        fail_silently=True,
    )


def send_reply_notification(reply):
    """Send email notification for new reply"""
    if not settings.EMAIL_HOST:
        return
    
    ticket = reply.ticket
    
    if reply.reply_type == 'staff':
        # Notify customer
        recipient_email = ticket.user.email
        subject = f'پاسخ جدید برای تیکت: {ticket.title}'
    else:
        # Notify staff
        recipient_email = settings.DEFAULT_FROM_EMAIL
        subject = f'پاسخ مشتری برای تیکت: {ticket.title}'
    
    message = f"""
پاسخ جدیدی برای تیکت {ticket.ticket_id} ارسال شده است.

تیکت: {ticket.title}
پاسخ‌دهنده: {reply.user.get_full_name()}

متن پاسخ:
{reply.content}

برای مشاهده کامل تیکت، به پنل پشتیبانی مراجعه کنید.
"""
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [recipient_email],
        fail_silently=True,
    )
