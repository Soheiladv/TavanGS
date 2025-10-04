import os
import sys
from pathlib import Path
import django

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'takotech_website.settings')
django.setup()

from products.models import ProductCategory, Product
from services.models import ServiceCategory, Service


def seed_products():
    cat_finance, _ = ProductCategory.objects.get_or_create(
        name='راهکارهای مالی', slug='finance', defaults={'description': 'محصولات مالی', 'icon': 'wallet'}
    )
    cat_security, _ = ProductCategory.objects.get_or_create(
        name='راهکارهای امنیتی', slug='security', defaults={'description': 'محصولات امنیتی', 'icon': 'shield'}
    )

    Product.objects.get_or_create(
        name='BudgetPro',
        slug='takotech-budgetpro',
        defaults={
            'brand_prefix': 'TakoTech',
            'tagline': 'نرم‌افزار بودجه‌نویسی هوشمند',
            'description': 'مدیریت مالی و بودجه‌نویسی پیشرفته برای کسب‌وکارها',
            'short_description': 'بودجه‌نویسی سریع و دقیق',
            'category': cat_finance,
            'features': [{'title': 'گزارش‌گیری'}, {'title': 'پیش‌بینی'}],
            'has_trial': True,
            'is_featured': True,
        }
    )

    Product.objects.get_or_create(
        name='SecureAI',
        slug='takotech-secureai',
        defaults={
            'brand_prefix': 'TakoTech',
            'tagline': 'هوش مصنوعی امنیتی',
            'description': 'تحلیل امنیت و کشف تهدید با هوش مصنوعی',
            'short_description': 'تحلیل امنیتی هوشمند',
            'category': cat_security,
            'features': [{'title': 'تشخیص تهدید'}, {'title': 'گزارش امنیتی'}],
            'has_trial': True,
            'is_featured': True,
        }
    )


def seed_services():
    cat_consult, _ = ServiceCategory.objects.get_or_create(
        name='مشاوره فناوری', slug='it-consulting', defaults={'description': 'مشاوره فنی و استراتژیک', 'icon': 'comments'}
    )

    Service.objects.get_or_create(
        name='توسعه نرم‌افزار سفارشی',
        slug='custom-software-dev',
        defaults={
            'tagline': 'از ایده تا محصول',
            'description': 'طراحی و پیاده‌سازی نرم‌افزارهای سازمانی مطابق نیاز شما',
            'short_description': 'پیاده‌سازی سریع و باکیفیت',
            'category': cat_consult,
            'features': ['تحلیل نیاز', 'طراحی معماری', 'تست و استقرار'],
            'is_featured': True,
        }
    )


def main():
    seed_products()
    seed_services()
    print('Demo data seeded.')


if __name__ == '__main__':
    main()


