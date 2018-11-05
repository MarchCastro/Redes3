import os
import time
import rrdtool
import tempfile
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from time import ctime

def check_CPU2(name, ds, upper, inicio):
    print('checking.....')

    info = rrdtool.info(name)
    rrdstep = int(info['step'])
    estimado = int(inicio) +  rrdstep
    graphtmpfile = tempfile.NamedTemporaryFile()
    while 1:
        #print('Hora estimada = ' + str(ctime(estimado)) + ' - ' + str(estimado))
        values = rrdtool.graph(graphtmpfile.name + 'F',#name.split('.')[0] + '.png',
                               "--start", str(inicio),
                               "--end", str(estimado),
                               "DEF:carga=" + name + ':' + ds + ':LAST',  # trend.rrd:CPUload:AVERAGE
                               "VDEF:a=carga,LSLSLOPE",
                               "VDEF:b=carga,LSLINT",
                               'CDEF:avg2=carga,POP,a,COUNT,*,b,+',
                               'PRINT:avg2:LAST:%1.0lf')

        #print(values)
        try:

            fail = int(values[2][0])
            if int(fail) >= int(upper):
                print('Encontramos la falla en:' + str(estimado) )
                return estimado
            else:
                if int(fail) > int(100):
                    print('ERROR :(' + str(estimado - 150759900) )
                    return int( rrdtool.last(name) )
        except:
            print('Sin valores')

        estimado = estimado + int(rrdstep)


def send_alert_attached(subject, nombre):
    """ Will send e-mail, attaching png
    files in the flist.
    """
    mailsender = 'arturordz.ipn@gmail.com'
    # digitalnevada30@gmail.com
    mailreceip = ['arturordz.ipn@gmail.com']  # "admins@my-domain.com", "support@my-domain.com"
    mailserver = 'smtp.gmail.com'
    COMMASPACE = ', '

    pngpath = nombre + os.sep + 'IM' + os.sep

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = mailsender
    msg['To'] = COMMASPACE.join(mailreceip)
    #png_file = pngpath + 'netP.png'
    png_file = nombre.split('.')[0] + '.png'
    #print(png_file)
    fp = open(png_file, 'rb')
    while 1:
        try:
            img = MIMEImage(fp.read())
            break
        except:
            print("reintentando adjuntar.........")

    fp.close()
    msg.attach(img)
    mserver = smtplib.SMTP(mailserver , 587)
    mserver.starttls()
    mserver.login('arturordz.ipn@gmail.com', 'contrasena')
    mserver.sendmail(mailsender, mailreceip, msg.as_string())
    mserver.quit()
    print('Correo enviado Exitosamente!')
    return