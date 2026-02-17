import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'venturehub.settings')
django.setup()

from django.contrib.auth import get_user_model
from startups.models import Startup

User = get_user_model()

def add_data():
    startups_data = [
        {"name": "Zepto", "niche": "Instant Grocery Delivery", "val": 1400000000, "stage": "Growth Stage", "vision": "Deliver groceries in 10 minutes", "email": "contact@zepto.com", "phone": "9000000001", "website": "https://www.zepto.com"},
        {"name": "Swiggy", "niche": "Food Delivery", "val": 10000000000, "stage": "Late Growth", "vision": "Convenience ecosystem", "email": "contact@swiggy.com", "phone": "9000000002", "website": "https://www.swiggy.com"},
        {"name": "Zomato", "niche": "Restaurant Discovery", "val": 12000000000, "stage": "Public Company", "vision": "Better food for more people", "email": "contact@zomato.com", "phone": "9000000003", "website": "https://www.zomato.com"},
        {"name": "Ola", "niche": "Ride Sharing", "val": 7000000000, "stage": "Late Growth", "vision": "Mobility for a billion", "email": "contact@olacabs.com", "phone": "9000000004", "website": "https://www.olacabs.com"},
        {"name": "Razorpay", "niche": "FinTech", "val": 7500000000, "stage": "Growth", "vision": "Simplify payments", "email": "contact@razorpay.com", "phone": "9000000005", "website": "https://www.razorpay.com"},
        {"name": "CRED", "niche": "Credit Rewards", "val": 6000000000, "stage": "Growth", "vision": "Reward responsible behavior", "email": "contact@cred.club", "phone": "9000000006", "website": "https://www.cred.club"},
        {"name": "Meesho", "niche": "Social Commerce", "val": 4900000000, "stage": "Growth", "vision": "Enable small businesses", "email": "contact@meesho.com", "phone": "9000000007", "website": "https://www.meesho.com"},
        {"name": "BYJU’S", "niche": "EdTech", "val": 5000000000, "stage": "Late Growth", "vision": "Engaging learning", "email": "contact@byjus.com", "phone": "9000000008", "website": "https://www.byjus.com"},
        {"name": "Unacademy", "niche": "EdTech", "val": 3000000000, "stage": "Growth", "vision": "Democratize education", "email": "contact@unacademy.com", "phone": "9000000009", "website": "https://www.unacademy.com"},
        {"name": "Groww", "niche": "Investment Platform", "val": 3000000000, "stage": "Growth", "vision": "Make investing simple", "email": "contact@groww.in", "phone": "9000000010", "website": "https://www.groww.in"},
        {"name": "PhonePe", "niche": "Digital Payments", "val": 12000000000, "stage": "Growth", "vision": "Financial inclusion", "email": "contact@phonepe.com", "phone": "9000000011", "website": "https://www.phonepe.com"},
        {"name": "Nykaa", "niche": "Beauty E-commerce", "val": 6000000000, "stage": "Public Company", "vision": "Beauty for modern India", "email": "contact@nykaa.com", "phone": "9000000012", "website": "https://www.nykaa.com"},
        {"name": "boAt", "niche": "Electronics", "val": 1400000000, "stage": "Growth", "vision": "Lifestyle electronics", "email": "contact@boat-lifestyle.com", "phone": "9000000013", "website": "https://www.boat-lifestyle.com"},
        {"name": "Lenskart", "niche": "Eyewear", "val": 4000000000, "stage": "Growth", "vision": "Vision for every Indian", "email": "contact@lenskart.com", "phone": "9000000014", "website": "https://www.lenskart.com"},
        {"name": "OYO", "niche": "Hospitality", "val": 2500000000, "stage": "Late Growth", "vision": "Affordable stays", "email": "contact@oyorooms.com", "phone": "9000000015", "website": "https://www.oyorooms.com"},
        {"name": "Urban Company", "niche": "Home Services", "val": 2000000000, "stage": "Growth", "vision": "Organized marketplace", "email": "contact@urbancompany.com", "phone": "9000000016", "website": "https://www.urbancompany.com"},
        {"name": "Blinkit", "niche": "Quick Commerce", "val": 1000000000, "stage": "Growth", "vision": "Groceries in minutes", "email": "contact@blinkit.com", "phone": "9000000017", "website": "https://www.blinkit.com"},
        {"name": "Delhivery", "niche": "Logistics", "val": 3000000000, "stage": "Late Growth", "vision": "Logistics backbone", "email": "contact@delhivery.com", "phone": "9000000018", "website": "https://www.delhivery.com"},
        {"name": "Freshworks", "niche": "SaaS", "val": 4000000000, "stage": "Global Growth", "vision": "Easy business software", "email": "contact@freshworks.com", "phone": "9000000019", "website": "https://www.freshworks.com"},
        {"name": "Paytm", "niche": "FinTech", "val": 5000000000, "stage": "Late Growth", "vision": "Digital payments", "email": "contact@paytm.com", "phone": "9000000020", "website": "https://www.paytm.com"},
    ]

    for data in startups_data:
        username = f"founder_{data['name'].lower().replace(' ', '_').replace('’', '').replace('`', '')}"

        founder, created_user = User.objects.get_or_create(
            username=username,
            defaults={
                "email": data["email"],
                "role": "STARTUP"
            }
        )

        if created_user:
            founder.set_password("password123")
            founder.save()

        startup, created = Startup.objects.get_or_create(
            name=data['name'],
            defaults={
                'founder': founder,
                'niche': data['niche'],
                'valuation': data['val'],
                'stage': data['stage'],
                'vision': data['vision'],
                'email': data['email'],
                'phone': data['phone'],
                'website': data['website'],
                'approved': True
            }
        )

        if created:
            print(f"✅ Added: {data['name']}")
        else:
            print(f"⚠️ Skip: {data['name']} already exists")

if __name__ == '__main__':
    add_data()
    print("✨ All 20 Startups Successfully Synced!")