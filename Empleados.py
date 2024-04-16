import tkinter as tk
from tkinter import ttk, messagebox
import os

# Clase para representar un empleado
class Empleado:
    def __init__(self, id, nombre, apellido, edad, cargo, salario):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.cargo = cargo
        self.salario = salario

# Clase para manejar el archivo de empleados
class ArchivoEmpleados:
    _instancia = None  # Singleton

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia

    def __init__(self):
        self.archivo = "empleados.txt"
        self.id_actual = self.obtenerUltimoID() + 1

    def obtenerUltimoID(self):
        if os.path.exists(self.archivo):
            with open(self.archivo, "r") as f:
                lineas = f.readlines()
                if lineas:
                    ultimo_empleado = lineas[-1].split(",")[0]
                    return int(ultimo_empleado)
        return 0

    def guardarEmpleado(self, empleado):
        empleado.id = self.id_actual
        self.id_actual += 1
        with open(self.archivo, "a") as f:
            f.write(f"{empleado.id},{empleado.nombre},{empleado.apellido},{empleado.edad},{empleado.cargo},{empleado.salario}\n")


    def leerEmpleados(self):
        empleados = []
        if os.path.exists(self.archivo):
            with open(self.archivo, "r") as f:
                for linea in f:
                    datos = linea.strip().split(",")
                    empleado = Empleado(int(datos[0]), datos[1], datos[2], datos[3], datos[4], datos[5])
                    empleados.append(empleado)
        return empleados

    def eliminarEmpleado(self, id):
        empleados = self.leerEmpleados()
        empleados = [emp for emp in empleados if emp.id != id]
        with open(self.archivo, "w") as f:
            for empleado in empleados:
                f.write(
                    f"{empleado.id},{empleado.nombre},{empleado.apellido},{empleado.edad},{empleado.cargo},{empleado.salario}\n")
        messagebox.showinfo("Éxito", "Empleado eliminado correctamente")

    def actualizarEmpleado(self, empleadoActualizado):
        empleados = self.leerEmpleados()
        for i, emp in enumerate(empleados):
            if emp.id == empleadoActualizado.id:
                empleados[i] = empleadoActualizado
                break
        with open(self.archivo, "w") as f:
            for empleado in empleados:
                f.write(f"{empleado.id},{empleado.nombre},{empleado.apellido},{empleado.edad},{empleado.cargo},{empleado.salario}\n")
        messagebox.showinfo("Éxito", "Empleado actualizado correctamente")

