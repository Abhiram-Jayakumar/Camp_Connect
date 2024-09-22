from django.db import models

# Create your models here for ADMIN.

class Admintable(models.Model):
    email = models.EmailField(unique=True)
    password=models.CharField(max_length=50)


class Complaint(models.Model):
    COMPLAINT_TYPE_CHOICES = [
        ('User', 'User'),
        ('Camp', 'Camp'),
    ]

    complainant_type = models.CharField(max_length=10, choices=COMPLAINT_TYPE_CHOICES)
    complainant_id = models.IntegerField()  # User or Camp ID
    subject = models.CharField(max_length=200)
    message = models.TextField()
    date_submitted = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)