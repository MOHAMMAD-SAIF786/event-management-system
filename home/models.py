from django.db import models

# Create your models here.
class HomePage(models.Model):
    hero_title = models.CharField(max_length=200)
    hero_description = models.TextField()
    hero_image = models.ImageField(upload_to='home/hero/')

    def __str__(self):
        return "Homepage Hero"
    
class Feature(models.Model):
    icon = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title
    
class ContactInfo(models.Model):
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return "Contact Information"