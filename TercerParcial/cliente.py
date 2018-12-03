#!/usr/bin/python
from socket import timeout
import urllib
import datetime
import httplib
import os
import paramiko
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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

def sensor_correo():
    '''
    Antes de ejecutar la funcion se debe establecer una conexion
    inicial con el servidor ssh para intercambiar firmas.
    '''
    ssh_hostname = '192.168.0.32' # IP del servidor
    ssh_port = 22
    ssh_username = 'root'
    ssh_password = 'hola123.,'
    
    sender = 'root'
    sender_pass = 'hola123.,'
    receiver = 'marcela@redes3.local'
    server = 'server1.redes3.local' # Cambiar la IP en /etc/hosts
    email_port = 25

    correo = MIMEMultipart()
    correo['From'] = sender
    correo['To'] = receiver
    correo['Subject'] = "sensor-SMTP-redes3.local"
    correo.attach(MIMEText('Correo de prueba - Hacer caso omiso.'))

    mailServer = smtplib.SMTP(server,25)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    #mailServer.login(sender,sender_pass)
    tiempo_inicio = int(round(time.time() * 1000)) # Milisegundos
    #print 'Tiempo inicial: '+str(tiempo_inicio)
    mailServer.sendmail(sender,receiver,correo.as_string()) # No so por que se puede hacer esto sin autenticacion - checar. Si se descomenta la linea anterior el mensaje es AUTH not supported by server
    tiempo_fin_smtp = int(round(time.time() * 1000))
    tiempo_smtp = abs(tiempo_fin_smtp - tiempo_inicio)
    print 'Tiempo de respuesta SMTP: '+str(tiempo_smtp) + 'ms'
    mailServer.close()

    paramiko.util.log_to_file('paramiko.log')
    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.connect(ssh_hostname,ssh_port,ssh_username,ssh_password)
    stdin, stdout, stderr = s.exec_command("find /home/marcela/Maildir/new/ -printf '%C@\n' | tail -1") 
    tiempo_imap = abs(int(round(float(stdout.read()) * 1000)) - tiempo_inicio)
    print 'Tiempo de respuesta IMAP: ' + str(tiempo_imap) + 'ms'
    print 'Tiempo total: '+str(tiempo_smtp + tiempo_imap) + 'ms'

    stdin, stdout, stderr = s.exec_command("find /home/marcela/Maildir/new/ | tail -1")
    archivo = stdout.read()
    stdin, stdout, stderr = s.exec_command("rm "+archivo)
    s.close()

def ftp_counter():
    ssh_hostname = '192.168.0.32' # IP del servidor
    ssh_port = 22
    ssh_username = 'root'
    ssh_password = 'hola123.,'
    
    paramiko.util.log_to_file('paramiko.log')
    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.connect(ssh_hostname,ssh_port,ssh_username,ssh_password)
    stdin, stdout, stderr = s.exec_command("ls -1 /home/samuel/ | wc -l")
    print 'Numero de archivos alojados en el servidor FTP: '+stdout.read()
    s.close()

def sensor_ssh():
    ssh_hostname = '192.168.0.32' # IP del servidor
    ssh_port = 22
    ssh_username = 'root'
    ssh_password = 'hola123.,'
    
    paramiko.util.log_to_file('paramiko.log')
    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.connect(ssh_hostname,ssh_port,ssh_username,ssh_password)
    stdin, stdout, stderr = s.exec_command("netstat -tnpa | grep 'ESTABLISHED.*sshd' | wc -l")
    num = int(stdout.read())
    print 'Numero de conexiones SSH en el servidor: '+str(num)
    if(num > 0):
        print "Destino         Origen                  Usuario\n"
        stdin, stdout, stderr = s.exec_command("netstat -tnpa | grep 'ESTABLISHED.*sshd' | tr -s ' ' | cut -d' ' -f4,5,8 | tr ' ' '\t'")
        print stdout.read()
    s.close()

if __name__ == "__main__":
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
            sensor_correo()
        elif opcion == 2:
            print ("\n---- SENSOR HTTP ----")
            tiempoRespuestaHTTP()
        elif opcion == 3:
            print ("\n---- SENSOR FTP ----")
        elif opcion == 4:
            print ("\n---- SENSOR FTP Server File Count ----")
            ftp_counter()
        elif opcion == 5:
            print ("\n---- SENSOR DE IMPRESION ----")
        elif opcion == 6:
            print ("\n---- SENSOR SSH ----")
            sensor_ssh()
        elif opcion == 7:
            print ("\n---- ADMINISTRACION DE ARCHIVOS DE CONFIGURACION ----")
        elif opcion == 8:
            salir = True
        else:
            print ("Introduce un numero entre 1 y 8")
     
    print ("Fin")
