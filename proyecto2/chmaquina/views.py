from django.http import HttpResponse 
from django.template import Template, Context
from django.template.loader import get_template
from django.shortcuts import render
from django.views.generic.edit import UpdateView, CreateView
from django.core.files import File
from django.urls import reverse_lazy
from .models import Archivo,Kernel,Lea,Paso, MetodoPlanificacion
from .verSintax import sintax
from .ejecucion import ejecutar,chEjecguardado
from django.urls import path
from django.shortcuts import redirect
import numpy as np
import sqlite3
from sqlite3 import Error
from django.db import connection
import os
import pickle
import copy
import random


class VistaPrincipal(CreateView):

    model = Archivo
    fields = ['archivo', 'memoria','kernel']
    model2=  Kernel
    model3 = Lea
    model4 = Paso
    model5 = MetodoPlanificacion

    fields2=['memoK','kerK']
    fields3 = ['lea']
    fields4 = ['paso']
    fields5 = ['metodo']
    success_url= reverse_lazy('home')
    template_name = "core/base.html" 
    def __init__(self,redirigido=False,w=0):
        self.Errores=[]
        self.nombres=[]
        self.kernel=9
        self.memoria=100
        self.nombreArch="Luis Eduardo O"
        self.ID=0
        self.arch=""
        self.acumulador="Por:"
        self.pc="Cod= 0917524"
        self.OK=True
        self.modoKernel=False
        self.INS=[]
        self.RB=[]
        self.RLC=[]
        self.RLP=[]
        self.Memoria=[]
        self.posMem=self.kernel+1
        self.Variables=[]
        self.posVars=[]
        self.Etiquetas=[]
        self.posEtis=[]
        self.mostrar=[]
        self.imprimir=[]
        self.IDs=[]
        self.guardado=False
        self.MetodoPlanificacion=""
        self.orden=[]
        self.almacen=[]

    def get(self, request,almacenar=False, *args, **kwargs):
        elementos = Archivo.objects.all()
        if list(elementos)==[]:
            self.Errores.append("Bienvenido a CH maquina")
            self.Errores.append("por:")
            self.Errores.append("Luis Eduardo Ocampo Wilches")
            self.Errores.append("cod:   0917524")
            self.Errores.append("CC:    1010111852")
            self.Errores.append("Agradecimientos a:")
            self.Errores.append("Hans Rivera")
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
                self.memoria=100
                self.kernel=9
                self.Errores.append("a la memoria y el kernel se asignan los valores defecto")
                self.Errores.append("Recuerda que para almacenar los datos de la memoria y kernel se debe precionar Mostrar Memoria")
        # aquí se verifica cuanta memoria disponible hay (kernel - acumulador - total memoria)
        if not (self.kernel<self.memoria):
            self.Errores.append("la cantidad de memoria es insuficiente se le agregara memoria")
            self.memoria=self.kernel+3 
        self.posMem=self.kernel+1
        self.acumulador=0
        for elemento in elementos:
            try:
                self.nombreArch = list((str(elemento.archivo).split('/')))[1]    
                self.nombres.append(self.nombreArch)
                self.IDs.append(self.ID)
                self.ID+=1
            except:
                self.nombreArch = "ERROR"
                self.Errores.append("Error en la busqueda del archivo")
                W=self.paraFront()
                return render(request, self.template_name,W) 

            #se verifica que el archivo sea legible
            ok=self.leerch()
            if not ok:
                #el leerch manda el mensaje de error a la pantalla
                W=self.paraFront()
                return render(request, self.template_name,W) 

            # una vez cargado el archivo se verifica si la Sintaxis esta bien
        try:
            self.MetodoPlanificacion=list(MetodoPlanificacion.objects.all())[-1].metodo
        except:
            with connection.cursor() as conn:
                conn.execute("INSERT INTO 'chmaquina_metodoplanificacion'  (id,metodo)  VALUES (1,'RR');")
            self.MetodoPlanificacion="Prioridad"
        
        self.ordenar()
        print(self.orden)
        for num in self.orden:    
            self.nombreArch=self.nombres[num]
            self.ID=self.IDs[num]
            self.leerch()
            sixCH=sintax(self.arch)
            self.arch=sixCH.ch
            if sixCH.OK:
                self.OK=self.OK and sixCH
                self.Errores.append("*****No hay errores de compilacion*****")
                self.Errores.append("***** en el archivo "+str(self.nombreArch)+"*****") 
            else:
                self.OK=False
                self.Errores.append("*****Se encontraron errores en el archivo:*****")
                self.Errores.append("*****"+str(self.nombreArch)+"*****")
                self.Errores.extend(sixCH.errors)
                """W=self.paraFront()
                return render(request, self.template_name,W)"""
            if self.OK:
                chEjec=ejecutar(self.arch,self.kernel,self.memoria,self.acumulador,self.ID,almacenar)
                if almacenar:
                    for ch in chEjec.almacen:
                        self.almacen.append(self.paraFrontporPaso(ch))
                self.pc=chEjec.linea
                self.acumulador=chEjec.acumulador
                self.Errores.extend(chEjec.errors)
                self.Memoria.extend(chEjec.Memoria)
                self.Variables.extend(chEjec.variables)
                self.posVars.extend(chEjec.posVar)
                self.Etiquetas.extend(chEjec.etiquetas)
                self.posEtis.extend(chEjec.posEt)
                self.INS.append(len(chEjec.arch))
                self.RB.append(self.posMem)
                self.RLC.append(len(chEjec.arch)+self.posMem)
                self.RLP.append(len(self.Memoria)+self.kernel)
                self.mostrar.extend(chEjec.mostrar)
                self.imprimir.extend(chEjec.imprimir)
                self.posMem+=chEjec.posMem
                if chEjec.noAcabe:
                    self.guardar(self.paraFrontEje())
                    self.guardado=True
                    W=self.paraFrontEjecNoFin(chEjec.varLeer)
                    return render(request,self.template_name,W)
            else:
                self.Errores.append("no se puede ejecutar "+str(self.nombreArch) + " tiene errores de ejecucion")
                return render(request, self.template_name,self.paraFront())
        W=self.paraFrontEje()
        return render(request, self.template_name,W)

    def paraFront(self):
        numKernels=[]
        numMemorias=[]
        
        numKernels.extend(range(1,self.kernel+1))
        numMemorias.extend(range(self.posMem, self.memoria))
        try:
            plan=list(MetodoPlanificacion.objects.all())[-1].metodo
            boolPlanificacion=False
        except :
            plan="RR"
            boolPlanificacion=True
        
        return  {
                'memoria':self.memoria,
                'kernel':self.kernel,
                'errores':self.Errores,
                'nombre':self.nombreArch,
                'MemoriaLibre': numMemorias, 
                'numKernels': numKernels,
                'pc':self.pc,
                'acumulador':self.acumulador,
                'modoKernel':self.modoKernel,
                'Memoria':enumerate(self.Memoria,self.kernel+1),
                'Memoria2':enumerate(self.Memoria,self.kernel+1),
                'MetodoPlanificacion': boolPlanificacion,
                'plan':plan
                }

    def paraFrontEje(self):
        
        resp=self.paraFront()
        variables=[]
        variables.append(self.posVars)
        variables.append(self.Variables)
        variables=np.column_stack(variables)
        resp['Variables']=variables
        
        etiquetas=[]
        etiquetas.append(self.posEtis)
        etiquetas.append(self.Etiquetas)
        etiquetas=np.column_stack(etiquetas)
        resp['Etiquetas']=etiquetas
        
        programas=[]
        programas.append(self.IDs)
        programas.append(self.nombres)
        programas.append(self.INS)
        programas.append(self.RB)
        programas.append(self.RLC)
        programas.append(self.RLP)
        programas=np.column_stack(programas)
        resp['Programas']=programas
        resp['noPantalla']=self.mostrar
        resp['noImpresora']=self.imprimir
        return resp
    
    def paraFrontEjecNoFin(self,lea):
        resp=self.paraFrontEje()
        resp['ModalActivado']=True
        resp['lea']=lea
        return resp
    
    def paraFrontporPaso(self,chEjec):
        errores=self.Errores.copy()
        errores.extend(chEjec.errors)
        copMemoria=self.Memoria.copy()
        copMemoria.extend(chEjec.Memoria)
        copVariables=self.Variables.copy()
        copVariables.extend(chEjec.variables)
        copposVar=self.posVars.copy()
        copposVar.extend(chEjec.posVar)
        copEtiquetas=self.Etiquetas.copy()
        copEtiquetas.extend(chEjec.etiquetas)
        copposEtis=self.posEtis.copy()
        copposEtis.extend(chEjec.posEt)
        copINS=self.INS.copy()
        copINS.append(len(self.arch))
        copRB=self.RB.copy()
        copRB.append(self.posMem)
        copRLC=self.RLC.copy()
        copRLC.append(len(self.arch)+self.posMem)
        copRLP=self.RLP.copy()
        copRLP.append(len(self.Memoria)+self.kernel)
        copmostrar=self.mostrar.copy()
        copmostrar.extend(chEjec.mostrar)
        copimprimir=self.imprimir.copy()
        copimprimir.extend(chEjec.imprimir)
        copposMem=self.posMem
        copposMem+=chEjec.posMem

        numKernels=[]
        numMemorias=[]
        
        numKernels.extend(range(1,self.kernel+1))
        numMemorias.extend(range(copposMem, self.memoria))
        variables=[]
        variables.append(copposVar)
        variables.append(copVariables)
        variables=np.column_stack(variables)
        
        etiquetas=[]
        etiquetas.append(copposEtis)
        etiquetas.append(copEtiquetas)
        etiquetas=np.column_stack(etiquetas)
        
        programas=[]
        programas.append(self.IDs)
        programas.append(self.nombres)
        programas.append(copINS)
        programas.append(copRB)
        programas.append(copRLC)
        programas.append(copRLP)
        programas=np.column_stack(programas)
        
        return  {
                'memoria':self.memoria,
                'kernel':self.kernel,
                'errores':errores,
                'nombre':self.nombreArch,
                'MemoriaLibre': numMemorias, 
                'numKernels': numKernels,
                'pc':chEjec.linea,
                'acumulador':chEjec.acumulador,
                'modoKernel':self.modoKernel,
                'Memoria':enumerate(copMemoria,self.kernel+1),
                'Memoria2':enumerate(copMemoria,self.kernel+1),
                'Variables':variables,
                'Etiquetas':etiquetas,
                'Programas':programas,
                'Pantalla':copmostrar,
                'Impresora':copimprimir
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
    
    def guardar(self,resp,extra=""):
        with open('media/bodega/chEjeRESP'+str(extra)+'.pkl','wb') as output:
            pickle.dump(resp,output,pickle.HIGHEST_PROTOCOL)

    def ordenar(self):
        if self.MetodoPlanificacion=="FCFS":
            self.orden= range(len(self.nombres))
        
        if self.MetodoPlanificacion=="SJF":
            menor=[]
            ids=[]
            i=0
            for nombre in self.nombres:
                self.nombreArch=nombre
                self.leerch()
                bandera= False
                if nombre==self.nombres[0]:
                    menor.append(len(self.arch))
                    ids.append(0)
                else:
                    for longitud in menor:
                        if len(self.arch)<longitud:
                            i+=1
                            num=menor.index(longitud)
                            menor.insert(num,len(self.arch))
                            ids.insert(num,i)
                            bandera=True
                            break
                    if not bandera:
                        i+=1
                        menor.append(len(self.arch))
                        ids.append(i)
            self.orden=ids
        
        if self.MetodoPlanificacion=="Prioridad":
            mayor=[]
            ids=[]
            i=0
            for nombre in self.nombres:
                self.nombreArch=nombre
                self.leerch()
                bandera= False
                if nombre==self.nombres[0]:
                    mayor.append(random.randint(1,101))
                    ids.append(0)
                else:
                    for prio in mayor:
                        ran= random.randint(1,101)
                        if ran>prio:
                            i+=1
                            num=mayor.index(prio)
                            mayor.insert(num,ran)
                            ids.insert(num,i)
                            bandera=True
                            break
                    if not bandera:
                        i+=1
                        mayor.append(ran)
                        ids.append(i)
            self.orden=ids
            
            if self.MetodoPlanificacion=="" or self.MetodoPlanificacion=="RR" :
                print("hola")


        
        
class vistaMetodoPlan(CreateView):
    model=MetodoPlanificacion
    fields=['metodo']
    template_name = "core/base.html" 
    success_url= reverse_lazy('home')

    def __init__(self):
        self.vista=VistaPrincipal()
    
    def get(self, request,almacenar=False, *args, **kwargs):

        self.vista.Errores.append("Porfavor selecciones un metodo de planeacion")
        self.vista.Errores.append("de lo contrario se asignara Round Robin")
        plan=list(MetodoPlanificacion.objects.all())
        try:
            metodo=plan[-1].metodo
        except:
            metodo="RR"

        self.vista.MetodoPlanificacion=metodo
        self.vista.modoKernel=True
        W=self.vista.paraFront()
        return render(request,self.template_name,W)
      
class vistaEjecucion(VistaPrincipal):
    def __init__(self):
        super().__init__()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        if not self.guardado:
            if not self.OK:
                self.Errores.append("no se puede ejecutar"+str(self.nombreArch) + "tiene errores de ejecucion")
                return render(request, self.template_name,self.paraFront())
            return render(request, self.template_name,self.paraFrontEje2())
        if self.guardado:
            visSave=chEjecguardado("RESPEJEC")
            W=self.paraFrontTerminar(visSave)
            return render(request,self.template_name,W)

    def paraFrontEje2(self):
        resp=super().paraFrontEje()
        resp['Pantalla']=self.mostrar
        resp['Impresora']=self.imprimir
        return resp
    def paraFrontTerminar(self,resp):
        resp['Pantalla']=resp['noPantalla']
        resp['Impresora']=resp['noImpresora']
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
        carpeta="media/bodega"
        for archivo in os.listdir(carpeta):
            os.remove(carpeta+'/'+archivo)
        
        with connection.cursor() as conn:
            conn.execute("DELETE FROM 'chmaquina_Kernel'")
            conn.execute("DELETE FROM 'chmaquina_archivo'")
            conn.execute("DELETE FROM 'chmaquina_lea'")
            conn.execute("DELETE FROM 'chmaquina_paso'")
            conn.execute("DELETE FROM 'chmaquina_metodoplanificacion'")
            return redirect('obtenerPlan')


class terminarEjec(VistaPrincipal):
    model = Lea
    fields = ['lea']
    success_url= reverse_lazy('lea')
    template_name = "core/base.html" 
    def __init__(self):
        super().__init__()
    
    def get(self, request, *args, **kwargs):
        visSave=chEjecguardado("RESP")
        self.actualizar(visSave)
        chEjec=chEjecguardado()
        DBlea=Lea.objects.all()
        valLea=list(DBlea)[-1]
        
        tempErr=[err for err in self.Errores if err not in chEjec.errors]
        self.Errores=tempErr
        chMemo=[]
        for chmem in chEjec.Memoria:
            chMemo.append(str(chmem))
        tempMem=[mem for mem in self.Memoria if mem not in chMemo]
        self.Memoria=tempMem
        tempVar=[var for var in self.Variables if var not in chEjec.variables]
        self.Variables=tempVar
        temposVar=[posVar for posVar in self.posVars if posVar not in chEjec.posVar]
        self.posVars=temposVar
        tempEtis=[eti for eti in self.Etiquetas if eti not in chEjec.etiquetas]
        self.Etiquetas=tempEtis
        tempposEti=[posEti for posEti in self.posEtis if posEti not in chEjec.posEt]
        self.posEtis=tempposEti
        tempmos=[mos for mos in self.mostrar if mos not in chEjec.mostrar]
        self.mostrar=tempmos
        tempimp=[imp for imp in self.imprimir if imp not in chEjec.imprimir]
        self.imprimir=tempimp
        self.posMem-=chEjec.posMem

        linea=chEjec.linea.split()
        chEjec.almacene(linea,valLea.lea)
        chEjec.noAcabe=False
        chEjec.lineaAlinea()
        self.pc=chEjec.linea
        self.acumulador=chEjec.acumulador
        self.Errores.extend(chEjec.errors)
        self.Memoria.extend(chEjec.Memoria)
        self.Variables.extend(chEjec.variables)
        self.posVars.extend(chEjec.posVar)
        self.Etiquetas.extend(chEjec.etiquetas)
        self.posEtis.extend(chEjec.posEt)
        self.mostrar.extend(chEjec.mostrar)
        self.imprimir.extend(chEjec.imprimir)
        self.posMem+=chEjec.posMem
        VP= VistaPrincipal()
        VP=self
        if chEjec.noAcabe:
            W=VP.paraFrontEjecNoFin(chEjec.varLeer)
            return render(request,self.template_name,W)
        W=VP.paraFrontEje()
        VP.guardar(W,"EJEC")
        return render(request,self.template_name,W)
    
    def actualizar(self,resp):
        self.memoria=resp['memoria']
        self.kernel=resp['kernel']
        self.Errores=resp['errores']
        self.nombreArch=resp['nombre']
        self.posMem=resp['MemoriaLibre'][0] 
        self.pc=resp['pc']
        self.acumulador=resp['acumulador']
        self.modoKernel=resp['modoKernel']
        temp=resp['Memoria']
        for num,mem in temp:
            self.Memoria.append(mem)
        
        for posVar,Var in resp['Variables']:
            self.posVars.append(int(posVar))
            self.Variables.append(Var)
        
        for posET,Eti in resp['Etiquetas']:
            self.posEtis.append(int(posET))
            self.Etiquetas.append(Eti)
        
        for ID,Nom,ins,rb,rlc,rlp in resp['Programas']:
            self.IDs.append(ID)
            self.nombres.append(Nom)
            self.INS.append(ins)
            self.RB.append(rb)
            self.RLC.append(rlc)
            self.RLP.append(rlp)

class PasoAPaso(VistaPrincipal):
    model=Paso
    fields=['paso']
    success_url= reverse_lazy('pap')
    template_name = "core/base.html" 
    def __init__(self):
        super().__init__()
        self.paso=0

    def get(self, request, *args, **kwargs):
        super().get(request,True, *args, **kwargs)
        if not self.OK:
            self.Errores.append("no se puede ejecutar"+str(self.nombreArch) + "tiene errores de ejecucion")
            return render(request, self.template_name,self.paraFront())
        DBpasos=Paso.objects.all()
        DBpasos=list(DBpasos)
        if(DBpasos==[]):
            return render(request, self.template_name,self.paraFrontPaP(self.almacen[0]))
        else:
            self.paso=(DBpasos[-1]).paso
            if self.paso<len(self.almacen):
                return render(request, self.template_name,self.paraFrontPaP(self.almacen[self.paso]))
            else:
                self.mostrar.append("Acabo el paso a paso")
                return render(request, self.template_name,self.paraFrontEje())
    def paraFrontPaP(self,resp):
        resp['PaP']=True
        resp['paso']=self.paso+1
        return resp