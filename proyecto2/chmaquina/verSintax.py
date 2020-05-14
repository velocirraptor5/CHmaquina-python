from django.core.files import File


class sintax:
    def __init__(self,ch):
        self.errors=[]
        self.OK=True
        self.ch = ch
        self.variables=[]
        self.tipoVar=[]
        self.etiquetas=[]
        self.numRetornes=0
        self.verificacion()
        
    def verificacion(self):
        for num,linea in enumerate(self.ch):
            linea=linea.split()
            self.comprueba(linea,num)

        if self.numRetornes==0:
            self.OK=False
            self.errors.append("No tiene el retorne")

    def comprueba(self, linea,num):
        if linea==[]:
            tipo=" "
        else:
            tipo=str(linea[0])
        ok=True
        estand=["cargue","almacene","lea"]
        opereandnorm=["sume","reste","multiplique","divida","modulo"]
        if tipo in estand:
            ok= self.estandar(linea)
        elif tipo == "vaya":
            ok= self.vaya(linea)
        elif tipo == "vayasi":
            ok= self.vayasi(linea)
        elif tipo == "nueva":
            ok= self.nueva(linea)
        elif tipo == "etiqueta":
            ok= self.etiqueta(linea)
        elif tipo in opereandnorm:
            ok= self.operandos(linea)
        elif tipo == "potencia":
            ok= self.operandos(linea,['I'])
        elif tipo == "concatene":
            ok= self.operandos(linea,['C'])
        elif tipo == "elimine":
            ok= self.operandos(linea,['C'])
        elif tipo == "Extraiga":
            ok= self.operandos(linea,['I'])
        elif tipo == "Y":
            ok= self.opLog(linea)
        elif tipo == "O":
            ok= self.opLog(linea)
        elif tipo == "NO":
            ok= self.NO(linea)
        elif tipo == "muestre":
            ok= self.mue_im(linea)
        elif tipo == "imprima":
            ok= self.mue_im(linea)
        elif tipo == "retorne":
            ok= self.retorne(linea)
            self.numRetornes+=1
        elif tipo == " " or (tipo[0]=="/" and tipo[1]=="/"):
            pass
        else:
            ok=False
            self.errors.append("no se pudo difinir lo operacion")
        
        if not ok:
            self.errors.append("error en la linea" + str(num+1))
            self.OK=False

    
    def estandar(self,linea):
        if len(linea)!=2:
            self.errors.append("la cantidad de parametros no coinciden")
            return False

        if linea[1] not in self.variables:
            self.errors.append("no exite la variable"+ linea[1]) 
        
        return ((len(linea)==2) and (linea[1] in self.variables))      

    def vaya(self,linea):
        if len(linea)!=2:
            self.errors.append("la cantidad de parametros no coinciden")
            return False
        if linea[1] not in self.etiquetas:
            self.errors.append("no exite la etiqueta"+ linea[1])
        
        return linea[1] in self.etiquetas
         
    def vayasi(self,linea):
        if len(linea)!=3:
            self.errors.append("la cantidad de parametros no coinciden")
            return False
        if linea[1] not in self.etiquetas:
            self.errors.append("no exite la etiqueta"+ linea[1])
            return False
        if linea[2] not in self.etiquetas:
            self.errors.append("no exite la etiqueta"+ linea[2])

        return linea[2] in self.etiquetas
    
    def nueva(self,linea):
        opciones=['C','I','R','L']
        if len(linea)!=4:
            if len(linea)!=3:
                self.errors.append("la cantidad de parametros no coinciden")
                return False
             
        if linea[2] in opciones:
            if linea[2]=='I':
                try:
                    n=int(linea[3])
                except:
                    self.errors.append("el valor de la variable asigna no es entera")
                    return False
            if linea[2]=='R':
                try:
                    n=float(linea[3])
                except:
                    self.errors.append("el valor de la variable asigna no es real")
                    return False
            if linea[2]=='L':
                try:
                    n=int(linea[3])
                    if n not in [1,0]:
                        self.errors.append("el valor de la variable asigna no es 0 o 1 para convertirla a logica")
                        return False
                except:
                    self.errors.append("el valor de la variable asigna no es 0 o 1 para convertirla a logica")
                    return False
            
            self.variables.append(linea[1])
            self.tipoVar.append(linea[2])
            return True
        else:
            self.errors.append("no exite el tipo de variable"+linea[2])
            return False 
         
    def etiqueta(self,linea):
        if len(linea)!=3:
            self.errors.append("la cantidad de parametros no coinciden")
            return False
        try:
            n= int(linea[2])
        except:
            self.errors.append("la direccion de la etiqueta debe ser un entero")
            return False
        
        self.etiquetas.append(linea[2])
        return True   
    
    def operandos(self,linea,valid=['I','R']):
        if self.estandar(linea):
            tipovar=self.getTipovar(linea[1])
            if tipovar in valid
                return True
            else:
                self.errors.append("el tipo de variable de "+str(linea[1])+"---" + str(tipovar)+"no puede ser usado para esta operacion matematica")
                return False
        return False

    
    def tipoCorrecto(self,nom,tipo):
        i= self.variables.index(nom)
        if self.tipoVar[i]==tipo:
            self.errors.append("el tipo de variable"+str(nom)+"-----"+str(self.tipoVar[i])+ "es incorrecto para esta operacion logica")
            return False
        return True

    def opLog(self,linea):
        if len(linea)!=4:
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
        
        if linea[3] not in self.variables:
            self.errors.append("no exite la variable"+ linea[3])      
            return False
        if  not self.tipoCorrecto(linea[3],'L'):            
            return False 
        return True
   
    
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
        
    def mue_im(self,linea):
        if self.estandar(linea):
            return True
        else:
            if(linea[1]=='acumulador'):
                return True
            return False

    def retorne(self,linea):
        if len(linea)>2:
            self.errors.append("la cantidad de parametros no coinciden")
        if self.numRetornes == 2:
            self.errors.append("hay mas de un retorne")
        return ((len(linea)<=2))

    





