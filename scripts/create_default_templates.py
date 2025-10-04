#!/usr/bin/env python
"""
اسکریپت ایجاد قالب‌های پیش‌فرض محاسباتی
این اسکریپت قالب‌های نمونه برای انواع مختلف محاسبات ایجاد می‌کند
"""

import os
import sys
import django
import json

# تنظیم Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'takotech_website.settings')
django.setup()

from computation_engine.models import ComputationTemplate


def create_budget_calculation_template():
    """ایجاد قالب محاسبه بودجه"""
    template = ComputationTemplate.objects.create(
        name="محاسبه بودجه پروژه",
        description="""
        قالب محاسبه بودجه برای پروژه‌های مختلف.
        این قالب شامل محاسبه هزینه‌های مستقیم، غیرمستقیم، مالیات و سود می‌باشد.
        
        ویژگی‌ها:
        - محاسبه هزینه‌های مواد اولیه
        - محاسبه دستمزد نیروی کار
        - محاسبه سربار و سود
        - محاسبه مالیات
        """,
        session_type="budget_calculation",
        input_schema={
            "type": "object",
            "properties": {
                "project_name": {"type": "string", "description": "نام پروژه"},
                "duration_months": {"type": "integer", "minimum": 1, "description": "مدت پروژه (ماه)"},
                "team_size": {"type": "integer", "minimum": 1, "description": "تعداد اعضای تیم"},
                "hourly_rate": {"type": "number", "minimum": 0, "description": "نرخ ساعتی (تومان)"},
                "materials_cost": {"type": "number", "minimum": 0, "description": "هزینه مواد اولیه"},
                "overhead_percentage": {"type": "number", "minimum": 0, "maximum": 100, "description": "درصد سربار"},
                "profit_margin": {"type": "number", "minimum": 0, "maximum": 100, "description": "حاشیه سود (%)"},
                "tax_rate": {"type": "number", "minimum": 0, "maximum": 100, "description": "نرخ مالیات (%)"}
            },
            "required": ["project_name", "duration_months", "team_size", "hourly_rate"]
        },
        output_schema={
            "type": "object",
            "properties": {
                "total_labor_cost": {"type": "number", "description": "کل هزینه نیروی کار"},
                "total_materials_cost": {"type": "number", "description": "کل هزینه مواد"},
                "overhead_cost": {"type": "number", "description": "هزینه سربار"},
                "subtotal": {"type": "number", "description": "جمع کل قبل از سود"},
                "profit_amount": {"type": "number", "description": "مبلغ سود"},
                "tax_amount": {"type": "number", "description": "مبلغ مالیات"},
                "total_budget": {"type": "number", "description": "بودجه کل پروژه"},
                "monthly_budget": {"type": "number", "description": "بودجه ماهانه"},
                "breakdown": {
                    "type": "object",
                    "description": "جزئیات محاسبات",
                    "properties": {
                        "labor_breakdown": {"type": "array", "description": "جزئیات هزینه نیروی کار"},
                        "materials_breakdown": {"type": "array", "description": "جزئیات هزینه مواد"}
                    }
                }
            }
        },
        default_config={
            "algorithm": "standard_budget",
            "precision": 2,
            "currency": "IRR",
            "timeout": 300,
            "retry_count": 3,
            "cache_duration": 3600
        },
        estimated_time_seconds=30,
        memory_requirement_mb=128,
        cpu_intensive=False,
        required_user_type="free",
        is_active=True
    )
    print(f"✅ قالب محاسبه بودجه ایجاد شد: {template.name}")
    return template


