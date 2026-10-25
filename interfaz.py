import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter.font import Font
from altas import ventana_altas
from bajasCambios import ventana_bajasCambios
from consultas import VentanaConsultas
from reportes import Reportes
import psycopg2
import xml.etree.ElementTree as ET
from io import BytesIO  # Cambiar StringIO por BytesIO para manejar bytes
# Imports artisticos
from PIL import Image, ImageTk
import os

# Crear un panel para 'Consultas' y 'Reportes' que se divida en dos partes
def mostrar_panel_consultas_reportes(tipo):
    # Limpiar el panel principal
    for widget in frame_principal.winfo_children():
        widget.destroy()

    reportes = Reportes()

    if tipo == "reportes":
        reportes.mostrar_panel_reportes(frame_principal)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Interfaz de Gestión")
ventana.geometry("1400x800")

# Obtener la ruta relativa de las imágenes de fondo
directorio_actual = os.path.dirname(__file__)
ruta_fondo_principal = os.path.join(directorio_actual, "Stile", "interfaz2.jpg")
ruta_fondo_lateral = os.path.join(directorio_actual, "Stile", "fondo3.jpg")

# Cargar las imágenes de fondo
imagen_fondo_principal = Image.open(ruta_fondo_principal)
imagen_fondo_principal = imagen_fondo_principal.resize((1300, 900), Image.Resampling.LANCZOS)
imagen_fondo_principal_tk = ImageTk.PhotoImage(imagen_fondo_principal)

imagen_fondo_lateral = Image.open(ruta_fondo_lateral)
imagen_fondo_lateral = imagen_fondo_lateral.resize((200, 900), Image.Resampling.LANCZOS)
imagen_fondo_lateral_tk = ImageTk.PhotoImage(imagen_fondo_lateral)

# Panel lateral
frame_botones = tk.Frame(ventana, width=200, height=900)
frame_botones.pack(side=tk.LEFT, fill=tk.Y)

# Canvas para el fondo del panel lateral
canvas_lateral = tk.Canvas(frame_botones, width=200, height=900)
canvas_lateral.pack(fill="both", expand=True)
canvas_lateral.create_image(0, 0, image=imagen_fondo_lateral_tk, anchor="nw")

# Panel principal
frame_principal = tk.Frame(ventana, width=1300, height=900)
frame_principal.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Canvas para el fondo del panel principal
canvas_principal = tk.Canvas(frame_principal, width=1300, height=900)
canvas_principal.pack(fill="both", expand=True)
canvas_principal.create_image(0, 0, image=imagen_fondo_principal_tk, anchor="nw")


# Clase para generar XML
class GeneradorXML:
    def __init__(self, conexion):
        self.conexion = conexion

    def generar_xml(self, tabla_seleccionada, archivo_salida="salida.xml"):
        try:
            cursor = self.conexion.cursor()
            query = f"SELECT * FROM {tabla_seleccionada}"
            esquema = "SET search_path TO prueba;"
            cursor.execute(esquema)
            cursor.execute(query)
            columnas = [desc[0] for desc in cursor.description]
            registros = cursor.fetchall()

            # Crear la estructura XML
            raiz = ET.Element("Tabla", nombre=tabla_seleccionada)
            for registro in registros:
                elemento_fila = ET.SubElement(raiz, "Fila")
                for columna, valor in zip(columnas, registro):
                    elemento_columna = ET.SubElement(elemento_fila, columna)
                    elemento_columna.text = str(valor) if valor is not None else "NULL"

            # Guardar el archivo XML
            tree = ET.ElementTree(raiz)
            tree.write(archivo_salida, encoding="utf-8", xml_declaration=True)
            messagebox.showinfo("Éxito", f"Archivo XML generado: {archivo_salida}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el archivo XML: {e}")
        finally:
            cursor.close()

    @staticmethod
    def seleccionar_tabla_y_generar(conexion):
        ventana_seleccion = tk.Toplevel()
        ventana_seleccion.title("Seleccionar Tabla")
        ventana_seleccion.geometry("300x200")

        label = tk.Label(ventana_seleccion, text="Seleccione una tabla:")
        label.pack(pady=10)

        tablas_disponibles = ["persona", "cliente", "empleado", "proveedor", "categoria_producto"]

        combo_tablas = tk.StringVar(ventana_seleccion)
        combo_tablas.set(tablas_disponibles[0])

        menu_tablas = tk.OptionMenu(ventana_seleccion, combo_tablas, *tablas_disponibles)
        menu_tablas.pack(pady=10)

        def generar():
            tabla_seleccionada = combo_tablas.get()
            GeneradorXML(conexion).generar_xml(tabla_seleccionada)
            xml = open('salida.xml','r')
            xmlTxt = xml.read()
            mostrar_xml_en_panel(xmlTxt, frame_principal)
            ventana_seleccion.destroy()

        boton_generar = tk.Button(ventana_seleccion, text="Generar XML", command=generar)
        boton_generar.pack(pady=10)

def mostrar_xml_en_panel(xml_content, frame_principal):
    """Función para mostrar el contenido XML en un widget de texto en el panel principal."""
    # Limpiar el panel principal
    for widget in frame_principal.winfo_children():
        widget.destroy()

    # Crear un widget Text para mostrar el contenido del XML
    text_widget = tk.Text(frame_principal, wrap=tk.WORD)
    text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Insertar el contenido XML en el widget de texto
    text_widget.insert(tk.END, xml_content)

    # Deshabilitar la edición para que solo se pueda visualizar
    text_widget.config(state=tk.DISABLED)

fuente = Font(family="Code New Roman", size=11)

# Botones del menú
boton_altas = tk.Button(canvas_lateral, text="Altas", font=fuente, bg="white", command=lambda: ventana_altas(frame_principal))
boton_altas.pack(fill=tk.X, padx=10, pady=5)

boton_bajasCambios = tk.Button(canvas_lateral, text="Bajas/Cambios", font=fuente, bg="white", command=lambda: ventana_bajasCambios(frame_principal))
boton_bajasCambios.pack(fill=tk.X, padx=10, pady=5)

boton_consultas = tk.Button(canvas_lateral, text="Consultas", font=fuente, bg="white", command=lambda: VentanaConsultas(frame_principal))
boton_consultas.pack(fill=tk.X, padx=10, pady=5)

boton_reportes = tk.Button(canvas_lateral, text="Reportes", font=fuente, bg="white", command=lambda: mostrar_panel_consultas_reportes("reportes"))
boton_reportes.pack(fill=tk.X, padx=10, pady=5)

reportes = Reportes()  # Instancia de la clase Reportes
boton_generar_xml = tk.Button(canvas_lateral, text="Generar XML", font=fuente, bg="white", command=lambda: GeneradorXML.seleccionar_tabla_y_generar(reportes.conexion))
boton_generar_xml.pack(fill=tk.X, padx=10, pady=5)

boton_salir = tk.Button(canvas_lateral, text="Salir", font=fuente, bg="white", command=ventana.destroy)
boton_salir.pack(fill=tk.X, padx=10, pady=5)

# Etiqueta de información principal
label_info = tk.Label(frame_principal, text="Panel que muestra la información de cada botón", bg="gray", fg="white")
label_info.pack(expand=True)

ventana.mainloop()
