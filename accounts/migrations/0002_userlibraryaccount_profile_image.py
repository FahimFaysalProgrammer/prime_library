# Generated by Django 5.0.1 on 2024-01-31 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userlibraryaccount',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='accounts/media/uploads/'),
        ),
    ]