def create_security_analysis_template():
    """ایجاد قالب تحلیل امنیتی"""
    template = ComputationTemplate.objects.create(
        name="تحلیل امنیتی سیستم",
        description="""
        قالب تحلیل امنیتی برای ارزیابی آسیب‌پذیری‌های سیستم.
        این قالب شامل بررسی امنیت شبکه، نرم‌افزار و زیرساخت می‌باشد.
        
        ویژگی‌ها:
        - اسکن آسیب‌پذیری‌ها
        - ارزیابی سطح ریسک
        - پیشنهادات امنیتی
        - گزارش جامع امنیتی
        """,
        session_type="security_analysis",
        input_schema={
            "type": "object",
            "properties": {
                "system_type": {"type": "string", "enum": ["web", "mobile", "desktop", "network"], "description": "نوع سیستم"},
                "target_url": {"type": "string", "format": "uri", "description": "آدرس هدف"},
                "scan_depth": {"type": "string", "enum": ["basic", "standard", "deep"], "description": "عمق اسکن"},
                "check_ssl": {"type": "boolean", "description": "بررسی SSL"},
                "check_headers": {"type": "boolean", "description": "بررسی هدرها"},
                "check_ports": {"type": "boolean", "description": "بررسی پورت‌ها"},
                "custom_checks": {"type": "array", "items": {"type": "string"}, "description": "بررسی‌های سفارشی"}
            },
            "required": ["system_type", "target_url", "scan_depth"]
        },
        output_schema={
            "type": "object",
            "properties": {
                "overall_risk_score": {"type": "number", "minimum": 0, "maximum": 100, "description": "امتیاز کلی ریسک"},
                "vulnerabilities": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "severity": {"type": "string", "enum": ["low", "medium", "high", "critical"]},
                            "description": {"type": "string"},
                            "recommendation": {"type": "string"}
                        }
                    }
                },
                "security_headers": {"type": "object", "description": "وضعیت هدرهای امنیتی"},
                "ssl_analysis": {"type": "object", "description": "تحلیل SSL"},
                "recommendations": {"type": "array", "items": {"type": "string"}},
                "report_summary": {"type": "string", "description": "خلاصه گزارش"}
            }
        },
        default_config={
            "algorithm": "security_scanner",
            "scan_timeout": 600,
            "max_vulnerabilities": 50,
            "severity_threshold": "medium",
            "generate_report": True
        },
        estimated_time_seconds=120,
        memory_requirement_mb=256,
        cpu_intensive=True,
        required_user_type="premium",
        is_active=True
    )
    print(f"✅ قالب تحلیل امنیتی ایجاد شد: {template.name}")
    return template


def create_performance_test_template():
    """ایجاد قالب تست عملکرد"""
    template = ComputationTemplate.objects.create(
        name="تست عملکرد سرور",
        description="""
        قالب تست عملکرد برای ارزیابی سرعت و کارایی سرورها.
        این قالب شامل تست بار، تست استرس و تحلیل عملکرد می‌باشد.
        
        ویژگی‌ها:
        - تست بار (Load Testing)
        - تست استرس (Stress Testing)
        - تست حجم (Volume Testing)
        - تحلیل عملکرد
        """,
        session_type="performance_test",
        input_schema={
            "type": "object",
            "properties": {
                "target_url": {"type": "string", "format": "uri", "description": "آدرس هدف"},
                "test_type": {"type": "string", "enum": ["load", "stress", "volume"], "description": "نوع تست"},
                "concurrent_users": {"type": "integer", "minimum": 1, "description": "تعداد کاربران همزمان"},
                "test_duration": {"type": "integer", "minimum": 60, "description": "مدت تست (ثانیه)"},
                "ramp_up_time": {"type": "integer", "minimum": 10, "description": "زمان افزایش بار (ثانیه)"},
                "request_types": {"type": "array", "items": {"type": "string"}, "description": "انواع درخواست"},
                "expected_response_time": {"type": "number", "description": "زمان پاسخ مورد انتظار (میلی‌ثانیه)"}
            },
            "required": ["target_url", "test_type", "concurrent_users", "test_duration"]
        },
        output_schema={
            "type": "object",
            "properties": {
                "test_summary": {
                    "type": "object",
                    "properties": {
                        "total_requests": {"type": "integer"},
                        "successful_requests": {"type": "integer"},
                        "failed_requests": {"type": "integer"},
                        "average_response_time": {"type": "number"},
                        "max_response_time": {"type": "number"},
                        "min_response_time": {"type": "number"},
                        "requests_per_second": {"type": "number"}
                    }
                },
                "performance_metrics": {
                    "type": "object",
                    "properties": {
                        "cpu_usage": {"type": "number"},
                        "memory_usage": {"type": "number"},
                        "network_throughput": {"type": "number"},
                        "error_rate": {"type": "number"}
                    }
                },
                "recommendations": {"type": "array", "items": {"type": "string"}},
                "bottlenecks": {"type": "array", "items": {"type": "string"}},
                "test_report": {"type": "string", "description": "گزارش کامل تست"}
            }
        },
        default_config={
            "algorithm": "performance_tester",
            "monitoring_interval": 5,
            "alert_threshold": 80,
            "generate_charts": True,
            "export_format": "json"
        },
        estimated_time_seconds=300,
        memory_requirement_mb=512,
        cpu_intensive=True,
        required_user_type="premium",
        is_active=True
    )
    print(f"✅ قالب تست عملکرد ایجاد شد: {template.name}")
    return template


