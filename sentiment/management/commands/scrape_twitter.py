from django.core.management.base import BaseCommand
import time
import datetime
import pytz
import snscrape.modules.twitter as sntwitter
from sentiment.models import Tweet
from bacapres.models import Bacapres

# class Command(BaseCommand):
#     help = 'Scrape data from Twitter'

#     def handle(self, *args, **options):
#         bacapres = Bacapres.objects.all()
#         i = 1