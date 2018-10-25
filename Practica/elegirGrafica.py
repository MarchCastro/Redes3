#!/usr/bin/python

import threading
import Tkinter as tk
from actualizarRRD import actualizar
from graficarRRD import graficar, graficar_HW, graficar_LB
from PIL import ImageTk, Image

class VentanaGraficas(object):
	def __init__(self,root,host,limites_LB):
		self.root = root
		self.window = None
		self.host = host
		self.limites_LB = limites_LB

		self.rrd_name = host+"-net.rrd"
		#variables HW
		self.rrd_name_LB = host+"-LB.rrd"
		#variables HW
		self.rrd_name_HW = host+"_HW.rrd"
		#self.rrd_name = "net3.rrd" # Nombre de la rrd del host
		
		#self.b = tk.Button(self.root, text="Graficas de la interfaz", command=self.create_window)
		#self.b.pack()
		self.create_window()
		
	def create_window(self):
		self.window = tk.Toplevel(self.root)
		self.window.title("Graficos")
		tk.Label(self.window, text='Servicio', fg='black').grid(row=0, column=0)
		tk.Label(self.window, text='Algoritmos', fg='black').grid(row=0, column=1)
		tk.Button(self.window, text='Trafico de la interfaz', command= lambda: self.inicia_ventana_grafica(1)).grid(row=1, column=0)
		tk.Button(self.window, text='Linea de base - CPU', command= lambda: self.inicia_ventana_grafica_LB(2)).grid(row=1, column=1)
		tk.Button(self.window, text='Holt Winters trafico interfaz', command= lambda: self.inicia_ventana_grafica_holtW(1)).grid(row=1, column=2)
		tk.Button(self.window, text='Conexiones TCP establecidas', command= lambda: self.inicia_ventana_grafica(2)).grid(row=2, column=0)
		tk.Button(self.window, text='Linea de base - RAM', command= lambda: self.inicia_ventana_grafica_LB(2)).grid(row=2, column=1)
		tk.Button(self.window, text='Holt Winters conexiones TCP', command= lambda: self.inicia_ventana_grafica_holtW(2)).grid(row=2, column=2)
		tk.Button(self.window, text='Segmentos TCP', command= lambda: self.inicia_ventana_grafica(3)).grid(row=3, column=0)
		tk.Button(self.window, text='Linea de base - HDD', command= lambda: self.inicia_ventana_grafica_LB(2)).grid(row=3, column=1)
		tk.Button(self.window, text='Holt Winters segmentos TCP', command= lambda: self.inicia_ventana_grafica_holtW(3)).grid(row=3, column=2)
		tk.Button(self.window, text='Estadisticas ICMP', command= lambda: self.inicia_ventana_grafica(4)).grid(row=4, column=0)
		tk.Button(self.window, text='Holt Winters estadisticas ICMP', command= lambda: self.inicia_ventana_grafica_holtW(4)).grid(row=4, column=2)
		tk.Button(self.window, text='Respuestas SNMP', command= lambda: self.inicia_ventana_grafica(5)).grid(row=5, column=0)
		tk.Button(self.window, text='Holt Winters respuestas SNMP', command= lambda: self.inicia_ventana_grafica_holtW(5)).grid(row=5, column=2)
		
	def inicia_ventana_grafica(self,id_grafica):
		a = Grafica(self.root,self.rrd_name,self.host+"-"+str(id_grafica)+".png",id_grafica)
	def inicia_ventana_grafica_LB(self,id_grafica):
		a = Grafica_LB(self.root,self.rrd_name_LB,self.host+"-"+str(id_grafica)+"-LB.png",id_grafica,self.limites_LB)
	def inicia_ventana_grafica_holtW(self,id_grafica):
		a = Grafica_HW(self.root,self.rrd_name_HW,self.host+"_"+str(id_grafica)+"_HW.png",id_grafica)	
		
