# Generated by Django 3.2.19 on 2023-05-24 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uaa', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='branch',
            name='email',
        ),
        migrations.AddField(
            model_name='branch',
            name='phoneNumber',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
