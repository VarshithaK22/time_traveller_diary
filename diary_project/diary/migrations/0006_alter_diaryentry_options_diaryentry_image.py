# Generated by Django 5.1.2 on 2024-11-04 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0005_remove_diaryentry_year_in_period_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='diaryentry',
            options={'ordering': ['-updated_at', '-created_at']},
        ),
        migrations.AddField(
            model_name='diaryentry',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='adventure_images/'),
        ),
    ]
