#!/usr/bin/env python
"""
اسکریپت مدیریت قالب‌های محاسباتی
این اسکریپت برای مدیریت، مشاهده و حذف قالب‌ها و جلسات محاسباتی استفاده می‌شود
"""

import os
import sys
import django
import json
from datetime import datetime, timedelta

# تنظیم Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'takotech_website.settings')
django.setup()

from computation_engine.models import ComputationTemplate, ComputationSession, ComputationResult


def list_templates():
    """نمایش فهرست قالب‌های محاسباتی"""
    print("📋 فهرست قالب‌های محاسباتی:")
    print("=" * 80)
    
    templates = ComputationTemplate.objects.all().order_by('name')
    
    if not templates:
        print("❌ هیچ قالب محاسباتی موجود نیست.")
        return
    
    for i, template in enumerate(templates, 1):
        print(f"{i:2d}. {template.name}")
        print(f"    نوع: {template.session_type}")
        print(f"    کاربر: {template.required_user_type}")
        print(f"    زمان: {template.estimated_time_seconds} ثانیه")
        print(f"    حافظه: {template.memory_requirement_mb} MB")
        print(f"    CPU-Intensive: {'بله' if template.cpu_intensive else 'خیر'}")
        print(f"    فعال: {'بله' if template.is_active else 'خیر'}")
        print(f"    استفاده: {template.usage_count} بار")
        print(f"    موفقیت: {template.success_rate}%")
        print()


def list_sessions():
    """نمایش فهرست جلسات محاسباتی"""
    print("📊 فهرست جلسات محاسباتی:")
    print("=" * 80)
    
    sessions = ComputationSession.objects.all().order_by('-created_at')[:20]  # 20 جلسه آخر
    
    if not sessions:
        print("❌ هیچ جلسه محاسباتی موجود نیست.")
        return
    
    for i, session in enumerate(sessions, 1):
        print(f"{i:2d}. {session.product_name or 'بدون نام'}")
        print(f"    ID: {session.session_id}")
        print(f"    نوع: {session.session_type}")
        print(f"    وضعیت: {session.status}")
        print(f"    پیشرفت: {session.progress_percentage}%")
        print(f"    زمان: {session.processing_time_seconds or 'نامشخص'} ثانیه")
        print(f"    حافظه: {session.memory_usage_mb or 'نامشخص'} MB")
        print(f"    CPU: {session.cpu_usage_percent or 'نامشخص'}%")
        print(f"    تاریخ: {session.created_at.strftime('%Y-%m-%d %H:%M')}")
        print()


def show_template_details(template_id):
    """نمایش جزئیات قالب"""
    try:
        template = ComputationTemplate.objects.get(id=template_id)
        
        print(f"🔍 جزئیات قالب: {template.name}")
        print("=" * 80)
        print(f"نام: {template.name}")
        print(f"توضیحات: {template.description}")
        print(f"نوع جلسه: {template.session_type}")
        print(f"نوع کاربر: {template.required_user_type}")
        print(f"زمان تخمینی: {template.estimated_time_seconds} ثانیه")
        print(f"نیاز حافظه: {template.memory_requirement_mb} MB")
        print(f"CPU-Intensive: {'بله' if template.cpu_intensive else 'خیر'}")
        print(f"فعال: {'بله' if template.is_active else 'خیر'}")
        print(f"تعداد استفاده: {template.usage_count}")
        print(f"نرخ موفقیت: {template.success_rate}%")
        print(f"تاریخ ایجاد: {template.created_at}")
        print(f"آخرین به‌روزرسانی: {template.updated_at}")
        
        print("\n📄 اسکیمای ورودی:")
        print(json.dumps(template.input_schema, indent=2, ensure_ascii=False))
        
        print("\n📄 اسکیمای خروجی:")
        print(json.dumps(template.output_schema, indent=2, ensure_ascii=False))
        
        print("\n⚙️ پیکربندی پیش‌فرض:")
        print(json.dumps(template.default_config, indent=2, ensure_ascii=False))
        
    except ComputationTemplate.DoesNotExist:
        print(f"❌ قالب با ID {template_id} یافت نشد.")


