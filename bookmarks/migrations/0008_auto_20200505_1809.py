# Generated by Django 3.0.5 on 2020-05-05 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookmarks', '0007_auto_20200505_1803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmark',
            name='selection',
            field=models.TextField(blank=True),
        ),
    ]