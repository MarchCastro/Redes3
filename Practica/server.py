#!usr/bin/python

# block_server.py

import socket
import Tkinter
import time
import threading
import os
import ttk
import tkMessageBox
import subprocess
import PIL
from Tkinter import *
from tkMessageBox import showinfo
from pysnmp.hlapi import *
from time import sleep
from getSNMP import consultaSNMP
import MigetSNMP
from MigetSNMP import *
from actualizarRRD import actualizar, actualizarLB, actualizarHW
from graficarRRD import graficar
from elegirGrafica import VentanaGraficas
from PIL import Image, ImageTk

agentCount = 0
final_result = ''
#Declaro mi ventana principal
top = Tkinter.Tk()
top.title("Bienvenido a casi Observium :)")
top.geometry('1845x850')

photoFrame = Frame(top, width=1830, height=800)
photoFrame.grid()
photoFrame.rowconfigure(0, weight=1) 
photoFrame.columnconfigure(0, weight=1) 

photoCanvas = Canvas(photoFrame,width=1830, height=800)
photoCanvas.grid(row=0, column=5, sticky="nsew")

#canvasFrame = Frame(photoCanvas,  width=1830, height=800)
canvasFrame = None

#La siguiente lista contiene los limites para linea base y notificaciones
limites_LB = [30,50,60]

fields = 'Hostname', 'Version SNMP', 'Puerto', 'Comunidad'

alive_hosts = []
agentes_nombre = ''
def fetch(entries): #Recorre todos los datos que agregue y me los imprime en consola
	showinfo('Agente creado!', 'Se ha creado correctamente un agente nuevo')
	concatenation = ''
	for entry in entries:
		field = entry[0]
		text  = entry[1].get()
		concatenation = concatenation + text + ' '
		print('%s: "%s"' % (field, text)) 
	file = open("hosts.txt","a+")
	file.write(concatenation +'\n')
	file.close()
		

def makeform(root, fields): #Acomoda label en ventana de agregar agente
   entries = []
   for field in fields:
      row = Frame(root)
      lab = Label(row, width=15, text=field, anchor='w')
      ent = Entry(row)
      row.pack(side=TOP, fill=X, padx=5, pady=5)
      lab.pack(side=LEFT)
      ent.pack(side=RIGHT, expand=YES, fill=X)
      entries.append((field, ent))
   return entries

def addClient(): #Abre un recuadro a partir del recuadro principal y muestra su propio boton para 
	#llamar a la funcion fetch
   root = Tkinter.Toplevel(canvasFrame)
   root.title("Agregar un nuevo agente")
   ents = makeform(root, fields)
   root.bind('<Return>', (lambda event, e=ents: fetch(e)))   
   b1 = Button(root, text='Agregar agente',command=(lambda e=ents: fetch(e)))
   b1.pack(side=LEFT, padx=5, pady=5)

def graphics(parametros): #Abre un recuadro a partir del recuadro principal y muestra su propio boton para 
	#llamar a la funcion fetch
   #graphic_window = Tkinter.Toplevel(top)
   #graphic_window.title("Graficos")
   #print parametros
   a = VentanaGraficas(top,parametros[2],limites_LB)
   #print comunidad, puerto, ip, oid


def deleteClient():
    ventana = Toplevel()
    ventana.title('Lista de Agentes')
    ventana.geometry('500x200+500+250')

    # ttk.Style().configure("TButton", foreground='#0fbc74', background='#8c1f09')
    # definicion de variables
    IDborrar = IntVar()
    Agentes = []

    # definicion de widgets
    btnEliminar = ttk.Button(ventana, command=lambda: Eliminar(IDborrar.get(), Agentes), text='Eliminar')
    btnCerrar = ttk.Button(ventana, command=lambda: ventana.destroy(), text='Cerrar')

    # definicion de radio Buttons
    ruta = 'hosts.txt'
    archivo = open(ruta, 'r')
    while len(Agentes) > 0:
        Agentes.pop()
    while 1:
        linea = archivo.readline()
        if not linea:
            break
        else:
            Agentes.append(linea)
    archivo.close()
    listaBorrar = []

    for i in range(len(Agentes)):
        nombre = Agentes[i].split(' ')[0]  # obtenemos el hostname
        listaBorrar.append(ttk.Radiobutton(ventana, text=nombre, variable=IDborrar, value=i))
    i = 0
    for radio in listaBorrar:
        radio.grid(column=1, row=i, sticky=W)
        i = i + 1
    i = i + 1

    # establecer en pantalla los widgets
    # Modificarlo-------------------------------------------------
    btnEliminar.grid(column=0, row=i)
    btnCerrar.grid(column=2, row=i)


