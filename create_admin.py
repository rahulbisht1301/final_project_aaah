import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'venturehub.settings')
django.setup()

from accounts.models import User

# Create admin user
username = input("Enter admin username (default: admin): ").strip() or "admin"
email = input("Enter admin email (default: admin@venturehub.com): ").strip() or "admin@venturehub.com"
password = input("Enter admin password: ").strip()

if not password:
    print("❌ Password cannot be empty!")
    exit(1)

if User.objects.filter(username=username).exists():
    print(f"❌ Username '{username}' already exists!")
    exit(1)

try:
    admin_user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password,
        role='ADMIN'
    )
    print(f"✅ Admin user '{username}' created successfully!")
    print(f"📍 Admin login: http://localhost:8000/admin-dashboard/login/")
except Exception as e:
    print(f"❌ Error creating admin user: {e}")
