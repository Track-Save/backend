# Generated by Django 5.1.9 on 2025-06-19 20:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_remove_user_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='specification',
            new_name='description',
        ),
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.CharField(default='Generic Brand', max_length=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('computer', 'Computer'), ('keyboard', 'Keyboard'), ('mouse', 'Mouse'), ('monitor', 'Monitor'), ('motherboard', 'Motherboard'), ('ram', 'Ram'), ('gpu', 'Gpu')], max_length=20),
        ),
        migrations.CreateModel(
            name='Computer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_notebook', models.BooleanField()),
                ('motherboard', models.CharField(max_length=100)),
                ('cpu', models.CharField(max_length=100)),
                ('ram', models.IntegerField()),
                ('storage', models.IntegerField()),
                ('gpu', models.CharField(max_length=100)),
                ('inches', models.FloatField()),
                ('panel_type', models.CharField(max_length=50)),
                ('resolution', models.CharField(max_length=50)),
                ('refresh_rate', models.CharField(max_length=50)),
                ('color_support', models.CharField(max_length=50)),
                ('output', models.CharField(max_length=50)),
                ('prod', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.product')),
            ],
        ),
        migrations.CreateModel(
            name='Cpu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=255)),
                ('integrated_video', models.CharField(max_length=255)),
                ('socket', models.CharField(max_length=255)),
                ('core_number', models.IntegerField()),
                ('thread_number', models.IntegerField()),
                ('frequency', models.FloatField()),
                ('mem_speed', models.FloatField()),
                ('prod', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.product')),
            ],
        ),
        migrations.CreateModel(
            name='Gpu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=255)),
                ('vram', models.IntegerField()),
                ('chipset', models.CharField(max_length=255)),
                ('max_resolution', models.CharField(max_length=255)),
                ('output', models.CharField(max_length=255)),
                ('tech_support', models.TextField()),
                ('prod', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.product')),
            ],
        ),
        migrations.CreateModel(
            name='Keyboard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=255)),
                ('key_type', models.CharField(max_length=255)),
                ('layout', models.CharField(max_length=255)),
                ('connectivity', models.CharField(max_length=255)),
                ('dimension', models.CharField(max_length=255)),
                ('prod', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.product')),
            ],
        ),
        migrations.CreateModel(
            name='Monitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=255)),
                ('inches', models.FloatField()),
                ('panel_type', models.CharField(max_length=255)),
                ('proportion', models.CharField(max_length=255)),
                ('resolution', models.CharField(max_length=255)),
                ('refresh_rate', models.CharField(max_length=255)),
                ('color_support', models.CharField(max_length=255)),
                ('output', models.CharField(max_length=255)),
                ('prod', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.product')),
            ],
        ),
        migrations.CreateModel(
            name='Mouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=255)),
                ('brand', models.CharField(max_length=255)),
                ('dpi', models.IntegerField()),
                ('connectivity', models.CharField(max_length=255)),
                ('color', models.CharField(max_length=255)),
                ('prod', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.product')),
            ],
        ),
        migrations.CreateModel(
            name='Ram',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=255)),
                ('model', models.CharField(max_length=255)),
                ('capacity', models.FloatField()),
                ('ddr', models.CharField(max_length=255)),
                ('speed', models.FloatField()),
                ('prod', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.product')),
            ],
        ),
        migrations.CreateModel(
            name='UserSpecification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpu', models.CharField(max_length=100)),
                ('ram', models.CharField(max_length=100)),
                ('motherboard', models.CharField(max_length=100)),
                ('cooler', models.CharField(max_length=100)),
                ('gpu', models.CharField(max_length=100)),
                ('storage', models.CharField(max_length=100)),
                ('psu', models.CharField(max_length=100)),
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
