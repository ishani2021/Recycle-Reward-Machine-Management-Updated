from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser

class user(AbstractUser):
    credits = models.IntegerField(default=0)
    def increment_credits(self):
        self.credits+=1
        self.save()
        
        
class Waste(models.Model):
    waste_type = models.CharField(max_length=100)
    count = models.IntegerField(default=0)

    def increment_count(self):
        self.count += 1
        self.save()

    def decrement_count(self, amount):
        self.count -= amount
        self.save()

class PlasticWaste(Waste):
    pass

class MetalWaste(Waste):
    pass

class PaperWaste(Waste):
    pass
