import Tkinter
import ttk
from Tkinter import *
from MigetSNMP import *
import rrdtool
from rrdtool import *
import sys
import os, time, threading, shutil
from pysnmp.hlapi import *
from datetime import date

#from server import graphics, ping


class Estado():
    def __init__(self, cadena):
        self.info = cadena
        self.raiz = Tk()
        self.raiz.title('Reporte de Equipo')
        self.raiz.geometry('370x300+300+0')
        self.widgets()
        self.raiz.mainloop()

    def widgets(self):
        self.definicionVariables()
        self.recuperacionInformacion()
        self.definicionWidgets()
        self.insertarWidigets()

    def definicionVariables(self):
        #formato: version puerto comunidad IP
        self.version = self.info.split(' ')[3]
        self.puerto = self.info.split(' ')[2]
        self.comunidad = self.info.split(' ')[1]
        self.ip = self.info.split(' ')[0]

        self.sistema = ''
        self.numInterfaces = ''
        self.reinicio = ''
        self.ubicacion = ''
        self.administrador = ''
        self.pic = ''

    def recuperacionInformacion(self):
        #comunidad,host,oid,puerto
        print('Recuperando informacion...')
        self.sistema = consultaSNMP2(self.comunidad , self.ip , '1.3.6.1.2.1.1.1.0',int( self.puerto ) )
        self.numInterfaces = consultaSNMP(self.comunidad , self.ip , '1.3.6.1.2.1.2.1.0',int( self.puerto ) )
        #centecimas de segundo
        self.reinicio = consultaSNMP(self.comunidad , self.ip , '1.3.6.1.2.1.1.3.0',int( self.puerto ) )
        self.ubicacion = consultaSNMPcompleto(self.comunidad , self.ip , '1.3.6.1.2.1.1.6.0',int( self.puerto ) )
        self.administrador = consultaSNMPcompleto(self.comunidad , self.ip , '1.3.6.1.2.1.1.5.0',int( self.puerto ) )

    def definicionWidgets(self):
        self.lcomunidad = ttk.Label(self.raiz, text= 'Comunidad')

        if self.sistema.find('Linux', 0, len(self.sistema)) >= 0:
            print('aqui: ' + self.sistema)
            self.pic = PhotoImage(file = 'Logo/linux.png')
        else:
            self.pic = PhotoImage(file = 'Logo/windows.png')
            print('aqui: ' + self.sistema)

        self.logo = ttk.Label(self.raiz, image= self.pic)
        self.lip = ttk.Label(self.raiz, text= 'IP')
        self.lnombre = ttk.Label(self.raiz, text= 'Sistema')
        self.lversion = ttk.Label(self.raiz, text= 'Version')
        self.lnumInterfaces = ttk.Label(self.raiz, text= 'Num. Interfaces')
        self.lreinicio = ttk.Label(self.raiz, text= 'Ultimo reinicio')
        self.lubicacion = ttk.Label(self.raiz, text= 'Ubicacion')
        self.ladministrador = ttk.Label(self.raiz, text= 'Administrador')

        self.txtcom = Text(self.raiz, width=15, height=1)
        self.txtcom.insert("1.0", self.comunidad)
        self.txtcom.config(state=DISABLED)

        self.txtIP = Text(self.raiz, width=15, height=1)
        self.txtIP.insert("1.0", self.ip)
        self.txtIP.config(state=DISABLED)

        self.txtNom = Text(self.raiz, width=15, height=1)
        self.txtNom.insert("1.0", self.sistema)
        self.txtNom.config(state=DISABLED)

        self.txtVer = Text(self.raiz, width=15, height=1)
        self.txtVer.insert("1.0", self.version)
        self.txtVer.config(state=DISABLED)

        self.txtInt = Text(self.raiz, width=15, height=1)
        self.txtInt.insert("1.0", self.numInterfaces)
        self.txtInt.config(state=DISABLED)

        self.txtRe = Text(self.raiz, width=15, height=1)
        self.txtRe.insert("1.0", self.reinicio)
        self.txtRe.config(state=DISABLED)

        self.txtUb = Text(self.raiz, width=15, height=1)
        self.txtUb.insert("1.0", self.ubicacion)
        self.txtUb.config(state=DISABLED)

        self.txtadmin = Text(self.raiz, width=15, height=1)
        self.txtadmin.insert("1.0", self.administrador)
        self.txtadmin.config(state=DISABLED)

        self.btnCerrar = ttk.Button(self.raiz, command=lambda: self.raiz.destroy(), text="Cerrar")

    def insertarWidgets(self):
        #primera fila
        self.lcomunidad.grid(column = 0 , row = 0, sticky=W,)
        self.txtcom.grid(column=1, row=0)
        self.logo.grid(column = 2 , row = 0, rowspan = 2, padx = 15, sticky = W+E+N+S)
        #segunda fila
        self.lip.grid(column = 0 , row = 1, sticky=W, pady = 5)
        self.txtIP.grid(column = 1 , row = 1)
        #tercera fila
        self.lnombre.grid(column = 0 , row = 2, sticky=W, pady = 5)
        self.txtNom.grid(column=1, row=2)
        # cuarta fila
        self.lversion.grid(column=0, row=3, sticky=W, pady = 5)
        self.txtVer.grid(column=1, row=3)
        # quinta fila
        self.lnumInterfaces.grid(column=0, row=4, sticky=W, pady = 5)
        self.txtInt.grid(column=1, row=4)
        # sexta fila
        self.lreinicio.grid(column=0, row=5, sticky=W, pady = 5)
        self.txtRe.grid(column=1, row=5)
        # septima fila
        self.lubicacion.grid(column=0, row=6, sticky=W, pady = 5)
        self.txtUb.grid(column=1, row=6)
        # octava fila
        self.ladministrador.grid(column=0, row=7, sticky=W, pady = 5)
        self.txtadmin.grid(column=1, row=7)
        #novena fila
        self.btnCerrar.grid(column=1 , row=8)






