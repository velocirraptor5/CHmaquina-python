class ejecutar:
    def __init__(self,arch,kernel,memoria):
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
        self.errors=[]
        self.run()

    def run(self):
        for linea in self.arch:
            self.Memoria.append(linea)
            self.posMem+=1

        for linea in self.arch:
            linea=linea.split()
            if linea[0] == "nueva":
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
            if linea[0]=="etiqueta":
                self.etiquetas.append(linea[1])
                self.posEt.append(int(linea[2])+self.kernel)
            
        for num,self.linea in enumerate(self.arch):
            linea=self.linea.split()
            self.accion(linea)

        

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
            return
        elif tipo == "nueva":
            return
        elif tipo == "etiqueta":
            return
        elif tipo == "lea":
            self.lea(linea)
            return
        elif tipo == "sume":
            #self.sume(linea)
            return
        elif tipo == "reste":
            #self.reste(linea)
            return
        elif tipo == "multiplique":
            #self.multiplique(linea)
            return
        elif tipo == "divida":
            #self.divida(linea)
            return
        elif tipo == "potencia":
            #self.potencia(linea)
            return
        elif tipo == "modulo":
            #self.modulo(linea)
            return
        elif tipo == "concatene":
            #self.concatene(linea)
            return
        elif tipo == "elimine":
            #self.elimine(linea)
            return
        elif tipo == "Extraiga":
            #self.Extraiga(linea)
            return
        elif tipo == "Y":
            #self.Y(linea)
            return
        elif tipo == "O":
            #self.O(linea)
            return
        elif tipo == "NO":
            #self.NO(linea)
            return
        elif tipo == "muestre":
            #self.muestre(linea)
            return
        elif tipo == "imprima":
            #self.imprima(linea)
            return
        elif tipo == "retorne":
            #self.retorne(linea)
            return
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
            self.linea=self.arch[self.posEt[i]]
        if(acumtemp<0):
            i=self.etiquetas.index(linea[2])
            self.linea=self.arch[self.posEt[i]]
        else:
            return

    def lea(self,linea):
        input("ingrese el valor para la variable"+str(linea))

    def sume(self,linea):
        if self.estandar(linea):
            i=self.variables.index(linea[1])
            valid=['I','R']
            return self.tipoVar[i] in valid    
    
    def reste(self,linea):
        if len(linea)!=2:
            self.errors.append("la cantidad de parametros no coinciden")
            return False
        if linea[1] not in self.variables:
            self.errors.append("no exite la variable"+ linea[1])
        
        return ((len(linea)==2) and (linea[1] in self.variables))
    
    def multiplique(self,linea):
        if len(linea)!=2:
            self.errors.append("la cantidad de parametros no coinciden")
            return Fa
        if linea[1] not in self.variables:
            self.errors.append("no exite la variable"+ linea[1])
        
        return ((len(linea)==2) and (linea[1] in self.variables))

    def divida(self,linea):
        if len(linea)!=2:
            self.errors.append("la cantidad de parametros no coinciden")
            return False
        if linea[1] not in self.variables:
            self.errors.append("no exite la variable"+ linea[1])

        return ((len(linea)==2) and (linea[1] in self.variables))
    
    def potencia(self,linea):
        if len(linea)!=2:
            self.errors.append("la cantidad de parametros no coinciden")
            return False
        i=self.variables.index(linea[1])
        if linea[1] not in self.variables:
            self.errors.append("no exite la variable"+ linea[1])

        return ((len(linea)==2) and (linea[1] in self.variables) and self.tipoVar[i]== 'I')

    def modulo(self,linea):
        if len(linea)!=2:
            self.errors.append("la cantidad de parametros no coinciden")
            return False
        if linea[1] not in self.variables:
            self.errors.append("no exite la variable"+ linea[1])
        return ((len(linea)==2) and (linea[1] in self.variables))

    def concatene(self,linea):
        if len(linea)!=2:
            self.errors.append("la cantidad de parametros no coinciden")
            return False
        if linea[1] not in self.variables:
            self.errors.append("no exite la variable"+ linea[1])
        return ((len(linea)==2) and (linea[1] in self.variables))
    
    def elimine(self,linea):
        if len(linea)!=2:
            self.errors.append("la cantidad de parametros no coinciden")
            return False
        if linea[1] not in self.variables:
            self.errors.append("no exite la variable"+ linea[1])
        return ((len(linea)==2) and (linea[1] in self.variables))
    
    def Extraiga(self,linea):
        if len(linea)!=2:
            self.errors.append("la cantidad de parametros no coinciden")
            return False
        if linea[1] not in self.variables:
            self.errors.append("no exite la variable"+ linea[1])
        return ((len(linea)==2) and (linea[1] in self.variables))

    def Y(self,linea):
        if len(linea)!=4:
            self.errors.append("la cantidad de parametros no coinciden")
            return False
        if linea[1] not in self.variables:
            self.errors.append("no exite la variable"+ linea[1])
            return False

        tip = self.getTipovar(linea[1])
        if tip != 'C':
            self.errors.append("el tipo de variable"+str(linea[1])+"-----"+str(tip)+ "es incorrecto para esta operacion logica")
            return False
        
        if linea[2] not in self.variables:
            self.errors.append("no exite la variable"+ linea[2])
            return False

        tip = self.getTipovar(linea[2])
        if tip != 'C':
            self.errors.append("el tipo de variable"+str(linea[2])+"-----"+str(tip)+ "es incorrecto para esta operacion logica")
            return False

        if linea[3] not in self.variables:
            self.errors.append("no exite la variable"+ linea[3])      
            return False

        tip = self.getTipovar(linea[3])
        if tip != 'C':
            self.errors.append("el tipo de variable"+str(linea[3])+"-----"+str(tip)+ "es incorrecto para esta operacion logica")
            return False

        return True
    
    def O(self,linea):
        if len(linea)!=4:
            self.errors.append("la cantidad de parametros no coinciden")
            return False
        if linea[1] not in self.variables:
            self.errors.append("no exite la variable"+ linea[1])
        if linea[2] not in self.variables:
            self.errors.append("no exite la variable"+ linea[2])
        if linea[3] not in self.variables:
            self.errors.append("no exite la variable"+ linea[3])      
        return ((len(linea)==4) and (linea[1] in self.variables) and (linea[2] in self.variables) and (linea[3] in self.variables))

    def NO(self,linea):
        if len(linea)!=3:
            self.errors.append("la cantidad de parametros no coinciden")
            return False
        if linea[1] not in self.variables:
            self.errors.append("no exite la variable"+ linea[1])
            return False
        if  not self.tipoCorrecto(linea[1],'L'):            
            return False
    
        if linea[2] not in self.variables:
            self.errors.append("no exite la variable"+ linea[2])
            return False
        if  not self.tipoCorrecto(linea[2],'L'):            
            return False
        
        return True
        
    def muestre(self,linea):
        if len(linea)!=2:
            self.errors.append("la cantidad de parametros no coinciden")
            return False
        if linea[1] not in self.variables:
            self.errors.append("no exite la variable"+ linea[1])
        return ((len(linea)==2) and (linea[1] in self.variables))
    
    def imprima(self,linea):
        if len(linea)!=2:
            self.errors.append("la cantidad de parametros no coinciden")
            return False
        if linea[1] not in self.variables:
            self.errors.append("no exite la variable"+ linea[1])
        return ((len(linea)==2) and (linea[1] in self.variables))
    def retorne(self,linea):
        if len(linea)>2:
            self.errors.append("la cantidad de parametros no coinciden")
        return ((len(linea)<=2))
