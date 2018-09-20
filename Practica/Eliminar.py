from Tkinter import *
import ttk
import tkMessageBox
import os

class Aplicacion():
    def __init__(self):
        self.raiz = Tk()
        self.raiz.title('Lista de Agentes')
        self.raiz.geometry('500x200+500+250')
        self.raiz.configure( background = '#9e9c9c' )
        self.widgets()
        self.raiz.mainloop()


    def widgets(self):
        ttk.Style().configure("TButton", foreground='#0fbc74', background='#8c1f09')
        # definicion de variables
        self.IDborrar = IntVar()
        self.Agentes = []

        # definicion de widgets
        self.btnEliminar = ttk.Button(self.raiz, command=self.Eliminar, text='Eliminar')
        self.btnCerrar = ttk.Button(self.raiz, command=self.Cerrar, text='Cerrar')

        # definicion de radio Buttons
        self.seleccionar()
        listaBorrar = []

        for i in range(len(self.Agentes)):
            nombre = self.Agentes[i].split(' ')[0]  # obtenemos el hostname
            listaBorrar.append(ttk.Radiobutton(self.raiz, text=nombre, variable=self.IDborrar, value=i))
        i = 0
        for radio in listaBorrar:
            radio.grid(column=1, row=i, sticky=W)
            i = i + 1
        i = i + 1

        # establecer en pantalla los widgets
        #Modificarlo-------------------------------------------------
        self.btnEliminar.grid(column=0, row=i)
        self.btnCerrar.grid(column=2, row=i)

    def seleccionar(self):
        # HN, Version,Puerto,Comunidad
        ruta = 'hosts.txt'
        archivo = open(ruta, 'r')
        while len(self.Agentes) > 0:
            self.Agentes.pop()
        while 1:
            linea = archivo.readline()
            if not linea:
                break
            else:
                self.Agentes.append(linea)
        archivo.close()

    def Eliminar(self):
        print('Funcion eliminar')
        pos = self.IDborrar.get()
        # funcion que manda a eliminar la carpeta de este dispositivo
        ip=self.Agentes[pos].split(' ')[0]
        print("esta es la ip "+ip)
        os.system('rm' +ip +'*')
        self.Agentes.pop(pos)
        tkMessageBox.showinfo(title='Eliminar',
                              message='Agente Eliminado')
        self.borrarArchivoPC()
        self.Cerrar()

    def borrarArchivoPC(self):
        archivo = open("hosts.txt", "w")
        for dispositivo in self.Agentes:
            archivo.write(dispositivo)
        archivo.close()

    def Cerrar(self):
        self.raiz.destroy()

def main():
    app = Aplicacion()
    return 0

if __name__ == '__main__':
    main()