def show_session_details(session_id):
    """نمایش جزئیات جلسه"""
    try:
        session = ComputationSession.objects.get(session_id=session_id)
        
        print(f"🔍 جزئیات جلسه: {session.session_id}")
        print("=" * 80)
        print(f"نام محصول: {session.product_name or 'بدون نام'}")
        print(f"نوع جلسه: {session.session_type}")
        print(f"وضعیت: {session.status}")
        print(f"پیشرفت: {session.progress_percentage}%")
        print(f"زمان پردازش: {session.processing_time_seconds or 'نامشخص'} ثانیه")
        print(f"استفاده حافظه: {session.memory_usage_mb or 'نامشخص'} MB")
        print(f"استفاده CPU: {session.cpu_usage_percent or 'نامشخص'}%")
        print(f"اولویت: {session.priority}")
        print(f"تاریخ ایجاد: {session.created_at}")
        print(f"تاریخ شروع: {session.started_at or 'شروع نشده'}")
        print(f"تاریخ تکمیل: {session.completed_at or 'تکمیل نشده'}")
        
        if session.error_message:
            print(f"پیام خطا: {session.error_message}")
        if session.error_code:
            print(f"کد خطا: {session.error_code}")
        
        print("\n📥 داده‌های ورودی:")
        print(json.dumps(session.input_data, indent=2, ensure_ascii=False))
        
        print("\n📤 داده‌های خروجی:")
        print(json.dumps(session.output_data, indent=2, ensure_ascii=False))
        
        print("\n⚙️ پیکربندی:")
        print(json.dumps(session.configuration, indent=2, ensure_ascii=False))
        
    except ComputationSession.DoesNotExist:
        print(f"❌ جلسه با ID {session_id} یافت نشد.")


def delete_old_sessions(days=30):
    """حذف جلسات قدیمی"""
    cutoff_date = datetime.now() - timedelta(days=days)
    old_sessions = ComputationSession.objects.filter(created_at__lt=cutoff_date)
    count = old_sessions.count()
    
    if count == 0:
        print(f"✅ هیچ جلسه قدیمی‌تر از {days} روز یافت نشد.")
        return
    
    print(f"🗑️  {count} جلسه قدیمی‌تر از {days} روز یافت شد.")
    response = input("آیا می‌خواهید آن‌ها را حذف کنید؟ (y/n): ")
    
    if response.lower() == 'y':
        old_sessions.delete()
        print(f"✅ {count} جلسه قدیمی حذف شد.")
    else:
        print("❌ عملیات لغو شد.")


def reset_template_usage():
    """بازنشانی آمار استفاده قالب‌ها"""
    templates = ComputationTemplate.objects.all()
    count = templates.count()
    
    if count == 0:
        print("❌ هیچ قالب محاسباتی موجود نیست.")
        return
    
    print(f"🔄 {count} قالب محاسباتی یافت شد.")
    response = input("آیا می‌خواهید آمار استفاده را بازنشانی کنید؟ (y/n): ")
    
    if response.lower() == 'y':
        for template in templates:
            template.usage_count = 0
            template.success_rate = 100.0
            template.save()
        print(f"✅ آمار {count} قالب بازنشانی شد.")
    else:
        print("❌ عملیات لغو شد.")


