from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.encoders import encode_base64
import smtplib

def enviaCorreo_LB(mensaje):
	msg = MIMEMultipart()
	msg['From']="asantiagom1401@alumno.ipn.mx" 
	msg['To']="asantiagom1401@alumno.ipn.mx"
	msg['Subject']="Alerta - MiniObservium"
	msg.attach(MIMEText(mensaje))
	mailServer = smtplib.SMTP('smtp.office365.com',587)
	mailServer.ehlo()
	mailServer.starttls()
	mailServer.ehlo()
	mailServer.login("asantiagom1401@alumno.ipn.mx","7122871228")
	mailServer.sendmail("asantiagom1401@alumno.ipn.mx", "asantiagom1401@alumno.ipn.mx", msg.as_string())
	mailServer.close() 
