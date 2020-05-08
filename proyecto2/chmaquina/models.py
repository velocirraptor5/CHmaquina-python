from django.db import models

# Create your models here.
"""
class Project(models.Model):
    descripcion = models.TextField()
    imagen= models.ImageField()
    class Meta:
        verbose_name="proyecto"
        verbose_name_plural="proyectos"
"""
class Archivo(models.Model):
    
    archivo = models.FileField(upload_to='bodega/', null=True, blank =True)
    memoria = models.IntegerField(null=True, blank =True)
    kernel = models.IntegerField(null=True, blank =True)