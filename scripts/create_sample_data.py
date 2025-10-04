#!/usr/bin/env python
"""
اسکریپت ایجاد داده‌های نمونه برای قالب‌های محاسباتی
این اسکریپت نمونه‌های کاربردی برای تست قالب‌ها ایجاد می‌کند
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
from accounts.models import CustomUser


def create_sample_budget_session():
    """ایجاد نمونه جلسه محاسبه بودجه"""
    template = ComputationTemplate.objects.get(name="محاسبه بودجه پروژه")
    
    # داده‌های ورودی نمونه
    input_data = {
        "project_name": "توسعه وب‌سایت فروشگاهی",
        "duration_months": 6,
        "team_size": 5,
        "hourly_rate": 150000,
        "materials_cost": 5000000,
        "overhead_percentage": 20,
        "profit_margin": 25,
        "tax_rate": 9
    }
    
    # نتیجه محاسبه شده
    output_data = {
        "total_labor_cost": 108000000,  # 5 نفر × 6 ماه × 30 روز × 8 ساعت × 150,000
        "total_materials_cost": 5000000,
        "overhead_cost": 22600000,  # 20% از (108,000,000 + 5,000,000)
        "subtotal": 135600000,
        "profit_amount": 33900000,  # 25% از 135,600,000
        "tax_amount": 15255000,  # 9% از (135,600,000 + 33,900,000)
        "total_budget": 184455000,
        "monthly_budget": 30742500,
        "breakdown": {
            "labor_breakdown": [
                {"role": "توسعه‌دهنده ارشد", "hours": 960, "cost": 43200000},
                {"role": "توسعه‌دهنده", "hours": 1440, "cost": 43200000},
                {"role": "طراح UI/UX", "hours": 480, "cost": 14400000},
                {"role": "تست‌کننده", "hours": 240, "cost": 3600000},
                {"role": "مدیر پروژه", "hours": 480, "cost": 3600000}
            ],
            "materials_breakdown": [
                {"item": "سرور", "cost": 2000000},
                {"item": "دامین و هاستینگ", "cost": 1000000},
                {"item": "ابزارهای توسعه", "cost": 2000000}
            ]
        }
    }
    
    session = ComputationSession.objects.create(
        session_type=template.session_type,
        product_name="محاسبه بودجه پروژه",
        input_data=input_data,
        output_data=output_data,
        status="completed",
        progress_percentage=100,
        processing_time_seconds=25.5,
        memory_usage_mb=45.2,
        cpu_usage_percent=15.8,
        configuration=template.default_config,
        priority=5
    )
    
    print(f"✅ نمونه جلسه محاسبه بودجه ایجاد شد: {session.session_id}")
    return session


def create_sample_security_session():
    """ایجاد نمونه جلسه تحلیل امنیتی"""
    template = ComputationTemplate.objects.get(name="تحلیل امنیتی سیستم")
    
    input_data = {
        "system_type": "web",
        "target_url": "https://toketech.ir",
        "scan_depth": "standard",
        "check_ssl": True,
        "check_headers": True,
        "check_ports": True,
        "custom_checks": ["sql_injection", "xss", "csrf"]
    }
    
    output_data = {
        "overall_risk_score": 75,
        "vulnerabilities": [
            {
                "name": "Missing Security Headers",
                "severity": "medium",
                "description": "هدرهای امنیتی X-Frame-Options و X-Content-Type-Options موجود نیست",
                "recommendation": "اضافه کردن هدرهای امنیتی مناسب"
            },
            {
                "name": "Weak SSL Configuration",
                "severity": "high",
                "description": "پیکربندی SSL ضعیف و استفاده از پروتکل‌های قدیمی",
                "recommendation": "به‌روزرسانی تنظیمات SSL و استفاده از TLS 1.3"
            }
        ],
        "security_headers": {
            "x_frame_options": "missing",
            "x_content_type_options": "missing",
            "strict_transport_security": "present",
            "content_security_policy": "weak"
        },
        "ssl_analysis": {
            "certificate_valid": True,
            "protocol_version": "TLS 1.2",
            "cipher_suite": "weak",
            "expiry_date": "2024-12-31"
        },
        "recommendations": [
            "اضافه کردن هدرهای امنیتی",
            "به‌روزرسانی پیکربندی SSL",
            "فعال‌سازی Content Security Policy",
            "استفاده از HTTPS اجباری"
        ],
        "report_summary": "سیستم دارای آسیب‌پذیری‌های متوسط تا بالا است که نیاز به توجه فوری دارد."
    }
    
    session = ComputationSession.objects.create(
        session_type=template.session_type,
        product_name="تحلیل امنیتی وب‌سایت",
        input_data=input_data,
        output_data=output_data,
        status="completed",
        progress_percentage=100,
        processing_time_seconds=95.3,
        memory_usage_mb=180.7,
        cpu_usage_percent=45.2,
        configuration=template.default_config,
        priority=7
    )
    
    print(f"✅ نمونه جلسه تحلیل امنیتی ایجاد شد: {session.session_id}")
    return session


def create_sample_performance_session():
    """ایجاد نمونه جلسه تست عملکرد"""
    template = ComputationTemplate.objects.get(name="تست عملکرد سرور")
    
    input_data = {
        "target_url": "https://api.example.com/v1/users",
        "test_type": "load",
        "concurrent_users": 100,
        "test_duration": 300,
        "ramp_up_time": 60,
        "request_types": ["GET", "POST", "PUT"],
        "expected_response_time": 200
    }
    
    output_data = {
        "test_summary": {
            "total_requests": 15000,
            "successful_requests": 14850,
            "failed_requests": 150,
            "average_response_time": 185.5,
            "max_response_time": 2500.0,
            "min_response_time": 45.2,
            "requests_per_second": 50.0
        },
        "performance_metrics": {
            "cpu_usage": 75.5,
            "memory_usage": 68.2,
            "network_throughput": 125.8,
            "error_rate": 1.0
        },
        "recommendations": [
            "بهینه‌سازی کوئری‌های دیتابیس",
            "اضافه کردن کش Redis",
            "استفاده از CDN",
            "بهینه‌سازی تصاویر"
        ],
        "bottlenecks": [
            "دیتابیس: کوئری‌های کند",
            "شبکه: پهنای باند محدود",
            "CPU: استفاده بالا در زمان اوج"
        ],
        "test_report": "تست عملکرد نشان می‌دهد که سیستم در شرایط عادی عملکرد مناسبی دارد اما در زمان اوج بار نیاز به بهینه‌سازی دارد."
    }
    
    session = ComputationSession.objects.create(
        session_type=template.session_type,
        product_name="تست عملکرد API",
        input_data=input_data,
        output_data=output_data,
        status="completed",
        progress_percentage=100,
        processing_time_seconds=285.7,
        memory_usage_mb=420.3,
        cpu_usage_percent=85.1,
        configuration=template.default_config,
        priority=6
    )
    
    print(f"✅ نمونه جلسه تست عملکرد ایجاد شد: {session.session_id}")
    return session


def create_sample_data_processing_session():
    """ایجاد نمونه جلسه پردازش داده"""
    template = ComputationTemplate.objects.get(name="پردازش و تحلیل داده‌ها")
    
    input_data = {
        "data_source": "sales_data_2024.csv",
        "data_format": "csv",
        "processing_type": "analyze",
        "data_size": 10000,
        "analysis_parameters": {
            "statistical_tests": ["correlation", "regression", "trend_analysis"],
            "visualization_types": ["line_chart", "bar_chart", "scatter_plot"],
            "output_format": "html"
        },
        "filters": {
            "date_range": {"start": "2024-01-01", "end": "2024-12-31"},
            "min_amount": 100000,
            "categories": ["electronics", "clothing", "books"]
        }
    }
    
    output_data = {
        "processing_summary": {
            "total_records": 10000,
            "processed_records": 9850,
            "cleaned_records": 150,
            "processing_time": 45.2
        },
        "statistical_analysis": {
            "descriptive_stats": {
                "mean_sales": 2500000,
                "median_sales": 1800000,
                "std_deviation": 1200000,
                "total_revenue": 25000000000
            },
            "correlations": {
                "price_vs_quantity": -0.65,
                "season_vs_sales": 0.78,
                "category_vs_profit": 0.45
            },
            "trends": [
                "افزایش 15% فروش در فصل تابستان",
                "کاهش 8% فروش در ماه‌های زمستان",
                "رشد 25% فروش آنلاین"
            ]
        },
        "visualizations": [
            {"type": "line_chart", "title": "روند فروش ماهانه", "url": "/charts/sales_trend.png"},
            {"type": "bar_chart", "title": "فروش بر اساس دسته‌بندی", "url": "/charts/category_sales.png"},
            {"type": "scatter_plot", "title": "رابطه قیمت و فروش", "url": "/charts/price_sales.png"}
        ],
        "insights": [
            "فروش الکترونیک 40% از کل فروش را تشکیل می‌دهد",
            "قیمت‌گذاری بالای 2 میلیون تومان باعث کاهش فروش می‌شود",
            "فروش آنلاین در حال رشد است و 60% از فروش کل را شامل می‌شود"
        ],
        "report_url": "/reports/sales_analysis_2024.html"
    }
    
    session = ComputationSession.objects.create(
        session_type=template.session_type,
        product_name="تحلیل فروش 2024",
        input_data=input_data,
        output_data=output_data,
        status="completed",
        progress_percentage=100,
        processing_time_seconds=165.8,
        memory_usage_mb=850.4,
        cpu_usage_percent=72.3,
        configuration=template.default_config,
        priority=4
    )
    
    print(f"✅ نمونه جلسه پردازش داده ایجاد شد: {session.session_id}")
    return session


def create_sample_ai_session():
    """ایجاد نمونه جلسه استنتاج هوش مصنوعی"""
    template = ComputationTemplate.objects.get(name="استنتاج هوش مصنوعی")
    
    input_data = {
        "model_type": "classification",
        "model_name": "sentiment_analysis_v2",
        "input_data": [
            {"text": "این محصول عالی است و کیفیت بالایی دارد", "id": 1},
            {"text": "خدمات ضعیف و ناراضی کننده بود", "id": 2},
            {"text": "قیمت مناسب و ارزش خرید دارد", "id": 3},
            {"text": "تحویل دیر شد و کیفیت پایین", "id": 4},
            {"text": "توصیه می‌کنم این محصول را بخرید", "id": 5}
        ],
        "model_parameters": {
            "language": "persian",
            "confidence_threshold": 0.7,
            "batch_size": 5
        },
        "confidence_threshold": 0.7,
        "batch_size": 5
    }
    
    output_data = {
        "predictions": [
            {"id": 1, "sentiment": "positive", "confidence": 0.92},
            {"id": 2, "sentiment": "negative", "confidence": 0.88},
            {"id": 3, "sentiment": "positive", "confidence": 0.85},
            {"id": 4, "sentiment": "negative", "confidence": 0.91},
            {"id": 5, "sentiment": "positive", "confidence": 0.89}
        ],
        "confidence_scores": [0.92, 0.88, 0.85, 0.91, 0.89],
        "model_metrics": {
            "accuracy": 0.94,
            "precision": 0.92,
            "recall": 0.89,
            "f1_score": 0.90
        },
        "inference_time": 2.3,
        "model_info": {
            "version": "2.1.0",
            "training_date": "2024-01-15",
            "vocabulary_size": 50000,
            "model_size": "125MB"
        }
    }
    
    session = ComputationSession.objects.create(
        session_type=template.session_type,
        product_name="تحلیل احساسات نظرات",
        input_data=input_data,
        output_data=output_data,
        status="completed",
        progress_percentage=100,
        processing_time_seconds=3.2,
        memory_usage_mb=1800.5,
        cpu_usage_percent=65.4,
        configuration=template.default_config,
        priority=8
    )
    
    print(f"✅ نمونه جلسه استنتاج هوش مصنوعی ایجاد شد: {session.session_id}")
    return session


def create_sample_custom_session():
    """ایجاد نمونه جلسه محاسبات سفارشی"""
    template = ComputationTemplate.objects.get(name="محاسبات سفارشی")
    
    input_data = {
        "computation_type": "optimization",
        "algorithm": "genetic_algorithm",
        "parameters": {
            "population_size": 100,
            "generations": 50,
            "mutation_rate": 0.1,
            "crossover_rate": 0.8
        },
        "data": [
            {"x": 1, "y": 2, "value": 10},
            {"x": 3, "y": 4, "value": 20},
            {"x": 5, "y": 6, "value": 30},
            {"x": 7, "y": 8, "value": 40},
            {"x": 9, "y": 10, "value": 50}
        ],
        "options": {
            "objective": "maximize",
            "constraints": ["x + y <= 15", "x >= 0", "y >= 0"],
            "precision": 0.001
        }
    }
    
    output_data = {
        "result": {
            "optimal_solution": {"x": 7.5, "y": 7.5, "value": 75.0},
            "fitness_score": 0.95,
            "convergence_rate": 0.88,
            "iterations_to_converge": 35
        },
        "computation_time": 45.7,
        "memory_used": 256.8,
        "status": "converged",
        "metadata": {
            "algorithm": "genetic_algorithm",
            "population_evolution": "stable",
            "best_fitness_history": [0.2, 0.4, 0.6, 0.8, 0.95],
            "convergence_point": 35
        }
    }
    
    session = ComputationSession.objects.create(
        session_type=template.session_type,
        product_name="بهینه‌سازی الگوریتم ژنتیک",
        input_data=input_data,
        output_data=output_data,
        status="completed",
        progress_percentage=100,
        processing_time_seconds=98.4,
        memory_usage_mb=380.2,
        cpu_usage_percent=78.9,
        configuration=template.default_config,
        priority=6
    )
    
    print(f"✅ نمونه جلسه محاسبات سفارشی ایجاد شد: {session.session_id}")
    return session


def main():
    """تابع اصلی برای ایجاد داده‌های نمونه"""
    print("🚀 شروع ایجاد داده‌های نمونه محاسباتی...")
    print("=" * 60)
    
    # بررسی وجود قالب‌ها
    templates_count = ComputationTemplate.objects.count()
    if templates_count == 0:
        print("❌ هیچ قالب محاسباتی موجود نیست. ابتدا قالب‌ها را ایجاد کنید.")
        return False
    
    print(f"📋 {templates_count} قالب محاسباتی موجود است.")
    
    # بررسی وجود جلسات قبلی
    existing_sessions = ComputationSession.objects.count()
    if existing_sessions > 0:
        print(f"⚠️  {existing_sessions} جلسه موجود است.")
        response = input("آیا می‌خواهید جلسات نمونه جدید اضافه کنید؟ (y/n): ")
        if response.lower() != 'y':
            print("❌ عملیات لغو شد.")
            return False
    
    sessions_created = []
    
    try:
        # ایجاد جلسات نمونه
        sessions_created.append(create_sample_budget_session())
        sessions_created.append(create_sample_security_session())
        sessions_created.append(create_sample_performance_session())
        sessions_created.append(create_sample_data_processing_session())
        sessions_created.append(create_sample_ai_session())
        sessions_created.append(create_sample_custom_session())
        
        print("=" * 60)
        print(f"✅ {len(sessions_created)} جلسه نمونه با موفقیت ایجاد شد!")
        print("\n📊 آمار جلسات ایجاد شده:")
        
        for session in sessions_created:
            print(f"  🔹 {session.product_name}")
            print(f"     - وضعیت: {session.status}")
            print(f"     - زمان پردازش: {session.processing_time_seconds} ثانیه")
            print(f"     - حافظه: {session.memory_usage_mb} MB")
            print(f"     - CPU: {session.cpu_usage_percent}%")
            print()
        
        print("🎉 تمام جلسات نمونه آماده استفاده هستند!")
        print("💡 می‌توانید از طریق پنل مدیریت به آن‌ها دسترسی داشته باشید.")
        
    except Exception as e:
        print(f"❌ خطا در ایجاد جلسات نمونه: {str(e)}")
        return False
    
    return True


if __name__ == "__main__":
    main()
