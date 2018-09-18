"""
SNMPv1
++++++

Send SNMP GET request using the following options:

  * with SNMPv1, community 'public'
  * over IPv4/UDP
  * to an Agent at demo.snmplabs.com:161
  * for two instances of SNMPv2-MIB::sysDescr.0 MIB object,

Functionally similar to:

| $ snmpget -v1 -c public localhost SNMPv2-MIB::sysDescr.0

"""#
'''
from pysnmp.hlapi import *

resultado_final = ''
def consultaSNMP(comunidad,host,oid):
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
            resultado= varB.split()
            concat = []
            valid = False

            for palabra in resultado: 
                if palabra == '=':
                    valid = True
                    continue 
                    
                if valid:
                    concat.append(palabra)
            global resultado_final
            resultado_final = ''
            for palabra in concat:
                resultado_final = resultado_final + ' ' + palabra
    return resultado_final


while 1: #Monitorizamos los valores de entrada y salida de octetos de informacion
    host = 'comunidad3'
    ip = '192.168.1.64'
    total_input_traffic = consultaSNMP(host,ip,
                    '1.3.6.1.2.1.1.1.0')

    valor = "N:" + total_input_traffic 
    print valor'''
"""
import os
hostname = "127.0.0.1" #example
response = os.system("ping -c 1 " + hostname)

#and then check the response...
if response == 0:
  print hostname, 'is up!'
else:
  print hostname, 'is down!'"""

import Tkinter as tk

root = tk.Tk()
root.grid_rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

frame_main = tk.Frame(root)
frame_main.grid(sticky='news')

label1 = tk.Label(frame_main, text="Label 1", fg="green")
label1.grid(row=0, column=0, pady=(5, 0), sticky='nw')

# Create a frame for the canvas with non-zero row&column weights
frame_canvas = tk.Frame(frame_main)
frame_canvas.grid(row=2, column=0, pady=(5, 0), sticky='nw')
frame_canvas.grid_rowconfigure(0, weight=1)
frame_canvas.grid_columnconfigure(0, weight=1)
# Set grid_propagate to False to allow 5-by-5 buttons resizing later
frame_canvas.grid_propagate(False)

# Add a canvas in that frame
canvas = tk.Canvas(frame_canvas, bg="yellow")
canvas.grid(row=0, column=0, sticky="news")

# Link a scrollbar to the canvas
vsb = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
vsb.grid(row=0, column=1, sticky='ns')
canvas.configure(yscrollcommand=vsb.set)

# Create a frame to contain the buttons
frame_buttons = tk.Frame(canvas, bg="blue")
canvas.create_window((0, 0), window=frame_buttons, anchor='nw')

# Add 9-by-5 buttons to the frame
rows = 9
columns = 5
buttons = [[tk.Button() for j in xrange(columns)] for i in xrange(rows)]
for i in range(0, rows):
    for j in range(0, columns):
        buttons[i][j] = tk.Button(frame_buttons, text=("%d,%d" % (i+1, j+1)))
        buttons[i][j].grid(row=i, column=j, sticky='news')

# Update buttons frames idle tasks to let tkinter calculate buttons sizes
frame_buttons.update_idletasks()

# Resize the canvas frame to show exactly 5-by-5 buttons and the scrollbar
first5columns_width = sum([buttons[0][j].winfo_width() for j in range(0, 5)])
first5rows_height = sum([buttons[i][0].winfo_height() for i in range(0, 5)])
frame_canvas.config(width=first5columns_width + vsb.winfo_width(),
                    height=first5rows_height)

# Set the canvas scrolling region
canvas.config(scrollregion=canvas.bbox("all"))

# Launch the GUI
root.mainloop()

'''
import Tkinter as tk
root=tk.Tk()

vscrollbar = tk.Scrollbar(root)

c= tk.Canvas(root,background = "#D2D2D2",yscrollcommand=vscrollbar.set)

vscrollbar.config(command=c.yview)
vscrollbar.pack(side=tk.LEFT, fill=tk.Y) 

f=tk.Frame(c) #Create the frame which will hold the widgets

c.pack(side="left", fill="both", expand=True)
c.create_window(0,0,window=f, anchor='nw')

testcontentA = tk.Label(f,wraplength=350 ,text=r"hola")
testcontentB = tk.Button(f,text="anytext")
testcontentA.pack()
testcontentB.pack()

root.update()
c.config(scrollregion=c.bbox("all"))

root.mainloop()'''
#https://stackoverflow.com/questions/42237310/tkinter-canvas-scrollbar