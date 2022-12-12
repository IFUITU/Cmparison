# Generated by Django 4.0.4 on 2022-12-12 16:50

from django.db import migrations, models
import main.helpers


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_service'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='service',
            name='icon',
            field=models.ImageField(null=True, upload_to=main.helpers.upload_file_name),
        ),
    ]
