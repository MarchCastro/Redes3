import rrdtool as rrdtool
import notify
from time import ctime

def graficarLectura(nombre , hora , upper, ds, fallo2):

    #fallo2 = int(notify.check_CPU2(nombre, ds, upper, hora))
    str_fallo = ctime(fallo2).split(':')

    hora_final = str(fallo2 + 600)  # str(int(hora) + int(fallo) ) #rrdtool.last(nombre) + 15000

    try:
        ret = rrdtool.graph(nombre.split('.')[0] + '.png',
                            "--start", hora,
                            "--end", hora_final,
                            "--vertical-label=uso CPU",
                            "--title=Uso de CPU",
                            "--color", "ARROW#009900",
                            '--vertical-label', "Uso de CPU (%)",
                            '--lower-limit', '0',
                            '--upper-limit', '100',
                            "DEF:carga=" + nombre + ':' + ds + ':LAST',  # trend.rrd:CPUload:AVERAGE
                            "AREA:carga#00FF00:CPU usage",

                            "LINE1:" + upper + "#FF0000: Upper Limit",  # "LINE1:50#FF0000: Limite"
                            "VDEF:a=carga,LSLSLOPE",
                            "VDEF:b=carga,LSLINT",
                            'CDEF:avg2=carga,POP,a,COUNT,*,b,+',
                            # "GPRINT:avg2:AVERAGE:%7.0lf",
                            # 'PRINT:avg2:AVERAGE:%1.0lf',
                            "LINE2:avg2#FFBB00:MMC",
                            'VRULE:' + str(fallo2) + '#f72ce9:Fallo',
                            "COMMENT:        Prediction Detected at  " + str_fallo[0] + '.' + str_fallo[1] + '.' +
                            str_fallo[2])
        return 'Exito'
    except:
        return 'Error'

    #notify.send_alert_attached('Fallo en carga CPU', nombre)
