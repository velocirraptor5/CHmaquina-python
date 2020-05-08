from django.http import HttpResponse 
from django.template import Template, Context
from django.template.loader import get_template
from django.shortcuts import render
from django.views.generic.edit import UpdateView, CreateView
from django.urls import reverse_lazy
from .models import Archivo
from .comprobar import sintax

#__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
""" 
def saludo(request):
    nombre= "Luis Eduardo"
    apellido= "Ocampo Wilches"
    numero= "3002354040"
    correo= "locampow@unal.edu.co"
    #doc_externo = open(os.path.join(__location__, 'plantillas/miplantilla.html'))
    #plt= Template(doc_externo.read())
    #doc_externo.close()

    #doc_externo= get_template('miplantilla.html')

    #ctx=Context({"nombre_pesona":nombre,"apellido_persona":apellido})
    
    #documento= doc_externo.render({"nombre_pesona":nombre,"apellido_persona":apellido})

    #return HttpResponse(documento)
    persona= {"nombre_pesona":nombre,
            "apellido_persona":apellido,
            "numero_persona":numero,
            "correo_persona":correo}
    return render(request,"core/miplantilla.html",persona)

def cursoCfunc(request):
    fecha_actual=datetime.datetime.now()
    return render(request,"core/CursoC.html",{"dameFecha":fecha_actual})

def basefunc(request):
    return render(request,"core/base.html")


"""
class VistaPrincipal(CreateView):
    #form_class = ArchivoForm
    #model = ArchivosCh se cambió el modelo para poder recuperar la memoria y el kernel
    model = Archivo
    fields = ['archivo', 'memoria','kernel']
    

    success_url= reverse_lazy('home')
    template_name = "core/base.html" #### puede dar error
    
    
    def get(self, request, *args, **kwargs):
        elementos = Archivo.objects.all()
        nombre="nombre pred"
        elemento = list(elementos)[-1]
        memoria= elemento.memoria
        kernel = elemento.kernel
        try:
            nombre = list((str(elemento.archivo).split('/')))[1]    
        except:
            nombre = "ERROR"
         

        """
        for elemento in elementos:
            memorias= elemento.memoria # aquí se toman las cantidades de memoria guardadas en la bd
            kernels=elemento.kernel # aquí se toman las cantidades de kernel guardadas en la bd
            nombre = (str(parte.archivo).split('/'))[1]
            memoriaFinal=int(memorias) # con esto sabemos cuanto es la memoria final entregado por el usuario
            kernelFinal=int(kernels) # con esto sabemos cuanto es el kernel final entregado por el usuario
        """
        
        MemoriaLibre = int(memoria) - int(kernel) -1 # aquí se verifica cuanta memoria disponible hay (kernel - acumulador - total memoria)
        Kernels=[] # se utilizan listas para mostrar las posiciones de memoria en el kernel 
        Memorias=[] # se utulizan listas para mostrar las posiciones de memoria disponible  
        
        for i in range (MemoriaLibre): #aqui se llena la lista con los valores de la posicion de memoria disponible
            Memorias.append(i+kernelFinal+1) 
        
        for i in range (kernelFinal): #aqui se llena la lista con los valores de la posicion de memoria que ocupa el kernel
            Kernels.append(i+1) 

        ###instancia= sintax() # se crea una instancia de la clase sintax para poder llamar el método que prueba toda la sintaxis de un archivo .ch
        #print(sintax.abrirArchivo(self))    
        return render(request, self.template_name,{'sintax':instancia.pruebaTotal(),'nombre':nombre,'memoriaLibre': Memorias, 'kernel': Kernels}) # })#,
        ###
        #'sintax':instancia.abrirArchivo()

    """
    def get_object(self, queryset=None):
        return get_object_or_404(ArchivosCh)
    """
    
    def get_object(self, queryset=None):
        #recuperar el objeto que se va a editar
        #profile, created= ArchivosCh.objects.get_or_create()
        profile, created= Archivo.objects.get_or_create()
        return profile      
