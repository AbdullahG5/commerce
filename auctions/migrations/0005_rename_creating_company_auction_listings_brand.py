# Generated by Django 4.2.3 on 2023-09-07 00:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auction_listings_creating_company_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auction_listings',
            old_name='Creating_company',
            new_name='Brand',
        ),
    ]