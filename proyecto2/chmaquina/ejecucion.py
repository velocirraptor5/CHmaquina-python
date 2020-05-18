import copy
class ejecutar:
    def __init__(self,arch,kernel,memoria,almacenar=False):
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
        self.acumulador=0
        self.linea=0
        self.noAcabe=False
        self.imprimir=[]
        self.mostrar=[]
        self.errors=[]
        self.almacenar=almacenar
        self.almacen=[]
        self.run()

    def run(self):
        for linea in self.arch:
            self.Memoria.append(linea)
            self.posMem+=1

        for linea in self.arch:
            linea=linea.split()
            
            if linea[0]=="etiqueta":
                self.etiquetas.append(linea[1])
                self.posEt.append(int(linea[2])+self.kernel)
            
        for num,self.linea in enumerate(self.arch):
            linea=self.linea.split()
            self.accion(linea)
            if self.almacenar:
                self.almacen=copy.deepcopy(self)


        

    def accion(self,linea):
        if linea==[]:
            return
        else:
            tipo=str(linea[0])
        
        if tipo == "cargue":
            self.cargue(linea)
        elif tipo == "almacene":
            self.almacene(linea)
        elif tipo == "vaya":
            self.vaya(linea)
        elif tipo == "vayasi":
            self.vayasi(linea)
        elif tipo == "nueva":
            self.nueva(linea)
        elif tipo == "etiqueta":
            return
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
            return
        else:
            self.errors.append("no se pudo difinir lo operacion")

    def cargue(self,linea):
        i=self.variables.index(linea[1])
        RposVar=self.posVar[i]-self.kernel-1
        valor=self.Memoria[RposVar]
        self.acumulador=valor

    def almacene(self,linea):
        i=self.variables.index(linea[1])
        RposVar=self.posVar[i]-self.kernel-1
        self.Memoria[RposVar]=self.acumulador

    def vaya(self,linea):
        i=self.etiquetas.index(linea[1])
        self.linea=self.arch[self.posEt[i]]
         
    def vayasi(self,linea):
        try:
            acumtemp=float(self.acumulador)
        except:
            self.errors.append("el Acumulador no puede ser convertido en valor numerico")
            return

        if(acumtemp>0):
            i=self.etiquetas.index(linea[1])
            self.linea=self.arch[self.posEt[i]-self.kernel]
        if(acumtemp<0):
            i=self.etiquetas.index(linea[2])
            self.linea=self.arch[self.posEt[i]-self.kernel]
        else:
            return

    def nueva(self,linea):
        self.posMem+=1
        self.variables.append(linea[1])
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

    def lea(self,linea):
        self.noAcabe=True
        input("ingrese el valor para la variable"+str(linea))

    def sume(self,linea):
        try:
            acumtemp=int(self.acumulador)
        except:
            try:
                acumtemp=float(self.acumulador)
            except:
                self.errors.append("el Acumulador no puede ser convertido en valor numerico")
                return  
          
        i=self.variables.index(linea[1])
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

        i=self.variables.index(linea[1])
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

        i=self.variables.index(linea[1])
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

        i=self.variables.index(linea[1])
        RposVar=self.posVar[i]-self.kernel-1
        valor=self.Memoria[RposVar]
        tipoV=self.tipoVar[i]
        if tipoV == "I":
            valor=int(valor)
        else:
            valor=float(valor)
        
        self.acumulador=acumtemp/valor

    def potencia(self,linea):
        try:
            acumtemp=int(self.acumulador)
        except:
            try:
                acumtemp=float(self.acumulador)
            except:
                self.errors.append("el Acumulador no puede ser convertido en valor numerico")
                return  

        i=self.variables.index(linea[1])
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

        i=self.variables.index(linea[1])
        RposVar=self.posVar[i]-self.kernel-1
        valor=self.Memoria[RposVar]
        tipoV=self.tipoVar[i]
        if tipoV == "I":
            valor=int(valor)
        else:
            valor=float(valor)
        
        self.acumulador=acumtemp%valor

    def concatene(self,linea):       
        i=self.variables.index(linea[1])
        RposVar=self.posVar[i]-self.kernel-1
        valor=self.Memoria[RposVar]
        self.acumulador=self.acumulador+valor

    def elimine(self,linea):
        i=self.variables.index(linea[1])
        RposVar=self.posVar[i]-self.kernel-1
        valor=self.Memoria[RposVar]
        while valor in self.acumulador:
            del self.acumulador[valor]
    
    def Extraiga(self,linea):
        i=self.variables.index(linea[1])
        RposVar=self.posVar[i]-self.kernel-1
        valor=self.Memoria[RposVar]
        self.acumulador=self.acumulador[:valor]

    def Y(self,linea):
        i=self.variables.index(linea[1])
        RposVar=self.posVar[i]-self.kernel-1
        valor1=self.Memoria[RposVar]

        i=self.variables.index(linea[2])
        RposVar=self.posVar[i]-self.kernel-1
        valor2=self.Memoria[RposVar]

        i=self.variables.index(linea[3])
        RposVar=self.posVar[i]-self.kernel-1
        self.Memoria[RposVar] = (bool(valor1) and bool(valor2))

    def O(self,linea):
        i=self.variables.index(linea[1])
        RposVar=self.posVar[i]-self.kernel-1
        valor1=self.Memoria[RposVar]

        i=self.variables.index(linea[2])
        RposVar=self.posVar[i]-self.kernel-1
        valor2=self.Memoria[RposVar]

        i=self.variables.index(linea[3])
        RposVar=self.posVar[i]-self.kernel-1
        self.Memoria[RposVar] = (bool(valor1) or bool(valor2))
        
    def NO(self,linea):
        i=self.variables.index(linea[1])
        RposVar=self.posVar[i]-self.kernel-1
        valor1=self.Memoria[RposVar]

        i=self.variables.index(linea[2])
        RposVar=self.posVar[i]-self.kernel-1
        self.Memoria[RposVar] = not bool(valor1)
        
        
    def muestre(self,linea):
        if linea[1]== "acumulador":
            self.mostrar.append(self.acumulador)
            return
        i=self.variables.index(linea[1])
        RposVar=self.posVar[i]-self.kernel-1
        valor=self.Memoria[RposVar]
        self.mostrar.append(valor)
    
    def imprima(self,linea):
        if linea[1]== "acumulador":
            self.imprimir.append(self.acumulador)
            return
        i=self.variables.index(linea[1])
        RposVar=self.posVar[i]-self.kernel-1
        valor=self.Memoria[RposVar]
        self.imprimir.append(valor)
    
    def retorne(self,linea):
        return 
