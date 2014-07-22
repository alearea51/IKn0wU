#!/usr/bin/python
# -*- coding: utf-8 -*-

import optparse
from function import diccionario
import PyPDF2
from PyPDF2 import PdfFileReader
import datetime
import subprocess
import mechanize, urllib, urllib2
from bs4 import BeautifulSoup
from urllib import FancyURLopener
from HTMLParser import HTMLParser



outfd = open('archivo_out', 'w+')
errfd = open('archivo_err', 'w+')

print ("==========================================================================")
print ("=                                                                        =")
print ("=                                                                        =")
print ("=                                                                        =")
print ("=                                                                        =")
print ("=                                                                        =")
print ("=   W3lc0m3 t0                                                           =")
print ("=   _ _ _   _ _   _ _                                       __      __   =")
print ("=  |      ||   | /  /  _ _ _      \_|_|_/ _ _          _ _ |  |    |  |  =")
print ("=  |_    _||   |/  /  |      \    / / \ \ \  \        /  / |  |    |  |  =")
print ("=    |  |  |      /   |       \  / _ _ _ \ \  \      /  /  |  |    |  |  =")
print ("=    |  |  |      \   |        \ || / \ ||  \  \ _  /  /   |  |    |  |  =")
print ("=   _|  |_ |   \   \  |    _   | ||_\_/_||   \  / \/  /    |   \__/   |  =")
print ("=  |      ||   |\   \ |   ||   | \ \   / /    \      /     |          |  =")
print ("=  |_ _ _ ||_ _| \_ _\|_ _||_ _|  \_\_/_/      \_/\_/       \_ _ _ _ /   =")
print ("=                                 / | | \                                =")
print ("=                                                     by Sephiroot       =")
print ("=                                                                        =")
print ("=                                                                        =")
print ("=                                                                        =")
print ("=                                                                        =")
print ("=                                                                        =")
print ("=                                                                        =")
print ("==========================================================================")
print

