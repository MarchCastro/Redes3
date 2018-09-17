#!usr/bin/python

#block_server.py

import socket
import Tkinter
import time
import os 
import threading
from Tkinter import *
from tkMessageBox import *
from pysnmp.hlapi import *
from time import sleep
from threading import Thread 

ip = []
comunnity = []
port = []
version = []
agentCount = 0
final_result = ''
#Declaro mi ventana principal
top = Tkinter.Tk()
top.title("Bienvenido a casi Observium :)")
top.geometry('2080x800')
scrollbar = Scrollbar(top)

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
	file.write(concatenation)
	file.write('\n')
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
   #root = Tk()
   root = Tkinter.Toplevel(top)
   root.title("Agregar un nuevo agente")
   ents = makeform(root, fields)
   root.bind('<Return>', (lambda event, e=ents: fetch(e)))   
   b1 = Button(root, text='Agregar agente',command=(lambda e=ents: fetch(e)))
   b1.pack(side=LEFT, padx=5, pady=5)
   #b2 = Button(root, text='Quit', command=root.quit)
   #b2.pack(side=LEFT, padx=5, pady=5)

def deleteClient():
	tkMessageBox.showinfo( "Agregar un nuevo agente", "Hello World")

def getHostInfo():
	#while True:
	global agentCount
	global ip,comunnity,port
	agentCount = 0
	ip = []
	comunnity = []
	file = open("hosts.txt", "r")
	for linea in file.readlines():
		#global ip,comunnity,port
		agentCount = agentCount + 1 #Aqui esta mi contador 
		palabras = linea.split(" ")
		#ip = palabras[0]
		ip.append(palabras[0])
		#version = palabras[1]
		#port = palabras[2]
		comunnity.append(palabras[3])
		#print ip,comunnity
	getAgentInfo(ip,comunnity)
	#print agentCount
	Label(text='Numero de agentes: ' + str(agentCount), width=25, fg='black').grid(row=1, column=1)
	file.close()
	scrollbar.pack(side = 'right', fill= Y)
	#getAgentStatus()
	top.after(30000,getHostInfo)

def ping(ip):
	response = os.system("ping -c 1 " + ip)
	if response == 0:
		#print ip, 'Activa'
		status = 'Activa'
	else:
		#print ip, 'Inactiva'
		status = 'Inactiva'
	return status

def consultaSNMP(comunidad,host,oid):
	#print comunidad, host
	errorIndication, errorStatus, errorIndex, varBinds = next(
		getCmd(SnmpEngine(),
			CommunityData(comunidad),
			UdpTransportTarget((host, 161)),
			ContextData(),
			ObjectType(ObjectIdentity(oid))))

	if errorIndication:
		print(errorIndication)
	elif errorStatus:
		print('%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
	else:
		for varBind in varBinds:
			varB=(' = '.join([x.prettyPrint() for x in varBind]))
			result= varB.split()
			concat = []
			valid = False

		for palabra in result: 
			if palabra == '=':
				valid = True
				continue 
				
			if valid:
				concat.append(palabra)

		global final_result
		final_result = ''
		for palabra in concat:
			final_result = final_result + ' ' + palabra
	return final_result


def getAgentInfo(ip,comunnity):
	info_array = []
	status_array = []
	interfaces_number = []
	interfaces_name = []
	interfaces_status = []
	for ip_for,community_for in zip(ip,comunnity):
		#print ip_for, community_for
		#agents = consultaSNMP(community_for,ip_for, '1.3.6.1.2.1.1.1.0')
		agents = consultaSNMP('comunidadMarcela','127.0.0.1', '1.3.6.1.2.1.1.1.0')
		interfaces = consultaSNMP('comunidadMarcela','127.0.0.1', '1.3.6.1.2.1.2.1.0')
		info_array.append(agents)
		interfaces_number.append(interfaces)
		for i in range(1,int(interfaces)+1):
			name_interfaces = consultaSNMP('comunidadMarcela','127.0.0.1', '1.3.6.1.2.1.2.2.1.2.'+str(i))

			status_inter = consultaSNMP('comunidadMarcela','127.0.0.1', '1.3.6.1.2.1.2.2.1.8.'+str(i))
			#print 'Status', status_inter
			interfaces_name.append(name_interfaces)
			interfaces_status.append(status_inter)
			#print name_interfaces			

	for ip_for in zip(ip):
		status_received = ping('127.0.0.1')
		status_array.append(status_received)	
		

	r = 6
	for info,status,interfacesN in zip(info_array,status_array,interfaces_number):
		Label(text=info, width=85, fg='black').grid(row=r, column=0)
		Label(text=status, width=10, fg='black').grid(row=r, column=1)
		Label(text=interfacesN, width=10, fg='black').grid(row=r, column=2)
		r = r + int(interfacesN)
		#Label(text=agents, width=100, height=20, fg='black').grid(row=5, column=1)
	r = 6
	for name, status in zip(interfaces_name, interfaces_status):
		Label(text=name, width=25, fg='black').grid(row=r, column=3)
		'''if status_inter == 1:
				interfaces_status.append('Activo')
			elif status_inter == 2:
				interfaces_status.append('Inactivo')
			elif status_inter == 3:
				interfaces_status.append('Testing')'''
		if int(status) == 1:
			Label(text='Activo', width=20, fg='black').grid(row=r, column=4)
		elif int(status) == 2:
			Label(text='Inactivo', width=20, fg='black').grid(row=r, column=4)
		elif int(status) == 3:
			Label(text='Testing', width=20, fg='black').grid(row=r, column=4)
		#Label(text=status, width=20, fg='black').grid(row=r, column=4)
		r = r+1

def main():
	add = Tkinter.Button(top, text ="Agregar agente", width=25, command = addClient).grid(row=0, column=0)
	delete = Tkinter.Button(top, text ="Eliminar agente", width=25, command = addClient).grid(row=1, column=0)
	agentInfo = Tkinter.Button(top, text ="Informacion de agente",width=25, command = deleteClient).grid(row=2, column=0)

	getHostInfo()
	#getAgentStatus()
	#print agentCount
	#TITULO
	Label(text='Dispositivos monitoreados', width=20, fg='black').grid(row=0, column=1)

	title = ['Nombre del agente', 'Status', 'No. de interfaces', 'Nombre interfaz', 'Status interfaz']
	col = 0
	row = 3
	for c in title:
		Label(text=c, width=20, fg='black').grid(row=row, column=col)
		col = col + 1

	top.after(0, getHostInfo)
	top.mainloop()

if __name__== '__main__': 
	main()