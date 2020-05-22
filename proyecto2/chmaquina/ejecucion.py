import copy
import pickle
class ejecutar:
    def __init__(self,arch,kernel,memoria,acumulador,ID,almacenar=False):
        self.arch = arch
        self.memoria=memoria
        self.kernel=kernel
        self.Memoria=[]
        self.posMem=0
        self.variables=[]
        self.tipoVar=[]
        self.posVar=[]
        self.etiquetas=[]
        self.posEt=[]
        self.acumulador=acumulador
        self.linea=""
        self.NumLin=0
        self.noAcabe=False
        self.imprimir=[]
        self.mostrar=[]
        self.errors=[]
        self.almacenar=almacenar
        self.almacen=[]
        self.varLeer=0
        self.ID=ID
        self.run()
    
    def cop(self):
        cop=copia(self.Memoria,self.posMem,self.variables,self.tipoVar,self.posVar,self.etiquetas,self.posEt
        ,self.acumulador,self.linea,self.NumLin,self.noAcabe,self.imprimir,self.mostrar,self.errors)
        return copy.deepcopy(cop)
    def run(self):
        for linea in self.arch:
            self.Memoria.append(linea)
            self.posMem+=1

        for linea in self.arch:
            linea=linea.split()
            if linea[0]=="nueva":
                self.nueva(linea)
            if linea[0]=="etiqueta":
                self.etiquetas.append(str(self.ID)+str(linea[1]))
                self.posEt.append(int(linea[2])+self.kernel)
        self.lineaAlinea()

        #for self.linea in self.arch:
    def lineaAlinea(self):
        while self.NumLin < len(self.arch):  
            if self.noAcabe:
                self.NumLin+=1
                self.guardar()
                break
            self.linea=self.arch[self.NumLin]
            linea=self.linea.split()
            self.accion(linea)
            if self.almacenar:
                self.almacen.append(self.cop())
     
    def accion(self,linea):
        if linea==[]:
            pass
        else:
            tipo=str(linea[0])
        
        if tipo == "cargue":
            self.cargue(linea)
        elif tipo == "almacene":
            self.almacene(linea)
        elif tipo == "limpie":
            self.acumulador=0
        elif tipo == "vaya":
            self.vaya(linea)
            return
        elif tipo == "vayasi":
            self.vayasi(linea)
            return
        elif tipo == "nueva":
            pass
        elif tipo == "etiqueta":
            pass
        elif tipo == "lea":
            self.lea(linea)
        elif tipo == "sume":
            self.sume(linea)
        elif tipo == "reste":
            self.reste(linea)
        elif tipo == "multiplique":
            self.multiplique(linea)
        elif tipo == "divida":
            self.divida(linea)
        elif tipo == "potencia":
            self.potencia(linea)
        elif tipo == "modulo":
            self.modulo(linea)
        elif tipo == "concatene":
            self.concatene(linea)
        elif tipo == "elimine":
            self.elimine(linea)
        elif tipo == "Extraiga":
            self.Extraiga(linea)
        elif tipo == "Y":
            self.Y(linea)
        elif tipo == "O":
            self.O(linea)
        elif tipo == "NO":
            self.NO(linea)
        elif tipo == "muestre":
            self.muestre(linea)
        elif tipo == "imprima":
            self.imprima(linea)
        elif tipo == "retorne":
            self.retorne(linea)
        elif tipo[0]=="/" and tipo[1]=="/":
            pass
        else:
            self.errors.append("no se pudo difinir lo operacion")
        
        self.NumLin+=1

    def cargue(self,linea):
        i=self.variables.index(str(self.ID)+str(linea[1]))
        RposVar=self.posVar[i]-self.kernel-1
        valor=self.Memoria[RposVar]
        self.acumulador=valor

    def almacene(self,linea,pasw="www5"):
        i=self.variables.index(str(self.ID)+str(linea[1]))
        RposVar=self.posVar[i]-self.kernel-1
        if pasw=="www5":
            self.Memoria[RposVar]=self.acumulador
        else:
            tipoV=self.tipoVar[i]
            if tipoV=='I' or tipoV=='L':
                try:
                    self.Memoria[RposVar]=int(pasw)
                except:
                    self.errors.append("el tipo de variable declarado no concide con el valor ingresado")
                
            if tipoV=='R':
                try:
                    self.Memoria[RposVar]=float(pasw)
                except:
                    self.errors.append("el tipo de variable declarado no concide con el valor ingresado")
                
            if tipoV=='C':
                self.Memoria[RposVar]=pasw
                
            

    def vaya(self,linea):
        i=self.etiquetas.index(str(self.ID)+str(linea[1]))
        self.NumLin=self.posEt[i]-self.kernel-1
         
    def vayasi(self,linea):
        try:
            acumtemp=float(self.acumulador)
        except:
            self.errors.append("el Acumulador no puede ser convertido en valor numerico")
            self.NumLin+=1
            return

        if(acumtemp>0):
            i=self.etiquetas.index(str(self.ID)+str(linea[1]))
            self.NumLin=self.posEt[i]-self.kernel-1
        if(acumtemp<0):
            i=self.etiquetas.index(str(self.ID)+str(linea[2]))
            self.NumLin=self.posEt[i]-self.kernel-1
        if(acumtemp==0):
            self.NumLin+=1
            return

    def lea(self,linea):
        self.noAcabe=True
        self.varLeer=linea[1]
        print("ingrese el valor para la variable"+str(linea))
        
    def nueva(self,linea):
        self.posMem+=1
        self.variables.append(str(self.ID)+str(linea[1]))
        self.tipoVar.append(linea[2])
        if(len(linea)==4):
            self.Memoria.append(linea[3])
        else:
            temp=['I','R','L']
            if linea[2] in temp:
                n=0
            if linea[2]=='C':
                n=' '
            self.Memoria.append(n)
        self.posVar.append(self.posMem+self.kernel)

    def sume(self,linea):
        try:
            acumtemp=int(self.acumulador)
        except:
            try:
                acumtemp=float(self.acumulador)
            except:
                self.errors.append("el Acumulador no puede ser convertido en valor numerico")
                return  
          
        i=self.variables.index(str(self.ID)+str(linea[1]))
        RposVar=self.posVar[i]-self.kernel-1
        valor=self.Memoria[RposVar]

        tipoV=self.tipoVar[i]
        if tipoV == "I":
            valor=int(valor)
        else:
            valor=float(valor)

        self.acumulador=acumtemp+valor
    
    def reste(self,linea):
        try:
            acumtemp=int(self.acumulador)
        except:
            try:
                acumtemp=float(self.acumulador)
            except:
                self.errors.append("el Acumulador no puede ser convertido en valor numerico")
                return  

        i=self.variables.index(str(self.ID)+str(linea[1]))
        RposVar=self.posVar[i]-self.kernel-1
        valor=self.Memoria[RposVar]
        tipoV=self.tipoVar[i]
        
        if tipoV == "I":
            valor=int(valor)
        else:
            valor=float(valor)
        
        self.acumulador=acumtemp-valor

    def multiplique(self,linea):
        try:
            acumtemp=int(self.acumulador)
        except:
            try:
                acumtemp=float(self.acumulador)
            except:
                self.errors.append("el Acumulador no puede ser convertido en valor numerico")
                return  

        i=self.variables.index(str(self.ID)+str(linea[1]))
        RposVar=self.posVar[i]-self.kernel-1
        valor=self.Memoria[RposVar]
        tipoV=self.tipoVar[i]
        if tipoV == "I":
            valor=int(valor)
        else:
            valor=float(valor)
        
        self.acumulador= acumtemp*valor

    def divida(self,linea):
        try:
            acumtemp=int(self.acumulador)
        except:
            try:
                acumtemp=float(self.acumulador)
            except:
                self.errors.append("el Acumulador no puede ser convertido en valor numerico")
                return  

        i=self.variables.index(str(self.ID)+str(linea[1]))
        RposVar=self.posVar[i]-self.kernel-1
        valor=self.Memoria[RposVar]
        tipoV=self.tipoVar[i]
        if tipoV == "I":
            valor=int(valor)
        else:
            valor=float(valor)
        if valor!=0:
            self.acumulador=acumtemp/valor
        else:
            self.errors.append("ERROR se Divide Por Cero")

    def potencia(self,linea):
        try:
            acumtemp=int(self.acumulador)
        except:
            try:
                acumtemp=float(self.acumulador)
            except:
                self.errors.append("el Acumulador no puede ser convertido en valor numerico")
                return  

        i=self.variables.index(str(self.ID)+str(linea[1]))
        RposVar=self.posVar[i]-self.kernel-1
        valor=self.Memoria[RposVar]
        tipoV=self.tipoVar[i]
        if tipoV == "I":
            valor=int(valor)
        else:
            valor=float(valor)
        
        self.acumulador=acumtemp**valor

    def modulo(self,linea):
        try:
            acumtemp=int(self.acumulador)
        except:
            try:
                acumtemp=float(self.acumulador)
            except:
                self.errors.append("el Acumulador no puede ser convertido en valor numerico")
                return  

        i=self.variables.index(str(self.ID)+str(linea[1]))
        RposVar=self.posVar[i]-self.kernel-1
        valor=self.Memoria[RposVar]
        tipoV=self.tipoVar[i]
        if tipoV == "I":
            valor=int(valor)
        else:
            valor=float(valor)
        
        self.acumulador=acumtemp%valor

    def concatene(self,linea):       
        i=self.variables.index(str(self.ID)+str(linea[1]))
        RposVar=self.posVar[i]-self.kernel-1
        valor=self.Memoria[RposVar]
        self.acumulador=self.acumulador+valor

    def elimine(self,linea):
        i=self.variables.index(str(self.ID)+str(linea[1]))
        RposVar=self.posVar[i]-self.kernel-1
        valor=self.Memoria[RposVar]
        while valor in self.acumulador:
            del self.acumulador[valor]
    
    def Extraiga(self,linea):
        i=self.variables.index(str(self.ID)+str(linea[1]))
        RposVar=self.posVar[i]-self.kernel-1
        valor=self.Memoria[RposVar]
        self.acumulador=self.acumulador[:valor]

    def Y(self,linea):
        i=self.variables.index(str(self.ID)+str(linea[1]))
        RposVar=self.posVar[i]-self.kernel-1
        valor1=self.Memoria[RposVar]

        i=self.variables.index(str(self.ID)+str(linea[2]))
        RposVar=self.posVar[i]-self.kernel-1
        valor2=self.Memoria[RposVar]

        i=self.variables.index(str(self.ID)+str(linea[3]))
        RposVar=self.posVar[i]-self.kernel-1
        self.Memoria[RposVar] = (bool(valor1) and bool(valor2))

    def O(self,linea):
        i=self.variables.index(str(self.ID)+str(linea[1]))
        RposVar=self.posVar[i]-self.kernel-1
        valor1=self.Memoria[RposVar]

        i=self.variables.index(str(self.ID)+str(linea[2]))
        RposVar=self.posVar[i]-self.kernel-1
        valor2=self.Memoria[RposVar]

        i=self.variables.index(str(self.ID)+str(linea[3]))
        RposVar=self.posVar[i]-self.kernel-1
        self.Memoria[RposVar] = (bool(valor1) or bool(valor2))
        
    def NO(self,linea):
        i=self.variables.index(str(self.ID)+str(linea[1]))
        RposVar=self.posVar[i]-self.kernel-1
        valor1=self.Memoria[RposVar]

        i=self.variables.index(str(self.ID)+str(linea[2]))
        RposVar=self.posVar[i]-self.kernel-1
        self.Memoria[RposVar] = not bool(valor1)
        
    def muestre(self,linea):
        if linea[1]== "acumulador":
            self.mostrar.append(self.acumulador)
            return
        i=self.variables.index(str(self.ID)+str(linea[1]))
        RposVar=self.posVar[i]-self.kernel-1
        valor=self.Memoria[RposVar]
        self.mostrar.append(valor)
    
    def imprima(self,linea):
        if linea[1]== "acumulador":
            self.imprimir.append(self.acumulador)
            return
        i=self.variables.index(str(self.ID)+str(linea[1]))
        RposVar=self.posVar[i]-self.kernel-1
        valor=self.Memoria[RposVar]
        self.imprimir.append(valor)
    
    def retorne(self,linea):
        return 

    def guardar(self,id=0):
        with open('media/bodega/chEje'+str(id)+'.pkl','wb') as output:
            pickle.dump(self,output,pickle.HIGHEST_PROTOCOL)

class copia:
    def __init__(self,Memoria,posMem,variables,tipoVar,posVar,etiquetas,posEt,acumulador,linea,Numlin,noAcabe,imprimir,mostrar,errors):
        self.Memoria=Memoria
        self.posMem=posMem
        self.variables=variables
        self.tipoVar=tipoVar
        self.posVar=posVar
        self.etiquetas=etiquetas
        self.posEt=posEt
        self.acumulador=acumulador
        self.linea=linea
        self.NumLin=Numlin
        self.noAcabe=noAcabe
        self.imprimir=imprimir
        self.mostrar=mostrar
        self.errors=errors

def chEjecguardado(id=0):
    with open('media/bodega/chEje'+str(id)+'.pkl','rb') as input:
        return pickle.load(input)