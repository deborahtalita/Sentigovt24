from django.db import models

class Tweet(models.Model):
    # id = models.AutoField()
    tweet_id = models.TextField(default=None)
    text = models.TextField(default=None)
    user_name = models.TextField(default=None)
    created_at = models.TextField(default=None)
    # text_preprocessed
    # sentiment
