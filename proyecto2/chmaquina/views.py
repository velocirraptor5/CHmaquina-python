from django.http import HttpResponse 
from django.template import Template, Context
from django.template.loader import get_template
from django.shortcuts import render
from django.views.generic.edit import UpdateView, CreateView
from django.core.files import File
from django.urls import reverse_lazy
from .models import Archivo,Kernel
from .verSintax import sintax
from .ejecucion import ejecutar
from django.urls import path
from django.shortcuts import redirect
import numpy as np
import sqlite3
from sqlite3 import Error
from django.db import connection


class VistaPrincipal(CreateView):
    model = Archivo
    model2=  Kernel
    fields = ['archivo', 'memoria','kernel']
    fields2=['memoK','kerK']
    

    success_url= reverse_lazy('home')
    template_name = "core/base.html" 
    def __init__(self):
        self.Errores=[]
        self.nombres=[]
        self.kernel=9
        self.memoria=100
        self.nombreArch="Luis Eduardo O"
        self.arch=""
        self.acumulador="Por:"
        self.pc="Cod= 0917524"
        self.OK=True
        self.modoKernel=False
    def get(self, request, *args, **kwargs):
        elementos = Archivo.objects.all()
        if list(elementos)==[]:
            self.Errores.append("Bienvenido a CH maquina")
            self.modoKernel=True
            W=self.paraFront()
            return  render(request, self.template_name,W)
            #return redirect('memoria')
        #ya se subio algun elemento a la base de datos
        memoria= elementos[0].memoria
        kernel = elementos[0].kernel
        #con prueba de que memoria y kernel sean numeros
        try:
            self.memoria= int(memoria) 
            self.kernel= int(kernel) 
        except:
            try:
                elementoK = Kernel.objects.all()
                elemK = list(elementoK)[-1]
                self.memoria=int(elemK.memoK)
                self.kernel=int(elemK.kerK)
            except:
                self.Errores.append("no fue capa de sacar el kernel")
                self.Errores.append("Error en la difinicion de la memoria y/o el kernel se asignan los valores defecto")
                W=self.paraFront()
                return render(request, self.template_name,W)
        # aquí se verifica cuanta memoria disponible hay (kernel - acumulador - total memoria)
        if not (self.kernel<self.memoria):
            self.Errores.append("la cantidad de memoria es insuficiente se le agregara memoria")
            self.memoria=self.kernel+3 

        for elemento in elementos:
            try:
                self.nombreArch = list((str(elemento.archivo).split('/')))[1]    
                self.nombres.append(self.nombreArch)
            except:
                self.nombreArch = "ERROR"
                self.Errores.append("Error en la busqueda del archivo")
                W=self.paraFront()
                return render(request, self.template_name,W) 
        
            #se verifica que el archivo sea legible
            ok=self.leerch()
            if not ok:
                W=self.paraFront()
                return render(request, self.template_name,W) 

            # una vez cargado el archivo se verifica si la Sintaxis esta bien
            sixCH=sintax(self.arch)
            self.arch=sixCH.ch
            if sixCH.OK:
                self.OK=self.OK and True
                self.Errores.append("*****No hay errores de compilacion*****")
                self.Errores.append("***** en el archivo "+str(self.nombreArch)+"*****") 
            else:
                self.OK=False
                self.Errores.append("*****Se encontraron errores en el archivo:*****")
                self.Errores.append("*****"+str(self.nombreArch)+"*****")
                self.Errores.extend(sixCH.errors)
                W=self.paraFront()
                return render(request, self.template_name,W)

        W=self.paraFront()
        return render(request, self.template_name,W)

    def paraFront(self):
        numKernels=[]
        numMemorias=[]
        
        numKernels.extend(range(1,self.kernel+1))
        numMemorias.extend(range(self.kernel+1, self.memoria))
        
        return  {
                'memoria':self.memoria,
                'kernel':self.kernel,
                'errores':self.Errores,
                'nombre':self.nombreArch,
                'MemoriaLibre': numMemorias, 
                'numKernels': numKernels,
                'pc':self.pc,
                'acumulador':self.acumulador,
                'modoKernel':self.modoKernel
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
            if chEjec.noAcabe:
                pass
            else:
                pass
        else:
            self.Errores.append("no se puede ejecutar tiene errores de ejecucion")
            return render(request, self.template_name,self.paraFront())
        
        return render(request, self.template_name,self.paraFrontEje(chEjec))
    
    def paraFrontEje(self,chEjec):
        resp=super().paraFront()
        resp['acumulador']=self.acumulador
        resp['pc']=self.pc
        numMemorias=[]
        numMemorias.extend(range(self.kernel+1+chEjec.posMem, self.memoria))
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
        resp['Pantalla']=chEjec.mostrar
        resp['Impresora']=chEjec.imprimir
        return resp


class vistaMemoria(CreateView):
    model = Kernel
    fields = ['memoK','kerK']
    success_url= reverse_lazy('memoria')
    template_name = "core/base.html" 
    def __init__(self):
        self.memoria=100
        self.kernel=9
        self.nombreArch="Luis Eduardo O"
        self.modoKernel=True
        self.Errores=["Bienvenido a CH maquina"]
        self.acumulador="Por:"
        self.pc="Cod= 0917524"

    def get(self, request, *args, **kwargs):
        elementoK = Kernel.objects.all()
        try:
            elemK = list(elementoK)[-1]
            self.memoria=int(elemK.memoK)
            self.kernel=int(elemK.kerK)
        except:
            self.Errores.append("no fue capa de sacar el kernel")
        w=self.paraFrontMem()
        return render(request, self.template_name,w)

    def get_object(self, queryset=None):
        profile, created= Kernel.objects.get_or_create()
        return profile 

    def paraFrontMem(self):
        numKernels=[]
        numMemorias=[]
        
        numKernels.extend(range(1,self.kernel+1))
        numMemorias.extend(range(self.kernel+1, self.memoria))
        
        return  {
                'memoria':self.memoria,
                'kernel':self.kernel,
                'errores':self.Errores,
                'nombre':self.nombreArch,
                'MemoriaLibre': numMemorias, 
                'numKernels': numKernels,
                'modoKernel':self.modoKernel,
                'pc':self.pc,
                'acumulador':self.acumulador
                }

class Salir(VistaPrincipal):
    def __init__(self):
        super().__init__()

    def get(self, request, *args, **kwargs):
        #database = r"C:\sqlite\db\pythonsqlite.db"

        # create a database connection
        with connection.cursor() as conn:
            conn.execute("DELETE FROM 'chmaquina_Kernel'")
            conn.execute("DELETE FROM 'chmaquina_archivo'")
            return redirect('home')