# Generated by Django 5.1.2 on 2024-10-29 16:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('concert', '0002_alter_concert_price'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='concert',
            name='seats',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_seats', models.PositiveIntegerField()),
                ('concert', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='concert.concert')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
