#!/usr/bin/python

import subprocess
import mechanize, urllib, urllib2
from bs4 import BeautifulSoup
from urllib import FancyURLopener
from HTMLParser import HTMLParser

resp = "n"
while resp=="n":

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

    print("1 - Whois para Dominios de Argentina")
    print("2 - Buscar Datos")
    print("3 - Buscar Datos (conociendo nombre completo y CUIT)")
    print("4 - Buscar Nro de Telefono Ingresando Titular")
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

    elif opt == "2":
        
        br = mechanize.Browser()
        br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6')]
        nom = raw_input("Introduce nombre: ")
        ape = raw_input("Introduce apellido: ")
        anid = raw_input("Anio desde: ")
        anih = raw_input("Anio hasta: ")
        print ("Please wait...")
        #resp = br.open('http://buscardatos.com')
        #print resp.get_data
        br.open("http://buscardatos.com/Personas/Apellido/apellido.php?nombre="+nom+"&apellido="+ape+"&Sex=&desde="+anid+"&hasta="+anih)
        
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
                print (cabecera[i]+": ",td.find(text=True))   
                i = i + 1
                

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

        cla = soup.findAll('li' , {'class' : 'resultado'}) 
        for cla in soup.findAll('p'):
                
                print cla.findAll(text=True)
                print
                
    else: 
        br = mechanize.Browser()
        br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6')]
        #resp = br.open('http://buscardatos.com')
        print ("Please wait...")
        br.open("http://buscardatos.com/Personas/DNI/")
        
        br.select_form(name="input")
        br['DNI']= "31616783"
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
        print h.container

    print
    resp = raw_input("Desea salir? s/n  ")
    
