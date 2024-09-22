# Generated by Django 5.0.4 on 2024-08-31 13:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0003_remove_booking_total_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_status', models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending', max_length=50)),
                ('booking', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='User.booking')),
            ],
        ),
    ]
