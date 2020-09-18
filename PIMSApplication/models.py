from django.db import models

class Article(models.Model):
    SKU = models.IntegerField(blank=False,default='0')
    EAN = models.IntegerField(blank=False,default='0')
    Name = models.JSONField(blank=False,default=dict)
    Stock_quantity = models.IntegerField(blank=False,default='0')
    price = models.IntegerField(blank=False,default='-1')
    active = models.BooleanField(blank=False,default='false')

class User(models.Model):
    username = models.CharField(max_length=70, blank=False, default='')
    active = models.BooleanField(blank=False,default='false')
