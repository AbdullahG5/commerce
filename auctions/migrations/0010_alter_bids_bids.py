# Generated by Django 4.2.3 on 2023-09-13 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_bids_bids_bids_users_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bids',
            name='bids',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
