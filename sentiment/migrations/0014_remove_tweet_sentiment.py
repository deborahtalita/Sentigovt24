# Generated by Django 4.2 on 2023-05-09 00:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sentiment', '0013_tweet_text_preprocessed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tweet',
            name='sentiment',
        ),
    ]