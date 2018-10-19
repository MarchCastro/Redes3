import os
import time
import rrdtool
import tempfile
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.encoders import encode_base64

def enviaCorreo_LB(mensaje):
	msg = MIMEMultipart()
	msg['From']='ruben.murga.d@gmail.com' 
	msg['To']="march.castrof@gmail.com"
	#msg['From']="asantiagom1401@alumno.ipn.mx" 
	#msg['To']="asantiagom1401@alumno.ipn.mx"
	msg['Subject']="Alerta - MiniObservium"
	msg.attach(MIMEText(mensaje))
	png_file = '192.168.1.66-2-LB.png'
    #print png_file
	fp = open(png_file, 'rb')
	img = MIMEImage(fp.read())
	fp.close()
	msg.attach(img)

	mailServer = smtplib.SMTP('smtp.gmail.com',587)
	#mailServer = smtplib.SMTP('smtp.office365.com',587)
	mailServer.ehlo()
	mailServer.starttls()
	mailServer.ehlo()
	mailServer.login('ruben.murga.d@gmail.com',"aqolqmlxpyvfzcpy")
	#mailServer.login("asantiagom1401@alumno.ipn.mx","7122871228")
	mailServer.sendmail('ruben.murga.d@gmail.com', "march.castrof@gmail.com", msg.as_string())
	#mailServer.sendmail("asantiagom1401@alumno.ipn.mx", "asantiagom1401@alumno.ipn.mx", msg.as_string())
	mailServer.close() 
