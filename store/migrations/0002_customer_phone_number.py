# Generated by Django 3.1 on 2020-08-14 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='phone_number',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
