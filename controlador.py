from tkinter import Tk
from vista.vista import MainView
from logs.observer import ObservadorConcretoA

class Controller:
    
    def __init__(self, master):
        self.master = master
        self.vista = MainView(self.master)
        self.observador = ObservadorConcretoA(self.vista.obj)
        self.master.mainloop()

if __name__ == "__main__":
    Controller(Tk())