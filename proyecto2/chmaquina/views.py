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
        try:
            elemento = list(elementos)[-1]
            
        except:
            memoria =100
            kernel = 10
            nombre = "......"
            return  render(request, self.template_name,self.paraFront(memoria,kernel,nombre)) 
        
        
        
        memoria= elemento.memoria
        kernel = elemento.kernel

        try:
            memoria= int(memoria) 
            kernel= int(kernel) 
        except:
            kernel=3
            memoria=6
            Errores.append("Error en la difinicion de la memoria y/o el kernel")
            
        if not (kernel<memoria):
            Errores.append("la cantidad de memoria es insuficiente se le agregara memoria")
            memoria+=3 

        Errores.append("pruebas")
         # aquí se verifica cuanta memoria disponible hay (kernel - acumulador - total memoria)
        try:
            nombreArch = list((str(elemento.archivo).split('/')))[1]    
        except:
            nombreArch = "ERROR"
            Errores.append("Error en la busqueda del archivo")

        return render(request, self.template_name,self.paraFront(memoria,kernel,nombreArch,Errores)) 

    def paraFront(memoria,kernel,nombreArch,Errores=[]):
        Kernels=[]
        Memorias=[]
        
        Kernels.extend(range(1,kernel+1))
        Memorias.extend(range(kernel+1, memoria+1))
        
        return  {
                'memoria':memoria,
                'kernel':kernel,
                'errores':Errores,
                'nombre':nombreArch,
                'memoriaLibre': Memorias, 
                'Kernels': Kernels
                }

    def get_object(self, queryset=None):
        #recuperar el objeto que se va a editar
        #profile, created= ArchivosCh.objects.get_or_create()
        profile, created= Archivo.objects.get_or_create()
        return profile      

