from django.db import models

# Create your models here.

class Archivo(models.Model):
    descripcion = models.TextField()
    imagen= models.ImageField()
    class Meta:
        verbose_name="proyecto"
        verbose_name_plural="proyectos"
    