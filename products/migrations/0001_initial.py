# Generated by Django 5.1.2 on 2024-10-28 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField()),
                ('quantity', models.IntegerField()),
                ('category', models.CharField(choices=[('Foods', 'Foods'), ('Clothes', 'Clothes'), ('Electronics', 'Electronics'), ('Other', 'Other')], max_length=20)),
                ('out_of_stock', models.BooleanField(default=False)),
                ('image_url', models.URLField(blank=True, max_length=300, null=True)),
            ],
        ),
    ]
