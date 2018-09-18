#!usr/bin/python

#block_server.py

import socket
import Tkinter 
import time
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
top.geometry('2080x800')
'''frame_main = Frame(top)
frame_main.grid(sticky='news')

canvas = Canvas(frame_main)
canvas.grid(row=0, column=0, sticky="news")
canvas.grid_columnconfigure(0, minsize=20)
canvas.grid_rowconfigure(0, minsize=20)
# Link a scrollbar to the canvas
vsb = Scrollbar(frame_main, orient="vertical", command=canvas.yview)
vsb.grid_rowconfigure(0, minsize=20)
canvas.configure(yscrollcommand=vsb.set)
canvas.config(scrollregion=canvas.bbox("all"))'''

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
   root = Tkinter.Toplevel(top)
   root.title("Agregar un nuevo agente")
   ents = makeform(root, fields)
   root.bind('<Return>', (lambda event, e=ents: fetch(e)))   
   b1 = Button(root, text='Agregar agente',command=(lambda e=ents: fetch(e)))
   b1.pack(side=LEFT, padx=5, pady=5)

def graphics(): #Abre un recuadro a partir del recuadro principal y muestra su propio boton para 
	#llamar a la funcion fetch
   graphic_window = Tkinter.Toplevel(top)
   graphic_window.title("Graficos")
   ents = makeform(graphic_window, fields) 
   b1 = Button(root, text='Agregar agente',command='AQUI TU MENU')
   b1.pack(side=LEFT, padx=5, pady=5)

def deleteClient():
	tkMessageBox.showinfo( "Agregar un nuevo agente", "Hello World")

def getHostInfo():
	ip_comunnity = [] # va con doble m no doble n	
	try:
		file = open("hosts.txt", "r")
		for linea in file.readlines():
			palabras = linea.split(" ")
			if palabras[3].endswith('\n'):
				palabras[3] = palabras[3][:-1]
				ip_comunnity.append({'ip' : str(palabras[0]), 'community' : str(palabras[3])})
			else:
				ip_comunnity.append({'ip' : str(palabras[0]), 'community' : str(palabras[3])})

		getAgentInfo(ip_comunnity)
		file.close()
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
	return is_up

def consultaSNMP(comunidad,host,oid):
	global resultado_final
	try:
		errorIndication, errorStatus, errorIndex, varBinds = next(
			getCmd(SnmpEngine(),
					CommunityData(comunidad),
					UdpTransportTarget((host, 161), timeout=0.25, retries=0),
					ContextData(),
					ObjectType(ObjectIdentity(oid))))
		if errorIndication:
			print(errorIndication),comunidad,host
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
	status_array = []
	interface_name_status= []
	global agentCount
	agentCount = 0
	r = 6
	for computer in ip_community:
		status_received = ping(computer['ip']) #ip_for['ip]
		status_array.append(status_received)
		if status_received != 'Activa':
			continue	

		agents = consultaSNMP(computer['community'],computer['ip'], '1.3.6.1.2.1.1.1.0')
		if not agents:
			continue
		
		agentCount = agentCount + 1 #Aqui esta mi contador
		interfaces = consultaSNMP(computer['community'],computer['ip'], '1.3.6.1.2.1.2.1.0')

		for i in range(1,int(interfaces)+1):
			name_interfaces = consultaSNMP(computer['community'],computer['ip'], '1.3.6.1.2.1.2.2.1.2.'+str(i))
			status_inter = consultaSNMP(computer['community'],computer['ip'], '1.3.6.1.2.1.2.2.1.8.'+str(i))
			if name_interfaces[1] == '0':
				interface_name_status.append({'interface_name' : name_interfaces[3:].decode('hex'), 'interface_status' : status_inter})
			else:
				interface_name_status.append({'interface_name' : name_interfaces, 'interface_status' : status_inter})
		
		
		Label(text=agents, width=70, fg='black').grid(row=r, column=0)
		Label(text=status_received, width=10, fg='black').grid(row=r, column=1)
		Label(text=interfaces, width=10, fg='black').grid(row=r, column=2)
		Tkinter.Button(text ="Graficas",width=10, command = graphics).grid(row=r, column=5)
		r = r + int(interfaces)
	
	Label(text='Numero de agentes: ' + str(agentCount), width=25, fg='black').grid(row=1, column=1)
		
	r = 6
	for inter_value in interface_name_status:
		Label(text=inter_value['interface_name'], width=100, fg='black').grid(row=r, column=3)

		if int(inter_value['interface_status']) == 1:
			Label(text='Activo', width=20, fg='black').grid(row=r, column=4)
		elif int(inter_value['interface_status']) == 2:
			Label(text='Inactivo', width=20, fg='black').grid(row=r, column=4)
		elif int(inter_value['interface_status']) == 3:
			Label(text='Testing', width=20, fg='black').grid(row=r, column=4)
		#Label(text=status, width=20, fg='black').grid(row=r, column=4)
		r = r+1

def main():

	add = Tkinter.Button(top, text ="Agregar agente", width=25, command = addClient).grid(row=0, column=0)
	delete = Tkinter.Button(top, text ="Eliminar agente", width=25, command = addClient).grid(row=1, column=0)
	agentInfo = Tkinter.Button(top, text ="Informacion de agente",width=25, command = deleteClient).grid(row=2, column=0)
	agentInfo = Tkinter.Button(top, text ="Informacion de agente",width=25, command = deleteClient).grid(row=2, column=0)

	getHostInfo()

	Label(text='Dispositivos monitoreados', width=25, fg='black').grid(row=0, column=1)

	title = ['Nombre del agente', 'Status', 'No. de interfaces', 'Nombre interfaz', 'Status interfaz']
	col = 0
	row = 3
	for c in title:
		Label(text=c, width=20, fg='black').grid(row=row, column=col)
		col = col + 1

	top.after(30000, getHostInfo)
	top.mainloop()

if __name__== '__main__': 
	main()