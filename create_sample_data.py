import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'venturehub.settings')
django.setup()

from accounts.models import User
from startups.models import Startup

startups_data = [
    {
        'username': 'techvision',
        'user_email': 'techvision@example.com',
        'name': 'TechVision AI',
        'niche': 'Artificial Intelligence',
        'valuation': 5000000,
        'stage': 'Series A',
        'vision': 'Building next-generation AI solutions for healthcare diagnostics. Our platform uses deep learning to detect diseases early with 99% accuracy.',
        'email': 'contact@techvision.ai',
        'phone': '+1-555-0101',
        'website': 'https://techvision.ai'
    },
    {
        'username': 'greenergy',
        'user_email': 'greenergy@example.com',
        'name': 'GreenErgy Solutions',
        'niche': 'Clean Energy',
        'valuation': 8000000,
        'stage': 'Series B',
        'vision': 'Revolutionizing renewable energy storage with advanced battery technology. Our batteries last 3x longer and charge 5x faster than competitors.',
        'email': 'hello@greenergy.com',
        'phone': '+1-555-0202',
        'website': 'https://greenergy.com'
    },
    {
        'username': 'foodtech',
        'user_email': 'foodtech@example.com',
        'name': 'FoodTech Labs',
        'niche': 'Food Technology',
        'valuation': 3000000,
        'stage': 'Seed',
        'vision': 'Creating sustainable plant-based proteins that taste like real meat. Our patented process uses 90% less water and produces zero carbon emissions.',
        'email': 'info@foodtechlabs.io',
        'phone': '+1-555-0303',
        'website': 'https://foodtechlabs.io'
    },
    {
        'username': 'smartlogistics',
        'user_email': 'smartlogistics@example.com',
        'name': 'SmartLogistics Pro',
        'niche': 'Supply Chain',
        'valuation': 12000000,
        'stage': 'Series B',
        'vision': 'AI-powered supply chain optimization reducing delivery times by 40% and costs by 25%. Trusted by 500+ enterprises worldwide.',
        'email': 'sales@smartlogistics.pro',
        'phone': '+1-555-0404',
        'website': 'https://smartlogistics.pro'
    },
    {
        'username': 'healthwear',
        'user_email': 'healthwear@example.com',
        'name': 'HealthWear Tech',
        'niche': 'Wearable Technology',
        'valuation': 6500000,
        'stage': 'Series A',
        'vision': 'Smart wearables that monitor vital signs 24/7 and predict health issues before they occur. FDA approved and doctor recommended.',
        'email': 'support@healthwear.tech',
        'phone': '+1-555-0505',
        'website': 'https://healthwear.tech'
    }
]

for data in startups_data:
    if not User.objects.filter(username=data['username']).exists():
        user = User.objects.create_user(
            username=data['username'],
            email=data['user_email'],
            password='startup123',
            role='STARTUP'
        )
        
        startup = Startup.objects.get(founder=user)
        startup.name = data['name']
        startup.niche = data['niche']
        startup.valuation = data['valuation']
        startup.stage = data['stage']
        startup.vision = data['vision']
        startup.email = data['email']
        startup.phone = data['phone']
        startup.website = data['website']
        startup.approved = True
        startup.save()
        print(f'Created: {data["name"]}')
    else:
        print(f'Already exists: {data["username"]}')

print('Done! Sample startups created.')
