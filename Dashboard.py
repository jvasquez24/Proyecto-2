import tkinter as tk
from PIL import Image, ImageTk
from Empleados import VentanaGestionEmpleados
from Salarios import VentanaGestionSalarios

class MetaSingleton(type):
    """Metaclass para implementar el patrón Singleton."""
    _instancia = None

    def __call__(cls, *args, **kwargs):
        if cls._instancia is None:
            cls._instancia = super().__call__(*args, **kwargs)
        return cls._instancia

class VentanaDashboard(tk.Tk, metaclass=MetaSingleton):
    def __init__(self):
        super().__init__()
        self.title("Dashboard")
        self.geometry("626x391")
        self.configure(bg="white")
        self.ventanaCentrada()

        try:
            self.imagenFondo = Image.open("imagenes/fondo_dashboard.png")
            self.fotoFondo = ImageTk.PhotoImage(self.imagenFondo)
            self.canvas = tk.Canvas(self, width=self.imagenFondo.width, height=self.imagenFondo.height, bg="white", highlightthickness=0)
            self.canvas.pack(fill=tk.BOTH, expand=True)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.fotoFondo)
        except FileNotFoundError:
            print("La imagen de fondo no se encontró.")

        self.marco = tk.Frame(self.canvas, bg="white")
        self.marco.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.tituloLabel = tk.Label(self.marco, text="Bienvenido al Dashboard", font=("Helvetica", 20), bg="white")
        self.tituloLabel.pack(pady=20)

        self.tituloSistemaLabel = tk.Label(self.marco, text="(Sistema de Empleados)", font=("Helvetica", 20), bg="white")
        self.tituloSistemaLabel.pack(pady=5)

        self.iconoEmpleados = self.cargarIcono("iconos/icono_empleado.png", tamaño=(70, 70))
        self.iconoSalario = self.cargarIcono("iconos/icono_salario.png", tamaño=(70, 70))

        self.estiloBoton = {"font": ("Helvetica", 12), "bd": 0, "bg": "#3498db", "fg": "white"}

        self.botonEmpleados = tk.Button(self.marco, text="Datos de Empleados", image=self.iconoEmpleados, compound=tk.TOP, command=self.abrirEmpleados, **self.estiloBoton)
        self.botonEmpleados.pack(pady=15)

        self.botonSalario = tk.Button(self.marco, text="Cálculos de Salario", image=self.iconoSalario, compound=tk.TOP, command=self.abrirSalario, **self.estiloBoton)
        self.botonSalario.pack(pady=15)

    def ventanaCentrada(self):
        anchoPantalla = self.winfo_screenwidth()
        altoPantalla = self.winfo_screenheight()
        x = (anchoPantalla / 2) - (626 / 2)
        y = (altoPantalla / 2) - (391 / 2)
        self.geometry("626x391+%d+%d" % (x, y))

    def cargarIcono(self, nombreArchivo, tamaño):
        imagen = Image.open(nombreArchivo)
        imagen = imagen.resize(tamaño)
        icono = ImageTk.PhotoImage(imagen)
        return icono

    def abrirEmpleados(self):
        print("Abriendo datos de empleados...")
        app = VentanaGestionEmpleados()
        app.mainloop()

    def abrirSalario(self):
        print("Abriendo cálculos de salario...")
        app = VentanaGestionSalarios()
        app.mainloop()
