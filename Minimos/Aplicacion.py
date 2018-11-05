from tkinter import *
from tkinter import ttk, font, filedialog
import notify
import operaciones
import time
import rrdtool

Background = '#0b0e0f'

class Aplicacion():
    def __init__(self):
        self.raiz = Tk()
        self.raiz.geometry('600x350+300+200')
        self.raiz.title('Prediccion Lineal')
        self.raiz.configure(background = Background)
        self.variables()
        self.widgets()
        self.colocar()
        self.raiz.mainloop()

    def variables(self):
        self.txt_ruta_archivo = StringVar(value = '')
        self.txt_ruta_imagen = StringVar(value = '')
        self.txt_limite = StringVar(value = '50')
        self.txt_fecha_inicio = StringVar(value = '1507575000')
        self.txt_ds = StringVar(value = 'CPUload')

    def widgets(self):
        self.style = ttk.Style()
        self.style.configure("LBL.TLabel", foreground="White" , background = Background , font = 'verdana 12')
        self.style.configure("LBL2.TLabel", foreground="#ed6f09", background='#2b2933', font='verdana 12')
        self.style.map("BTN.TButton" ,
                             foreground=[('pressed', '#6f16ce'), ('active', 'white')],
                             background=[('pressed', '!disabled', '#726e77'), ('active', '#38c0ed')]
                      )
        self.style.configure("BTN.TButton" , font='verdana 12' , foreground = 'white' , background = '#38c0ed')
        self.style.configure("SEP.TSeparator" , background = 'black' )
        #self.style.configure("BTN.TButton", foreground="White", background='#38c0ed', font='verdana 12')
        self.separador = ttk.Separator(orient = HORIZONTAL , style = "SEP.TSeparator")
        self.separador2 = ttk.Separator(orient=HORIZONTAL, style="SEP.TSeparator")
        self.separador3 = ttk.Separator(orient=HORIZONTAL, style="SEP.TSeparator")

        self.text_1 = Text(self.raiz, width=60 , height = 1)
        self.text_1.config(state = DISABLED)
        self.entry_2 = ttk.Entry(self.raiz, textvariable = self.txt_limite)
        self.entry_3 = ttk.Entry(self.raiz, textvariable = self.txt_fecha_inicio)
        self.entry_4 = ttk.Entry(self.raiz, textvariable = self.txt_ds)

        self.btn_archivo = ttk.Button( self.raiz, text='. . .', style = "BTN.TButton", command= lambda: self.seleccionar_archivo()  , width = 3)
        self.lbl_1 = ttk.Label(self.raiz , text = 'Selecciona archivo rrd' , style="LBL.TLabel" , width = 20)
        self.lbl_2 = ttk.Label(self.raiz , text = 'Limite (0 - 100)' , style="LBL.TLabel" , width = 20)
        self.lbl_3 = ttk.Label(self.raiz , text = 'Fecha Inicio (Unix time)' , style="LBL.TLabel" , width = 20)
        self.lbl_4 = ttk.Label(self.raiz , text = 'Data Source' , style = 'LBL.TLabel' , width = 20)
        self.btn_ayuda = ttk.Button(self.raiz , text = '?' , style = "BTN.TButton",command = lambda: self.ayuda() , width = 3)
        self.btn_evaluar = ttk.Button(self.raiz , text = 'Evaluar' , style = "BTN.TButton" , command = lambda: self.Evaluar())

    def Evaluar(self):
        ruta = self.txt_ruta_archivo.get()
        inicio = 0
        limite = 0
        ds = self.txt_ds.get()
        if ruta == '':
            self.txt_ruta_imagen.set('')
            print('Error')
            return
        self.txt_ruta_imagen.set( self.txt_ruta_archivo.get().split('.')[0] + '.png' )
        try:
            inicio = int(self.txt_fecha_inicio.get())
            limite= int( self.txt_limite.get() )
        except:
            print('Error')
            return

        if limite < 0 or limite > 100:
            print('Error')
            return
        if ds == '':
            print('Error')
            return

        self.graficar(ruta , limite , inicio , ds)

    def graficar(self , ruta , limite , inicio , ds):
        self.raiz.withdraw()
        estimado = notify.check_CPU2(ruta , ds , limite , inicio) #int
        respuesta = operaciones.graficarLectura(ruta,str(inicio),str(limite),ds,estimado)
        if respuesta == 'Error':
            print('Se ha generado un Error, linea 87')
            return

        ventana = Toplevel()
        ventana.geometry('800x300+150+100')
        ventana.title('Prediccion Minimos Cuadrados')
        ventana.configure(background = Background)
        try:
            str_inicio = str( time.ctime(inicio) )
            str_fin = str( time.ctime(rrdtool.last(ruta)) )
            str_pred = str( time.ctime(estimado) )

            self.pic = PhotoImage(file = self.txt_ruta_imagen.get())
            imagen = ttk.Label(ventana , image = self.pic)

            lbl_1 = ttk.Label(ventana , text = 'Inicio de Captura:', style = 'LBL.TLabel')
            lbl_2 = ttk.Label(ventana , text = str_inicio, style = 'LBL2.TLabel')

            lbl_3 = ttk.Label(ventana , text = 'Ultima Captura:', style = 'LBL.TLabel')
            lbl_4 = ttk.Label(ventana, text=str_fin, style = 'LBL2.TLabel')

            lbl_5 = ttk.Label(ventana, text='Prediccion Estimada:', style = 'LBL.TLabel')
            lbl_6 = ttk.Label(ventana, text=str_pred , style = 'LBL2.TLabel')

            btn_cerrar = ttk.Button(ventana , text = 'Volver' , command = lambda:self.cerrar(ventana) , style = 'BTN.TButton')

            imagen.grid(column = 0 , row = 0 , rowspan = 7 , pady = 10 , padx = 10)
            lbl_1.grid(column = 1 , row = 0)
            lbl_2.grid(column = 1 , row = 1)
            lbl_3.grid(column = 1 , row = 2)
            lbl_4.grid(column = 1 , row = 3)
            lbl_5.grid(column = 1 , row = 4)
            lbl_6.grid(column = 1 , row = 5)
            btn_cerrar.grid(column = 1 , row = 6)
        except:
            print('Error al imprimir imagen')

    def cerrar(self, ventana):
        ventana.destroy()
        self.raiz.deiconify()


    def colocar(self):
        self.lbl_1.grid( column = 1 , row = 0 )
        self.btn_archivo.grid( column = 0 , row = 1 )
        self.text_1.grid( column = 1 , row = 1)

        self.separador.grid(column = 0 , row = 2 , columnspan = 2 , pady = 10)

        self.lbl_2.grid( column = 1 , row = 3 , sticky = 'S')
        self.entry_2.grid( column = 1 , row = 4 )

        self.separador2.grid(column=0, row=5, columnspan=2, pady=10)

        self.lbl_3.grid( column = 1 , row = 6 )
        self.btn_ayuda.grid( column = 0 , row = 7 )
        self.entry_3.grid( column = 1 , row = 7 )

        self.separador3.grid(column=0, row=8, columnspan=2, pady=10)

        self.lbl_4.grid( column = 1 , row = 9 )
        self.entry_4.grid(column=1, row=10)

        self.btn_evaluar.grid(column = 1 , row = 11 , pady = 15)




    def ayuda(self):
        ventana = Toplevel()
        ventana.geometry('380x110+300+200')
        ventana.title('Ayuda con tiempo UNIX')
        ventana.configure(background = Background)

        actual = str(int(time.time()))

        lbl_1 = ttk.Label(ventana , text = '1507575000 = ' + str( time.ctime( 1507575000 ) ) , style="LBL.TLabel")
        lbl_2 = ttk.Label(ventana , text = actual + ' = ' + str( time.ctime(int(actual)) ) , style="LBL.TLabel")
        btn_volver = ttk.Button(ventana , text = 'volver' , command =  lambda: ventana.withdraw() , style="BTN.TButton")

        lbl_1.pack()
        lbl_2.pack( pady = 15)
        btn_volver.pack()

    def seleccionar_archivo(self):
        r = filedialog.askopenfilename(initialdir='./',
                                       title='Select File',
                                       filetypes=(('RRD files', '*.rrd'),)
                                       )
        self.txt_ruta_archivo.set(r)
        self.text_1.config(state=NORMAL)
        self.text_1.delete('1.0', END)
        self.text_1.insert('1.0', self.txt_ruta_archivo.get())
        self.text_1.config(state=DISABLED)


def main():
    app = Aplicacion()
    return 0

if __name__ == '__main__':
    main()


'''
t1 = Text(ventana, width=30, height=10)
        t1.delete("1.0", END)
        t1.insert("1.0", cadena)
        t1.config(state=DISABLED)
'''