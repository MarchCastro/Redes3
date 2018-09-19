#!usr/bin/python

#block_server.py

import socket
import Tkinter 
import time
import threading
import os
import subprocess
from Tkinter import *
from tkMessageBox import showinfo
from pysnmp.hlapi import *
from time import sleep

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

canvasFrame = Frame(photoCanvas,  width=1830, height=800)
photoCanvas.create_window(0, 0, window=canvasFrame, anchor='nw')

fields = 'Hostname', 'Version SNMP', 'Puerto', 'Comunidad'

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
   graphic_window = Tkinter.Toplevel(top)
   graphic_window.title("Graficos")
   print parametros
   #print comunidad, puerto, ip, oid

def deleteClient():
	tkMessageBox.showinfo( "Agregar un nuevo agente", "Hello World")

def update_scrollregion(event):
    photoCanvas.configure(scrollregion=photoCanvas.bbox("all"))

def getHostInfo():
	print 'holaaaaaa'
	global agentCount
	ip_comunnity = [] # va con doble m no doble n	
	try:
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
	except: 
   		pass

def ping(ip):
	#response = os.system("ping -c 1 -q" + ip)
	with open(os.devnull, 'w') as DEVNULL:
		try:
			subprocess.check_call(
			['ping', '-c', '1', ip],
				stdout=DEVNULL,  # suppress output
				stderr=DEVNULL
			)
			is_up = 'Activa'
		except subprocess.CalledProcessError:
			is_up = 'Inactiva'
	print is_up
	return is_up

def consultaSNMP(comunidad,port,host,oid):
	global resultado_final
	#print comunidad,port,host,oid
	try:
		errorIndication, errorStatus, errorIndex, varBinds = next(
			getCmd(SnmpEngine(),
					CommunityData(comunidad),
					UdpTransportTarget((host, int(port)), timeout=0.25, retries=0),
					ContextData(),
					ObjectType(ObjectIdentity(oid))))
		if errorIndication:
			print(errorIndication),comunidad,host,oid
			return None
		elif errorStatus:
			print('%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
			return None
		else:
			for varBind in varBinds:
				varB=(' = '.join([x.prettyPrint() for x in varBind]))
				resultado= varB.split()
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
	interface_name_status= []
	global agentCount
	r = 6
	ro = 6
	for computer in ip_community:
		status_received = ping(computer['ip']) #ip_for['ip]
		status_array.append(status_received)
		if status_received == 'Activa':
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
					Tkinter.Button(canvasFrame, text ="Graficas",width=10, command= lambda  name = [computer['community'], computer['port'], computer['ip'], '1.3.6.1.2.1.2.2.1.2.'+str(i)] : graphics(name)).grid(row=ro, column=5, sticky="nsew")
				else:
					Label(canvasFrame, text=name_interfaces, width=100, fg='black').grid(row=ro, column=3, sticky="nsew")
					Tkinter.Button(canvasFrame, text ="Graficas",width=10, command = lambda  name = [computer['community'], computer['port'], computer['ip'], '1.3.6.1.2.1.2.2.1.2.'+str(i)] : graphics(name)).grid(row=ro, column=5, sticky="nsew")
				
				if int(status_inter) == 1:
					Label(canvasFrame, text='Activo', width=20, fg='black').grid(row=ro, column=4, sticky="nsew")
				elif int(status_inter) == 2:
					Label(canvasFrame, text='Inactivo', width=20, fg='black').grid(row=ro, column=4, sticky="nsew")
				elif int(status_inter) == 3:
					Label(canvasFrame, text='Testing', width=20, fg='black').grid(row=ro, column=4, sticky="nsew")
				ro = ro + 1
			
			Label(canvasFrame, text=agents, width=70, fg='black').grid(row=r, column=0, sticky="nsew")
			Label(canvasFrame, text=status_received, width=10, fg='black').grid(row=r, column=1, sticky="nsew")
			Label(canvasFrame, text=interfaces, width=10, fg='black').grid(row=r, column=2, sticky="nsew")
			Tkinter.Button(canvasFrame, text ="Estado",width=10, command = graphics).grid(row=r, column=6, sticky="nsew")
			r = r + int(interfaces)
		else:
			Label(canvasFrame, text = computer['ip'], width=70, fg='red').grid(row=r, column=0, sticky="nsew")
			Label(canvasFrame, text=status_received, width=10, fg='red').grid(row=r, column=1, sticky="nsew")
			Label(canvasFrame, text='Informacion no disponible', width=50, fg='red').grid(row=ro, column=3, sticky="nsew")
			r = r + 1
			ro = ro + 1

	Label(canvasFrame, text='Numero de agentes: ' + str(agentCount), width=25, fg='black').grid(row=1, column=1, sticky="nsew")

def main():

	add = Tkinter.Button(canvasFrame, text ="Agregar agente", width=25, command = addClient).grid(row=0, column=0, sticky="nsew")
	delete = Tkinter.Button(canvasFrame, text ="Eliminar agente", width=25, command = addClient).grid(row=1, column=0, sticky="nsew")
	agentInfo = Tkinter.Button(canvasFrame, text ="Informacion de agente",width=25, command = deleteClient).grid(row=2, column=0, sticky="nsew")

	#getHostInfo()

	Label(canvasFrame, text='Dispositivos monitoreados', width=25, fg='black').grid(row=0, column=1, sticky="nsew")

	title = ['Nombre del agente', 'Status', 'No. de interfaces', 'Nombre interfaz', 'Status interfaz']
	col = 0
	row = 3
	for c in title:
		Label(canvasFrame, text=c, width=20, fg='black').grid(row=row, column=col, sticky="nsew")
		col = col + 1

	top.after(0, getHostInfo)
	top.mainloop()

if __name__== '__main__': 
	main()