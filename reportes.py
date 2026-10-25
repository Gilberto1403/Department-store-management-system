import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
from datetime import datetime
from tkinter.font import Font
from tkcalendar import Calendar
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Reportes:

    def __init__(self):
         # Conexión a la base de datos en el constructor
        self.conexion = self.conectar_bd()
        self.tipo_grafico = tk.StringVar(value="bar")  # Tipo de gráfico por defecto
        self.graficas_mostradas = []  # Lista para almacenar las gráficas activas

    def conectar_bd(self):
        try:
            conexion = psycopg2.connect(
                dbname="postgres", user="postgres", password="diegomc21", host="localhost", port="5432"
            )
            return conexion
        except psycopg2.OperationalError as e:
            messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos: {e}")
            return None

    def mostrar_panel_reportes(self, frame_principal):
        """Configura la interfaz de los reportes."""
        # Limpiar el panel principal
        for widget in frame_principal.winfo_children():
            widget.destroy()

        fuente = Font(family="Code New Roman", size=10)

        # Crear un panel para la selección de fechas y opciones
        panel_fechas = tk.Frame(frame_principal, bg="lightgray", height=200)
        panel_fechas.pack(fill=tk.X, padx=10, pady=5)

        # Panel para gráficos, guardado como atributo de la clase
        self.panel_graficas = tk.Frame(frame_principal, bg="darkgray")
        self.panel_graficas.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Crear calendario para seleccionar las fechas
        label_inicio = tk.Label(panel_fechas, text="Fecha de inicio:", font=fuente, bg="lightgray")
        label_inicio.pack(side=tk.LEFT, padx=5)

        self.cal_inicio = Calendar(panel_fechas, selectmode='day', date_pattern='yyyy-mm-dd')
        self.cal_inicio.pack(side=tk.LEFT, padx=5)

        label_fin = tk.Label(panel_fechas, text="Fecha de fin:", font=fuente, bg="lightgray")
        label_fin.pack(side=tk.LEFT, padx=5)

        self.cal_fin = Calendar(panel_fechas, selectmode='day', date_pattern='yyyy-mm-dd')
        self.cal_fin.pack(side=tk.LEFT, padx=5)

        # Menú desplegable para seleccionar tipo de gráfica
        label_tipo = tk.Label(panel_fechas, text="Tipo de gráfica:", font=fuente, bg="lightgray")
        label_tipo.pack(side=tk.LEFT, padx=5)

        opciones_tipo = ttk.Combobox(panel_fechas, textvariable=self.tipo_grafico, values=["bar", "line", "scatter", "pie"])
        opciones_tipo.pack(side=tk.LEFT, padx=5)

        # Botón para generar el reporte ROLLUP
        boton_rollup = tk.Button(panel_fechas, text="Generar Reporte ROLLUP", font=fuente, bg="darkgray", command=lambda: self.generar_rollup())
        boton_rollup.pack(side=tk.LEFT, pady=10, padx=5)

    def generar_rollup(self):
        # Solicitar al usuario el producto (por ejemplo, ID)
        producto_id = simpledialog.askstring("Producto", "Ingrese el ID del producto (deje en blanco para todos)")

        # Si el campo está vacío, asignamos None (para no filtrar por producto)
        if producto_id == '':
            producto_id = None
        else:
            try:
                producto_id = int(producto_id)
            except ValueError:
                messagebox.showerror("Error", "El ID del producto debe ser un número entero.")
                return

        # Obtener las fechas seleccionadas desde el calendario
        fecha_inicio = self.cal_inicio.get_date()
        fecha_fin = self.cal_fin.get_date()

        if fecha_inicio > fecha_fin:
            messagebox.showerror("Error", "La fecha de inicio no puede ser mayor que la fecha de fin.")
            return

        rango_fechas = (fecha_inicio, fecha_fin)

        # Llamar al método de ROLLUP para obtener los datos
        df = self.realizar_rollup(producto_id, rango_fechas)

        # Si se obtuvieron resultados, graficar los datos
        if df is not None and not df.empty:
            self.agregar_grafica(df)
            self.generar_resumen_estadistico(df)  # Llama al método para generar el resumen

        else:
            messagebox.showinfo("Sin Datos", "No se encontraron datos para los parámetros proporcionados.")

    def realizar_rollup(self, producto_id, rango_fechas):
        """
        Ejecuta la consulta ROLLUP basada en el ID del producto y el rango de fechas.
        
        :param producto_id: ID del producto para filtrar, o None si no aplica.
        :param rango_fechas: Tupla con las fechas de inicio y fin.
        :return: DataFrame con los datos de ventas o None.
        """
        try:
            cursor = self.conexion.cursor()
            esquema = "SET search_path TO prueba;"
            cursor.execute(esquema)
            
            # Construir consulta dinámica dependiendo del ID del producto
            if producto_id is None:
                query = """
                    SELECT fecha_venta, 
                           SUM(total_venta) AS total_ventas, 
                           SUM(cantidad_productos) AS cantidad_productos 
                    FROM venta 
                    WHERE fecha_venta BETWEEN %s AND %s 
                    GROUP BY fecha_venta 
                    ORDER BY fecha_venta
                """
                params = (rango_fechas[0], rango_fechas[1])
            else:
                query = """
                    SELECT fecha_venta, 
                           SUM(total_venta) AS total_ventas, 
                           SUM(cantidad_productos) AS cantidad_productos 
                    FROM venta 
                    WHERE sku_producto = %s AND fecha_venta BETWEEN %s AND %s 
                    GROUP BY fecha_venta 
                    ORDER BY fecha_venta
                """
                params = (producto_id, rango_fechas[0], rango_fechas[1])
            
            cursor.execute(query, params)
            data = cursor.fetchall()

            # Convertir los resultados a un DataFrame
            return pd.DataFrame(data, columns=["fecha_venta", "total_ventas", "cantidad_productos"]) \
                if data else None

        except Exception as e:
            messagebox.showerror(
                "Error al ejecutar la consulta", 
                f"Ha ocurrido un error al ejecutar la consulta: {e}"
            )
            return None

    def agregar_grafica(self, df):
        """Agrega una gráfica al panel de gráficas si no se supera el límite."""
        if len(self.graficas_mostradas) >= 3:
            messagebox.showerror("Límite Alcanzado", "Solo puedes mostrar un máximo de tres gráficas al mismo tiempo.")
            return

        # Crear el gráfico
        fig, ax = plt.subplots(figsize=(8, 4))
        tipo = self.tipo_grafico.get()

        try:
            if tipo == "bar":
                df.groupby("fecha_venta")["total_ventas"].sum().plot(kind="bar", ax=ax)
            elif tipo == "line":
                df.groupby("fecha_venta")["total_ventas"].sum().plot(kind="line", ax=ax)
            elif tipo == "scatter":
                ax.scatter(df["fecha_venta"], df["total_ventas"], c="blue")
                ax.set_title("Gráfico de Dispersión")
            elif tipo == "pie":
                df.groupby("fecha_venta")["total_ventas"].sum().plot(kind="pie", ax=ax, autopct="%1.1f%%")
                ax.set_ylabel("")

            ax.set_title("Reporte de Ventas")
            ax.set_xlabel("Fecha")
            ax.set_ylabel("Total de Ventas")

            # Integrar el gráfico en el panel de gráficas
            frame_grafica = tk.Frame(self.panel_graficas, bg="white", relief=tk.SUNKEN, borderwidth=1)
            frame_grafica.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

            canvas = FigureCanvasTkAgg(fig, master=frame_grafica)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

            # Agregar el marco a la lista de gráficas activas
            self.graficas_mostradas.append(frame_grafica)

            fuente = Font(family="Code New Roman", size=11)

            # Botón para cerrar esta gráfica específica
            boton_cerrar = tk.Button(frame_grafica, text="Cerrar Gráfica", font=fuente, bg="red", fg="white", command=lambda: self.eliminar_grafica(frame_grafica))
            boton_cerrar.pack()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el gráfico: {e}")
    
    def eliminar_grafica(self, frame_grafica):
        """Elimina una gráfica del panel de gráficas."""
        frame_grafica.destroy()
        self.graficas_mostradas.remove(frame_grafica)

    def graficar_en_frame(self, df, frame):
        fig, ax = plt.subplots(figsize=(8, 4))
        df.groupby('fecha_venta')['total_ventas'].sum().plot(kind='bar', ax=ax)
        ax.set_title("Reporte de Ventas")
        ax.set_xlabel("Fecha")
        ax.set_ylabel("Total de Ventas")

        for widget in frame.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def generar_resumen_estadistico(self, df):
        total_ventas = df['total_ventas'].sum()
        promedio_ventas = df['total_ventas'].mean()
        max_venta = df['total_ventas'].max()
        min_venta = df['total_ventas'].min()

        resumen = (
            f"Total de Ventas: {total_ventas}\n"
            f"Promedio Diario de Ventas: {promedio_ventas:.2f}\n"
            f"Venta Máxima: {max_venta}\n"
            f"Venta Mínima: {min_venta}"
        )
        messagebox.showinfo("Resumen Estadístico", resumen)
