# Generated by Django 3.1.5 on 2021-01-31 09:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20210131_0947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='parent',
            field=models.ForeignKey(blank=True, default=0, on_delete=django.db.models.deletion.CASCADE, to='blog.tag'),
        ),
    ]