from django.db import models

# Create your models here.
class Bacapres(models.Model):
    name = models.CharField(default=None, max_length=50)
    desc = models.CharField(default=None, null=True)
    keyword = models.CharField(default=None,max_length=50)
    avatar = models.ImageField(default='default.jpg', upload_to='bacapres_pics/')