def create_data_processing_template():
    """ایجاد قالب پردازش داده"""
    template = ComputationTemplate.objects.create(
        name="پردازش و تحلیل داده‌ها",
        description="""
        قالب پردازش داده برای تحلیل و پردازش مجموعه‌های داده بزرگ.
        این قالب شامل تمیز کردن داده، تحلیل آماری و تولید گزارش می‌باشد.
        
        ویژگی‌ها:
        - تمیز کردن داده‌ها
        - تحلیل آماری
        - تولید نمودار
        - گزارش‌گیری خودکار
        """,
        session_type="data_processing",
        input_schema={
            "type": "object",
            "properties": {
                "data_source": {"type": "string", "description": "منبع داده"},
                "data_format": {"type": "string", "enum": ["csv", "json", "xml", "excel"], "description": "فرمت داده"},
                "processing_type": {"type": "string", "enum": ["clean", "analyze", "visualize", "report"], "description": "نوع پردازش"},
                "data_size": {"type": "integer", "minimum": 1, "description": "حجم داده (رکورد)"},
                "analysis_parameters": {
                    "type": "object",
                    "properties": {
                        "statistical_tests": {"type": "array", "items": {"type": "string"}},
                        "visualization_types": {"type": "array", "items": {"type": "string"}},
                        "output_format": {"type": "string", "enum": ["pdf", "html", "excel", "json"]}
                    }
                },
                "filters": {"type": "object", "description": "فیلترهای داده"}
            },
            "required": ["data_source", "data_format", "processing_type"]
        },
        output_schema={
            "type": "object",
            "properties": {
                "processing_summary": {
                    "type": "object",
                    "properties": {
                        "total_records": {"type": "integer"},
                        "processed_records": {"type": "integer"},
                        "cleaned_records": {"type": "integer"},
                        "processing_time": {"type": "number"}
                    }
                },
                "statistical_analysis": {
                    "type": "object",
                    "properties": {
                        "descriptive_stats": {"type": "object"},
                        "correlations": {"type": "object"},
                        "trends": {"type": "array"}
                    }
                },
                "visualizations": {"type": "array", "items": {"type": "object"}},
                "insights": {"type": "array", "items": {"type": "string"}},
                "report_url": {"type": "string", "description": "لینک گزارش"}
            }
        },
        default_config={
            "algorithm": "data_processor",
            "chunk_size": 1000,
            "parallel_processing": True,
            "cache_results": True,
            "quality_threshold": 0.95
        },
        estimated_time_seconds=180,
        memory_requirement_mb=1024,
        cpu_intensive=True,
        required_user_type="enterprise",
        is_active=True
    )
    print(f"✅ قالب پردازش داده ایجاد شد: {template.name}")
    return template


def create_ai_inference_template():
    """ایجاد قالب استنتاج هوش مصنوعی"""
    template = ComputationTemplate.objects.create(
        name="استنتاج هوش مصنوعی",
        description="""
        قالب استنتاج هوش مصنوعی برای مدل‌های ML و AI.
        این قالب شامل پیش‌بینی، طبقه‌بندی و تحلیل هوش مصنوعی می‌باشد.
        
        ویژگی‌ها:
        - پیش‌بینی با مدل‌های ML
        - طبقه‌بندی داده‌ها
        - تحلیل احساسات
        - تشخیص الگو
        """,
        session_type="ai_inference",
        input_schema={
            "type": "object",
            "properties": {
                "model_type": {"type": "string", "enum": ["classification", "regression", "clustering", "nlp"], "description": "نوع مدل"},
                "model_name": {"type": "string", "description": "نام مدل"},
                "input_data": {"type": "array", "items": {"type": "object"}, "description": "داده‌های ورودی"},
                "model_parameters": {"type": "object", "description": "پارامترهای مدل"},
                "confidence_threshold": {"type": "number", "minimum": 0, "maximum": 1, "description": "آستانه اطمینان"},
                "batch_size": {"type": "integer", "minimum": 1, "description": "اندازه دسته"}
            },
            "required": ["model_type", "model_name", "input_data"]
        },
        output_schema={
            "type": "object",
            "properties": {
                "predictions": {"type": "array", "items": {"type": "object"}},
                "confidence_scores": {"type": "array", "items": {"type": "number"}},
                "model_metrics": {
                    "type": "object",
                    "properties": {
                        "accuracy": {"type": "number"},
                        "precision": {"type": "number"},
                        "recall": {"type": "number"},
                        "f1_score": {"type": "number"}
                    }
                },
                "inference_time": {"type": "number", "description": "زمان استنتاج"},
                "model_info": {"type": "object", "description": "اطلاعات مدل"}
            }
        },
        default_config={
            "algorithm": "ai_inference",
            "gpu_acceleration": True,
            "model_cache": True,
            "batch_processing": True,
            "optimization_level": "high"
        },
        estimated_time_seconds=60,
        memory_requirement_mb=2048,
        cpu_intensive=True,
        required_user_type="enterprise",
        is_active=True
    )
    print(f"✅ قالب استنتاج هوش مصنوعی ایجاد شد: {template.name}")
    return template


