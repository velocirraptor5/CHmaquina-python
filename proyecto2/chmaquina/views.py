from django.http import HttpResponse 
from django.template import Template, Context
from django.template.loader import get_template
from django.shortcuts import render
import datetime

#__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
 
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
