#!/usr/bin/python
# -*- coding: utf-8 -*-

import optparse
import re
import os
from os import listdir
from function import diccionario
from function import diccionario2
import PyPDF2
from PyPDF2 import PdfFileReader
import datetime
import subprocess
import base64
import mechanize, urllib, urllib2
from bs4 import BeautifulSoup
import Cookie
import cookielib
cj = cookielib.LWPCookieJar()



#outfd = open('archivo_out', 'w+')
#errfd = open('archivo_err', 'w+')

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
    print("1 - Buscar Datos de una persona")
    print("2 - Ver objetivos")
    print("3 - Buscar Nro de Telefono y direccion Ingresando Titular")
    print("4 - Buscar Titular y direccion ingresando Nro de Telefono")
    print("5 - Obtener direcciones de correo de sitio web")
    print("6 - Generar diccionario a partir de datos personales")
    print("7 - Obtener metadatos de archivo PDF")      
    print("8 - Salir")
    print
    opt = raw_input("Seleccione una opción:")
   
    if opt == "1":

        br = mechanize.Browser()
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
        br.open("http://buscardatos.com/Personas/Apellido/")
        br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6')]
        br.select_form(nr=0)
        br['nombre']= nom
        br['apellido']= ape
        br['desde']= str(anid)
        br['hasta']= str(anih)
        br.submit()
        
        br.open("http://buscardatos.com/Personas/Apellido/preapellidos.php")
        br.open("http://buscardatos.com/Personas/Apellido/apellido.php?nombre="+nom+"&apellido="+ape+"&Sex=&desde="+str(anid)+"&hasta="+str(anih))


        htmld = br.response().read()
        soup = BeautifulSoup(htmld)

        table = soup.find("table", attrs={"id":"hor-minimalist-b"})
        rows = table.findAll('tr')
        
        cabecera = ["datos","cuit","dni","edad","nombre","direccion","codigo postal"]
        i = 0
        for tr in rows:
            cols = tr.findAll('td')
            print
            for td in cols:
                tar = open('Targets/target.txt', 'a')
                print str(("[+]",cabecera[i]+": ",td.find(text=True))).decode('string_escape')

                if i==4:
                   try: 
                    dat = td.find(text=True)
                   except:
                    dat = "sin info"   

                else:
                   try: 
                    s = (td.find(text=True)).encode('ascii', 'replace')
                    dat = s
                   except:
                    dat = "sin info"
                if i!=0:   
                   tar.write(str(dat))
                   tar.write("\n")
                   
                if i==3:
                   nom_obj= td.find(text=True)
                   
                i = i + 1
                    
                
                if i>=7:
                   tar.close()
                   os.rename("Targets/target.txt", "Targets/"+str(nom_obj)+".txt")
                   i = 0
                   print '---------------------------------------------------------------------' 
                
                

       
        raw_input()

    elif opt == "2":
        k = 1
        obje = []
        print ""
        print "Objetivos:"
        print ""
        for cosa in listdir("Targets/"):
           print k,")",cosa
           obje.append(cosa)
           k = k + 1
        print ""   
        sel = raw_input("Ingrese numero para seleccionar objetivo: ")
        val = int(sel) - 1
        print ""
        print "Has seleccionado el archivo: ", obje[val]
        print ""
        print "Que desea hacer?"
        print ""
        print "1) Ver datos del objetivo"
        print "2) Agregar información"
        print "3) Generar diccionario para fuerza bruta"
        print "4) Intentar obtener numero de telefono de la casa"
        print ""
        opti = raw_input("Opcion:")
        
        if opti == "1":
          objetivo = open('Targets/'+obje[val], 'rb')
          dato = objetivo.read()
          print dato
          objetivo.close()
          
        if opti == "2":
          objetivo = open('Targets/'+obje[val], 'a') 
          info = raw_input('Ingrese dato para anexar al archivo')
          objetivo.write(info)
        
        if opti == "3":
           regex = '(?<=-)(.*)(?=-)'
           valor = ["","","",""] 
           w = 0
           objetivo = open('Targets/'+obje[val], 'rb')
           
           while w<3:
             line = objetivo.readline()
             print line
             if w==0:
               searchObj = re.search(regex, line)
               if not searchObj:
                continue

               match = searchObj.group()
               valor[w] = match
             elif w==2:
               ape = line.split(' ', 1)
               valor[w] = ape[0]
               nomb = ape[1].split(' ', 1)
               valor[w] = ape[0]
               valor[w+1] = nomb[0]
             else:
               valor[w] = line
             w = w + 1
           objetivo.close()
           dni=valor[0]
           apel=valor[2]
           nomb=valor[3]
           edad=valor[1]
           actual = datetime.date.today().year 
           anio = (int(actual) - int(edad))
           
         
           diccionario2(nomb,apel,edad,anio,actual,dni)

        if opti == "4":
           def buscanom(infile, n):
               with open(infile,'r') as fi:
                  for i in range(n-1):
                      fi.next()
                  return fi.next()
           
           nom = buscanom('Targets/'+obje[val],3)
           print nom
           br = mechanize.Browser()
           br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6')]
        
           print ("Please wait...")
           br.open("http://www.telexplorer.com.ar/fletes")


           def is_sblock_form(form):
             return "id" in form.attrs and form.attrs['id'] == "form_res1"

           br.select_form(predicate=is_sblock_form)
           br['nombre']= nom
           br.submit()
           htmld = br.response().read()    
           soup = BeautifulSoup(htmld)

           cla = soup.findAll({'class' : 'groupTitle'} and {'class':'searchPhone'}) 
           for cla in soup.findAll('h2'):
                
                print cla.findAll(text=True)
                print 
        

           cla = soup.findAll({'class' : 'groupTitle'} and {'class':'searchPhone'}) 
           for cla in soup.findAll('span'):
                
                print cla.findAll(text=True)
                print 
           raw_input()

    elif opt == "3":
        nom = str(raw_input("Ingrese Apellido y Nombre: "))
        br = mechanize.Browser()
        br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6')]
        
        print ("Please wait...")
        br.open("http://www.telexplorer.com.ar/fletes")

        def is_sblock_form(form):
             return "id" in form.attrs and form.attrs['id'] == "form_res1"

        br.select_form(predicate=is_sblock_form)

        
        br['nombre']= nom

        br.submit()
        htmld = br.response().read()

        soup = BeautifulSoup(htmld)

        cla = soup.findAll({'class' : 'groupTitle'} and {'class':'searchPhone'}) 
        for cla in soup.findAll('h2'):
                
                print cla.findAll(text=True)
                print 
        

        cla = soup.findAll({'class' : 'groupTitle'} and {'class':'searchPhone'}) 
        for cla in soup.findAll('span'):
                
                print cla.findAll(text=True)
                print 
        raw_input()
         
 
    elif opt == '4': 
        area = str(raw_input("Ingrese Codigo de Area: "))
        num = str(raw_input("Ingrese Numero: "))
        br = mechanize.Browser()
        br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6')]
        
        print ("Please wait...")
        br.open("http://www.telexplorer.com.ar/fletes")
        
        br.select_form(nr=1)
        br['area']= area
        br['telefono']= num
        br.submit()
        htmld = br.response().read()
        soup = BeautifulSoup(htmld)


        cla = soup.findAll('li' , {'class' : 'resultado_titulo'}) 
        for cla in soup.findAll('p'):
                
                print cla.findAll(text=True)
                print
        raw_input()

    elif opt == '5':    

         site = raw_input("Ingrese sitio web en la forma 'http://www.dominio.com': ")
         print 
         br = mechanize.Browser()
         br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6')] 
         page = br.open(site)
         source = page.read()
         soup = BeautifulSoup(source)
       
         
         for cla in soup.findAll(href=re.compile("mailto")):
          print(cla.get('href'))
          
    elif opt == '6':

         nomb = raw_input("Ingrese nombre o alias: ")
         apel = raw_input("Ingrese apellido: ")
         edad = raw_input("Ingrese edad: ")
         gus =  raw_input("Ingrese gustos de la persona: ")
         org =  raw_input("Ingrese organizacion para la cual trabaja: ")
         actual = datetime.date.today().year 
         anio = (int(actual) - int(edad))
         
         diccionario(nomb,apel,edad,gus,org,anio,actual)
         
    elif opt == '7':

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
    
    
