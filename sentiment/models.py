from django.db import models
from bacapres.models import Bacapres

class Tweet(models.Model):
    # id = models.AutoField()
    tweet_id = models.TextField(default=None)
    text = models.TextField(default=None)
    user_name = models.CharField(default=None)
    created_at = models.DateTimeField(default=None)
    text_preprocessed = models.TextField(default=None)
    sentiment = models.TextField(default=None)
    bacapres = models.IntegerField(default=None)

class History(models.Model):
    start_date = models.DateTimeField(default=None)
    end_date = models.DateTimeField(default=None)

    tweet = models.ManyToManyField(Tweet)
    bacapres = models.ManyToManyField(Bacapres)

# class Bacapres(models.Model):
#     name = models.CharField(default=None, max_length=50)
#     desc = models.CharField(default=None, null=True)
#     keyword = models.CharField(default=None,max_length=50)
#     avatar = models.ImageField(default='default.jpg', upload_to='bacapres_pics/')

# class BacapresKeyword(models.Model):
#     keyword = models.CharField(max_length=50)
#     bacapres = models.ForeignKey(Bacapres, on_delete=models.CASCADE)
