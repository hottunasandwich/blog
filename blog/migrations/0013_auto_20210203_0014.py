# Generated by Django 3.1.5 on 2021-02-03 00:14

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20210202_2326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='img',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(location='/media/img'), upload_to=''),
        ),
    ]