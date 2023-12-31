# Generated by Django 4.2.1 on 2023-06-08 21:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('added_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('for_sale', models.BooleanField(default=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_property', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'properties',
            },
        ),
        migrations.CreateModel(
            name='PropertyPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_type', models.CharField(choices=[('Offers over', 'Offers over'), ('Fixed price', 'Fixed price')], default='Offers over', max_length=20)),
                ('price', models.BigIntegerField()),
                ('added_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('property', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='property_price', to='property.property')),
            ],
        ),
        migrations.CreateModel(
            name='PropertyImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='property/')),
                ('is_feature', models.BooleanField(default=False)),
                ('alt_text', models.CharField(max_length=100)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='property.property')),
            ],
        ),
        migrations.CreateModel(
            name='PropertyFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_type', models.CharField(choices=[('Detached', 'Detached'), ('Semi-detached', 'Semi-detached'), ('Flat', 'Flat'), ('Bangalow', 'Bangalow')], max_length=20)),
                ('bedroom', models.IntegerField()),
                ('toilet', models.IntegerField()),
                ('property', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='property_feature', to='property.property')),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line_1', models.CharField(max_length=120)),
                ('line_2', models.CharField(blank=True, max_length=120, null=True)),
                ('town', models.CharField(max_length=50)),
                ('region', models.CharField(blank=True, max_length=50, null=True)),
                ('postcode', models.CharField(max_length=10)),
                ('property', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='property_address', to='property.property')),
            ],
        ),
    ]