def Eliminar(idBorrar, Agentes):
    print('Funcion eliminar')
    pos = idBorrar
    # funcion que manda a eliminar la carpeta de este dispositivo
    ip = Agentes[pos].split(' ')[0]
    print("esta es la ip " + ip)
    os.system('rm ' + ip + '*')
    Agentes.pop(pos)
    tkMessageBox.showinfo(title='Eliminar',
                          message='Agente Eliminado')

    archivo = open("hosts.txt", "w")
    for dispositivo in Agentes:
        archivo.write(dispositivo)
    archivo.close()


def MostrarEstado(ip):
	cadena = ''
	f = open('hosts.txt', 'r')
	while 1:
		linea = f.readline()
		if not linea:
			break
		else:
			if linea.find(ip) >= 0:
				print('Encontrado: ' + linea)
				cadena = linea
			else:
				print('buscando')
	f.close()

	info = cadena
	ventana = Tkinter.Toplevel(canvasFrame)
	ventana.title('Reporte de Equipo')
	ventana.geometry('600x400')

	version = info.split(' ')[1]
	print(version)
	if version == str(1):
		version = 'v1'
	else:
		version = 'v2c'

	puerto = info.split(' ')[2]
	comunidad = info.split(' ')[3]
	ip = info.split(' ')[0]

	if comunidad.endswith('\n'):
		comunidad = comunidad[:-1]
	
	print('Recuperando informacion...')
	sistema = consultaSNMP2(comunidad, ip, '1.3.6.1.2.1.1.1.0', int(puerto))
	numInterfaces = MigetSNMP.consultaSNMP(comunidad, ip, '1.3.6.1.2.1.2.1.0', int(puerto))
	# centecimas de segundo
	reinicio = MigetSNMP.consultaSNMP(comunidad, ip, '1.3.6.1.2.1.1.3.0', int(puerto))
	ubicacion = consultaSNMPcompleto(comunidad, ip, '1.3.6.1.2.1.1.6.0', int(puerto))
	administrador = consultaSNMPcompleto(comunidad, ip, '1.3.6.1.2.1.1.5.0', int(puerto))

	print sistema, numInterfaces, reinicio, ubicacion, administrador, version, ip
	lcomunidad = ttk.Label(ventana, text='Comunidad')

	if sistema.find('Linux', 0, len(sistema)) >= 0:
		print('aqui: ' + sistema)
		pic = "Logo/linux.png"
	else:
		pic = "Logo/windows.png"
		print('aqui: ' + sistema)
	
	bar = Frame(ventana, relief=RIDGE, borderwidth=5)
	bar.grid(column=2, row=0, rowspan=2, padx=15, sticky=W)
	iconPath = pic
	icon = ImageTk.PhotoImage(Image.open(iconPath))
	icon_size = Label(bar)
	icon_size.image = icon
	icon_size.configure(image=icon)
	icon_size.pack(side=LEFT)

	lip = ttk.Label(ventana, text='IP')
	lnombre = ttk.Label(ventana, text='Sistema')
	lversion = ttk.Label(ventana, text='Version')
	lnumInterfaces = ttk.Label(ventana, text='Num. Interfaces')
	lreinicio = ttk.Label(ventana, text='Ultimo reinicio')
	lubicacion = ttk.Label(ventana, text='Ubicacion')
	ladministrador = ttk.Label(ventana, text='Administrador')

	txtcom = Text(ventana, width=50, height=1)
	txtcom.insert("1.0", comunidad)
	txtcom.config(state=DISABLED)

	txtIP = Text(ventana, width=50, height=1)
	txtIP.insert("1.0", ip)
	txtIP.config(state=DISABLED)

	txtNom = Text(ventana, width=50, height=1)
	txtNom.insert("1.0", sistema)
	txtNom.config(state=DISABLED)

	txtVer = Text(ventana, width=50, height=1)
	txtVer.insert("1.0", version)
	txtVer.config(state=DISABLED)

	txtInt = Text(ventana, width=50, height=1)
	txtInt.insert("1.0", str(numInterfaces))
	txtInt.config(state=DISABLED)

	txtRe = Text(ventana, width=50, height=1)
	txtRe.insert("1.0", str(reinicio))
	txtRe.config(state=DISABLED)

	txtUb = Text(ventana, width=50, height=1)
	txtUb.insert("1.0", ubicacion)
	txtUb.config(state=DISABLED)

	txtadmin = Text(ventana, width=50, height=1)
	txtadmin.insert("1.0", administrador)
	txtadmin.config(state=DISABLED)

	btnCerrar = ttk.Button(ventana, command=lambda: ventana.destroy(), text="Cerrar")

	# primera fila
	lcomunidad.grid(column=0, row=0, sticky=W, )
	txtcom.grid(column=1, row=0)
	'''logo.grid(column=2, row=0, rowspan=2, padx=15, sticky=W + E + N + S)'''
	# segunda fila
	lip.grid(column=0, row=1, sticky=W, pady=5)
	txtIP.grid(column=1, row=1)
	# tercera fila
	lnombre.grid(column=0, row=2, sticky=W, pady=5)
	txtNom.grid(column=1, row=2)
	# cuarta fila
	lversion.grid(column=0, row=3, sticky=W, pady=5)
	txtVer.grid(column=1, row=3)
	# quinta fila
	lnumInterfaces.grid(column=0, row=4, sticky=W, pady=5)
	txtInt.grid(column=1, row=4)
	# sexta fila
	lreinicio.grid(column=0, row=5, sticky=W, pady=5)
	txtRe.grid(column=1, row=5)
	# septima fila
	lubicacion.grid(column=0, row=6, sticky=W, pady=5)
	txtUb.grid(column=1, row=6)
	# octava fila
	ladministrador.grid(column=0, row=7, sticky=W, pady=5)
	txtadmin.grid(column=1, row=7)
	# novena fila
	btnCerrar.grid(column=1, row=8)



