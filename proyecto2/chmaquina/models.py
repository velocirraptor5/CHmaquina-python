from django.db import models

# Create your models here.

class Archivo(models.Model):
    
    archivo = models.FileField(upload_to='bodega/', null=True, blank =True)
    memoria = models.IntegerField(null=True, blank =True)
    kernel = models.IntegerField(null=True, blank =True)

class Kernel(models.Model):
    memoK = models.IntegerField(null=True, blank =True)
    kerK = models.IntegerField(null=True, blank =True)
