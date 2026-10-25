import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
import psycopg2
from tkinter import messagebox

class ConexionDB:
    def __init__(self):
        try:
            self.conexion = psycopg2.connect(
                dbname="postgres",
                user="postgres",
                password="diegomc21",
                host="localhost",
                port=5432
            )
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo conectar a la base de datos: {e}")

    def ejecutar_query(self, query, params=None):
        try:
            cursor = self.conexion.cursor()
            esquema = "SET search_path TO prueba;"
            cursor.execute(esquema)
            cursor.execute(query, params or ())
            resultado = {"filas": cursor.fetchall(), "descripcion": cursor.description}
            cursor.close()
            return resultado
        except Exception as e:
            messagebox.showerror("Error", f"Error al ejecutar la consulta: {e}")
            return None

    def obtener_columnas(self, tabla):
        try:
            cursor = self.conexion.cursor()
            cursor.execute("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = %s;
            """, (tabla,))
            columnas = [row[0] for row in cursor.fetchall()]
            cursor.close()
            return columnas
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener columnas: {e}")
            return []

    def cerrar(self):
        self.conexion.close()

class VentanaConsultas:
    def __init__(self, frame_principal):
        self.frame_principal = frame_principal
        self.panel_abajo = None
        self.combo_tablas = None
        self.entry_busqueda = None
        self.db = ConexionDB()  # Conexión reutilizable
        self.inicializar_panel()

    def inicializar_panel(self):
        for widget in self.frame_principal.winfo_children():
            widget.destroy()

        fuente = Font(family="Code New Roman", size=11)

        panel_arriba = tk.Frame(self.frame_principal, bg="lightgray", height=150)
        panel_arriba.pack(fill=tk.X, padx=10, pady=5)

        panel_arriba.grid_rowconfigure(0, weight=1)
        panel_arriba.grid_rowconfigure(1, weight=1)
        panel_arriba.grid_rowconfigure(2, weight=1)
        panel_arriba.grid_columnconfigure(0, weight=1)
        panel_arriba.grid_columnconfigure(1, weight=1)

        label_arriba = tk.Label(panel_arriba, text="Seleccione una tabla para consultar datos", font=fuente, bg="lightgray")
        label_arriba.grid(row=0, column=0, columnspan=2, pady=5)

        label_tabla = tk.Label(panel_arriba, text="Tabla:", font=fuente, bg="lightgray")
        label_tabla.grid(row=1, column=0, padx=5, pady=5)

        tablas = ["categoria_producto", "persona", "cliente", "empleado", "facturacion", "inventario",
                  "metodo_pago", "producto", "proveedor", "tienda", "usuarios", "venta"]
        self.combo_tablas = ttk.Combobox(panel_arriba, values=tablas)
        self.combo_tablas.grid(row=1, column=1, padx=5, pady=5)

        label_busqueda = tk.Label(panel_arriba, text="Buscar:", font=fuente, bg="lightgray")
        label_busqueda.grid(row=2, column=0, padx=5, pady=5)

        self.entry_busqueda = tk.Entry(panel_arriba)
        self.entry_busqueda.grid(row=2, column=1, padx=5, pady=5)

        boton_continuar = tk.Button(panel_arriba, text="Consultar", font=fuente, command=self.consultar_tabla)
        boton_continuar.grid(row=3, column=0, columnspan=2, pady=10)

        canvas = tk.Canvas(self.frame_principal)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(self.frame_principal, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.panel_abajo = tk.Frame(canvas, bg="lightgray")
        canvas.create_window((0, 0), window=self.panel_abajo, anchor="nw")

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        self.panel_abajo.bind("<Configure>", on_frame_configure)
        canvas.configure(yscrollcommand=scrollbar.set)

    def consultar_tabla(self):
        tabla_seleccionada = self.combo_tablas.get()
        termino_busqueda = self.entry_busqueda.get()

        if tabla_seleccionada:
            self.mostrar_resultados(tabla_seleccionada, termino_busqueda)
        else:
            messagebox.showwarning("Advertencia", "Seleccione una tabla válida para consultar.")

    def mostrar_resultados(self, tabla, termino_busqueda):
        for widget in self.panel_abajo.winfo_children():
            widget.destroy()

        fuente = Font(family="Code New Roman", size=11)

        columnas = self.db.obtener_columnas(tabla)
        if not columnas:
            return

        query, params = self.formar_consulta(tabla, columnas, termino_busqueda)
        resultados = self.db.ejecutar_query(query, params)

        if resultados:
            encabezados = [desc[0] for desc in resultados["descripcion"]]
            for col, encabezado in enumerate(encabezados):
                label = tk.Label(self.panel_abajo, text=encabezado, font=fuente, bg="gray", fg="white", width=15)
                label.grid(row=0, column=col, padx=5, pady=5)

            for fila, datos in enumerate(resultados["filas"], start=1):
                for col, valor in enumerate(datos):
                    label = tk.Label(self.panel_abajo, text=valor, font=fuente, bg="white", width=15, relief="solid")
                    label.grid(row=fila, column=col, padx=5, pady=5)
        else:
            messagebox.showinfo("Información", f"No se encontraron resultados en la tabla '{tabla}'.")

    def formar_consulta(self, tabla, columnas, termino_busqueda):
        if termino_busqueda:
            palabras = termino_busqueda.split()
            condiciones = []

            for palabra in palabras:
                condiciones_por_palabra = [
                    f"CAST({col} AS TEXT) ILIKE %s" for col in columnas
                ]
                condiciones.append(f"({' OR '.join(condiciones_por_palabra)})")

            query = f"SELECT * FROM {tabla} WHERE {' AND '.join(condiciones)};"
            params = [f"%{palabra}%" for palabra in palabras for _ in columnas]
        else:
            query = f"SELECT * FROM {tabla};"
            params = []

        return query, params