def main():
    info = 'v1 161 public 10.100.69.223'
    #mandamos llamar a la aplicacion pasando como parametro la cadena leida del archivo host
    app = Estado(info)

if __name__ == '__main__':
    main()
























def consultaSNMP(comunidad, port, host, oid):
    global resultado_final
    # print comunidad,port,host,oid
    try:
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
                   CommunityData(comunidad),
                   UdpTransportTarget((host, int(port)), timeout=0.25, retries=0),
                   ContextData(),
                   ObjectType(ObjectIdentity(oid))))
        if errorIndication:
            print(errorIndication), comunidad, host
            return None
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
            return None
        else:
            for varBind in varBinds:
                varB = (' = '.join([x.prettyPrint() for x in varBind]))
                resultado = varB.split()
                concat = []
                valid = False

                for palabra in resultado:
                    if palabra == '=':
                        valid = True
                        continue

                    if valid:
                        concat.append(palabra)
                resultado_final = ''
                for palabra in concat:
                    if palabra == '-' or palabra == 'SMP':
                        resultado_final = resultado_final + ' ' + palabra + '\n'
                    else:
                        resultado_final = resultado_final + ' ' + palabra
        return resultado_final
    except Exception as error:
        print error


def getAgentInfo(ip_community):
    print 'getAgentInfo'
    status_array = []
    interface_name_status = []
    global agentCount
    r = 6
    ro = 6
    for computer in ip_community:
        status_received = ping(computer['ip'])  # ip_for['ip]
        status_array.append(status_received)
        if status_received == 'Activa':
            agents = consultaSNMP(computer['community'], computer['port'], computer['ip'], '1.3.6.1.2.1.1.1.0')
            print agents
            if not agents:
                continue

            interfaces = consultaSNMP(computer['community'], computer['port'], computer['ip'], '1.3.6.1.2.1.2.1.0')

            for i in range(1, int(interfaces) + 1):
                name_interfaces = consultaSNMP(computer['community'], computer['port'], computer['ip'],
                                               '1.3.6.1.2.1.2.2.1.2.' + str(i))
                status_inter = consultaSNMP(computer['community'], computer['port'], computer['ip'],
                                            '1.3.6.1.2.1.2.2.1.8.' + str(i))

                if name_interfaces[1] == '0':
                    interface_name = name_interfaces[3:].decode('hex')
                    Label(text=interface_name, width=100, fg='black').grid(row=ro, column=3)
                    Tkinter.Button(text="Graficas", width=10, command=lambda
                        name=[computer['community'], computer['port'], computer['ip'],
                              '1.3.6.1.2.1.2.2.1.2.' + str(i)]: graphics(name)).grid(row=ro, column=5)
                # data = [computer['community'], computer['port'], computer['ip'], '1.3.6.1.2.1.2.2.1.2.'+str(i)]
                # widget = Tkinter.Button(text='Graficas', width = 10).grid(row=ro, column=5)
                # widget.bind('<ButtonPress -1>', lambda event, arg = data : self.graphics(event, arg))
                else:
                    Label(text=name_interfaces, width=100, fg='black').grid(row=ro, column=3)
                    # data = [computer['community'], computer['port'], computer['ip'], '1.3.6.1.2.1.2.2.1.2.'+str(i)]
                    # widget = Tkinter.Button(text='Graficas', width = 10).grid(row=ro, column=5)
                    # widget.bind('<ButtonPress -1>', lambda event, arg = data : self.graphics(event, arg))
                    Tkinter.Button(text="Graficas", width=10, command=lambda
                        name=[computer['community'], computer['port'], computer['ip'],
                              '1.3.6.1.2.1.2.2.1.2.' + str(i)]: graphics(name)).grid(row=ro, column=5)

                if int(status_inter) == 1:
                    Label(text='Activo', width=20, fg='black').grid(row=ro, column=4)
                elif int(status_inter) == 2:
                    Label(text='Inactivo', width=20, fg='black').grid(row=ro, column=4)
                elif int(status_inter) == 3:
                    Label(text='Testing', width=20, fg='black').grid(row=ro, column=4)
                ro = ro + 1

            Label(text=agents, width=70, fg='black').grid(row=r, column=0)
            Label(text=status_received, width=10, fg='black').grid(row=r, column=1)
            Label(text=interfaces, width=10, fg='black').grid(row=r, column=2)
            Tkinter.Button(text="Estado", width=10, command=graphics).grid(row=r, column=6)
            r = r + int(interfaces)
        else:
            Label(text=computer['ip'], width=70, fg='black').grid(row=r, column=0)
            Label(text=status_received, width=10, fg='black').grid(row=r, column=1)
            Label(text='Informacion no disponible', width=50, fg='black').grid(row=ro, column=3)
            r = r + 1
            ro = ro + 1

    Label(text='Numero de agentes: ' + str(agentCount), width=25, fg='black').grid(row=1, column=1)