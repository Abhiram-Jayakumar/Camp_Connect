# Generated by Django 5.0.4 on 2024-08-30 16:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Camp', '0010_camppackage_images'),
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_persons', models.PositiveIntegerField()),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('booking_date', models.DateTimeField(auto_now_add=True)),
                ('facilities', models.ManyToManyField(blank=True, related_name='bookings', to='Camp.campfacility')),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='Camp.camppackage')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='User.user')),
            ],
        ),
    ]
