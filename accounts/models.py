from django.db import models

from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    
    class Role(models.TextChoices):
        MEMBER = "MEMBER", 'Member'
        ADMIN = "ADMIN", 'Admin'
        SUPERADMIN = 'SUPERADMIN', 'Super Admin'
    
    base_role = Role.MEMBER

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50, choices=Role.choices)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def save(self, *arg, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*arg, **kwargs)
        
class Session(models.Model):
    id = models.CharField(primary_key=True)
    quota = models.IntegerField(default=3)