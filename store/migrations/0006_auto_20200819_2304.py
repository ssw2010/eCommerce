# Generated by Django 3.1 on 2020-08-19 23:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_auto_20200819_2236'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='Special_Features',
            new_name='Special_Feature',
        ),
    ]
