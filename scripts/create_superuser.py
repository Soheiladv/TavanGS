import os
import sys
from pathlib import Path
import django

# Ensure project root is on sys.path when running from scripts/
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'takotech_website.settings')
django.setup()

from django.contrib.auth import get_user_model


def main():
    User = get_user_model()
    email = os.environ.get('ADMIN_EMAIL', 'admin@takotech.local')
    password = os.environ.get('ADMIN_PASSWORD', 'D@d123')

    if User.objects.filter(email=email).exists():
        print(f'Superuser exists: {email}')
        return

    user = User.objects.create_superuser(email=email, password=password)
    print(f'Created superuser: {email}')


if __name__ == '__main__':
    main()


