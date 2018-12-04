#!/usr/bin/python
from socket import timeout
import urllib
import datetime
import httplib
import os
import paramiko
import smtplib
import time
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ftplib import FTP

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
 
def HTTPmethod():
    ip = str(input('Ingresa host del servidor: '))
    print
    #ip = '192.168.1.69'
    #nf = urllib.urlopen('http://'+ip).read()
    #Tiempo de respuesta
    conn = httplib.HTTPConnection(ip)
    start = datetime.datetime.now()
    print 'Inicio de solicitud: ', start 
    end = datetime.datetime.now()
    print 'Recepcion de solicitud: ', end 
    print 'Tiempo de respuesta de solicitud: ', end - start, 'segundos'
    #Bytes recibidos
    conn.request('GET', '/')
    res = conn.getresponse()
    data = res.read()
    print 'Bytes recibidos: ', (len(data)), 'bytes'
    #Ancho de banda    
    start = time.time()
    file = requests.get('http://'+ip)
    end = time.time()
    time_difference = end - start
    file_size = int(file.headers['Content-Length'])/1000    
    print 'Velocidad de ancho de banda', round(file_size / time_difference), 'Kb/s'
    #st = pyspeedtest.SpeedTest(ip)
    #print 'Velocidad de ancho de banda', st.download(), 'bytes por segundo'

def FTP_receive_method():
    """ip = str(input('Ingresa host del servidor: '))
    user = str(input('Ingresa el usuario: '))
    pss = str(input('Ingresa la contrasena: '))"""
    ip = '192.168.1.69'
    ftp = FTP(ip)
    #ftp.login(user,pss)
    ftp.login('marce','1596')
    ftp.cwd('/home/marce/')
    print 'Los archivos disponibles son: '
    ftp.retrlines('LIST')
    try:
        filename = str(input('Ingresa el nombre del archivo que deseas: '))
        start = time.time()
        tr_response = ftp.retrbinary('RETR '+filename, open(filename, 'wb').write)  
        print 
        end = time.time()
        print tr_response
        time_difference = end - start
        print 'Tamano de archivo recibido:', ftp.size(filename), 'bytes'
        print 'Tiempo de respuesta:', "{0:.5f}".format(time_difference), 'segundos'
    except:
        print 'Ocurrio un error al recibir el archivo'
    ftp.quit()
    ftp.close()

def FTP_upload_method():
    """ip = str(input('Ingresa host del servidor: '))
    user = str(input('Ingresa el usuario: '))
    pss = str(input('Ingresa la contrasena: '))"""
    ip = '192.168.1.69'
    ftp = FTP(ip)
    #ftp.login(user,pss)
    ftp.login('marce','1596')
    start = time.time()
    ftp.cwd('/home/marce/')
    try:
        ftp_response = ftp.storbinary("STOR " + 'prueba.jpg', open('prueba.jpg', 'r'))
        end = time.time()
        time_difference = end - start
        print
        print ftp_response
        print 'Archivo transferido: prueba.jpg'
        print 'Tamano de archivo transferido:', ftp.size('/home/marce/prueba.jpg'), 'bytes'
        print 'Tiempo de respuesta:', "{0:.5f}".format(time_difference), 'segundos'
    except:
        print 'Ocurrio un error al recibir el archivo'
    #ftp.delete('prueba.jpg')
    ftp.quit()
    ftp.close()

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

def pedirNumeroEntero2():
    correcto=False
    num=0
    while(not correcto):
        try:
            num = int(input("Selecciona una opcion (numero entero 1-3):"))
            correcto=True
        except ValueError:
            print('Error, introduce un numero entero')
    return num

def importar():
    with open("importar.conf",'r') as exportar:
        for linea in exportar.readlines():
            linea = linea.rstrip().split(' ')
            if len(linea[0]) > 0:
                if linea[0][0] != '#':
                    print linea
                    ftp = FTP(linea[0]) # Connect
                    ftp.login(linea[3],linea[4]) # Login
                    file = open(linea[2]+'.'+linea[5]+'.'+str(time.time()),'wb') # Abre archivo local
                    ftp.retrbinary('RETR %s' % linea[1],file.write) # Upload
                    ftp.quit()

def exportar():
    with open("exportar.conf",'r') as exportar:
        for linea in exportar.readlines():
            linea = linea.rstrip().split(' ')
            if len(linea[0]) > 0:
                if linea[0][0] != '#':
                    print linea
                    ftp = FTP(linea[0]) # Connect
                    ftp.login(linea[3],linea[4]) # Login
                    file = open(linea[1],'rb') # Abre archivo local
                    ftp.storbinary('STOR %s' % linea[2],file) # Upload
                    ftp.retrlines('LIST') # Lista archivos
                    ftp.quit()

def admin_conf_files():
    regresar = False
    opcion = 0
    while not regresar:
        print ("\n \n")
        print ("----- Menu de opciones de archivos de configuracion-----")
        print ("1. Importar archivos de configuracion")
        print ("2. Exportar archivos de configuracion")
        print ("3. Regresar") 
     
        opcion = pedirNumeroEntero2()
     
        if opcion == 1:
            print ("\n---- IMPORTAR ARCHIVOS DE CONFIGURACION ----")
            importar()
        elif opcion == 2:
            print ("\n---- EXPORTART ARCHIVOS DE CONFIGURACION ----")
            exportar()
        elif opcion == 3:
            regresar = True
        else:
            print ("Introduce un numero entre 1 y 3")

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
            HTTPmethod()
        elif opcion == 3:
            print ("\n---- SENSOR FTP ----")
            print '1. Descargar archivo desde servidor'
            print '2. Subir archivo a servidor'
            print '3. Salir'
            num = int(input("Selecciona una opcion (numero entero 1-3):"))
            while num != 3:    
                if num == 1:
                    FTP_receive_method()
                elif num == 2:
                    FTP_upload_method()
                print
                print ("\n---- SENSOR FTP ----")
                print '1. Descargar archivo desde servidor'
                print '2. Subir archivo a servidor'
                print '3. Salir'
                num = int(input("Selecciona una opcion (numero entero 1-3):"))
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
            admin_conf_files()
        elif opcion == 8:
            salir = True
        else:
            print ("Introduce un numero entre 1 y 8")
     
    print ("Fin")
