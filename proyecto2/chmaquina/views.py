from django.http import HttpResponse 
from django.template import Template, Context
from django.template.loader import get_template
from django.shortcuts import render
from django.views.generic.edit import UpdateView, CreateView
from django.urls import reverse_lazy
from .models import Archivo
from .comprobar import sintax

class VistaPrincipal(CreateView):
    #form_class = ArchivoForm
    #model = ArchivosCh se cambió el modelo para poder recuperar la memoria y el kernel
    model = Archivo
    fields = ['archivo', 'memoria','kernel']
    

    success_url= reverse_lazy('home')
    template_name = "core/base.html" 
    
    
    def get(self, request, *args, **kwargs):
        Errores=[]
        elementos = Archivo.objects.all()
        nombre="nombre pred"
        elemento = list(elementos)[-1]
        memoria= elemento.memoria
        kernel = elemento.kernel
        try:
            nombre = list((str(elemento.archivo).split('/')))[1]    
        except:
            nombre = "ERROR"
            Errores.append("Error en la busqueda del archivo")
        
        try:
            MemoriaLibre = int(memoria) - int(kernel) -1
        except:
            MemoriaLibre=3
            kernel=3
            memoria=6
            Errores.append("Error en la difinicion de la memoria y/o el kernel")
            


        
         # aquí se verifica cuanta memoria disponible hay (kernel - acumulador - total memoria)
        Kernels=[] # se utilizan listas para mostrar las posiciones de memoria en el kernel 
        Memorias=[] # se utulizan listas para mostrar las posiciones de memoria disponible  
        


        Kernels.extend(range(1,kernel+1))
        Memorias.extend(range(kernel+1, memoria+1))

        return render(request, self.template_name,{'sintax':sintax(nombre).pruebaTotal(),'nombre':nombre,'memoriaLibre': Memorias, 'kernel': Kernels}) # })#,

    
    def get_object(self, queryset=None):
        #recuperar el objeto que se va a editar
        #profile, created= ArchivosCh.objects.get_or_create()
        profile, created= Archivo.objects.get_or_create()
        return profile      

