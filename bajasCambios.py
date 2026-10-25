import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter.font import Font 

import psycopg2

# Función para conectar a PostgreSQL y ejecutar una consulta
def ejecutar_consulta(query, params=None, fetch=False):
    try:
        conexion = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="diegomc21",
            host="localhost",
            port=5432
        )
        cursor = conexion.cursor()
        esquema = "SET search_path TO prueba;"
        cursor.execute(esquema)
        cursor.execute(query, params)
        if fetch:
            return cursor.fetchall()
        conexion.commit()
        cursor.close()
        conexion.close()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo conectar a la base de datos: {e}")

# Función para manejar la inserción de datos en la tabla persona
def mostrar_registros_tabla(tabla, panel_abajo):
    # Limpiar el panel
    for widget in panel_abajo.winfo_children():
        widget.destroy()

    fuente = Font(family="Code New Roman", size=11)

    # Obtener las columnas de la tabla seleccionada
    columnas_query = f"""
    SELECT column_name 
    FROM information_schema.columns 
    WHERE table_name = %s
    ORDER BY ordinal_position;
    """
    columnas = ejecutar_consulta(columnas_query, params=(tabla,), fetch=True)
    nombres_columnas = [columna[0] for columna in columnas]

    # Obtener los registros de la tabla
    datos_query = f"SELECT * FROM {tabla}"
    registros = ejecutar_consulta(datos_query, fetch=True)

    # Crear el Treeview dinámicamente
    tree = ttk.Treeview(panel_abajo, columns=nombres_columnas, show="headings")
    tree.pack(fill=tk.BOTH, expand=True)

    # Configurar encabezados dinámicos
    for columna in nombres_columnas:
        tree.heading(columna, text=columna)
        tree.column(columna, width=100)

    # Insertar los registros obtenidos
    for registro in registros:
        tree.insert("", tk.END, values=registro)

    # Función para eliminar el registro seleccionado
    def eliminar_registro():
        seleccionado = tree.focus()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Por favor selecciona un registro.")
            return

        valores = tree.item(seleccionado, "values")
        id_registro = valores[0]  # Suponemos que la primera columna es la clave primaria
        columna_id = nombres_columnas[0]

        query = f"DELETE FROM {tabla} WHERE {columna_id} = %s"
        ejecutar_consulta(query, (id_registro,))
        messagebox.showinfo("Éxito", "Registro eliminado correctamente.")
        tree.delete(seleccionado)

    # Función para editar el registro seleccionado
    def editar_registro():
        seleccionado = tree.focus()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Por favor selecciona un registro.")
            return

        valores = tree.item(seleccionado, "values")

        # Crear ventana para editar
        ventana_editar = tk.Toplevel()
        ventana_editar.title("Editar Registro")
        ventana_editar.geometry("400x400")

        entradas = {}

        # Crear campos dinámicamente para cada columna
        for i, columna in enumerate(nombres_columnas):
            tk.Label(ventana_editar, text=f"{columna}:").pack(pady=5)
            entrada = tk.Entry(ventana_editar)
            entrada.insert(0, valores[i])  # Valor actual de la columna
            entrada.pack(pady=5)
            entradas[columna] = entrada

        def confirmar_cambios():
            nuevos_valores = {columna: entradas[columna].get() for columna in nombres_columnas}

            # Validar cambios (puedes añadir más validaciones aquí)
            if any(valor == "" for valor in nuevos_valores.values()):
                messagebox.showwarning("Advertencia", "Todos los campos deben estar completos.")
                return

            # Construir consulta de actualización dinámica
            set_clause = ", ".join(f"{columna} = %s" for columna in nombres_columnas[1:])  # Omitimos la PK
            params = [nuevos_valores[columna] for columna in nombres_columnas[1:]]  # Omitimos la PK
            params.append(valores[0])  # Agregamos la PK al final para el WHERE

            query = f"UPDATE {tabla} SET {set_clause} WHERE {nombres_columnas[0]} = %s"
            ejecutar_consulta(query, tuple(params))
            messagebox.showinfo("Éxito", "Registro actualizado correctamente.")
            ventana_editar.destroy()

            # Refrescar el registro en el Treeview
            tree.item(seleccionado, values=tuple(nuevos_valores.values()))

        # Botón de confirmación
        boton_confirmar = tk.Button(ventana_editar, text="Confirmar", font=fuente, command=confirmar_cambios)
        boton_confirmar.pack(pady=10)

    # Botones para eliminar y editar
    boton_eliminar = tk.Button(panel_abajo, text="Eliminar", font=fuente, command=eliminar_registro)
    boton_eliminar.pack(side=tk.LEFT, padx=10, pady=10)

    boton_editar = tk.Button(panel_abajo, text="Editar", font=fuente, command=editar_registro)
    boton_editar.pack(side=tk.RIGHT, padx=10, pady=10)
   