def show_statistics():
    """نمایش آمار کلی"""
    print("📈 آمار کلی سیستم محاسباتی:")
    print("=" * 80)
    
    # آمار قالب‌ها
    templates_count = ComputationTemplate.objects.count()
    active_templates = ComputationTemplate.objects.filter(is_active=True).count()
    inactive_templates = templates_count - active_templates
    
    print(f"📋 قالب‌های محاسباتی:")
    print(f"  کل: {templates_count}")
    print(f"  فعال: {active_templates}")
    print(f"  غیرفعال: {inactive_templates}")
    
    # آمار جلسات
    sessions_count = ComputationSession.objects.count()
    completed_sessions = ComputationSession.objects.filter(status='completed').count()
    failed_sessions = ComputationSession.objects.filter(status='failed').count()
    pending_sessions = ComputationSession.objects.filter(status='pending').count()
    processing_sessions = ComputationSession.objects.filter(status='processing').count()
    
    print(f"\n📊 جلسات محاسباتی:")
    print(f"  کل: {sessions_count}")
    print(f"  تکمیل شده: {completed_sessions}")
    print(f"  ناموفق: {failed_sessions}")
    print(f"  در انتظار: {pending_sessions}")
    print(f"  در حال پردازش: {processing_sessions}")
    
    # آمار عملکرد
    if completed_sessions > 0:
        avg_processing_time = ComputationSession.objects.filter(
            status='completed', 
            processing_time_seconds__isnull=False
        ).aggregate(avg_time=models.Avg('processing_time_seconds'))['avg_time'] or 0
        
        avg_memory_usage = ComputationSession.objects.filter(
            status='completed',
            memory_usage_mb__isnull=False
        ).aggregate(avg_memory=models.Avg('memory_usage_mb'))['avg_memory'] or 0
        
        print(f"\n⚡ عملکرد:")
        print(f"  میانگین زمان پردازش: {avg_processing_time:.2f} ثانیه")
        print(f"  میانگین استفاده حافظه: {avg_memory_usage:.2f} MB")
    
    # آمار نوع کاربر
    free_sessions = ComputationSession.objects.filter(
        session__template__required_user_type='free'
    ).count()
    premium_sessions = ComputationSession.objects.filter(
        session__template__required_user_type='premium'
    ).count()
    enterprise_sessions = ComputationSession.objects.filter(
        session__template__required_user_type='enterprise'
    ).count()
    
    print(f"\n👥 استفاده بر اساس نوع کاربر:")
    print(f"  رایگان: {free_sessions}")
    print(f"  پریمیوم: {premium_sessions}")
    print(f"  سازمانی: {enterprise_sessions}")


def main():
    """منوی اصلی"""
    while True:
        print("\n" + "=" * 60)
        print("🔧 مدیریت قالب‌های محاسباتی")
        print("=" * 60)
        print("1. نمایش قالب‌ها")
        print("2. نمایش جلسات")
        print("3. جزئیات قالب")
        print("4. جزئیات جلسه")
        print("5. حذف جلسات قدیمی")
        print("6. بازنشانی آمار قالب‌ها")
        print("7. نمایش آمار کلی")
        print("8. خروج")
        print("=" * 60)
        
        choice = input("انتخاب کنید (1-8): ").strip()
        
        if choice == '1':
            list_templates()
        elif choice == '2':
            list_sessions()
        elif choice == '3':
            template_id = input("ID قالب را وارد کنید: ").strip()
            if template_id.isdigit():
                show_template_details(int(template_id))
            else:
                print("❌ ID نامعتبر است.")
        elif choice == '4':
            session_id = input("ID جلسه را وارد کنید: ").strip()
            if session_id:
                show_session_details(session_id)
            else:
                print("❌ ID نامعتبر است.")
        elif choice == '5':
            days = input("جلسات قدیمی‌تر از چند روز حذف شوند؟ (پیش‌فرض: 30): ").strip()
            days = int(days) if days.isdigit() else 30
            delete_old_sessions(days)
        elif choice == '6':
            reset_template_usage()
        elif choice == '7':
            show_statistics()
        elif choice == '8':
            print("👋 خداحافظ!")
            break
        else:
            print("❌ انتخاب نامعتبر است.")
        
        input("\nبرای ادامه Enter را فشار دهید...")


if __name__ == "__main__":
    main()
