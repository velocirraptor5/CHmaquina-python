from django.contrib import admin
from .models import Archivo,Kernel,Lea,Paso,MetodoPlanificacion

# Register your models here.
admin.site.register(Archivo)
admin.site.register(Kernel)
admin.site.register(Lea)
admin.site.register(Paso)
admin.site.register(MetodoPlanificacion)