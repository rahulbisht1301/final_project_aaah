import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'venturehub.settings')
django.setup()

from accounts.models import User, AdminProfile

# Find existing superusers
superusers = User.objects.filter(is_superuser=True)

if not superusers.exists():
    print("❌ No superusers found in the database!")
    exit(1)

print("Found superusers:")
for i, user in enumerate(superusers, 1):
    print(f"{i}. {user.username} (email: {user.email}, role: {user.role})")

choice = input(f"\nEnter the number of the superuser you want to convert to ADMIN: ").strip()

try:
    choice = int(choice)
    if 1 <= choice <= len(superusers):
        user = list(superusers)[choice - 1]
        
        # Update role to ADMIN
        user.role = 'ADMIN'
        user.save()
        
        # Create or update AdminProfile
        admin_profile, created = AdminProfile.objects.get_or_create(
            user=user,
            defaults={'is_super_admin': True}
        )
        
        if created:
            print(f"✅ AdminProfile created for {user.username}")
        else:
            print(f"✅ AdminProfile already exists for {user.username}")
        
        print(f"✅ User '{user.username}' has been set as ADMIN!")
        print(f"📍 Admin login: http://localhost:8000/admin-dashboard/login/")
        
    else:
        print("❌ Invalid choice!")
        exit(1)
except ValueError:
    print("❌ Please enter a valid number!")
    exit(1)
