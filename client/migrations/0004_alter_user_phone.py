# Generated by Django 4.0.4 on 2022-12-10 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_user_company_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=13, null=True, unique=True),
        ),
    ]
