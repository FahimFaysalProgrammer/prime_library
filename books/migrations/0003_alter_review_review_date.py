# Generated by Django 5.0.1 on 2024-01-30 09:58

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_alter_review_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='review_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
