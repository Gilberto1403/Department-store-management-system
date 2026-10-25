import psycopg2
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
# Imports artisticos
from PIL import Image, ImageTk
import os

# Configuración de conexión a la base de datos
db_config = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "diegomc21",
    "host": "localhost",
    "port": 5432,
    "client_encoding": "UTF8"
}


# Función para verificar usuario y contraseña
def verificar_usuario_contrasena(usuario, contrasena):
    try:
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()
        query = "SELECT * FROM usuarios WHERE usuario = %s AND contrasena = %s"
        esquema = "SET search_path TO prueba;"
        cursor.execute(esquema)
        cursor.execute(query, (usuario, contrasena))
        return cursor.fetchone() is not None
    except psycopg2.Error as e:
        messagebox.showerror("Error", f"Error al conectar con la base de datos:\n{e}")
        return False
    finally:
        if 'connection' in locals() and connection:
            cursor.close()
            connection.close()


# Función para iniciar sesión
def iniciar_sesion():
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()

    if verificar_usuario_contrasena(usuario, contrasena):
        messagebox.showinfo("Inicio de sesión", "¡Inicio de sesión exitoso!")
        ventana_inicio.destroy()  # Cerrar la ventana actual

        # Ejecutar el segundo programa
        try:
            subprocess.run(["python", "interfaz.py"])
        except Exception as e:
            messagebox.showerror("Error", f"Error al ejecutar el programa:\n{e}")
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos.")


# Diseño visual
ventana_inicio = tk.Tk()
ventana_inicio.title("Inicio de sesión")
ventana_inicio.geometry("600x500")  # Tamaño actualizado
ventana_inicio.resizable(False, False)

# Obtener la ruta relativa de la imagen de fondo
directorio_actual = os.path.dirname(__file__)
ruta_fondo = os.path.join(directorio_actual, "Stile", "fondo2.jpg")
ruta_usuario_icono = os.path.join(directorio_actual, "Stile", "usuario2.png")
ruta_contrasena_icono = os.path.join(directorio_actual, "Stile", "contrasena2.png")

# Cargar la imagen de fondo
imagen_fondo = Image.open(ruta_fondo)
imagen_fondo = imagen_fondo.resize((600, 500), Image.Resampling.LANCZOS)  # Ajustar al nuevo tamaño
imagen_fondo_tk = ImageTk.PhotoImage(imagen_fondo)

# Cargar los íconos
icono_usuario = Image.open(ruta_usuario_icono)
icono_usuario_tk = ImageTk.PhotoImage(icono_usuario)

icono_contrasena = Image.open(ruta_contrasena_icono)
icono_contrasena_tk = ImageTk.PhotoImage(icono_contrasena)

# Crear un Canvas para mostrar la imagen de fondo
canvas = tk.Canvas(ventana_inicio, width=600, height=500, highlightthickness=0)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=imagen_fondo_tk, anchor="nw")

# Crear un frame blanco transparente con esquinas redondeadas
frame_x, frame_y, frame_width, frame_height = 150, 100, 300, 300  # Centrado en la ventana
canvas.create_rectangle(
    frame_x, frame_y, frame_x + frame_width, frame_y + frame_height,
    fill="#FFFFFF", outline="", width=0, stipple="gray50"
)

# Añadir widgets al canvas
# Ícono y campo de usuario
canvas.create_image(300, 160, image=icono_usuario_tk, anchor="center")  # Ícono de usuario centrado
entry_usuario = ttk.Entry(ventana_inicio, font=("Arial", 12))
canvas.create_window(300, 200, window=entry_usuario, width=250, height=30)

# Ícono y campo de contraseña
canvas.create_image(300, 260, image=icono_contrasena_tk, anchor="center")  # Ícono de contraseña centrado
entry_contrasena = ttk.Entry(ventana_inicio, font=("Arial", 12), show="*")
canvas.create_window(300, 300, window=entry_contrasena, width=250, height=30)

# Crear estilo personalizado para el botón
style = ttk.Style()
style.configure(
    "Custom.TButton",
    font=("Code New Roman", 12, "bold"),
    background="white",
    foreground="black",
    focuscolor="none",
    borderwidth=1
)
style.map(
    "Custom.TButton",
    background=[("active", "#E0E0E0")],  # Cambiar color al pasar el cursor
    relief=[("pressed", "groove")]
)

# Botón para iniciar sesión
boton = ttk.Button(ventana_inicio, text="Iniciar sesión", command=iniciar_sesion, style="Custom.TButton")
canvas.create_window(300, 380, window=boton, width=150)

# Ejecutar la ventana
ventana_inicio.mainloop()
