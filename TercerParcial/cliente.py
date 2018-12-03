#!/usr/bin/python
from socket import timeout
import urllib
import datetime
import httplib

def pedirNumeroEntero():
 
    correcto=False
    num=0
    while(not correcto):
        try:
            num = int(input("Selecciona una opcion (numero entero 1-8):"))
            correcto=True
        except ValueError:
            print('Error, introduce un numero entero')
     
    return num
 
def tiempoRespuestaHTTP():
    #ip = str(input('Ingresa host del servidor: '))
    ip = '192.168.1.69'
    #nf = urllib.urlopen('http://'+ip).read()
    conn = httplib.HTTPSConnection(ip)
    start = datetime.datetime.now()
    print 'Inicio de solicitud: ', start 
    end = datetime.datetime.now()
    print 'Recepcion de solicitud: ', end 
    print 'Tiempo de respuesta de solicitud: ', end - start

salir = False
opcion = 0
while not salir:
    print ("\n \n \n \n")
    print ("----- Menu de opciones -----")
    print ("1. Sensor SMTP")
    print ("2. Sensor HTTP")
    print ("3. Sensor FTP")
    print ("4. Sensor FTP Server File Count")
    print ("5. Sensor de impresion")
    print ("6. Sensor de acceso remoto")
    print ("7. Administracion de archivos de configuracion")
    print ("8. Salir") 
    
 
    opcion = pedirNumeroEntero()
 
    if opcion == 1:
        print ("\n---- SENSOR SMTP ----")
    elif opcion == 2:
        print ("\n---- SENSOR HTTP ----")
        tiempoRespuestaHTTP()
    elif opcion == 3:
        print ("\n---- SENSOR FTP ----")
    elif opcion == 4:
        print ("\n---- SENSOR FTP Server File Count ----")
    elif opcion == 5:
        print ("\n---- SENSOR DE IMPRESION ----")
    elif opcion == 6:
        print ("\n---- SENSOR SSH ----")
    elif opcion == 7:
        print ("\n---- ADMINISTRACION DE ARCHIVOS DE CONFIGURACION ----")
    elif opcion == 8:
        salir = True
    else:
        print ("Introduce un numero entre 1 y 8")
 
print ("Fin")