def create_custom_computation_template():
    """ایجاد قالب محاسبات سفارشی"""
    template = ComputationTemplate.objects.create(
        name="محاسبات سفارشی",
        description="""
        قالب عمومی برای محاسبات سفارشی و پیچیده.
        این قالب برای محاسبات خاص و الگوریتم‌های پیچیده طراحی شده است.
        
        ویژگی‌ها:
        - پشتیبانی از الگوریتم‌های سفارشی
        - محاسبات پیچیده ریاضی
        - پردازش موازی
        - قابلیت توسعه
        """,
        session_type="custom",
        input_schema={
            "type": "object",
            "properties": {
                "computation_type": {"type": "string", "description": "نوع محاسبه"},
                "algorithm": {"type": "string", "description": "الگوریتم مورد استفاده"},
                "parameters": {"type": "object", "description": "پارامترهای محاسبه"},
                "data": {"type": "array", "description": "داده‌های ورودی"},
                "options": {"type": "object", "description": "گزینه‌های محاسبه"}
            },
            "required": ["computation_type", "algorithm", "data"]
        },
        output_schema={
            "type": "object",
            "properties": {
                "result": {"type": "object", "description": "نتیجه محاسبه"},
                "computation_time": {"type": "number", "description": "زمان محاسبه"},
                "memory_used": {"type": "number", "description": "حافظه استفاده شده"},
                "status": {"type": "string", "description": "وضعیت محاسبه"},
                "metadata": {"type": "object", "description": "اطلاعات اضافی"}
            }
        },
        default_config={
            "algorithm": "custom_computation",
            "parallel_processing": True,
            "optimization": "auto",
            "debug_mode": False,
            "result_caching": True
        },
        estimated_time_seconds=120,
        memory_requirement_mb=512,
        cpu_intensive=True,
        required_user_type="premium",
        is_active=True
    )
    print(f"✅ قالب محاسبات سفارشی ایجاد شد: {template.name}")
    return template


def main():
    """تابع اصلی برای ایجاد قالب‌های پیش‌فرض"""
    print("🚀 شروع ایجاد قالب‌های پیش‌فرض محاسباتی...")
    print("=" * 60)
    
    # بررسی وجود قالب‌های قبلی
    existing_templates = ComputationTemplate.objects.count()
    if existing_templates > 0:
        print(f"⚠️  {existing_templates} قالب موجود است.")
        response = input("آیا می‌خواهید قالب‌های جدید اضافه کنید؟ (y/n): ")
        if response.lower() != 'y':
            print("❌ عملیات لغو شد.")
            return
    
    templates_created = []
    
    try:
        # ایجاد قالب‌های مختلف
        templates_created.append(create_budget_calculation_template())
        templates_created.append(create_security_analysis_template())
        templates_created.append(create_performance_test_template())
        templates_created.append(create_data_processing_template())
        templates_created.append(create_ai_inference_template())
        templates_created.append(create_custom_computation_template())
        
        print("=" * 60)
        print(f"✅ {len(templates_created)} قالب پیش‌فرض با موفقیت ایجاد شد!")
        print("\n📋 فهرست قالب‌های ایجاد شده:")
        for i, template in enumerate(templates_created, 1):
            print(f"  {i}. {template.name} ({template.session_type})")
            print(f"     - نوع کاربر: {template.required_user_type}")
            print(f"     - زمان تخمینی: {template.estimated_time_seconds} ثانیه")
            print(f"     - حافظه: {template.memory_requirement_mb} MB")
            print(f"     - CPU-Intensive: {'بله' if template.cpu_intensive else 'خیر'}")
            print()
        
        print("🎉 تمام قالب‌ها آماده استفاده هستند!")
        print("💡 می‌توانید از طریق پنل مدیریت به آن‌ها دسترسی داشته باشید.")
        
    except Exception as e:
        print(f"❌ خطا در ایجاد قالب‌ها: {str(e)}")
        return False
    
    return True


if __name__ == "__main__":
    main()
