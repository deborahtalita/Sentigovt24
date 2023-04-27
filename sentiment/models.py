from django.db import models

class Tweet(models.Model):
    # id = models.AutoField()
    tweet_id = models.TextField(default=None)
    text = models.TextField(default=None)
    user_name = models.TextField(default=None)
    created_at = models.TextField(default=None)
    # text_preprocessed
    sentiment = models.TextField(default=None)

class Bacapres(models.Model):
    name = models.TextField(default=None)
    keyword = models.TextField(default=None)
    desc = models.TextField(default=None)