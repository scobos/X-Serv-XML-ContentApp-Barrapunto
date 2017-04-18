from django.shortcuts import render
from django.http import HttpResponse
from barrapunto.models import Page
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from xml.sax.handler import ContentHandler
class myContentHandler(ContentHandler):

    def __init__ (self):
        self.inItem = False
        self.inContent = False
        self.theContent = ""
        self.line = ""

    def startElement (self, name, attrs):
        if name == 'item':
            self.inItem = True
        elif self.inItem:
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.inContent = True

    def endElement (self, name):
        if name == 'item':
            self.inItem = False
        elif self.inItem:
            if name == 'title':
                # To avoid Unicode trouble
                self.line = "Title: " + self.theContent + "."
                self.inContent = False
                self.theContent = ""
            elif name == 'link':
                lnk = "<li><a href='" + self.theContent + "'>" + self.line + "</a></li><br/>"
                print (lnk)
                self.inContent = False
                self.theContent = ""
                self.line = ""

    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars

def muestra_todo():
    lista = Page.objects.all()
    respuesta = "<ol>"
    for pag in lista:
        respuesta += '<li><a href="' + str(pag.id) + '">' + pag.name + '</a>'
    respuesta += "</ol>"
    return HttpResponse(respuesta)

@csrf_exempt
def pagina(request, recurso):
    if request.method ==  "GET":
        try:
            page = Page.objects.get(name = recurso)
            respuesta = ("<!DOCTYPE html><html><body><div>" +
                        page.page + "</div><div><ul>" + muestra_todo() + "</ul></div></body></html>")
            return HttpResponse(respuesta)
        except Page.DoesNotExist:
            respuesta = "No existe ese nombre con contenidos en la base de datos"
            return HttpResponse(respuesta, status = 404)
    elif request.method == "PUT":
        page = Page(name= recurso, page= request.body)
        page.save()
        respuesta = "La pagina ha sido añadida correctamente "
        return HttpResponse(respuesta + recurso)
    else:
        return HttpResponse("Method not allowed", status = 405)

#def update(request)
