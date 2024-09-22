from django.db import models
from django.utils import timezone

# Create your models here CAMP.

class Camp(models.Model):
    camp_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    camp_regno = models.CharField(max_length=100, unique=True)
    camp_provider_name = models.CharField(max_length=150)
    password = models.CharField(max_length=100)
    date_registered = models.DateTimeField(auto_now_add=True)
    vstatus=models.IntegerField(default=0)


class CampFacility(models.Model):
    CAMP_ITEM_CHOICES = [
        ('Bed', 'Bed'),
        ('Tent', 'Tent'),
        ('Food', 'Food'),
        ('Stool', 'Stool'),
        ('SleepingBag', 'Sleeping Bag'),
        ('Lantern', 'Lantern'),
        ('CampFire', 'Camp Fire'),
        ('FirstAid', 'First Aid Kit'),
        ('CookingGear', 'Cooking Gear'),
        ('Water', 'Water Supply'),
    ]

    facility_name = models.CharField(max_length=100, choices=CAMP_ITEM_CHOICES)
    quantity_available = models.PositiveIntegerField(default=0)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    description = models.TextField(blank=True, null=True)
    camp = models.ForeignKey('Camp', on_delete=models.CASCADE, related_name='facilities')




class CampProfile(models.Model):
    CAMP_TYPE_CHOICES = [
        ('Adventure', 'Adventure'),
        ('Luxury', 'Luxury'),
        ('Family', 'Family'),
        ('Eco', 'Eco'),
        ('Friends', 'Friends'),
    ]

    camp_name = models.CharField(max_length=200)
    description = models.TextField()
    camp_type = models.CharField(max_length=50, choices=CAMP_TYPE_CHOICES)
    operating_hours = models.CharField(max_length=100, blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)  
    pricing_info = models.TextField(blank=True, null=True)
    social_media_facebook = models.URLField(blank=True, null=True)
    social_media_twitter = models.URLField(blank=True, null=True)
    social_media_instagram = models.URLField(blank=True, null=True)
    camp = models.ForeignKey('Camp', on_delete=models.CASCADE, related_name='CampProfile')


class CampImage(models.Model):
    camp = models.ForeignKey('Camp', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='camp_images/')
    description = models.CharField(max_length=255, blank=True, null=True)


class CampPackage(models.Model):
    camp = models.ForeignKey('Camp', on_delete=models.CASCADE, related_name='packages')
    package_name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.TextField()
    camp_start_date = models.DateField(auto_now_add=True)
    camp_end_date = models.DateField()
    booking_start_date =models.DateField(auto_now_add=True)  
    booking_end_date = models.DateField()
    max_people = models.PositiveIntegerField()
    facilities_provided = models.ManyToManyField('CampFacility', related_name='camp_packages', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=True)
    images = models.ImageField(upload_to='package_images/', blank=True, null=True)
    