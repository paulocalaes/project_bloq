# Generated by Django 3.2.25 on 2024-11-18 10:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('locker', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rent',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('weight', models.FloatField()),
                ('size', models.CharField(choices=[('XS', 'Extra Small'), ('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'Extra Large')], max_length=2)),
                ('status', models.CharField(choices=[('CREATED', 'Created'), ('WAITING_DROPOFF', 'Waiting Dropoff'), ('WAITING_PICKUP', 'Waiting Pickup'), ('DELIVERED', 'Delivered')], max_length=20)),
                ('locker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locker.locker')),
            ],
        ),
    ]