def update_scrollregion(event):
    photoCanvas.configure(scrollregion=photoCanvas.bbox("all"))


def getHostInfo():
	print 'holaaaaaa'
	global agentCount
	global canvasFrame
	ip_comunnity = [] # va con doble m no doble n	
	try:
		if canvasFrame == None:
			canvasFrame = Frame(photoCanvas,  width=1830, height=800)
			photoCanvas.create_window(0, 0, window=canvasFrame, anchor='nw')

			add = Tkinter.Button(canvasFrame, text ="Agregar agente", width=25, command = addClient).grid(row=0, column=0, sticky="nsew")
			delete = Tkinter.Button(canvasFrame, text="Eliminar agente", width=25, command=deleteClient).grid(row=1, column=0,sticky="nsew")
			#agentInfo = Tkinter.Button(canvasFrame, text ="Informacion de agente",width=25, command = deleteClient).grid(row=2, column=0, sticky="nsew")

			#getHostInfo()

			Label(canvasFrame, text='Dispositivos monitoreados', width=25, fg='black').grid(row=0, column=1, sticky="nsew")

			title = ['Nombre del agente', 'Status', 'No. de interfaces', 'Nombre interfaz', 'Status interfaz']
			col = 0
			row = 3
			for c in title:
				Label(canvasFrame, text=c, width=20, fg='black').grid(row=row, column=col, sticky="nsew")
				col = col + 1
			
			file = open("hosts.txt", "r")
			agentCount = 0
			for linea in file.readlines():
				palabras = linea.split(" ")
				agentCount = agentCount + 1 #Aqui esta mi contador
				if palabras[3].endswith('\n'):
					palabras[3] = palabras[3][:-1]
					ip_comunnity.append({'ip' : str(palabras[0]), 'port' : str(palabras[2]), 'community' : str(palabras[3])})
				else:
					ip_comunnity.append({'ip' : str(palabras[0]), 'port' : str(palabras[2]), 'community' : str(palabras[3])})

			getAgentInfo(ip_comunnity)
			file.close()
			photoScroll = Scrollbar(photoFrame, orient=VERTICAL)
			photoScroll.config(command=photoCanvas.yview)
			photoCanvas.config(yscrollcommand=photoScroll.set)
			photoScroll.grid(row=0, column=1, sticky="ns")

			hsbar = Scrollbar(photoFrame, orient=HORIZONTAL, command=photoCanvas.xview)
			photoCanvas.config(xscrollcommand=hsbar.set)
			hsbar.grid(row=1, column=5, sticky="ew")
			
			canvasFrame.bind("<Configure>", update_scrollregion)
			top.after(30000,getHostInfo)
	except Exception as error: 
   		#pass
		print error