# Clase para la ventana de gestión de empleados
class VentanaGestionEmpleados(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Empleados")
        self.geometry("900x400")
        self.configure(bg="black")  # Fondo de la ventana en negro
        self.ventanaCentrada()
        self.archivoEmpleados = ArchivoEmpleados()

        # Estilo
        self.style = ttk.Style(self)
        self.style.theme_use("clam")  # Cambiar el tema del estilo
        self.style.configure("Treeview", background="light gray", foreground="black", fieldbackground="light gray")
        self.style.map("Treeview", background=[("selected", "blue")])

        # Añadiendo color celeste a los botones
        self.style.configure("Blue.TButton", foreground="white", background="#007bff")

        # Definir y posicionar los elementos de la interfaz
        self.labelNombre = ttk.Label(self, text="Nombre:", background="black", foreground="white")
        self.labelNombre.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entryNombre = ttk.Entry(self)
        self.entryNombre.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        self.labelApellido = ttk.Label(self, text="Apellido:", background="black", foreground="white")
        self.labelApellido.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entryApellido = ttk.Entry(self)
        self.entryApellido.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.labelEdad = ttk.Label(self, text="Edad:", background="black", foreground="white")
        self.labelEdad.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entryEdad = ttk.Entry(self)
        self.entryEdad.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        self.labelCargo = ttk.Label(self, text="Cargo:", background="black", foreground="white")
        self.labelCargo.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.comboCargo = ttk.Combobox(self, values=[cargo[0] for cargo in CARGOS])
        self.comboCargo.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        self.labelSalario = ttk.Label(self, text="Salario base:", background="black", foreground="white")
        self.labelSalario.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.entrySalario = ttk.Entry(self, state="readonly")
        self.entrySalario.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        self.buttonAgregar = ttk.Button(self, text="Agregar Empleado", command=self.agregarEmpleado, style="Blue.TButton")
        self.buttonAgregar.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

        self.buttonEliminar = ttk.Button(self, text="Eliminar Empleado", command=self.eliminarEmpleado, style="Blue.TButton")
        self.buttonEliminar.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

        self.buttonCerrar = ttk.Button(self, text="Cerrar Ventana", command=self.cerrarVentana, style="Blue.TButton")
        self.buttonCerrar.grid(row=7, column=0, columnspan=2, padx=10, pady=5)

        self.tree = ttk.Treeview(self, columns=("ID", "Nombre", "Apellido", "Edad", "Cargo", "Salario"), show="headings", style="Treeview")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Apellido", text="Apellido")
        self.tree.heading("Edad", text="Edad")
        self.tree.heading("Cargo", text="Cargo")
        self.tree.heading("Salario", text="Salario")
        self.tree.column("ID", width=50)  # Ancho de la columna ID
        self.tree.column("Nombre", width=120)  # Ancho de la columna Nombre
        self.tree.column("Apellido", width=120)  # Ancho de la columna Apellido
        self.tree.column("Edad", width=50)  # Ancho de la columna Edad
        self.tree.column("Cargo", width=120)  # Ancho de la columna Cargo
        self.tree.column("Salario", width=150)  # Ancho de la columna Salario
        self.tree.grid(row=0, column=2, rowspan=8, padx=14, pady=14, sticky="nsew")

        self.tree.bind("<Double-1>", self.editarEmpleado)  # Bind para doble clic en la tabla

        # Cargar datos al iniciar la ventana
        self.cargarCargos()
        self.actualizarTabla()

    def cargarCargos(self):
        # Actualizar la lista de cargos en el combo box
        self.comboCargo["values"] = [cargo[0] for cargo in CARGOS]
        self.comboCargo.bind("<<ComboboxSelected>>", self.actualizarSalario)

    def actualizarSalario(self, event):
        # Actualizar el salario base al seleccionar un cargo
        seleccion = self.comboCargo.current()
        salario = CARGOS[seleccion][1]
        self.entrySalario.config(state="normal")
        self.entrySalario.delete(0, tk.END)
        self.entrySalario.insert(0, salario)
        self.entrySalario.config(state="readonly")

    def agregarEmpleado(self):
        nombre = self.entryNombre.get()
        apellido = self.entryApellido.get()
        edad = self.entryEdad.get()
        cargo = self.comboCargo.get()
        salario = self.entrySalario.get()

        empleado = Empleado(None, nombre, apellido, edad, cargo, salario)  # Usar None para el ID
        self.archivoEmpleados.guardarEmpleado(empleado)
        messagebox.showinfo("Éxito", "Empleado agregado exitosamente")
        self.actualizarTabla()
        self.limpiarCamposEntrada()  # Limpiar los campos de texto después de agregar un empleado

    def limpiarCamposEntrada(self):
        self.entryNombre.delete(0, tk.END)
        self.entryApellido.delete(0, tk.END)
        self.entryEdad.delete(0, tk.END)
        self.comboCargo.set("")
        self.entrySalario.delete(0, tk.END)

    def eliminarEmpleado(self):
        # Obtener el ID del empleado seleccionado en la tabla
        item = self.tree.selection()[0]
        empleado_id = int(self.tree.item(item, "values")[0])

        # Llamar al método eliminarEmpleado del objeto ArchivoEmpleados
        self.archivoEmpleados.eliminarEmpleado(empleado_id)

        # Actualizar la tabla después de eliminar el empleado
        self.actualizarTabla()

    def editarEmpleado(self, event):
        # Obtener el ID del empleado seleccionado en la tabla
        item = self.tree.selection()[0]
        empleado_id = int(self.tree.item(item, "values")[0])

        # Llamar al método actualizarEmpleado con el ID correcto

        # Obtener los datos del empleado seleccionado
        empleados = self.archivoEmpleados.leerEmpleados()
        for empleado in empleados:
            if empleado.id == empleado_id:
                # Cargar los datos del empleado en los campos de entrada
                self.entryNombre.delete(0, tk.END)
                self.entryNombre.insert(0, empleado.nombre)
                self.entryApellido.delete(0, tk.END)
                self.entryApellido.insert(0, empleado.apellido)
                self.entryEdad.delete(0, tk.END)
                self.entryEdad.insert(0, empleado.edad)
                self.comboCargo.set(empleado.cargo)
                self.entrySalario.delete(0, tk.END)
                self.entrySalario.insert(0, empleado.salario)
                break

        # Desactivar el botón de agregar y cambiar el comando del botón agregar a actualizar
        self.buttonAgregar.config(text="Actualizar Empleado", command=lambda: self.actualizarEmpleado(empleado.id))
        self.buttonAgregar.grid(row=5, column=0, columnspan=2)

    def actualizarEmpleado(self, empleado_id):
        nombre = self.entryNombre.get()
        apellido = self.entryApellido.get()
        edad = self.entryEdad.get()
        cargo = self.comboCargo.get()
        salario = self.entrySalario.get()

        empleadoActualizado = Empleado(empleado_id, nombre, apellido, edad, cargo, salario)
        self.archivoEmpleados.actualizarEmpleado(empleadoActualizado)
        messagebox.showinfo("Éxito", "Empleado actualizado exitosamente")
        self.actualizarTabla()
        self.limpiarCamposEntrada()  # Limpiar los campos de texto después de actualizar un empleado

        # Restaurar el botón "Agregar Empleado" y su funcionalidad original
        self.buttonAgregar.config(text="Agregar Empleado", command=self.agregarEmpleado)
        self.buttonAgregar.grid(row=5, column=0, columnspan=2)

    def listarEmpleados(self):
        self.tree.delete(*self.tree.get_children())
        empleados = self.archivoEmpleados.leerEmpleados()
        for empleado in empleados:
            self.tree.insert("", "end", values=(empleado.id, empleado.nombre, empleado.apellido, empleado.edad, empleado.cargo, empleado.salario))

    def ventanaCentrada(self):
        # Método de ventanaCentrada: Centra la ventana en la pantalla
        anchoPantalla = self.winfo_screenwidth()
        altoPantalla = self.winfo_screenheight()
        x = (anchoPantalla / 2) - (900 / 2)
        y = (altoPantalla / 2) - (400 / 2)
        self.geometry("900x400+%d+%d" % (x, y))

    def actualizarTabla(self):
        self.listarEmpleados()

    def cerrarVentana(self):
        self.destroy()  # Cierra la ventana actual


# Cargos con sus salarios base
CARGOS = [
    ("Gerente", 1000000),
    ("Supervisor", 800000),
    ("Empleado", 600000)
]

