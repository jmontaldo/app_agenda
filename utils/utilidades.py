from tkinter import Button, Label, Entry
from tkinter import CENTER, W

class Entrada():

    def __init__(self, master, textvar, row, column, font):
        self.master = master
        self.textvar = textvar
        self.row = row
        self.column = column
        self.font = font
        e = Entry(master, textvariable=self.textvar, background="#ECF0F1", font=font)
        e.grid(row=self.row, column=self.column)

class Etiqueta():

    def __init__(self, master, text, row, column, font):
        self.master = master
        self.text = text
        self.row = row
        self.column = column
        self.font = font
        l = Label(master, text=self.text ,anchor=CENTER, pady=3, padx=5, 
            background="#2C3E50", foreground="#FFFFFF", font=font
        )
        l.grid(row=self.row, column=self.column, sticky=W)

class Boton():

    def __init__(self, master, text, row, column, font, comando):
        self.master = master
        self.text = text
        self.row = row
        self.column = column
        self.font = font
        self.comando = comando
        b = Button(master, text=self.text, background="#3498DB", foreground="#FFFFFF", 
            width=8, pady=2, font=font, command=self.comando
        )
        b.grid(row=self.row, column=self.column)