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
	
	msg['Subject']="Alerta - MiniObservium"
	msg.attach(MIMEText(mensaje))
	png_file = '10.100.71.106-2-LB.png'
    #print png_file
	fp = open(png_file, 'rb')
	img = MIMEImage(fp.read())
	fp.close()
	msg.attach(img)

	mailServer = smtplib.SMTP('smtp.gmail.com',587)
	
	mailServer.ehlo()
	mailServer.starttls()
	mailServer.ehlo()
	mailServer.login('ruben.murga.d@gmail.com',"aqolqmlxpyvfzcpy")
	
	mailServer.sendmail('ruben.murga.d@gmail.com', "march.castrof@gmail.com", msg.as_string())
	
	mailServer.close() 
