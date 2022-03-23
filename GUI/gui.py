import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from GUI.mainWindow import MainWindow


class Gui:
    # Settings iniciales de la aplicación
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Stock market forecast")
        style = Style(theme='superhero')
        self.root.resizable(True, True)
        self.app_running = True
        self.root.protocol("WM_DELETE_WINDOW", self.close_app)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = screen_width
        window_height = screen_height
        self.root.state('zoomed')
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        self.root.geometry("{}x{}+{}+{}".format(window_width,
                                                window_height, x_cordinate,
                                                y_cordinate))


    def run(self):
        mainwindow = MainWindow(self.root)
        mainwindow.show()

    def update(self):
        self.root.update()
        self.root.update_idletasks()

    def close_app(self):
        self.app_running = False
        self.root.destroy()
