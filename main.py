from GUI.gui import Gui

#Main de la aplicación
if __name__ == "__main__":
    app = Gui()
    app.run()
    while app.app_running:
        app.update()

