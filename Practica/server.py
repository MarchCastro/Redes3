#!usr/bin/python

#block_server.py

import socket
import Tkinter
import time
import os 
from Tkinter import *
from tkMessageBox import *
from pysnmp.hlapi import *
from time import sleep

ip = ''
comunnity = ''
port = ''
version = ''
agentCount = 0

#Declaro mi ventana principal
top = Tkinter.Tk()
top.title("Bienvenido a casi Observium :)")
top.geometry('400x400')

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
	while True:
		file = open("hosts.txt", "r")
		for linea in file.readlines():
			global agentCount,ip,comunnity,port
			agentCount = agentCount + 1 #Aqui esta mi contador 
			palabras = linea.split(" ")
			ip = palabras[0]
			version = palabras[1]
			port = palabras[2]
			comunnity = palabras[3]
			#print ip
			#response = os.system("ping -c 1 " + ip)
			# and then check the response...
			#if response == 0:
			#	pingstatus = "Network Active"
			#else:
			#	pingstatus = "Network Error"
		#print agentCount
		file.close() 
		sleep(0.0005)

def mib(): #No esta implementado aun
	errorIndication, errorStatus, errorIndex, varBinds = next(
    getCmd(SnmpEngine(),
           CommunityData('comunidadMarcela', mpModel=0),
           UdpTransportTarget(('localhost', 161)),
           ContextData(),
           ObjectType(ObjectIdentity('1.3.6.1.2.1.1.1.0')))
	)
	if errorIndication:
		print(errorIndication)
	elif errorStatus:
		print('%s at %s' % (errorStatus.prettyPrint(),
							errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
	else:
		for varBind in varBinds:
			print(' = '.join([x.prettyPrint() for x in varBind]))

def main():
	while True:
		file = open("hosts.txt", "r")
		for linea in file.readlines():
			global agentCount,ip,comunnity,port, version
			agentCount = agentCount + 1 #Aqui esta mi contador 
			palabras = linea.split(" ")
			ip = palabras[0]
			version = palabras[1]
			port = palabras[2]
			comunnity = palabras[3]
		
		add = Tkinter.Button(top, text ="Agregar agente", width=25, command = addClient).grid(row=0, column=0)
		delete = Tkinter.Button(top, text ="Eliminar agente", width=25, command = addClient).grid(row=1, column=0)
		agentInfo = Tkinter.Button(top, text ="Informacion de agente",width=25, command = deleteClient).grid(row=2, column=0)

		#getHostInfo()
		print agentCount
		#TITULO
		colors = ['Dispositivos monitoreados','Numero de dispositivos', 'Status de dispositivos']
		r = 3
		for c in colors:
			Label(text=c, width=25, fg='black').grid(row=r, column=0)
			r = r+1

		
		Label(text=agentCount, width=25, fg='black').grid(row=4, column=1)
		Label(text=agentCount, width=25, fg='black').grid(row=5, column=1)
		
		
		
		file.close() 
		sleep(0.0005)
		mainloop()

if __name__== '__main__': 
	main()