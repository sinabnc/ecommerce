from django.db import models

# Create your models here.
class Product(models.Model):
    name=models.CharField(max_length=50)
    price=models.FloatField()
    image=models.ImageField(upload_to="media")
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.name
    

class Contact(models.Model):
    name=models.CharField(max_length=50)
    number=models.FloatField()
    email=models.EmailField(max_length=50)
    text=models.TextField(max_length=150)

    def __str__(self):
        return self.name
    
class Checkout(models.Model):
    name=models.CharField(max_length=50)
    number=models.IntegerField()
    email=models.EmailField(max_length=50)
    address=models.CharField(max_length=150)
    house=models.CharField(max_length=150)
    pin=models.FloatField()
    
    def __str__(self):
        return self.name