def ping(ip):
    # response = os.system("ping -c 1 -q" + ip)
    with open(os.devnull, 'w') as DEVNULL:
        try:
            subprocess.check_call(
                ['ping', '-c', '1', ip],
                stdout=DEVNULL,  # suppress output
                stderr=DEVNULL
            )
            is_up = 'Activa'
            alive_hosts.append(ip)
        except subprocess.CalledProcessError:
            is_up = 'Inactiva'
    print is_up
    return is_up


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
            print(errorIndication), comunidad, host, oid
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


def eliminarAgente(ip):
	global agentes_nombre
	global canvasFrame
	print 'ip a eliminar',ip
	ip_Guardar = ''
	try:
		file = open("hosts.txt", "r")
		for linea in file.readlines():
			#print 'Entre for'
			palabras = linea.split(" ")
			#print palabras[0]
			if ip != palabras[0]:
				ip_Guardar = ip_Guardar + linea
			else:
				pass
		file.close()
		file = open("hosts.txt", "w")
		file.write(ip_Guardar)
		file.close()
		#photoCanvas.delete(agentes_nombre)
		#photoCanvas.update()
		#agentes.pack_forget()
		canvasFrame.destroy()
		canvasFrame = None
		showinfo('Agente eliminado!', 'Se ha eliminado correctamente el agente')
		main()
	except Exception as error: 
   		print error