class Grafica(object):
	def __init__(self, root, rrd_name, imagen, id_grafica):
	
		self.root = root
		self.rrd_name = rrd_name
		self.imagen = imagen
		self.id_grafica = id_grafica
	
		self.window1 = None
		self.img = None
		self.display = None	
	
		#Debe ser un hilo por cada grafica iniciada
		t2 = threading.Thread(target=graficar, args=("Graficando...",self.rrd_name,self.imagen,self.id_grafica,))
		t2.daemon = True
		t2.start()
	
		self.window1 = tk.Toplevel(self.root)

		if id_grafica == 1:
			self.window1.title("Trafico de la interfaz")			
		elif id_grafica == 2:
			self.window1.title("Conexiones TCP establecidas")
		elif id_grafica == 3:
			self.window1.title("Segmentos TCP")
		elif id_grafica == 4:
			self.window1.title("Estadisticas ICMP")
		elif id_grafica == 5:
			self.window1.title("Respuestas SNMP")
		else:
			self.window1.title("Graficos")	
			
			
		self.img = ImageTk.PhotoImage(Image.open(self.imagen))
		self.display = tk.Label(self.window1, image=self.img)
		self.display.pack(side = "bottom", fill = "both", expand = "yes")
		self.actualiza_imagen()
		
	def actualiza_imagen(self):
		self.img = ImageTk.PhotoImage(Image.open(self.imagen))
		self.display.config(image=self.img)
		self.window1.after(1000, self.actualiza_imagen)
		print "Actualizacion img..."			

#GRAFICA HOLT WINTERS
class Grafica_HW(object):
	def __init__(self, root, rrd_name, imagen, id_grafica):
		pngpath="./IMG_HW/"
		self.root = root
		self.rrd_name = rrd_name
		self.imagen = imagen
		self.id_grafica = id_grafica
	
		self.window1 = None
		self.img = None
		self.display = None	
	
		#Debe ser un hilo por cada grafica iniciada
		t2 = threading.Thread(target=graficar_HW, args=("Graficando HW...",self.rrd_name,self.imagen,self.id_grafica,))
		t2.daemon = True
		t2.start()
	
		self.window1 = tk.Toplevel(self.root)

		if id_grafica == 1:
			self.window1.title("Holt Winters para trafico de la interfaz")			
		elif id_grafica == 2:
			self.window1.title("Holt Winters para conexiones TCP establecidas")
		elif id_grafica == 3:
			self.window1.title("Holt Winters para segmentos TCP")
		elif id_grafica == 4:
			self.window1.title("Holt Winters para estadisticas ICMP")
		elif id_grafica == 5:
			self.window1.title("Holt Winters para respuestas SNMP")
		else:
			self.window1.title("Graficos")	
			
			
		self.img = ImageTk.PhotoImage(Image.open(pngpath+self.imagen))
		self.display = tk.Label(self.window1, image=self.img)
		self.display.pack(side = "bottom", fill = "both", expand = "yes")
		self.actualiza_imagen()
		
	def actualiza_imagen(self):
		pngpath="./IMG_HW/"
		self.img = ImageTk.PhotoImage(Image.open(pngpath+self.imagen))
		self.display.config(image=self.img)
		self.window1.after(1000, self.actualiza_imagen)
		print "Actualizacion img HW..."
		
#GRAFICA LINEA BASE
class Grafica_LB(object):
	def __init__(self, root, rrd_name, imagen, id_grafica,limites):
	
		self.root = root
		self.rrd_name = rrd_name
		self.imagen = imagen
		self.id_grafica = id_grafica
		self.limites = limites
	
		self.window1 = None
		self.img = None
		self.display = None	
	
		#Debe ser un hilo por cada grafica iniciada
		t2 = threading.Thread(target=graficar_LB, args=("Graficando LB...",self.rrd_name,self.imagen,self.id_grafica,limites,))
		t2.daemon = True
		t2.start()
	
		self.window1 = tk.Toplevel(self.root)

		if id_grafica == 1:
			self.window1.title("Linea base para el porcentaje de uso de CPU")			
		elif id_grafica == 2:
			self.window1.title("Linea base para el porcentaje de uso de RAM")
		elif id_grafica == 3:
			self.window1.title("Linea base para el porcentaje de uso de HDD")
		else:
			self.window1.title("Graficos")

		self.img = ImageTk.PhotoImage(Image.open(self.imagen))
		self.display = tk.Label(self.window1, image=self.img)
		self.display.pack(side = "bottom", fill = "both", expand = "yes")
		self.actualiza_imagen()

	def actualiza_imagen(self):
		self.img = ImageTk.PhotoImage(Image.open(self.imagen))
		self.display.config(image=self.img)
		self.window1.after(1000, self.actualiza_imagen)
		print "Actualizacion img LB..."

if __name__ == '__main__':
	#Este hilo debe inciar desde la pantalla principal
	t1 = threading.Thread(target=actualizar, args=('Actualizando...','comunidadSNMPsamuel','127.0.0.1',161,'127.0.0.1-net',))
	t1.daemon = True
	t1.start()
	
	root = tk.Tk() # Esta pantalla seria la pantalla principal de marcela
	
	a = VentanaGraficas(root,"127.0.0.1")
	root.mainloop()





