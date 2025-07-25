# Generated by Django 5.2.3 on 2025-07-06 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_alter_storage_read_speed_alter_storage_write_speed_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='computer',
            name='inches',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='computer',
            name='ram',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='computer',
            name='storage',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='cpu',
            name='core_number',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='cpu',
            name='frequency',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='cpu',
            name='mem_speed',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='cpu',
            name='thread_number',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='gpu',
            name='vram',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='monitor',
            name='inches',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='motherboard',
            name='m2_slot',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='motherboard',
            name='max_ram_capacity',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='motherboard',
            name='pcie_slots',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='motherboard',
            name='ram_slots',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='motherboard',
            name='sata_ports',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='mouse',
            name='dpi',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='ram',
            name='capacity',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='ram',
            name='speed',
            field=models.CharField(max_length=255),
        ),
    ]
