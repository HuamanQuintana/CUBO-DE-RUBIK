from Tkinter import *
from Rubik import Cube
root = Tk()
root.title('INGRESE SUS DATOS')
nombre_label = Label(root,text="Nombre :")
nombre_label.grid(row=1,column=1)
nombre_str = StringVar()
nombre_entry = Entry(root,textvariable=nombre_str)
nombre_entry.grid(row=1,column=2)
#row 2 : the last name
last_label= Label(root,text="Apellido : ")
last_label.grid(row=2,column=1)
last_str = StringVar()
last_entry = Entry(root,textvariable=last_str)
last_entry.grid(row=2,column=2)
#archi=open('datos.txt','w')
finish = Button(root,text="JUGAR")
finish.grid(row=4,column=2)

root.mainloop()