opt = "1"
while opt < "7":
    print
    print("-----------------------------------------------------------------------")
    print
    print("1 - Whois para Dominios de Argentina")
    print("2 - Buscar Datos de una persona")
    print("3 - Buscar Datos de una persona (conociendo nombre completo y CUIT)")
    print("4 - Buscar Nro de Telefono y direccion Ingresando Titular")
    print("5 - Buscar Titular y direccion ingresando Nro de Telefono")
    print("6 - Obtener metadatos de archivo PDF")
    print("7 - Generar diccionario a partir de datos personales")
    print("8 - Salir")
    print
    opt = raw_input("Select an option:")
    if opt == "1":

        dmn = raw_input("Introduce Domain Name to scan (sin extension): ")
        print ("Elige una de las siguientes opciones:")
        print
        print ("2 - .com.ar")
        print ("3 - .gob.ar")
        print ("4 - .int.ar")
        print ("5 - .mil.ar")
        print ("6 - .net.ar")
        print ("7 - .org.ar")
        print ("8 - .tur.ar")
        print
        ext = raw_input("Opcion: ")
        
        br = mechanize.Browser()
        br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6')]
        resp = br.open('https://nic.ar')
        print ("Please wait...")
        br.open("https://nic.ar/buscarDominio.xhtml")
        
        br.select_form(nr=2)
        br['busquedaDominioForm2:dominio']= dmn
        br.find_control(name='busquedaDominioForm2:j_idt56').value = [ext] 
        br.submit()
        htmld = br.response().read()
        
        soup = BeautifulSoup(htmld)

        
        for each_div in soup.findAll('div',{'class':'ui-dt-c'}):
                print each_div.findAll(text=True)

        raw_input()    
    elif opt == "2":
        
        br = mechanize.Browser()
        br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6')]
        nom = raw_input("Introduce nombre (sin apellido): ")
        ape = raw_input("Introduce apellido: ")
        edad = raw_input("Introduce edad aproximada (si la desconoce ingrese 0): ")
        if edad == "0":   
              print ("Debera ingresar rango de anios")
              print
              anid = raw_input("Anio desde: ")
              anih = raw_input("Anio hasta: ")
              print ("Please wait...")
        else:
              actual = datetime.date.today().year 
              anid = (int(actual) - int(edad)) - 3
              anih = (int(actual) - int(edad)) + 3
              print ("Se mostraran resultados entre "+str(int(edad)- 3)+" y "+str(int(edad)+ 3)+" anios")
        
        #resp = br.open('http://buscardatos.com')
        #print resp.get_data
        br.open("http://buscardatos.com/Personas/Apellido/apellido.php?nombre="+nom+"&apellido="+ape+"&Sex=&desde="+str(anid)+"&hasta="+str(anih))
        
        htmld = br.response().read()
        class HTMLCleaner(HTMLParser):

         container  = ""
         def handle_data(self, data):
             self.container += data
             return self.container
        h = HTMLCleaner()
        h.feed(htmld)

        f = open('result', 'a')
        f.write(htmld)
        f.close()

        soup = BeautifulSoup(htmld)

        table = soup.find("table", id = "hor-minimalist-b")

        rows = table.findAll('tr')
        cabecera = ["datos","cuit","dni","edad","nombre","dir","localidad","codigo postal","ocupacion"]
        i = 0
        for tr in rows:
            cols = tr.findAll('td')
            print
            for td in cols:
                if i>=9:
                   i = 0
                
                #print cabecera[i]
                print str((cabecera[i]+": ",td.find(text=True))).decode('string_escape')     
                i = i + 1
                
        raw_input()
    elif opt == "3":
        
        br = mechanize.Browser()
        br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6')]
        nom = str(raw_input("Introduce en este orden Apellido/Nombres: "))
        cuit = str(raw_input("Introduce CUIT: "))
        print ("Please wait...")
        resp = br.open('http://buscardatos.com')
        #print resp.get_data
        br.open("http://buscardatos.com/personas.php?nombre="+nom+"&cuit="+cuit)
        
        htmld = br.response().read()
        
        soup = BeautifulSoup(htmld)
        cla = soup.findAll('class') 
        for cla in soup.findAll('p'):
                 print str(cla.findAll(text=True))
                 print



    elif opt == "4":
        nom = str(raw_input("Ingrese Apellido y Nombre: "))
        br = mechanize.Browser()
        br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6')]
        
        print ("Please wait...")
        br.open("http://www.telexplorer.com.ar/abogados")
        
        br.select_form(nr=0)
        br['nombre']= nom
        #br.find_control(name='busquedaDominioForm2:j_idt56').value = [ext] 
        br.submit()
        htmld = br.response().read()
        class HTMLCleaner(HTMLParser):

         container  = ""
         def handle_data(self, data):
             self.container += data
             return self.container
        h = HTMLCleaner()
        h.feed(htmld)
        #print h.container
        soup = BeautifulSoup(htmld)

        
        #for each_div in soup.findAll('li',{'class':'resultado'}):
                #print each_div.findAll(text=True)

        cla = soup.findAll('li' , {'class' : 'resultado_telefono'}) 
        for cla in soup.findAll('p'):
                
                print cla.findAll(text=True)
                print
        raw_input()   
   
            

           
 
    elif opt == '5': 
        area = str(raw_input("Ingrese Codigo de Area: "))
        num = str(raw_input("Ingrese Numero: "))
        br = mechanize.Browser()
        br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6')]
        
        print ("Please wait...")
        br.open("http://www.telexplorer.com.ar/fletes")
        
        br.select_form(nr=1)
        br['area']= area
        br['telefono']= num
        #br.find_control(name='busquedaDominioForm2:j_idt56').value = [ext] 
        br.submit()
        htmld = br.response().read()
        class HTMLCleaner(HTMLParser):

         container  = ""
         def handle_data(self, data):
             self.container += data
             return self.container
        h = HTMLCleaner()
        h.feed(htmld)
        #print h.container
        soup = BeautifulSoup(htmld)

        
        #for each_div in soup.findAll('li',{'class':'resultado'}):
                #print each_div.findAll(text=True)

        cla = soup.findAll('li' , {'class' : 'resultado_titulo'}) 
        for cla in soup.findAll('p'):
                
                print cla.findAll(text=True)
                print
        raw_input()

    elif opt == '7':

         nomb = raw_input("Ingrese nombre o alias: ")
         apel = raw_input("Ingrese apellido: ")
         edad = raw_input("Ingrese edad: ")
         gus =  raw_input("Ingrese gustos de la persona: ")
         org =  raw_input("Ingrese organizacion para la cual trabaja: ")
         actual = datetime.date.today().year 
         anio = (int(actual) - int(edad))
         
         diccionario(nomb,apel,edad,gus,org,anio,actual)
         
    elif opt == '6':

         pdf_name= raw_input("Ingrese nombre de Archivo PDF: ")
         print 
         fileName = pdf_name
         pdfFile = PdfFileReader(file(fileName, 'rb'))
         meta = pdfFile.getDocumentInfo()
         print ' - Documento: ' + str(fileName)
         for metaItem in meta:
             print ' - ' + metaItem + ':' + meta[metaItem]
  
    else:
        print
        print ("GoodBye!")
    
    
