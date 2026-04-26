"""
Management command to seed the database with sample data.
Usage: python manage.py seed_data
"""

from django.core.management.base import BaseCommand
from accounts.models import User
from farmers.models import Vegetable, CropListing
from inquiries.models import Inquiry, InquiryReply
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Seeds the database with sample data for AgroLink Global'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...\n')

        # --- Vegetables ---
        vegetables_data = [
            ('Potato', 'আলু', 'rabi', 'Staple crop grown widely in northern Bangladesh'),
            ('Onion', 'পেঁয়াজ', 'rabi', 'High-demand crop with export potential'),
            ('Tomato', 'টমেটো', 'rabi', 'Versatile vegetable used in many cuisines'),
            ('Green Chili', 'কাঁচা মরিচ', 'year_round', 'Essential spice crop'),
            ('Bitter Gourd', 'করলা', 'kharif1', 'Popular in Asian cuisine, growing export demand'),
            ('Eggplant', 'বেগুন', 'year_round', 'Widely cultivated across Bangladesh'),
            ('Cauliflower', 'ফুলকপি', 'rabi', 'High-value winter vegetable'),
            ('Cabbage', 'বাঁধাকপি', 'rabi', 'Cool season crop with good yield'),
            ('Cucumber', 'শসা', 'kharif1', 'Summer crop with good market demand'),
            ('Pumpkin', 'কুমড়া', 'kharif2', 'Nutritious and long shelf life'),
            ('Spinach', 'পালং শাক', 'rabi', 'Nutritious leafy green'),
            ('Carrot', 'গাজর', 'rabi', 'Root vegetable popular in winter'),
        ]

        vegetables = []
        for name, local, season, desc in vegetables_data:
            veg, created = Vegetable.objects.get_or_create(
                name=name,
                defaults={'local_name': local, 'season': season, 'description': desc}
            )
            vegetables.append(veg)
            status = 'Created' if created else 'Exists'
            self.stdout.write(f'  {status}: {name}')

        # --- Farmers ---
        farmers_data = [
            ('farmer1', 'Rahim', 'Uddin', 'Rajshahi', '01711111111'),
            ('farmer2', 'Karim', 'Hossain', 'Bogra', '01722222222'),
            ('farmer3', 'Jamal', 'Ahmed', 'Dinajpur', '01733333333'),
            ('farmer4', 'Fatema', 'Begum', 'Rangpur', '01744444444'),
            ('farmer5', 'Sumon', 'Mia', 'Comilla', '01755555555'),
        ]

        farmers = []
        for uname, first, last, district, phone in farmers_data:
            user, created = User.objects.get_or_create(
                username=uname,
                defaults={
                    'first_name': first, 'last_name': last,
                    'email': f'{uname}@agrolink.test',
                    'role': 'farmer', 'district': district, 'phone': phone,
                }
            )
            if created:
                user.set_password('Test@1234')
                user.save()
            farmers.append(user)
            status = 'Created' if created else 'Exists'
            self.stdout.write(f'  {status}: Farmer {first} {last}')

        # --- Exporters ---
        exporters_data = [
            ('exporter1', 'David', 'Smith', 'Dhaka', '01811111111'),
            ('exporter2', 'Sarah', 'Johnson', 'Chittagong', '01822222222'),
            ('exporter3', 'Tanvir', 'Rahman', 'Dhaka', '01833333333'),
        ]

        exporters = []
        for uname, first, last, district, phone in exporters_data:
            user, created = User.objects.get_or_create(
                username=uname,
                defaults={
                    'first_name': first, 'last_name': last,
                    'email': f'{uname}@agrolink.test',
                    'role': 'exporter', 'district': district, 'phone': phone,
                }
            )
            if created:
                user.set_password('Test@1234')
                user.save()
            exporters.append(user)
            status = 'Created' if created else 'Exists'
            self.stdout.write(f'  {status}: Exporter {first} {last}')

        # --- Crop Listings ---
        districts = ['Rajshahi', 'Bogra', 'Dinajpur', 'Rangpur', 'Comilla', 'Dhaka', 'Jessore', 'Khulna']
        seasons = ['kharif1', 'kharif2', 'rabi', 'year_round']

        if CropListing.objects.count() < 5:
            for i in range(20):
                farmer = random.choice(farmers)
                veg = random.choice(vegetables)
                CropListing.objects.create(
                    farmer=farmer,
                    vegetable=veg,
                    quantity_kg=random.randint(100, 5000),
                    price_per_kg=round(random.uniform(10, 80), 2),
                    district=random.choice(districts),
                    season=random.choice(seasons),
                    harvest_date=date.today() + timedelta(days=random.randint(-30, 90)),
                    status=random.choice(['available', 'available', 'available', 'upcoming']),
                    description=f'Fresh {veg.name} from {farmer.district}',
                )
            self.stdout.write(f'  Created 20 crop listings')
        else:
            self.stdout.write(f'  Crop listings already exist')

        # --- Sample Inquiries ---
        if Inquiry.objects.count() == 0:
            listings = list(CropListing.objects.filter(status='available')[:5])
            for listing in listings:
                exp = random.choice(exporters)
                inquiry = Inquiry.objects.create(
                    exporter=exp,
                    farmer=listing.farmer,
                    crop_listing=listing,
                    subject=f'Interested in {listing.vegetable.name} from {listing.district}',
                    message=f'Hello, I am interested in purchasing {listing.vegetable.name}. Can you provide details about quality and delivery options?',
                    quantity_needed=random.randint(50, 2000),
                    status=random.choice(['pending', 'responded', 'accepted']),
                )
                InquiryReply.objects.create(
                    inquiry=inquiry,
                    sender=listing.farmer,
                    message=f'Thank you for your interest. Our {listing.vegetable.name} is of premium quality. We can arrange delivery within the week.',
                )
            self.stdout.write(f'  Created {len(listings)} sample inquiries')

        # --- Admin User ---
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'first_name': 'Admin', 'last_name': 'User',
                'email': 'admin@agrolink.test',
                'role': 'admin', 'is_staff': True, 'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('Admin@1234')
            admin_user.save()
        self.stdout.write(f'  {"Created" if created else "Exists"}: Admin user')

        self.stdout.write(self.style.SUCCESS('\nDatabase seeded successfully!'))
        self.stdout.write('\nLogin Credentials:')
        self.stdout.write('  Admin:    admin / Admin@1234')
        self.stdout.write('  Farmer:   farmer1 / Test@1234')
        self.stdout.write('  Exporter: exporter1 / Test@1234')
