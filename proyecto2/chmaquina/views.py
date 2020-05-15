from django.http import HttpResponse 
from django.template import Template, Context
from django.template.loader import get_template
from django.shortcuts import render
from django.views.generic.edit import UpdateView, CreateView
from django.core.files import File
from django.urls import reverse_lazy
from .models import Archivo
from .verSintax import sintax
from .ejecucion import ejecutar
import numpy as np

class VistaPrincipal(CreateView):
    model = Archivo
    fields = ['archivo', 'memoria','kernel']
    

    success_url= reverse_lazy('home')
    template_name = "core/base.html" 
    def __init__(self):
        self.Errores=[]
        self.kernel=9
        self.memoria=100
        self.nombreArch="Luis Eduardo O"
        self.arch=""
        self.acumulador="Por:"
        self.pc="Cod= 0917524"
        self.OK=True
    def get(self, request, *args, **kwargs):
        elementos = Archivo.objects.all()
        
        try:
            #ya se subio algun elemento a la base de datos
            elemento = list(elementos)[-1]
            
        except:
            #no se ha cargado nada a la base de datos
            self.Errores.append("Bienvenido a CH maquina")
            W=self.paraFront()
            return  render(request, self.template_name,W) 
        
        memoria= elemento.memoria
        kernel = elemento.kernel
        #con prueba de que memoria y kernel sean numeros
        try:
            self.memoria= int(memoria) 
            self.kernel= int(kernel) 
        except:
            self.Errores.append("Error en la difinicion de la memoria y/o el kernel se asignan los valores defecto")
        

        if not (kernel<memoria):
            self.Errores.append("la cantidad de memoria es insuficiente se le agregara memoria")
            self.memoria=self.kernel+3 

         # aquí se verifica cuanta memoria disponible hay (kernel - acumulador - total memoria)
        try:
            self.nombreArch = list((str(elemento.archivo).split('/')))[1]    
        except:
            self.nombreArch = "ERROR"
            self.Errores.append("Error en la busqueda del archivo")
            W=self.paraFront()
            return render(request, self.template_name,W) 
        
        #se verifica que el archivo sea legible
        ok=self.leerch()
        if ok:
            pass
        else:
            W=self.paraFront()
            return render(request, self.template_name,W) 

        # una vez cargado el archivo se verifica si la Sintaxis esta bien
        sixCH=sintax(self.arch)
        self.arch=sixCH.ch
        if sixCH.OK:
            self.OK=True
            self.acumulador=0
            self.pc=0
            self.Errores.append("No hay errores de compilacion")
            W=self.paraFront()
            return render(request, self.template_name,W) 
        else:
            self.OK=False
            self.Errores.extend(sixCH.errors)
            W=self.paraFront()
            return render(request, self.template_name,W) 

    def paraFront(self):
        numKernels=[]
        numMemorias=[]
        
        numKernels.extend(range(1,self.kernel+1))
        numMemorias.extend(range(self.kernel+1, self.memoria+1))
        
        return  {
                'acumulador':self.acumulador,
                'pc':self.pc,
                'memoria':self.memoria,
                'kernel':self.kernel,
                'errores':self.Errores,
                'nombre':self.nombreArch,
                'MemoriaLibre': numMemorias, 
                'numKernels': numKernels
                }

    def get_object(self, queryset=None):
        profile, created= Archivo.objects.get_or_create()
        return profile  

    def leerch(self):
        ruta= "media/bodega/"+str(self.nombreArch)
        try:
            f = open(ruta, "r")
            myfile = File(f)
            ch = myfile.readlines() 
            f.close()
            self.arch=ch
            return True
        except :
            self.Errores.append("no se puede abrir el archivo porfavor verificar el formato")
            return False 

class vistaEjecucion(VistaPrincipal):
    def __init__(self):
        super().__init__()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        if self.OK:
            chEjec=ejecutar(self.arch,self.kernel,self.memoria)
            self.acumulador=chEjec.acumulador
            self.Errores.extend(chEjec.errors)
            return render(request, self.template_name,self.paraFrontEje(chEjec))
        else:
            self.Errores.append("no se puede ejecutar tiene errores de ejecucion")
            return render(request, self.template_name,self.paraFront())
       
    
    def paraFrontEje(self,chEjec):
        resp=super().paraFront()
        numMemorias=[]
        numMemorias.extend(range(self.kernel+1+chEjec.posMem, self.memoria+1))
        resp['MemoriaLibre']=numMemorias
        resp['Memoria']=enumerate(chEjec.Memoria,self.kernel+1)
        resp['Memoria2']=enumerate(chEjec.Memoria,self.kernel+1)
        aux=[]
        aux.append(chEjec.posVar)
        aux.append(chEjec.variables)
        aux=np.column_stack(aux)
        resp['Variables']=aux
        aux=[]
        aux.append(chEjec.posEt)
        aux.append(chEjec.etiquetas)
        aux=np.column_stack(aux)
        resp['Etiquetas']=aux
        resp['INS']=len(chEjec.arch)
        resp['RB']=self.kernel+1
        resp['RLC']=len(chEjec.arch)+self.kernel
        resp['RLP']=len(chEjec.Memoria)+self.kernel
        return resp
