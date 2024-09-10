from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from enum import Enum

class user(AbstractUser):
    
    name = models.CharField(max_length=20)
    phone = models.CharField(max_length=10)
    credits = models.IntegerField(default=0)
    
    def increment_credits(self):
        #adding a single credit for one object
        self.credits+=1
        self.save()
        
    def increment_credits(self, nobj):
        #adding multiple credits for multiple objects
        self.credits += nobj
        self.save()
    
    def decrement_credits(self, amt):
        #withdrawing a certain amount of  credits
        self.credits = self.credits - amt
        self.save()
        
class wasteType(Enum):
    PLASTIC = 'Plastic'
    METAL = 'Metal'
    GLASS = 'Glass'
    PAPER = 'Paper'
    
    @classmethod
    def choices(cls):
        return [(key.name, key.value) for key in cls]
            
        
class Waste(models.Model):
    waste_type = models.CharField(max_length=100, choices = wasteType.choices())
    #created_at = models.DateTimeField(auto_now_add=True)
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


class Order(models.Model):
    company = models.ForeignKey(user, on_delete=models.CASCADE, limit_choices_to={'is_staff': True})
    waste_type = models.ForeignKey(Waste, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=(('Placed', 'Placed'), ('Cancelled', 'Cancelled')))

    def place_order(self):
        if self.waste_type.count >= self.quantity:
            self.waste_type.decrement_count(self.quantity)
            self.status = 'Placed'
            self.save()
        else:
            raise ValueError('Not enough waste available')

    def cancel_order(self):
        self.waste_type.increment_count(self.quantity)
        self.status = 'Cancelled'
        self.save()
