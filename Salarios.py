import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import time

# Patrón Singleton para manejar el archivo de empleados
class SingletonArchivoEmpleados:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.archivo = "empleados.txt"
        return cls._instance

    def leerEmpleados(self):
        empleados = {}
        try:
            with open(self.archivo, "r") as f:
                for linea in f:
                    datos = linea.strip().split(",")
                    empleado = {
                        "ID": int(datos[0]),
                        "Nombre": datos[1],
                        "Apellido": datos[2],
                        "Edad": int(datos[3]),
                        "Cargo": datos[4],
                        "Salario": float(datos[5])
                    }
                    empleados[empleado["ID"]] = empleado
        except FileNotFoundError:
            pass
        return empleados

# Decorador para medir el tiempo de ejecución
def Calculartiempo(func):
    def wrapper(*args, **kwargs):
        inicio = time.time()
        resultado = func(*args, **kwargs)
        fin = time.time()
        print(f"{func.__name__} tardó {fin - inicio} segundos.")
        return resultado
    return wrapper

# Clase para la ventana de gestión de salarios
class VentanaGestionSalarios(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Salarios")
        self.geometry("750x600")
        self.ventanaCentrada()
        self.archivoEmpleados = SingletonArchivoEmpleados()

        # Establecer colores
        self.configure(bg="black")
        self.label_color = "lightblue"
        self.entry_bg = "white"
        self.entry_fg = "black"
        self.button_bg = "lightblue"
        self.button_fg = "black"

        self.labelSeleccionar = tk.Label(self, text="Seleccionar empleado:", bg="black", fg=self.label_color)
        self.labelSeleccionar.pack(pady=5)

        self.comboEmpleados = ttk.Combobox(self)
        self.comboEmpleados.pack(pady=5)

        self.labelSalarioBase = tk.Label(self, text="Salario base:", bg="black", fg=self.label_color)
        self.labelSalarioBase.pack(pady=5)

        self.entrySalarioBase = tk.Entry(self, state="readonly", bg=self.entry_bg, fg=self.entry_fg)
        self.entrySalarioBase.pack(pady=5)

        self.labelHorasExtras = tk.Label(self, text="Horas extras:", bg="black", fg=self.label_color)
        self.labelHorasExtras.pack(pady=5)

        self.entryHorasExtras = tk.Entry(self, bg=self.entry_bg, fg=self.entry_fg)
        self.entryHorasExtras.pack(pady=5)

        self.labelCCSS = tk.Label(self, text="Porcentaje de CCSS:", bg="black", fg=self.label_color)
        self.labelCCSS.pack(pady=5)

        self.entryCCSS = tk.Entry(self, state="readonly", bg=self.entry_bg, fg=self.entry_fg)
        self.entryCCSS.pack(pady=5)

        self.buttonCalcular = tk.Button(self, text="Calcular Salario", bg=self.button_bg, fg=self.button_fg,
                                         command=self.calcularSalario)
        self.buttonCalcular.pack(pady=5)

        self.buttonCerrar = tk.Button(self, text="Cerrar Ventana", bg=self.button_bg, fg=self.button_fg,
                                      command=self.destroy)
        self.buttonCerrar.pack(pady=5)

        # Crear tabla de salarios
        self.tablaSalarios = ttk.Treeview(self, columns=(
            "Fecha", "Hora", "Nombre", "Salario Base", "CCSS", "Horas Extras", "Salario Neto"), show="headings")
        self.tablaSalarios.heading("Fecha", text="Fecha")
        self.tablaSalarios.heading("Hora", text="Hora")
        self.tablaSalarios.heading("Nombre", text="Nombre")
        self.tablaSalarios.heading("Salario Base", text="Salario Base")
        self.tablaSalarios.heading("CCSS", text="CCSS")
        self.tablaSalarios.heading("Horas Extras", text="Horas Extras")
        self.tablaSalarios.heading("Salario Neto", text="Salario Neto")
        self.tablaSalarios.pack(pady=5, expand=True, fill=tk.BOTH)

        # Ajustar el diseño de la tabla
        self.tablaSalarios.column("#0", width=0)  # Ocultar la primera columna
        self.tablaSalarios.column("#1", width=70)  # Ajustar el ancho de la columna Fecha
        self.tablaSalarios.column("#2", width=70)  # Ajustar el ancho de la columna Hora
        self.tablaSalarios.column("#3", width=140)  # Ajustar el ancho de la columna Nombre
        self.tablaSalarios.column("#4", width=80)  # Ajustar el ancho de la columna Salario Base
        self.tablaSalarios.column("#5", width=80)  # Ajustar el ancho de la columna CCSS
        self.tablaSalarios.column("#6", width=100)  # Ajustar el ancho de la columna Horas Extras
        self.tablaSalarios.column("#7", width=100)  # Ajustar el ancho de la columna Salario Neto

        # Cargar datos al iniciar la ventana
        self.cargarEmpleados()
        self.actualizarTabla()

    @Calculartiempo
    def calcularSalario(self):
        seleccion = self.comboEmpleados.current()
        empleados = self.archivoEmpleados.leerEmpleados()
        empleado_seleccionado = list(empleados.values())[seleccion]
        nombre_empleado = f"{empleado_seleccionado['Nombre']} {empleado_seleccionado['Apellido']}"
        salario_base = empleado_seleccionado["Salario"]
        try:
            horas_extras = int(self.entryHorasExtras.get())
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese un valor válido para las horas extras.")
            return

        if horas_extras < 0:
            messagebox.showerror("Error", "Las horas extras no pueden ser un valor negativo.")
            return

        # Calcular el salario total, incluyendo las horas extras y el descuento de CCSS
        salario_total = salario_base + (salario_base * 0.015 * horas_extras)  # Añadir el 1.5% por horas extras
        descuento_ccss = salario_total * 9 / 100  # Descuento del 9% por CCSS
        salario_neto = salario_total - descuento_ccss

        # Obtener la fecha y hora actual
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        hora_actual = datetime.now().strftime("%H:%M:%S")

        # Agregar datos a la tabla
        self.tablaSalarios.insert("", "end", values=(
            fecha_actual, hora_actual, nombre_empleado, f"{salario_base:.2f}",
            f"{descuento_ccss:.2f}", f"{(salario_base * 0.015 * horas_extras):.2f}", f"{salario_neto:.2f}"))

        # Guardar datos en el archivo
        with open("salarios.txt", "a") as file:
            file.write(
                f"{fecha_actual},{hora_actual},{nombre_empleado},{salario_base:.2f},{descuento_ccss:.2f},{(salario_base * 0.015 * horas_extras):.2f},{salario_neto:.2f}\n")

        # Limpiar los campos después de agregar el salario
        self.limpiarCampos()

    def ventanaCentrada(self):
        # Método de ventanaCentrada: Centra la ventana en la pantalla
        anchoPantalla = self.winfo_screenwidth()
        altoPantalla = self.winfo_screenheight()
        x = (anchoPantalla / 2) - (750 / 2)
        y = (altoPantalla / 2) - (600 / 2)  # Ajustando la altura de la ventana
        self.geometry("750x600+%d+%d" % (x, y))

    def cargarEmpleados(self):
        empleados = self.archivoEmpleados.leerEmpleados()
        nombres_apellidos = [f"{empleado['Nombre']} {empleado['Apellido']}" for empleado in empleados.values()]
        self.comboEmpleados["values"] = nombres_apellidos
        self.comboEmpleados.bind("<<ComboboxSelected>>", self.actualizarSalario)

    def actualizarSalario(self, event):
        seleccion = self.comboEmpleados.current()
        empleados = self.archivoEmpleados.leerEmpleados()
        empleado_seleccionado = list(empleados.values())[seleccion]
        salario_base = empleado_seleccionado["Salario"]
        self.entrySalarioBase.config(state="normal")
        self.entrySalarioBase.delete(0, tk.END)
        self.entrySalarioBase.insert(0, salario_base)
        self.entrySalarioBase.config(state="readonly")

        self.entryCCSS.config(state="normal")
        self.entryCCSS.delete(0, tk.END)
        self.entryCCSS.insert(0, "9%")
        self.entryCCSS.config(state="readonly")

    def limpiarCampos(self):
        self.entryHorasExtras.delete(0, tk.END)
        self.comboEmpleados.set('')  # Limpiar la selección del combo
        self.entrySalarioBase.config(state="normal")
        self.entrySalarioBase.delete(0, tk.END)
        self.entrySalarioBase.config(state="readonly")
        self.entryCCSS.config(state="normal")
        self.entryCCSS.delete(0, tk.END)
        self.entryCCSS.config(state="readonly")

    def actualizarTabla(self):
        # Limpiar la tabla antes de cargar los datos
        for row in self.tablaSalarios.get_children():
            self.tablaSalarios.delete(row)

        # Leer datos del archivo de salarios
        try:
            with open("salarios.txt", "r") as file:
                for line in file:
                    data = line.strip().split(",")
                    self.tablaSalarios.insert("", "end", values=data)
        except FileNotFoundError:
            pass


