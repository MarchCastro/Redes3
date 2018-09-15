#!usr/bin/python

#block_server.py

import socket
import Tkinter
import os 
from Tkinter import *
from tkMessageBox import *
from pysnmp.hlapi import *

ip = ''
comunnity = ''
port = ''
agentCount = 0
#Declaro mi ventana principal
top = Tkinter.Tk()
top.title("Bienvenido a casi Observium :)")
top.geometry('350x200')

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

def ping():
	file = open("hosts.txt", "r")
	#ip = ''
	for linea in file.readlines():
		#agentCount = agentCount + 1
		palabras = linea.split(" ")
		ip = palabras[0]
		print ip
		response = os.system("ping -c 1 " + ip)
		# and then check the response...
		if response == 0:
			pingstatus = "Network Active"
		else:
			pingstatus = "Network Error"
	print agentCount
	#check_ping(ip)
	file.close() 

def mib():
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

add = Tkinter.Button(top, text ="Agregar agente", command = addClient)
delete = Tkinter.Button(top, text ="Eliminar agente", command = ping)
agentInfo = Tkinter.Button(top, text ="Informacion de agente", command = deleteClient)

add.pack()
delete.pack()
agentInfo.pack()

#ping()
w = Label(top, width=20, text="Numero de dispositivos: ", fg="black", anchor='w')
w.pack(padx=5, pady=10, side=LEFT)
w = Label(top, text=agentCount, fg="black")
w.pack(padx=5, pady=20, side=LEFT)

top.mainloop()

#if __name__== 'main': 
	#tableMain()