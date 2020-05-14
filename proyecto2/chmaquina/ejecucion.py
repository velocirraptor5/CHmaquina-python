class ejecutar:
    def __init__(self,arch):
        self.arch = arch
        self.variables=[]
        self.tipoVar=[]
        self.etiquetas=[]
        self.linea=0
        self.run()

    def run(self):
        for lin in self.arch:
            print(lin)



    def cargue(self,linea):
        if len(linea)!=2:
            self.errors.append("la cantidad de parametros no coinciden")
            return False

        if linea[1] not in self.variables:
            self.errors.append("no exite la variable"+ linea[1]) 
        
        return ((len(linea)==2) and (linea[1] in self.variables)) 

    def almacene(self,linea):
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
            return False
        
        self.etiquetas.append(linea[2])

    def lea(self,linea):
        if len(linea)!=2:
            self.errors.append("la cantidad de parametros no coinciden")
            return False
        if linea[1] not in self.variables:
            self.errors.append("no exite la variable"+ linea[1])

        return ((len(linea)==2) and (linea[1] in self.variables))

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
        if self.numRetornes == 2:
            self.errors.append("hay mas de un retorne")
        return ((len(linea)<=2))