def getAgentInfo(ip_community):
	print 'getAgentInfo'
	status_array = []
	interface_name_status= []
	global agentCount
	r = 6
	ro = 6
	for computer in ip_community:
		status_received = ping(computer['ip']) #ip_for['ip]
		status_array.append(status_received)
		if status_received == 'Activa':
			print('\n * * * * * * * *\nEl status es: ' + status_received)
			agents = consultaSNMP(computer['community'], computer['port'], computer['ip'],'1.3.6.1.2.1.1.1.0')
			print agents
			if not agents:
				continue
			
			interfaces = consultaSNMP(computer['community'], computer['port'], computer['ip'], '1.3.6.1.2.1.2.1.0')
			print interfaces
			for i in range(1,int(interfaces)+1):
				name_interfaces = consultaSNMP(computer['community'], computer['port'], computer['ip'], '1.3.6.1.2.1.2.2.1.2.'+str(i))
				status_inter = consultaSNMP(computer['community'], computer['port'], computer['ip'], '1.3.6.1.2.1.2.2.1.8.'+str(i))
				
				if name_interfaces[1] == '0':
					interface_name = name_interfaces[3:].decode('hex')
					Label(canvasFrame, text=interface_name, width=100, fg='black').grid(row=ro, column=3, sticky="nsew")
				else:
					Label(canvasFrame, text=name_interfaces, width=100, fg='black').grid(row=ro, column=3, sticky="nsew")
				
				if int(status_inter) == 1:
					Label(canvasFrame, text='Activo', width=20, fg='black').grid(row=ro, column=4, sticky="nsew")
				elif int(status_inter) == 2:
					Label(canvasFrame, text='Inactivo', width=20, fg='black').grid(row=ro, column=4, sticky="nsew")
				elif int(status_inter) == 3:
					Label(canvasFrame, text='Testing', width=20, fg='black').grid(row=ro, column=4, sticky="nsew")
				ro = ro + 1
			
			agentes_nombre = Label(canvasFrame, text=agents, width=70, fg='black').grid(row=r, column=0, sticky="nsew")
			Label(canvasFrame, text=status_received, width=10, fg='black').grid(row=r, column=1, sticky="nsew")
			Label(canvasFrame, text=interfaces, width=10, fg='black').grid(row=r, column=2, sticky="nsew")
			Tkinter.Button(canvasFrame, text ="Graficas",width=10, command= lambda  name = [computer['community'], computer['port'], computer['ip'], '1.3.6.1.2.1.2.2.1.2.'+str(i)] : graphics(name)).grid(row=r, column=5, sticky="nsew")
			Tkinter.Button(canvasFrame, text ="Estado",width=10, command = lambda name = computer['ip']: MostrarEstado(name)).grid(row=r, column=6, sticky="nsew")
			Tkinter.Button(canvasFrame, text ="Eliminar",width=10, command = lambda  name = computer['ip'] : eliminarAgente(name)).grid(row=r, column=7, sticky="nsew")
			r = r + int(interfaces)
		else:
			Label(canvasFrame, text = computer['ip'], width=70, fg='red').grid(row=r, column=0, sticky="nsew")
			Label(canvasFrame, text=status_received, width=10, fg='red').grid(row=r, column=1, sticky="nsew")
			Label(canvasFrame, text='Informacion no disponible', width=50, fg='red').grid(row=ro, column=3, sticky="nsew")
			Tkinter.Button(canvasFrame, text ="Eliminar",width=10, command = lambda  name = computer['ip'] : eliminarAgente(name)).grid(row=r, column=7, sticky="nsew")
			r = r + 1
			ro = ro + 1

	Label(canvasFrame, text='Numero de agentes: ' + str(agentCount), width=25, fg='black').grid(row=1, column=1, sticky="nsew")
	
	#Inicia actualizaciones de las BD de cada host encontrado y vivo
	inicia_capturas()


def inicia_capturas():
	print "Iniciando..."
	hilos = []
	hilosLB = []
	hilosHW = []
	with open("hosts.txt", 'r') as hosts:
		for i in hosts.readlines():
			datos = i.split(' ')
			for j in alive_hosts:
				if j == datos[0] and datos[0] != "127.0.0.1":  # Si esta vivo inicia un hilo con sus actualizaciones
					if datos[3].endswith('\n'):
						datos[3] = datos[3][:-1]
						
					# Hilos de actualizacion de rrd primer parcial y linea base
					thread = threading.Thread(target=actualizar, args=(
					'Actualizando ' + datos[0] + ' ' + datos[3], datos[3], datos[0], datos[2],
					datos[0] + '-net',))
					
					# Hilos de actualizacion de rrd con Linea Base (ram, cpu, disco)
					threadLB = threading.Thread(target=actualizarLB, args=(
					'Actualizando LB' + datos[0] + ' ' + datos[3], datos[3], datos[0], datos[2],
					datos[0]+'_LB',limites_LB,))

					# Hilos de actualizacion de rrd con Holt Winters
					threadHW = threading.Thread(target=actualizarHW, args=(
					'Actualizando HW' + datos[0] + ' ' + datos[3], datos[3], datos[0], datos[2],
					datos[0]+'_HW',))

					thread.daemon = True
					threadLB.daemon = True
					threadHW.daemon = True
					hilos.append(thread)
					hilosLB.append(threadLB)
					hilosHW.append(threadHW)
					break

	for h in hilos:
		h.start()
	for h in hilosLB:
		h.start()		
	for h in hilosHW:
		h.start()	


def main():
	print 'main'
	top.after(0, getHostInfo)
	top.mainloop()



if __name__ == '__main__':
    main()
