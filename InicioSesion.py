import tkinter as Tk
from tkinter import messagebox
import os
from Dashboard import VentanaDashboard

class SingletonMeta(type):
    """Metaclass para implementar el patrón Singleton."""
    _instancia = {} # Usamos un diccionario para almacenar instancias únicas de clases

    """
    Método __call__:
    - Permite llamar a la clase como si fuera una función.
    - Verifica si la clase ya tiene una instancia creada y la devuelve.
    - Si no existe, crea una nueva instancia y la almacena para futuras llamadas.
    """
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instancia:
            cls._instancia[cls] = super().__call__(*args, **kwargs)
        return cls._instancia[cls]

class VentanaInicioSesion(Tk.Tk, metaclass=SingletonMeta):
    """
    Método __init__:
    - Constructor de la clase.
    - Configura la apariencia de la ventana y carga los objetos (botones, campos de texto, etc) necesarios.
    """
    def __init__(self):
        super().__init__()
        # Configuración de la ventana de inicio de sesión
        self.title("Inicio de sesión")
        self.geometry("500x350")
        self.ventanaCentrada()

        try:
            # Cargar imagen de fondo si existe, por alguna razon, si no se encuentra entro de un try, la imagen no se carga
            self.imagenFondo = Tk.PhotoImage(file="imagenes/fondo_inicio.png")
            self.etiquetaFondo = Tk.Label(self, image=self.imagenFondo)
            self.etiquetaFondo.place(relwidth=1, relheight=1)
        except Tk.TclError as e:
            # Manejo de errores si la imagen no se puede cargar
            print("Error al cargar la imagen de fondo:", e)

        # Creación de ventana, con sus respectivas etiquetas, y campos de texto y contraseña, además de los botones

        self.ventana = Tk.Frame(self, bg='#ffffff', bd=5)
        self.ventana.place(relx=0.5, rely=0.2, relwidth=0.85, relheight=0.35, anchor='n')

        self.etiquetaUsuario = Tk.Label(self.ventana, text="Usuario:", bg='#ffffff', fg='#333333', font=("Helvetica", 12))
        self.etiquetaUsuario.place(relx=0.05, rely=0.1, relwidth=0.2, relheight=0.2)

        self.campoUsuario = Tk.Entry(self.ventana, bg='#f0f0f0', font=("Helvetica", 12))
        self.campoUsuario.place(relx=0.3, rely=0.1, relwidth=0.65, relheight=0.2)

        self.etiquetaContraseña = Tk.Label(self.ventana, text="Contraseña:", bg='#ffffff', fg='#333333', font=("Helvetica", 12))
        self.etiquetaContraseña.place(relx=0.05, rely=0.4, relwidth=0.2, relheight=0.2)

        self.campoContraseña = Tk.Entry(self.ventana, bg='#f0f0f0', font=("Helvetica", 12), show="*")
        self.campoContraseña.place(relx=0.3, rely=0.4, relwidth=0.65, relheight=0.2)

        self.botonIniciarSesion = Tk.Button(self, text="Iniciar sesión", command=self.iniciarSesion, bg='#333333', fg='white', font=("Helvetica", 12))
        self.botonIniciarSesion.place(relx=0.5, rely=0.7, relwidth=0.3, relheight=0.1, anchor='n')

        self.botonRegistrar = Tk.Button(self, text="Registrar", command=self.registrar, bg='#333333', fg='white', font=("Helvetica", 12))
        self.botonRegistrar.place(relx=0.5, rely=0.85, relwidth=0.3, relheight=0.1, anchor='n')

        # Carga de datos de usuarios desde un archivo
        self.datosUsuario = {}
        if os.path.exists("usuarios.txt"):
            with open("usuarios.txt", "r") as archivo:
                for linea in archivo:
                    usuario, contraseña = linea.strip().split(":")
                    self.datosUsuario[usuario] = contraseña

    def ventanaCentrada(self):
        #Método de ventanaCentrada: Centra la ventana en la pantalla
        anchoPantalla = self.winfo_screenwidth()
        altoPantalla = self.winfo_screenheight()
        x = (anchoPantalla / 2) - (500 / 2)
        y = (altoPantalla / 2) - (350 / 2)
        self.geometry("500x350+%d+%d" % (x, y))


    def decoradorIniciarSesion(func):
        """
        Decorador decoradorIniciarSesion:
        - Obtiene los datos de usuario y contraseña del formulario.
        - Imprime un mensaje indicando el intento de inicio de sesión.
        """
        def manejoDatos(self):
            usuario = self.campoUsuario.get()
            contraseña = self.campoContraseña.get()
            print(f"Intento de inicio de sesión para usuario: {usuario}")
            return func(self, usuario, contraseña)
        return manejoDatos

    def decoradorRegistrar(func):
        """
        Decorador decoradorRegistrar:
        - Obtiene los datos de usuario y contraseña del formulario.
        - Imprime un mensaje indicando el intento de registro de usuario.
        """
        def manejoDatos(self):
            usuario = self.campoUsuario.get()
            contraseña = self.campoContraseña.get()
            print(f"Intento de registro para usuario: {usuario}")
            return func(self, usuario, contraseña)
        return manejoDatos

    @decoradorIniciarSesion
    def iniciarSesion(self, usuario, contraseña):
        """
        Método iniciarSesion:
        - Verifica las credenciales del usuario para iniciar sesión.
        - Muestra un mensaje estilo pop up con el resultado del inicio de sesión.
        """
        if usuario in self.datosUsuario:
            if self.datosUsuario[usuario] == contraseña:
                messagebox.showinfo("Inicio de sesión", "Inicio de sesión exitoso")
                #codigo para la siguiente pantalla
                self.destroy()
                app = VentanaDashboard()
                app.mainloop()
            else:
                messagebox.showerror("Error", "Contraseña incorrecta")
        else:
            messagebox.showerror("Error", "Usuario no encontrado")

    @decoradorRegistrar
    def registrar(self, usuario, contraseña):
        """
        Método registrar:
        - almacena las credenciales del usuario, en el archivo usuarios.txt, para un futuro iniciar sesión.
        - Muestra un mensaje estilo pop up con el resultado del registro.
        """
        if usuario in self.datosUsuario:
            messagebox.showerror("Error", "El usuario ya existe")
        else:
            self.datosUsuario[usuario] = contraseña
            with open("usuarios.txt", "a") as archivo:
                archivo.write(f"{usuario}:{contraseña}\n")
            messagebox.showinfo("Registro", "Usuario registrado exitosamente")
