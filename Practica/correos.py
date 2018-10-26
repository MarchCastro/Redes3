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

COMMASPACE = ', '
#mailsender = "march.castrof@gmail.com"
mailreceip = "march.castrof@gmail.com"
mailserver = 'mx.my-domain.com'
mailsender = 'ruben.murga.d@gmail.com'
gmail_password = 'aqolqmlxpyvfzcpy'

def enviaCorreo_LB(mensaje,imagen):
	msg = MIMEMultipart()
	msg['From']='ruben.murga.d@gmail.com'
	msg['To']="samuel.asantiagom@gmail.com"
	
	msg['Subject']="Alerta - MiniObservium"
	msg.attach(MIMEText(mensaje))
    #print png_file
	fp = open(imagen, 'rb')
	img = MIMEImage(fp.read())
	fp.close()
	msg.attach(img)

	mailServer = smtplib.SMTP('smtp.gmail.com',587)
	
	mailServer.ehlo()
	mailServer.starttls()
	mailServer.ehlo()
	mailServer.login('ruben.murga.d@gmail.com',"aqolqmlxpyvfzcpy")
	
	mailServer.sendmail('ruben.murga.d@gmail.com', "samuel.asantiagom@gmail.com", msg.as_string())
	
	mailServer.close() 

def send_alert_attached(subject,file):
    """ Will send e-mail, attaching png
    files in the flist.
    """
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = mailsender
    msg['To'] = mailreceip
    #for file in flist:
    png_file = file
    print png_file
    fp = open(png_file, 'rb')
    img = MIMEImage(fp.read())
    fp.close()
    msg.attach(img)

    mserver = smtplib.SMTP('smtp.gmail.com',587)
    mserver.ehlo()
    mserver.starttls()
    mserver.ehlo()
    mserver.login(mailsender, gmail_password)
    mserver.sendmail(mailsender, mailreceip, msg.as_string())
    mserver.close()


def check_aberration(rrdpath, fname):
    """ This will check for begin and end of aberration
        in file. Will return:
        0 if aberration not found.
        1 if aberration begins
        2 if aberration ends
    """
    ab_status = 0
    rrdfilename = rrdpath + fname
    print rrdfilename
    info = rrdtool.info(rrdfilename)
    
    rrdstep = int(info['step'])
    print 'STEP',rrdstep
    lastupdate = info['last_update']
    print 'LASTUPD ', int(lastupdate)
    previosupdate = str(lastupdate - rrdstep - 1)
    graphtmpfile = tempfile.NamedTemporaryFile()
    
    try:
        values = rrdtool.graph(graphtmpfile.name+'F',
                                '--start', str(previosupdate),
                                '--end', str(lastupdate),
                            'DEF:f0=' + rrdfilename + ':inoctets:FAILURES',#:start=' + previosupdate + ':end=' + str(lastupdate),
                            'PRINT:f0:LAST:%1.0lf')
        print values
        
        if str(values[2][0]) == '-nan':
            print 'ERROR'
        else:
            flast = int(values[2][0])
            if (flast == 1):
                ab_status = 1
            else:
                ab_status = 2
        return ab_status
    except:
        pass
