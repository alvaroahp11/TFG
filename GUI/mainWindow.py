import tkinter as tk
from tkinter import ttk

#Clase de la pantalla principal de la aplicación


class MainWindow:
    def __init__(self, root: tk.Tk):
        self.root = root
        # Frame
        self.mainWindow = tk.Frame(self.root)
        self.mainWindow.place(relheight=1, relwidth=1, relx=0, rely=0)
        stockList = ["TSLA", "PLTR", "SPY"]
        # stockListDisplay = ttk.Combobox(self.mainWindow, values=stockList)
        # stockListDisplay.set("Choose an stock")
        # stockListDisplay.place(relx=0.5, rely=0.5)

        box = ttk.Label(self.mainWindow, text ="hola")
        box.place(relx=0.5, rely=0.5)

    def show(self):
        self.mainWindow.tkraise()


