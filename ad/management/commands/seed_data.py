import json
from datetime import datetime
from django.core.management.base import BaseCommand
from campaign.models import FbCampaign
from ad.models import Ad


class Command(BaseCommand):
    help = 'Seed data into database'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str,
                            help='Path to the JSON file containing data')

    def handle(self, *args, **options):
        file_path = options['file_path']
        with open(file_path, 'r') as f:
            json_data = json.load(f)

        for item in json_data:
            ad_id = item.get('ad_id')
            xyz_campaign_id = item.get('xyz_campaign_id')
            fb_campaign_id = item.get('fb_campaign_id')
            age = item.get('age')
            gender = item.get('gender')
            interest = item.get('interest')
            impressions = item.get('Impressions')
            clicks = item.get('Clicks')
            spent = item.get('Spent')
            total_conversion = item.get('Total_Conversion')
            approved_conversion = item.get('Approved_Conversion')
            start_date_str = item.get('Start Date')
            end_date_str = item.get('End Date')

            # Convert date strings to date objects
            start_date = datetime.strptime(start_date_str, '%d-%b-%y').date()
            end_date = datetime.strptime(end_date_str, '%d-%b-%y').date()

            # Get or create FbCampaign object using fb_campaign_id as primary key
            fb_campaign, created = FbCampaign.objects.get_or_create(
                id=fb_campaign_id,
                defaults={'start_date': start_date, 'end_date': end_date,
                          'xyz_campaign_id': xyz_campaign_id}
            )

            # Get or create Ad object using ad_id as primary key
            ad, created = Ad.objects.get_or_create(
                id=ad_id,
                defaults={
                    'fb_campaign': fb_campaign,
                    'age': age,
                    'gender': gender,
                    'interest': interest,
                    'impressions': impressions,
                    'clicks': clicks,
                    'spent': spent,
                    'total_conversion': total_conversion,
                    'approved_conversion': approved_conversion
                }
            )

        self.stdout.write(self.style.SUCCESS('Data seeding complete'))
