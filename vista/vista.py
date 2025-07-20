from tkinter import StringVar, Entry, Frame, font, ttk, W, NS, SW
from utils.utilidades import Boton, Etiqueta, Entrada
from modelo.ormdb import CRUD

## ESTRUCTURA DE LA VISTA

class MainView():
    def __init__(self, master):
        self.master = master
        self.master.title("Agenda-App")
        self.master.configure(background="#2C3E50")
        self.custom_font = font.Font(family="Arial", size=10)

        #Variables
        self.var_nombre = StringVar()
        self.var_apellido = StringVar()
        self.var_telefono = StringVar()
        self.var_mail = StringVar()
        self.message = StringVar()
        self.params = [self.var_nombre, self.var_apellido, self.var_telefono, self.var_mail]
        self.obj = CRUD()

        #Entradas
        Etiqueta(self.master, text="INGRESE LOS DATOS:", font=self.custom_font, row=0, column=0)
        Etiqueta(self.master, text="Nombre", font=self.custom_font, row=1, column=0)
        Entrada(self.master, textvar=self.var_nombre, font=self.custom_font, row=1, column=1)
        Etiqueta(self.master, text="Apellido", font=self.custom_font, row=2, column=0)
        Entrada(self.master, textvar=self.var_apellido, font=self.custom_font, row=2, column=1)
        Etiqueta(self.master, text="Teléfono", font=self.custom_font, row=3, column=0)
        Entrada(self.master, textvar=self.var_telefono,font=self.custom_font, row=3, column=1)
        Etiqueta(self.master, text="Mail", font=self.custom_font, row=4, column=0)
        Entrada(self.master, textvar=self.var_mail, font=self.custom_font, row=4, column=1)

        #Separador
        self.separador = Frame(self.master, height=10, bd=1, relief="sunken", background="#2C3E50")
        self.separador.grid(row=5, column=0)

        #Botones
        Boton(self.master, text="Alta", comando=lambda:self.obj.alta(*self.params, self.tree, self.message), 
            font=self.custom_font,row=6 ,column=0)

        Boton(self.master, text="Baja", comando=lambda:self.obj.baja(self.tree, self.message),
            font=self.custom_font, row=6, column=1)
    
        Boton(self.master, text="Modificar", 
            comando=lambda:self.obj.modificar(*self.params, self.tree, self.message), 
            font=self.custom_font, row=6, column=2)
    
        Boton(self.master, text="Tomar",
            comando=lambda:self.obj.tomar(*self.params, self.tree),
            font=self.custom_font, row=6, column=5)
    
        #TreeView
        self.tree = ttk.Treeview(self.master, height=5)
        self.tree["columns"] = ("col1", "col2", "col3", "col4")
        self.tree.column("#0", width=40, minwidth=40, anchor=W)
        self.tree.heading("#0", text="ID")
        self.tree.column("col1", width=100, minwidth=100, anchor=W)
        self.tree.heading("col1", text="Nombre")
        self.tree.column("col2", width=100, minwidth=100, anchor=W)
        self.tree.heading("col2", text="Apellido")
        self.tree.column("col3", width=100, minwidth=100, anchor=W)
        self.tree.heading("col3", text="Teléfono")
        self.tree.column("col4", width=200, minwidth=200, anchor=W)
        self.tree.heading("col4", text="Mail")
        self.tree.grid(row=7, column=0, columnspan=8, pady=10, padx=5)

        #scrollbar
        self.scrollbar = ttk.Scrollbar(self.master, orient="vertical", command=self.tree.yview)
        self.scrollbar.grid(row=7, column=9, sticky=NS, pady=10 ,padx=5)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        #console
        Etiqueta(self.master, "Consola:", font=self.custom_font, row=8, column=0) 

        self.message_texts = Entry(master=self.master, textvariable=self.message, width=75,
            background="#ECF0F1", font=self.custom_font
        )
        self.message_texts.grid(row=9, column=0, columnspan=9, pady=10, padx=5, sticky=SW)

        self.obj.actualizar_treeview(self.tree)