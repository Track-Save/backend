# Generated by Django 5.2.3 on 2025-07-10 22:30

from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_computer_api_compute_cpu_32933f_idx_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                CREATE INDEX product_search_idx
                ON api_product
                USING gin (to_tsvector('portuguese', name || ' ' || description));
            """,
            reverse_sql="DROP INDEX IF EXISTS product_search_idx;"
        ),
    ]
