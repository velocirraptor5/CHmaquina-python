from django.core.files import File
from .models import Archivo


class sintax:
    def __init__(self,ruta):
        self.ruta= "media/bodega/"+str(ruta)
        self.errors=[]
        self.OK=True
        self.ch = self.leerch()
        self.variables=[]
        self.tipoVar=[]
        self.etiquetas=[]
        self.numRetornes=0
        if self.OK:
            self.verificacion()
        

        
    def leerch(self):
        try:
            f = open(self.ruta, "r")
            myfile = File(f)
            ch = myfile.readlines() 
            f.close()
            return ch
        except :
            self.errors.append("no se puede abrir el archivo porfavor verificar el formato")
            self.OK=False
            return ""
    

    def verificacion(self):
        for num,linea in enumerate(self.ch):
            linea=linea.split()
            self.comprueba(linea,num)
            self.errors.append(linea)

        if self.numRetornes==0:
            self.OK=False
            self.errors.append("No tiene el retorne")


    def comprueba(self, linea,num):
        print(linea)
        if linea==[]:
            tipo=" "
        else:
            tipo=str(linea[0])
        ok=True
        
        if tipo == "cargue":
            ok= self.cargue(linea)
        elif tipo == "almacene":
            ok= self.almacene(linea)
        elif tipo == "vaya":
            ok= self.vaya(linea)
        elif tipo == "vayasi":
            ok= self.vayasi(linea)
        elif tipo == "nueva":
            ok= self.nueva(linea)
        elif tipo == "etiqueta":
            ok= self.etiqueta(linea)
        elif tipo == "lea":
            ok= self.lea(linea)
        elif tipo == "sume":
            ok= self.sume(linea)
        elif tipo == "reste":
            ok= self.reste(linea)
        elif tipo == "multiplique":
            ok= self.multiplique(linea)
        elif tipo == "divida":
            ok= self.divida(linea)
        elif tipo == "potencia":
            ok= self.potencia(linea)
        elif tipo == "modulo":
            ok= self.modulo(linea)
        elif tipo == "concatene":
            ok= self.concatene(linea)
        elif tipo == "elimine":
            ok= self.elimine(linea)
        elif tipo == "Extraiga":
            ok= self.Extraiga(linea)
        elif tipo == "Y":
            ok= self.Y(linea)
        elif tipo == "O":
            ok= self.O(linea)
        elif tipo == "NO":
            ok= self.NO(linea)
        elif tipo == "muestre":
            ok= self.muestre(linea)
        elif tipo == "imprima":
            ok= self.imprima(linea)
        elif tipo == "retorne":
            ok= self.retorne(linea)
            self.numRetornes+=1
        elif tipo == " ":
            pass
        else:
            ok=False
            self.errors.append("no se pudo difinir lo operacion")
        
        if not ok:
            self.errors.append("error en la linea" + str(num+1))
            self.OK=False
            

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
        
        return ((len(linea)==2) and (linea[1] in self.etiquetas))
         

    def vayasi(self,linea):
        return True
    
    def nueva(self,linea):
        self.variables.append(linea[1]) 
        opciones=['C','I','R','L']
        print(linea)
        if len(linea)!=4:
            self.errors.append("la cantidad de parametros no coinciden")
            return False
        if linea[2] in opciones:
            self.tipoVar.append(linea[2])
            return len(linea)==4
        else:
            self.errors.append("no exite el tipo de variable"+linea[2])
            return False 
         
    def etiqueta(self,linea):
        self.etiquetas.append(linea[2])

        if len(linea)!=3:
            self.errors.append("la cantidad de parametros no coinciden")
        
        return len(linea)==3   

    def lea(self,linea):
        if len(linea)!=2:
            self.errors.append("la cantidad de parametros no coinciden")
            return False
        if linea[1] not in self.variables:
            self.errors.append("no exite la variable"+ linea[1])

        return ((len(linea)==2) and (linea[1] in self.variables))
        
    def sume(self,linea):
        if len(linea)!=2:
            self.errors.append("la cantidad de parametros no coinciden")
            return False
        if linea[1] not in self.variables:
            self.errors.append("no exite la variable"+ linea[1])
        
        return ((len(linea)==2) and (linea[1] in self.variables))
         
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
        if linea[2] not in self.variables:
            self.errors.append("no exite la variable"+ linea[2])
        if linea[3] not in self.variables:
            self.errors.append("no exite la variable"+ linea[3])      
        return ((len(linea)==4) and (linea[1] in self.variables) and (linea[2] in self.variables) and (linea[3] in self.variables))

        
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
        if linea[2] not in self.variables:
            self.errors.append("no exite la variable"+ linea[2])
        return ((len(linea)==3) and (linea[1] in self.variables) and (linea[2] in self.variables) )
        
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
        if self.retorne == 2:
            self.errors.append("hay mas de un retorne")
        return ((len(linea)<=2) and (linea[1] in self.variables))
        
    