# Función para mostrar el formulario y manejar la selección de la tabla
def ventana_bajasCambios(frame_principal):
    global entry_id_categoria

    # Limpiar el panel principal
    for widget in frame_principal.winfo_children():
        widget.destroy()

    fuente = Font(family="Code New Roman", size=11)

    # Crear los paneles dentro del frame_principal
    panel_arriba = tk.Frame(frame_principal, bg="lightgray", height=100)
    panel_arriba.pack(fill=tk.X, padx=10, pady=5)

    # Crear un canvas para añadir un scrollbar al panel de abajo
    canvas = tk.Canvas(frame_principal)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(frame_principal, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Crear el frame que contendrá el formulario dentro del canvas
    panel_abajo = tk.Frame(canvas, bg="lightgray")
    canvas.create_window((0, 0), window=panel_abajo, anchor="nw")

    # Configurar el canvas para que funcione con el scrollbar
    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    panel_abajo.bind("<Configure>", on_frame_configure)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Etiqueta en el panel de arriba
    label_arriba = tk.Label(panel_arriba, text="Seleccione una tabla para ingresar datos", font=fuente, bg="lightgray")
    label_arriba.pack(expand=True)

    # Menú de opciones para seleccionar la tabla
    label_tabla = tk.Label(panel_arriba, text="Tabla:", font=fuente, bg="lightgray")
    label_tabla.pack(pady=5)

    tablas = ["categoria_producto", "persona", "cliente", "empleado", "facturacion", "inventario","usuarios","metodo_pago","tienda","venta","proveedor","producto"]
    tabla_seleccionada = tk.StringVar()
    combo_tablas = ttk.Combobox(panel_arriba, textvariable=tabla_seleccionada, values=tablas)
    combo_tablas.pack(pady=5)

    def continuar():
        if combo_tablas.get():
            mostrar_registros_tabla(combo_tablas.get(), panel_abajo)

    # Botón para continuar con la tabla seleccionada
    boton_continuar = tk.Button(panel_arriba, text="Continuar", font=fuente, command=continuar)
    boton_continuar.pack(pady=10)

def mostrar_registros_inventario(panel_abajo):
    # Limpiar el panel
    for widget in panel_abajo.winfo_children():
        widget.destroy()

    # Obtener las columnas de la tabla inventario
    columnas_query = f"""
    SELECT column_name 
    FROM information_schema.columns 
    WHERE table_name = 'inventario'
    ORDER BY ordinal_position;
    """
    columnas = ejecutar_consulta(columnas_query, fetch=True)
    nombres_columnas = [columna[0] for columna in columnas]

    # Obtener los registros de la tabla
    datos_query = f"SELECT * FROM inventario"
    registros = ejecutar_consulta(datos_query, fetch=True)

    # Crear el Treeview dinámicamente
    tree = ttk.Treeview(panel_abajo, columns=nombres_columnas, show="headings")
    tree.pack(fill=tk.BOTH, expand=True)

    # Configurar encabezados dinámicos
    for columna in nombres_columnas:
        tree.heading(columna, text=columna)
        tree.column(columna, width=100)

    # Insertar los registros obtenidos
    for registro in registros:
        tree.insert("", tk.END, values=registro)

def mostrar_registros_facturacion(panel_abajo):
    # Limpiar el panel
    for widget in panel_abajo.winfo_children():
        widget.destroy()

    # Obtener las columnas de la tabla facturacion
    columnas_query = f"""
    SELECT column_name 
    FROM information_schema.columns 
    WHERE table_name = 'facturacion'
    ORDER BY ordinal_position;
    """
    columnas = ejecutar_consulta(columnas_query, fetch=True)
    nombres_columnas = [columna[0] for columna in columnas]

    # Obtener los registros de la tabla
    datos_query = f"SELECT * FROM facturacion"
    registros = ejecutar_consulta(datos_query, fetch=True)

    # Crear el Treeview dinámicamente
    tree = ttk.Treeview(panel_abajo, columns=nombres_columnas, show="headings")
    tree.pack(fill=tk.BOTH, expand=True)

    # Configurar encabezados dinámicos
    for columna in nombres_columnas:
        tree.heading(columna, text=columna)
        tree.column(columna, width=100)

    # Insertar los registros obtenidos
    for registro in registros:
        tree.insert("", tk.END, values=registro)

def mostrar_registros_empleado(panel_abajo):
    # Limpiar el panel
    for widget in panel_abajo.winfo_children():
        widget.destroy()

    # Obtener las columnas de la tabla empleado
    columnas_query = f"""
    SELECT column_name 
    FROM information_schema.columns 
    WHERE table_name = 'empleado'
    ORDER BY ordinal_position;
    """
    columnas = ejecutar_consulta(columnas_query, fetch=True)
    nombres_columnas = [columna[0] for columna in columnas]

    # Obtener los registros de la tabla
    datos_query = f"SELECT * FROM empleado"
    registros = ejecutar_consulta(datos_query, fetch=True)

    # Crear el Treeview dinámicamente
    tree = ttk.Treeview(panel_abajo, columns=nombres_columnas, show="headings")
    tree.pack(fill=tk.BOTH, expand=True)

    # Configurar encabezados dinámicos
    for columna in nombres_columnas:
        tree.heading(columna, text=columna)
        tree.column(columna, width=100)

    # Insertar los registros obtenidos
    for registro in registros:
        tree.insert("", tk.END, values=registro)

def mostrar_registros_cliente(panel_abajo):
    # Limpiar el panel
    for widget in panel_abajo.winfo_children():
        widget.destroy()

    # Obtener las columnas de la tabla cliente
    columnas_query = f"""
    SELECT column_name 
    FROM information_schema.columns 
    WHERE table_name = 'cliente'
    ORDER BY ordinal_position;
    """
    columnas = ejecutar_consulta(columnas_query, fetch=True)
    nombres_columnas = [columna[0] for columna in columnas]

    # Obtener los registros de la tabla
    datos_query = f"SELECT * FROM cliente"
    registros = ejecutar_consulta(datos_query, fetch=True)

    # Crear el Treeview dinámicamente
    tree = ttk.Treeview(panel_abajo, columns=nombres_columnas, show="headings")
    tree.pack(fill=tk.BOTH, expand=True)

    # Configurar encabezados dinámicos
    for columna in nombres_columnas:
        tree.heading(columna, text=columna)
        tree.column(columna, width=100)

    # Insertar los registros obtenidos
    for registro in registros:
        tree.insert("", tk.END, values=registro)

def mostrar_registros_persona(panel_abajo):
    # Limpiar el panel
    for widget in panel_abajo.winfo_children():
        widget.destroy()

    # Obtener las columnas de la tabla persona
    columnas_query = f"""
    SELECT column_name 
    FROM information_schema.columns 
    WHERE table_name = 'persona'
    ORDER BY ordinal_position;
    """
    columnas = ejecutar_consulta(columnas_query, fetch=True)
    nombres_columnas = [columna[0] for columna in columnas]

    # Obtener los registros de la tabla
    datos_query = f"SELECT * FROM persona"
    registros = ejecutar_consulta(datos_query, fetch=True)

    # Crear el Treeview dinámicamente
    tree = ttk.Treeview(panel_abajo, columns=nombres_columnas, show="headings")
    tree.pack(fill=tk.BOTH, expand=True)

    # Configurar encabezados dinámicos
    for columna in nombres_columnas:
        tree.heading(columna, text=columna)
        tree.column(columna, width=100)

    # Insertar los registros obtenidos
    for registro in registros:
        tree.insert("", tk.END, values=registro)

def mostrar_registros_categoria_producto(panel_abajo):
    # Limpiar el panel
    for widget in panel_abajo.winfo_children():
        widget.destroy()

    # Obtener las columnas de la tabla categoria_producto
    columnas_query = f"""
    SELECT column_name 
    FROM information_schema.columns 
    WHERE table_name = 'categoria_producto'
    ORDER BY ordinal_position;
    """
    columnas = ejecutar_consulta(columnas_query, fetch=True)
    nombres_columnas = [columna[0] for columna in columnas]

    # Obtener los registros de la tabla
    datos_query = f"SELECT * FROM categoria_producto"
    registros = ejecutar_consulta(datos_query, fetch=True)

    # Crear el Treeview dinámicamente
    tree = ttk.Treeview(panel_abajo, columns=nombres_columnas, show="headings")
    tree.pack(fill=tk.BOTH, expand=True)

    # Configurar encabezados dinámicos
    for columna in nombres_columnas:
        tree.heading(columna, text=columna)
        tree.column(columna, width=100)

    # Insertar los registros obtenidos
    for registro in registros:
        tree.insert("", tk.END, values=registro)
