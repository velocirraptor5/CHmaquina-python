from django.db import models
from django.forms import ModelForm

# Create your models here.

class Archivo(models.Model):
    
    archivo = models.FileField(upload_to='bodega/', null=True, blank =True)
    memoria = models.IntegerField(null=True, blank =True)
    kernel = models.IntegerField(null=True, blank =True)

class Kernel(models.Model):
    memoK = models.IntegerField(null=True, blank =True)
    kerK = models.IntegerField(null=True, blank =True)

class Lea(models.Model):
    lea = models.TextField(null=True,blank=True)

class Paso(models.Model):
    paso=models.IntegerField(null=True,blank=True)

class MetodoPlanificacion(models.Model):
    metodo=models.TextField(null=True,blank=True)
    




