from django.db import models

from Camp.models import CampFacility, CampPackage

# Create your models here for USER.

class User(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    password = models.CharField(max_length=100)
    id_number = models.CharField(max_length=50, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)




class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    package = models.ForeignKey(CampPackage, on_delete=models.CASCADE, related_name='bookings')
    facilities = models.ManyToManyField(CampFacility, related_name='bookings', blank=True)
    number_of_persons = models.PositiveIntegerField()
    booking_date = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        # Calculate total price dynamically
        facilities_price = sum(facility.price_per_item for facility in self.facilities.all())
        return self.package.price * self.number_of_persons + facilities_price


class Payment(models.Model):
    booking = models.OneToOneField('Booking', on_delete=models.CASCADE, related_name='payment')
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending')


class Feedback(models.Model):
    camp = models.ForeignKey('Camp.Camp', on_delete=models.CASCADE, related_name='feedbacks')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
