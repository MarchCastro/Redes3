import Tkinter
from Tkinter import *
from tkintertable.Tables import TableCanvas
from tkintertable.TableModels import TableModel

master = Tkinter.Tk()
master.title("Bienvenido a casi Observium :)")
master.geometry('400x400')
tframe = Frame(master)
tframe.pack()
table = TableCanvas(tframe)
table.createTableFrame()
data = {'rec1': {'col1': 'kalkjajaalksjaldkjalkdancljdnsjvn', 'col2': 108.79, 'label': 'rec1'},
'rec2': {'col1': 99.88, 'col2': 108.79, 'label': 'rec2'}}
model = table.model
model.importDict(data) #can import from a dictionary to populate model
table.redrawTable()

master.mainloop()