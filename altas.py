import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
import psycopg2
from tkinter import messagebox

# Función para conectar a PostgreSQL y ejecutar una consulta
def ejecutar_consulta(query, params):
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
        conexion.commit()
        cursor.close()
        conexion.close()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo conectar a la base de datos: {e}")

# Función para manejar la inserción de datos en la tabla usuarios
def insertar_usuario():
    global entry_usuario, entry_contrasena

    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()

    # Validaciones
    if len(usuario) == 0 or len(usuario) > 50:
        messagebox.showwarning("Advertencia", "El usuario no debe estar vacío ni exceder 50 caracteres.")
        return
    if len(contrasena) == 0 or len(contrasena) > 100:
        messagebox.showwarning("Advertencia", "La contraseña no debe estar vacía ni exceder 100 caracteres.")
        return

    # Insertar datos en la base de datos
    query = """
    INSERT INTO usuarios (usuario, contrasena)
    VALUES (%s, %s)
    """
    params = (usuario, contrasena)
    ejecutar_consulta(query, params)
    messagebox.showinfo("Éxito", "Usuario insertado correctamente.")

# Función para mostrar el formulario de usuarios
def mostrar_formulario_usuario():
    global entry_usuario, entry_contrasena

    for widget in panel_abajo.winfo_children():
        widget.destroy()

    fuente = Font(family="Code New Roman", size=11)

    # Crear entradas para usuarios
    label_usuario = tk.Label(panel_abajo, text="Usuario:", font=fuente, bg="lightgray")
    label_usuario.pack(pady=5)
    entry_usuario = tk.Entry(panel_abajo)
    entry_usuario.pack(pady=5)

    label_contrasena = tk.Label(panel_abajo, text="Contraseña:", font=fuente, bg="lightgray")
    label_contrasena.pack(pady=5)
    entry_contrasena = tk.Entry(panel_abajo, show="*")  # Ocultar contraseña con '*'
    entry_contrasena.pack(pady=5)

    # Botón para ingresar los datos
    boton_ingresar = tk.Button(panel_abajo, text="Ingresar", font=fuente, command=insertar_usuario)
    boton_ingresar.pack(pady=10)

# Función para manejar la inserción de datos en la tabla persona
def insertar_persona():
    global entry_id_persona, entry_nombre, entry_apellidos, entry_calle, entry_numero_exterior
    global entry_numero_interior, entry_estado, entry_municipio, entry_codigo_postal, entry_telefono, entry_email

    id_persona = entry_id_persona.get()
    nombre = entry_nombre.get()
    apellidos = entry_apellidos.get()
    calle = entry_calle.get()
    numero_exterior = entry_numero_exterior.get()
    numero_interior = entry_numero_interior.get()
    estado = entry_estado.get()
    municipio = entry_municipio.get()
    codigo_postal = entry_codigo_postal.get()
    telefono = entry_telefono.get()
    email = entry_email.get()

    # Validaciones
    if not id_persona.isdigit():
        messagebox.showwarning("Advertencia", "El ID de persona debe ser un número.")
        return
    if len(nombre) > 100:
        messagebox.showwarning("Advertencia", "El nombre no debe exceder 100 caracteres.")
        return
    if len(apellidos) > 120:
        messagebox.showwarning("Advertencia", "Los apellidos no deben exceder 120 caracteres.")
        return
    if len(calle) > 50:
        messagebox.showwarning("Advertencia", "La calle no debe exceder 50 caracteres.")
        return
    if len(numero_exterior) > 10:
        messagebox.showwarning("Advertencia", "El número exterior no debe exceder 10 caracteres.")
        return
    if len(numero_interior) > 10:
        messagebox.showwarning("Advertencia", "El número interior no debe exceder 10 caracteres.")
        return
    if len(estado) > 20:
        messagebox.showwarning("Advertencia", "El estado no debe exceder 20 caracteres.")
        return
    if len(municipio) > 20:
        messagebox.showwarning("Advertencia", "El municipio no debe exceder 20 caracteres.")
        return
    if len(codigo_postal) != 5:
        messagebox.showwarning("Advertencia", "El código postal debe tener 5 caracteres.")
        return
    if len(telefono) > 20:
        messagebox.showwarning("Advertencia", "El teléfono no debe exceder 20 caracteres.")
        return
    if len(email) > 40 or '@' not in email:
        messagebox.showwarning("Advertencia", "El email no es válido.")
        return

    # Insertar datos en la base de datos
    query = """
    INSERT INTO persona (id_persona, nombre, apellidos, direccion, telefono, email) 
    VALUES (%s, %s, %s, ROW(%s, %s, %s, %s, %s, %s), %s, %s)
    """
    params = (int(id_persona), nombre, apellidos, calle, numero_exterior, numero_interior, estado, municipio, codigo_postal, telefono, email)
    ejecutar_consulta(query, params)
    messagebox.showinfo("Éxito", "Datos insertados correctamente.")

# Función para mostrar los paneles de "Altas"
def ventana_altas(frame_principal):
    global entry_id_persona, entry_nombre, entry_apellidos, entry_calle, entry_numero_exterior
    global entry_numero_interior, entry_estado, entry_municipio, entry_codigo_postal, entry_telefono, entry_email

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

    tablas = ["categoria_producto", "persona", "cliente", "empleado", "facturacion", "inventario", "metodo_pago",
              "producto", "proveedor", "tienda", "usuarios", "venta"]
    tabla_seleccionada = tk.StringVar()
    combo_tablas = ttk.Combobox(panel_arriba, textvariable=tabla_seleccionada, values=tablas)
    combo_tablas.pack(pady=5)

    def continuar():
        if combo_tablas.get() == "persona":
            mostrar_formulario_persona()

    # Botón para continuar con la tabla seleccionada
    boton_continuar = tk.Button(panel_arriba, text="Continuar", font=fuente, command=continuar)
    boton_continuar.pack(pady=10)

    # Función para mostrar el formulario de persona
    def mostrar_formulario_persona():
        global entry_id_persona, entry_nombre, entry_apellidos, entry_calle, entry_numero_exterior
        global entry_numero_interior, entry_estado, entry_municipio, entry_codigo_postal, entry_telefono, entry_email

        for widget in panel_abajo.winfo_children():
            widget.destroy()

        # Crear entradas para persona
        campos = ["ID de Persona", "Nombre", "Apellidos", "Calle", "Número Exterior", "Número Interior",
                  "Estado", "Municipio", "Código Postal", "Teléfono", "Email"]
        entradas = {}

        for campo in campos:
            label = tk.Label(panel_abajo, text=f"{campo}:", font=fuente, bg="lightgray")
            label.pack(pady=5)
            entrada = tk.Entry(panel_abajo)
            entrada.pack(pady=5)
            entradas[campo] = entrada

        entry_id_persona = entradas["ID de Persona"]
        entry_nombre = entradas["Nombre"]
        entry_apellidos = entradas["Apellidos"]
        entry_calle = entradas["Calle"]
        entry_numero_exterior = entradas["Número Exterior"]
        entry_numero_interior = entradas["Número Interior"]
        entry_estado = entradas["Estado"]
        entry_municipio = entradas["Municipio"]
        entry_codigo_postal = entradas["Código Postal"]
        entry_telefono = entradas["Teléfono"]
        entry_email = entradas["Email"]

        # Botón para ingresar los datos
        boton_ingresar = tk.Button(panel_abajo, text="Ingresar", font=fuente, command=insertar_persona)
        boton_ingresar.pack(pady=10)

# Función para manejar la inserción de datos en la tabla categoria_producto
def insertar_categoria_producto():
    global entry_id_categoria, entry_nombre_categoria

    id_categoria = entry_id_categoria.get()
    nombre_categoria = entry_nombre_categoria.get()

    # Validaciones
    if not id_categoria.isdigit():
        messagebox.showwarning("Advertencia", "El ID de categoría debe ser un número.")
        return
    if len(nombre_categoria) > 20:
        messagebox.showwarning("Advertencia", "El nombre de la categoría no debe exceder 20 caracteres.")
        return
    if len(nombre_categoria) <= 2:
        messagebox.showwarning("Advertencia", "El nombre de la categoría debe tener más de 2 caracteres.")
        return

    # Insertar datos en la base de datos
    query = """
    INSERT INTO categoria_producto (id_categoria, nombre_categoria) 
    VALUES (%s, %s)
    """
    params = (int(id_categoria), nombre_categoria)
    ejecutar_consulta(query, params)
    messagebox.showinfo("Éxito", "Datos de la categoría insertados correctamente.")

# Función para mostrar el formulario de categoria_producto
def mostrar_formulario_categoria_producto():
    global entry_id_categoria, entry_nombre_categoria

    for widget in panel_abajo.winfo_children():
        widget.destroy()

    fuente = Font(family="Code New Roman", size=11)

    # Crear entradas para categoria_producto
    label_id_categoria = tk.Label(panel_abajo, text="ID de Categoría:", font=fuente, bg="lightgray")
    label_id_categoria.pack(pady=5)
    entry_id_categoria = tk.Entry(panel_abajo)
    entry_id_categoria.pack(pady=5)

    label_nombre_categoria = tk.Label(panel_abajo, text="Nombre de Categoría:", font=fuente, bg="lightgray")
    label_nombre_categoria.pack(pady=5)
    entry_nombre_categoria = tk.Entry(panel_abajo)
    entry_nombre_categoria.pack(pady=5)

    # Botón para ingresar los datos
    boton_ingresar = tk.Button(panel_abajo, text="Ingresar", font=fuente, command=insertar_categoria_producto)
    boton_ingresar.pack(pady=10)

# Función para mostrar el formulario de persona
def mostrar_formulario_persona():
    global entry_id_persona, entry_nombre, entry_apellidos, entry_calle, entry_numero_exterior
    global entry_numero_interior, entry_estado, entry_municipio, entry_codigo_postal, entry_telefono, entry_email

    for widget in panel_abajo.winfo_children():
        widget.destroy()

    fuente = Font(family="Code New Roman", size=11)

    # Crear entradas para persona
    campos = ["ID de Persona", "Nombre", "Apellidos", "Calle", "Número Exterior", "Número Interior",
              "Estado", "Municipio", "Código Postal", "Teléfono", "Email"]
    entradas = {}

    for campo in campos:
        label = tk.Label(panel_abajo, text=f"{campo}:", font=fuente, bg="lightgray")
        label.pack(pady=5)
        entrada = tk.Entry(panel_abajo)
        entrada.pack(pady=5)
        entradas[campo] = entrada

    entry_id_persona = entradas["ID de Persona"]
    entry_nombre = entradas["Nombre"]
    entry_apellidos = entradas["Apellidos"]
    entry_calle = entradas["Calle"]
    entry_numero_exterior = entradas["Número Exterior"]
    entry_numero_interior = entradas["Número Interior"]
    entry_estado = entradas["Estado"]
    entry_municipio = entradas["Municipio"]
    entry_codigo_postal = entradas["Código Postal"]
    entry_telefono = entradas["Teléfono"]
    entry_email = entradas["Email"]

    # Botón para ingresar los datos
    boton_ingresar = tk.Button(panel_abajo, text="Ingresar", font=fuente, command=insertar_persona)
    boton_ingresar.pack(pady=10)

# Función para manejar la inserción de datos en la tabla empleado
def insertar_empleado():
    global entry_id_persona, entry_cargo, entry_departamento, entry_salario, entry_id_tienda

    id_persona = entry_id_persona.get()
    cargo = entry_cargo.get()
    departamento = entry_departamento.get()
    salario = entry_salario.get()
    id_tienda = entry_id_tienda.get()

    # Validaciones
    if not id_persona.isdigit():
        messagebox.showwarning("Advertencia", "El ID de persona debe ser un número.")
        return
    if len(cargo) > 20:
        messagebox.showwarning("Advertencia", "El cargo no debe exceder 20 caracteres.")
        return
    if len(departamento) > 20:
        messagebox.showwarning("Advertencia", "El departamento no debe exceder 20 caracteres.")
        return
    try:
        salario = float(salario)
        if salario <= 0:
            raise ValueError
    except ValueError:
        messagebox.showwarning("Advertencia", "El salario debe ser un número mayor a 0.")
        return
    if not id_tienda.isdigit():
        messagebox.showwarning("Advertencia", "El ID de tienda debe ser un número.")
        return

    # Insertar datos en la base de datos
    query = """
    INSERT INTO empleado (id_persona, cargo, departamento, salario, id_tienda)
    VALUES (%s, %s, %s, %s, %s)
    """
    params = (int(id_persona), cargo, departamento, salario, int(id_tienda))
    ejecutar_consulta(query, params)
    messagebox.showinfo("Éxito", "Datos del empleado insertados correctamente.")

# Función para mostrar el formulario de empleado
def mostrar_formulario_empleado():
    global entry_id_persona, entry_cargo, entry_departamento, entry_salario, entry_id_tienda

    for widget in panel_abajo.winfo_children():
        widget.destroy()

    fuente = Font(family="Code New Roman", size=11)

    # Crear entradas para empleado
    campos = ["ID de Persona", "Cargo", "Departamento", "Salario", "ID de Tienda"]
    entradas = {}

    for campo in campos:
        label = tk.Label(panel_abajo, text=f"{campo}:", font=fuente, bg="lightgray")
        label.pack(pady=5)
        entrada = tk.Entry(panel_abajo)
        entrada.pack(pady=5)
        entradas[campo] = entrada

    entry_id_persona = entradas["ID de Persona"]
    entry_cargo = entradas["Cargo"]
    entry_departamento = entradas["Departamento"]
    entry_salario = entradas["Salario"]
    entry_id_tienda = entradas["ID de Tienda"]

    # Botón para ingresar los datos
    boton_ingresar = tk.Button(panel_abajo, text="Ingresar", font=fuente, command=insertar_empleado)
    boton_ingresar.pack(pady=10)

# Función para manejar la inserción de datos en la tabla cliente
def insertar_cliente():
    global entry_id_persona, entry_numero_cuenta, entry_tipo_cliente

    id_persona = entry_id_persona.get()
    numero_cuenta = entry_numero_cuenta.get()
    tipo_cliente = entry_tipo_cliente.get()

    # Validaciones
    if not id_persona.isdigit():
        messagebox.showwarning("Advertencia", "El ID de persona debe ser un número.")
        return
    if not numero_cuenta.isdigit() or len(numero_cuenta) < 10 or len(numero_cuenta) > 18:
        messagebox.showwarning("Advertencia", "El número de cuenta debe ser un número entre 10 y 18 dígitos.")
        return
    if tipo_cliente not in ['M', 'F']:
        messagebox.showwarning("Advertencia", "El tipo de cliente debe ser 'M' o 'F'.")
        return

    # Insertar datos en la base de datos
    query = """
    INSERT INTO cliente (id_persona, numero_cuenta, tipo_cliente)
    VALUES (%s, %s, %s)
    """
    params = (int(id_persona), int(numero_cuenta), tipo_cliente)
    ejecutar_consulta(query, params)
    messagebox.showinfo("Éxito", "Datos del cliente insertados correctamente.")

# Función para mostrar el formulario de cliente
def mostrar_formulario_cliente():
    global entry_id_persona, entry_numero_cuenta, entry_tipo_cliente

    for widget in panel_abajo.winfo_children():
        widget.destroy()

    fuente = Font(family="Code New Roman", size=11)
    
    # Crear entradas para cliente
    campos = ["ID de Persona", "Número de Cuenta", "Tipo de Cliente (M/F)"]
    entradas = {}

    for campo in campos:
        label = tk.Label(panel_abajo, text=f"{campo}:", font=fuente, bg="lightgray")
        label.pack(pady=5)
        entrada = tk.Entry(panel_abajo)
        entrada.pack(pady=5)
        entradas[campo] = entrada

    entry_id_persona = entradas["ID de Persona"]
    entry_numero_cuenta = entradas["Número de Cuenta"]
    entry_tipo_cliente = entradas["Tipo de Cliente (M/F)"]

    # Botón para ingresar los datos
    boton_ingresar = tk.Button(panel_abajo, text="Ingresar", font=fuente, command=insertar_cliente)
    boton_ingresar.pack(pady=10)

# Función para manejar la inserción de datos en la tabla proveedor
def insertar_proveedor():
    global entry_id_proveedor, entry_nombre_proveedor, entry_telefono_proveedor, entry_email_proveedor
    global entry_calle_proveedor, entry_numero_exterior_proveedor, entry_numero_interior_proveedor
    global entry_estado_proveedor, entry_municipio_proveedor, entry_codigo_postal_proveedor, entry_fecha_entrega

    id_proveedor = entry_id_proveedor.get()
    nombre = entry_nombre_proveedor.get()
    telefono = entry_telefono_proveedor.get()
    email = entry_email_proveedor.get()
    calle = entry_calle_proveedor.get()
    numero_exterior = entry_numero_exterior_proveedor.get()
    numero_interior = entry_numero_interior_proveedor.get()
    estado = entry_estado_proveedor.get()
    municipio = entry_municipio_proveedor.get()
    codigo_postal = entry_codigo_postal_proveedor.get()
    fecha_entrega = entry_fecha_entrega.get()

    # Validaciones
    if not id_proveedor.isdigit():
        messagebox.showwarning("Advertencia", "El ID de proveedor debe ser un número.")
        return
    if len(nombre) > 100:
        messagebox.showwarning("Advertencia", "El nombre del proveedor no debe exceder 100 caracteres.")
        return
    if len(telefono) > 20:
        messagebox.showwarning("Advertencia", "El teléfono no debe exceder 20 caracteres.")
        return
    if len(email) > 40 or '@' not in email:
        messagebox.showwarning("Advertencia", "El email no es válido.")
        return
    if len(calle) > 50:
        messagebox.showwarning("Advertencia", "La calle no debe exceder 50 caracteres.")
        return
    if len(numero_exterior) > 10:
        messagebox.showwarning("Advertencia", "El número exterior no debe exceder 10 caracteres.")
        return
    if len(numero_interior) > 10:
        messagebox.showwarning("Advertencia", "El número interior no debe exceder 10 caracteres.")
        return
    if len(estado) > 20:
        messagebox.showwarning("Advertencia", "El estado no debe exceder 20 caracteres.")
        return
    if len(municipio) > 20:
        messagebox.showwarning("Advertencia", "El municipio no debe exceder 20 caracteres.")
        return
    if len(codigo_postal) != 5 or not codigo_postal.isdigit():
        messagebox.showwarning("Advertencia", "El código postal debe tener 5 dígitos.")
        return

    # Insertar datos en la base de datos
    query = """
    INSERT INTO proveedor (id_proveedor, nombre, telefono, email, direccion, fecha_entrega)
    VALUES (%s, %s, %s, %s, ROW(%s, %s, %s, %s, %s, %s), %s)
    """
    params = (
        int(id_proveedor), nombre, telefono, email, calle, numero_exterior, numero_interior, estado, municipio,
        codigo_postal, fecha_entrega
    )
    ejecutar_consulta(query, params)
    messagebox.showinfo("Éxito", "Datos del proveedor insertados correctamente.")

# Función para mostrar el formulario de proveedor
def mostrar_formulario_proveedor():
    global entry_id_proveedor, entry_nombre_proveedor, entry_telefono_proveedor, entry_email_proveedor
    global entry_calle_proveedor, entry_numero_exterior_proveedor, entry_numero_interior_proveedor
    global entry_estado_proveedor, entry_municipio_proveedor, entry_codigo_postal_proveedor, entry_fecha_entrega

    for widget in panel_abajo.winfo_children():
        widget.destroy()

    fuente = Font(family="Code New Roman", size=11)

    # Crear entradas para proveedor
    campos = [
        "ID de Proveedor", "Nombre del Proveedor", "Teléfono", "Email", "Calle", "Número Exterior",
        "Número Interior", "Estado", "Municipio", "Código Postal", "Fecha de Entrega (YYYY-MM-DD)"
    ]
    entradas = {}

    for campo in campos:
        label = tk.Label(panel_abajo, text=f"{campo}:", font=fuente, bg="lightgray")
        label.pack(pady=5)
        entrada = tk.Entry(panel_abajo)
        entrada.pack(pady=5)
        entradas[campo] = entrada

    entry_id_proveedor = entradas["ID de Proveedor"]
    entry_nombre_proveedor = entradas["Nombre del Proveedor"]
    entry_telefono_proveedor = entradas["Teléfono"]
    entry_email_proveedor = entradas["Email"]
    entry_calle_proveedor = entradas["Calle"]
    entry_numero_exterior_proveedor = entradas["Número Exterior"]
    entry_numero_interior_proveedor = entradas["Número Interior"]
    entry_estado_proveedor = entradas["Estado"]
    entry_municipio_proveedor = entradas["Municipio"]
    entry_codigo_postal_proveedor = entradas["Código Postal"]
    entry_fecha_entrega = entradas["Fecha de Entrega (YYYY-MM-DD)"]

    # Botón para ingresar los datos
    boton_ingresar = tk.Button(panel_abajo, text="Ingresar", font=fuente, command=insertar_proveedor)
    boton_ingresar.pack(pady=10)

# Función para mostrar los paneles de "Altas"
def ventana_altas(frame_principal):
    global combo_tablas, panel_abajo  # Hacemos combo_tablas y panel_abajo globales

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
    label_arriba = tk.Label(panel_arriba, text="Seleccione una tabla para ingresar datos", bg="lightgray")
    label_arriba.pack(expand=True)

    # Menú de opciones para seleccionar la tabla
    label_tabla = tk.Label(panel_arriba, text="Tabla:", font=fuente, bg="lightgray")
    label_tabla.pack(pady=5)

    tablas = ["categoria_producto", "persona", "cliente", "empleado", "facturacion", "inventario", "metodo_pago",
              "producto", "proveedor", "tienda", "usuarios", "venta"]
    tabla_seleccionada = tk.StringVar()
    combo_tablas = ttk.Combobox(panel_arriba, textvariable=tabla_seleccionada, values=tablas, state="readonly")
    combo_tablas.pack(pady=5)
    combo_tablas.current(0)  # Seleccionar por defecto la primera opción

    # Botón para continuar con la tabla seleccionada
    boton_continuar = tk.Button(panel_arriba, text="Continuar", font=fuente, command=continuar)
    boton_continuar.pack(pady=10)

# Función para manejar la inserción de datos en la tabla venta
def insertar_venta():
    global entry_id_venta, entry_id_tienda, entry_fecha_venta, entry_id_cliente, entry_total_venta, entry_cantidad_productos, entry_sku_producto

    id_venta = entry_id_venta.get()
    id_tienda = entry_id_tienda.get()
    fecha_venta = entry_fecha_venta.get()
    id_cliente = entry_id_cliente.get()
    total_venta = entry_total_venta.get()
    cantidad_productos = entry_cantidad_productos.get()
    sku_producto = entry_sku_producto.get()

    # Validaciones
    if not id_venta.isdigit():
        messagebox.showwarning("Advertencia", "El ID de venta debe ser un número.")
        return
    if not id_tienda.isdigit():
        messagebox.showwarning("Advertencia", "El ID de tienda debe ser un número.")
        return
    if not id_cliente.isdigit():
        messagebox.showwarning("Advertencia", "El ID de cliente debe ser un número.")
        return
    if not sku_producto.isdigit():
        messagebox.showwarning("Advertencia", "El SKU del producto debe ser un número.")
        return

    try:
        float_total_venta = float(total_venta)
        if float_total_venta <= 0:
            messagebox.showwarning("Advertencia", "El total de venta debe ser mayor a 0.")
            return
    except ValueError:
        messagebox.showwarning("Advertencia", "El total de venta debe ser un número válido.")
        return

    try:
        int_cantidad_productos = int(cantidad_productos)
        if int_cantidad_productos <= 0:
            messagebox.showwarning("Advertencia", "La cantidad de productos debe ser mayor a 0.")
            return
    except ValueError:
        messagebox.showwarning("Advertencia", "La cantidad de productos debe ser un número entero.")
        return

    # Validar formato de fecha
    try:
        from datetime import datetime
        datetime.strptime(fecha_venta, '%Y-%m-%d')
    except ValueError:
        messagebox.showwarning("Advertencia", "El formato de fecha debe ser AAAA-MM-DD.")
        return

    # Insertar datos en la base de datos
    query = """
    INSERT INTO venta (id_venta, id_tienda, fecha_venta, id_cliente, total_venta, cantidad_productos, sku_producto) 
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    params = (int(id_venta), int(id_tienda), fecha_venta, int(id_cliente),
              float_total_venta, int_cantidad_productos, int(sku_producto))
    ejecutar_consulta(query, params)
    messagebox.showinfo("Éxito", "Datos de la venta insertados correctamente.")

# Función para mostrar el formulario de venta
def mostrar_formulario_venta():
    global entry_id_venta, entry_id_tienda, entry_fecha_venta, entry_id_cliente, entry_total_venta, entry_cantidad_productos, entry_sku_producto

    for widget in panel_abajo.winfo_children():
        widget.destroy()

    fuente = Font(family="Code New Roman", size=11)

    # Crear entradas para venta
    campos = [
        "ID de Venta", "ID de Tienda", "Fecha de Venta (AAAA-MM-DD)",
        "ID de Cliente", "Total de Venta", "Cantidad de Productos", "SKU de Producto"
    ]
    entradas = {}

    for campo in campos:
        label = tk.Label(panel_abajo, text=f"{campo}:", font=fuente, bg="lightgray")
        label.pack(pady=5)
        entrada = tk.Entry(panel_abajo)
        entrada.pack(pady=5)
        entradas[campo] = entrada

    entry_id_venta = entradas["ID de Venta"]
    entry_id_tienda = entradas["ID de Tienda"]
    entry_fecha_venta = entradas["Fecha de Venta (AAAA-MM-DD)"]
    entry_id_cliente = entradas["ID de Cliente"]
    entry_total_venta = entradas["Total de Venta"]
    entry_cantidad_productos = entradas["Cantidad de Productos"]
    entry_sku_producto = entradas["SKU de Producto"]

    # Botón para ingresar los datos
    boton_ingresar = tk.Button(panel_abajo, text="Ingresar", font=fuente, command=insertar_venta)
    boton_ingresar.pack(pady=10)

## Función para manejar la inserción de datos en la tabla tienda
def insertar_tienda():
    global entry_id_tienda, entry_calle, entry_numero_exterior, entry_numero_interior, entry_estado, entry_municipio
    global entry_codigo_postal

    id_tienda = entry_id_tienda.get()
    calle = entry_calle.get()
    numero_exterior = entry_numero_exterior.get()
    numero_interior = entry_numero_interior.get()
    estado = entry_estado.get()
    municipio = entry_municipio.get()
    codigo_postal = entry_codigo_postal.get()

    # Validaciones
    if not id_tienda.isdigit():
        messagebox.showwarning("Advertencia", "El ID de tienda debe ser un número.")
        return

    # Validaciones de longitud y formato para ubicación
    if len(calle) > 50:
        messagebox.showwarning("Advertencia", "La calle no debe exceder 50 caracteres.")
        return
    if len(numero_exterior) > 10:
        messagebox.showwarning("Advertencia", "El número exterior no debe exceder 10 caracteres.")
        return
    if len(numero_interior) > 10:
        messagebox.showwarning("Advertencia", "El número interior no debe exceder 10 caracteres.")
        return
    if len(estado) < 3 or len(estado) > 20:
        messagebox.showwarning("Advertencia", "El estado debe tener entre 3 y 20 caracteres.")
        return
    if len(municipio) < 3 or len(municipio) > 20:
        messagebox.showwarning("Advertencia", "El municipio debe tener entre 3 y 20 caracteres.")
        return
    if len(codigo_postal) != 5:
        messagebox.showwarning("Advertencia", "El código postal debe tener 5 caracteres.")
        return

    # Insertar datos en la base de datos
    query = """
    INSERT INTO tienda (id_tienda, ubicacion) 
    VALUES (%s, ROW(%s, %s, %s, %s, %s, %s))
    """
    params = (
        int(id_tienda),
        calle,
        numero_exterior,
        numero_interior,
        estado,
        municipio,
        codigo_postal
    )
    ejecutar_consulta(query, params)
    messagebox.showinfo("Éxito", "Datos de la tienda insertados correctamente.")

# Función para mostrar el formulario de tienda
def mostrar_formulario_tienda():
    global entry_id_tienda, entry_calle, entry_numero_exterior, entry_numero_interior
    global entry_estado, entry_municipio, entry_codigo_postal

    for widget in panel_abajo.winfo_children():
        widget.destroy()

    fuente = Font(family="Code New Roman", size=11)

    # Crear entradas para tienda
    campos = [
        "ID de Tienda", "Calle", "Número Exterior", "Número Interior",
        "Estado", "Municipio", "Código Postal"
    ]
    entradas = {}

    for campo in campos:
        label = tk.Label(panel_abajo, text=f"{campo}:", font=fuente, bg="lightgray")
        label.pack(pady=5)
        entrada = tk.Entry(panel_abajo)
        entrada.pack(pady=5)
        entradas[campo] = entrada

    entry_id_tienda = entradas["ID de Tienda"]
    entry_calle = entradas["Calle"]
    entry_numero_exterior = entradas["Número Exterior"]
    entry_numero_interior = entradas["Número Interior"]
    entry_estado = entradas["Estado"]
    entry_municipio = entradas["Municipio"]
    entry_codigo_postal = entradas["Código Postal"]

    # Botón para ingresar los datos
    boton_ingresar = tk.Button(panel_abajo, text="Ingresar", font=fuente, command=insertar_tienda)
    boton_ingresar.pack(pady=10)

# Función para manejar la inserción de datos en la tabla metodo_pago
def insertar_metodo_pago():
    global entry_id_metodo_pago, entry_descripcion_metodo

    id_metodo_pago = entry_id_metodo_pago.get()
    descripcion_metodo = entry_descripcion_metodo.get()

    # Validaciones
    if not id_metodo_pago.isdigit():
        messagebox.showwarning("Advertencia", "El ID de método de pago debe ser un número.")
        return

    # Validaciones de longitud para descripción
    if len(descripcion_metodo) < 3:
        messagebox.showwarning("Advertencia", "La descripción del método de pago debe tener al menos 3 caracteres.")
        return
    if len(descripcion_metodo) > 120:
        messagebox.showwarning("Advertencia", "La descripción del método de pago no debe exceder 120 caracteres.")
        return

    # Insertar datos en la base de datos
    query = """
    INSERT INTO metodo_pago (id_metodo_pago, descripcion_metodo) 
    VALUES (%s, %s)
    """
    params = (int(id_metodo_pago), descripcion_metodo)
    ejecutar_consulta(query, params)
    messagebox.showinfo("Éxito", "Datos del método de pago insertados correctamente.")

# Función para mostrar el formulario de metodo_pago
def mostrar_formulario_metodo_pago():
    global entry_id_metodo_pago, entry_descripcion_metodo

    for widget in panel_abajo.winfo_children():
        widget.destroy()

    fuente = Font(family="Code New Roman", size=11)

    # Crear entradas para método de pago
    label_id_metodo_pago = tk.Label(panel_abajo, text="ID de Método de Pago:", font=fuente, bg="lightgray")
    label_id_metodo_pago.pack(pady=5)
    entry_id_metodo_pago = tk.Entry(panel_abajo)
    entry_id_metodo_pago.pack(pady=5)

    label_descripcion_metodo = tk.Label(panel_abajo, text="Descripción del Método de Pago:", font=fuente, bg="lightgray")
    label_descripcion_metodo.pack(pady=5)
    entry_descripcion_metodo = tk.Entry(panel_abajo)
    entry_descripcion_metodo.pack(pady=5)

    # Botón para ingresar los datos
    boton_ingresar = tk.Button(panel_abajo, text="Ingresar", font=fuente, command=insertar_metodo_pago)
    boton_ingresar.pack(pady=10)

# Función para manejar la inserción de datos en la tabla inventario
def insertar_inventario():
    global entry_sku_inventario, entry_nombre_producto, entry_precio, entry_stock, entry_fecha_actualizacion
    global entry_calle, entry_numero_exterior, entry_numero_interior, entry_estado, entry_municipio
    global entry_codigo_postal, entry_stock_minimo, entry_stock_maximo, entry_sku_producto

    # Recoger todos los valores de las entradas
    sku_inventario = entry_sku_inventario.get()
    nombre_producto = entry_nombre_producto.get()
    precio = entry_precio.get()
    stock = entry_stock.get()
    fecha_actualizacion = entry_fecha_actualizacion.get()
    calle = entry_calle.get()
    numero_exterior = entry_numero_exterior.get()
    numero_interior = entry_numero_interior.get()
    estado = entry_estado.get()
    municipio = entry_municipio.get()
    codigo_postal = entry_codigo_postal.get()
    stock_minimo = entry_stock_minimo.get()
    stock_maximo = entry_stock_maximo.get()
    sku_producto = entry_sku_producto.get()

    # Validaciones
    # Validar SKU Inventario
    if not sku_inventario.isdigit():
        messagebox.showwarning("Advertencia", "El SKU de inventario debe ser un número.")
        return

    # Validar nombre de producto
    if len(nombre_producto) > 100:
        messagebox.showwarning("Advertencia", "El nombre del producto no debe exceder 100 caracteres.")
        return

    # Validar precio
    try:
        float_precio = float(precio)
        if float_precio <= 0:
            messagebox.showwarning("Advertencia", "El precio debe ser mayor a 0.")
            return
    except ValueError:
        messagebox.showwarning("Advertencia", "El precio debe ser un número válido.")
        return

    # Validar stock
    try:
        int_stock = int(stock)
    except ValueError:
        messagebox.showwarning("Advertencia", "El stock debe ser un número entero.")
        return

    # Validar fecha de actualización
    try:
        from datetime import datetime
        datetime.strptime(fecha_actualizacion, '%Y-%m-%d')
    except ValueError:
        messagebox.showwarning("Advertencia", "El formato de fecha debe ser AAAA-MM-DD.")
        return

    # Validar dirección de almacén
    if len(calle) > 50:
        messagebox.showwarning("Advertencia", "La calle no debe exceder 50 caracteres.")
        return
    if len(numero_exterior) > 10:
        messagebox.showwarning("Advertencia", "El número exterior no debe exceder 10 caracteres.")
        return
    if len(numero_interior) > 10:
        messagebox.showwarning("Advertencia", "El número interior no debe exceder 10 caracteres.")
        return
    if len(estado) > 20:
        messagebox.showwarning("Advertencia", "El estado no debe exceder 20 caracteres.")
        return
    if len(municipio) > 20:
        messagebox.showwarning("Advertencia", "El municipio no debe exceder 20 caracteres.")
        return
    if len(codigo_postal) != 5:
        messagebox.showwarning("Advertencia", "El código postal debe tener 5 caracteres.")
        return

    # Validar stock mínimo y máximo
    try:
        int_stock_minimo = int(stock_minimo)
        if int_stock_minimo <= 0:
            messagebox.showwarning("Advertencia", "El stock mínimo debe ser mayor a 0.")
            return
    except ValueError:
        messagebox.showwarning("Advertencia", "El stock mínimo debe ser un número entero.")
        return

    try:
        int_stock_maximo = int(stock_maximo)
        if int_stock_maximo <= int_stock_minimo:
            messagebox.showwarning("Advertencia", "El stock máximo debe ser mayor al stock mínimo.")
            return
    except ValueError:
        messagebox.showwarning("Advertencia", "El stock máximo debe ser un número entero.")
        return

    # Validar SKU de producto
    if not sku_producto.isdigit():
        messagebox.showwarning("Advertencia", "El SKU de producto debe ser un número.")
        return

    # Insertar datos en la base de datos
    query = """
    INSERT INTO inventario (
        sku_inventario, nombre_producto, precio, stock, fecha_actualizacion, 
        direccion_almacen, stock_minimo, stock_maximo, sku_producto
    ) VALUES (
        %s, %s, %s, %s, %s, 
        ROW(%s, %s, %s, %s, %s, %s), 
        %s, %s, %s
    )
    """
    params = (
        int(sku_inventario), nombre_producto, float_precio, int_stock, fecha_actualizacion,
        calle, numero_exterior, numero_interior, estado, municipio, codigo_postal,
        int_stock_minimo, int_stock_maximo, int(sku_producto)
    )

    ejecutar_consulta(query, params)
    messagebox.showinfo("Éxito", "Datos de inventario insertados correctamente.")

# Función para mostrar el formulario de inventario
def mostrar_formulario_inventario():
    global entry_sku_inventario, entry_nombre_producto, entry_precio, entry_stock, entry_fecha_actualizacion
    global entry_calle, entry_numero_exterior, entry_numero_interior, entry_estado, entry_municipio
    global entry_codigo_postal, entry_stock_minimo, entry_stock_maximo, entry_sku_producto

    for widget in panel_abajo.winfo_children():
        widget.destroy()

    fuente = Font(family="Code New Roman", size=11)

    # Crear entradas para inventario
    campos = [
        "SKU de Inventario", "Nombre de Producto", "Precio", "Stock",
        "Fecha de Actualización (AAAA-MM-DD)", "Calle de Almacén", "Número Exterior",
        "Número Interior", "Estado", "Municipio", "Código Postal",
        "Stock Mínimo", "Stock Máximo", "SKU de Producto"
    ]
    entradas = {}

    for campo in campos:
        label = tk.Label(panel_abajo, text=f"{campo}:", font=fuente, bg="lightgray")
        label.pack(pady=5)
        entrada = tk.Entry(panel_abajo)
        entrada.pack(pady=5)
        entradas[campo] = entrada

    # Asignar variables globales
    entry_sku_inventario = entradas["SKU de Inventario"]
    entry_nombre_producto = entradas["Nombre de Producto"]
    entry_precio = entradas["Precio"]
    entry_stock = entradas["Stock"]
    entry_fecha_actualizacion = entradas["Fecha de Actualización (AAAA-MM-DD)"]
    entry_calle = entradas["Calle de Almacén"]
    entry_numero_exterior = entradas["Número Exterior"]
    entry_numero_interior = entradas["Número Interior"]
    entry_estado = entradas["Estado"]
    entry_municipio = entradas["Municipio"]
    entry_codigo_postal = entradas["Código Postal"]
    entry_stock_minimo = entradas["Stock Mínimo"]
    entry_stock_maximo = entradas["Stock Máximo"]
    entry_sku_producto = entradas["SKU de Producto"]

    # Botón para ingresar los datos
    boton_ingresar = tk.Button(panel_abajo, text="Ingresar", font=fuente, command=insertar_inventario)
    boton_ingresar.pack(pady=10)

# Función para manejar la inserción de datos en la tabla facturacion
def insertar_facturacion():
    global entry_id_factura, entry_id_venta, entry_id_tienda, entry_id_metodo_pago, entry_total_venta, entry_cantidad_productos, entry_iva

    id_factura = entry_id_factura.get()
    id_venta = entry_id_venta.get()
    id_tienda = entry_id_tienda.get()
    id_metodo_pago = entry_id_metodo_pago.get()
    total_venta = entry_total_venta.get()
    cantidad_productos = entry_cantidad_productos.get()
    iva = entry_iva.get()

    # Validaciones
    if not id_factura.isdigit():
        messagebox.showwarning("Advertencia", "El ID de factura debe ser un número.")
        return
    if not id_venta.isdigit():
        messagebox.showwarning("Advertencia", "El ID de venta debe ser un número.")
        return
    if not id_tienda.isdigit():
        messagebox.showwarning("Advertencia", "El ID de tienda debe ser un número.")
        return
    if not id_metodo_pago.isdigit():
        messagebox.showwarning("Advertencia", "El ID de método de pago debe ser un número.")
        return

    # Validar total de venta
    try:
        float_total_venta = float(total_venta)
        if float_total_venta <= 0:
            messagebox.showwarning("Advertencia", "El total de venta debe ser mayor a 0.")
            return
    except ValueError:
        messagebox.showwarning("Advertencia", "El total de venta debe ser un número válido.")
        return

    # Validar cantidad de productos
    try:
        int_cantidad_productos = int(cantidad_productos)
        if int_cantidad_productos <= 0:
            messagebox.showwarning("Advertencia", "La cantidad de productos debe ser mayor a 0.")
            return
    except ValueError:
        messagebox.showwarning("Advertencia", "La cantidad de productos debe ser un número entero.")
        return

    # Validar IVA
    try:
        float_iva = float(iva)
        if float_iva < 0 or float_iva > 100:
            messagebox.showwarning("Advertencia", "El IVA debe estar entre 0 y 100.")
            return
    except ValueError:
        messagebox.showwarning("Advertencia", "El IVA debe ser un número válido.")
        return

    # Insertar datos en la base de datos
    query = """
    INSERT INTO facturacion (id_factura, id_venta, id_tienda, id_metodo_pago, total_venta, cantidad_productos, iva) 
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    params = (
        int(id_factura), int(id_venta), int(id_tienda), int(id_metodo_pago),
        float_total_venta, int_cantidad_productos, float_iva
    )
    ejecutar_consulta(query, params)
    messagebox.showinfo("Éxito", "Datos de facturación insertados correctamente.")

# Función para mostrar el formulario de facturacion
def mostrar_formulario_facturacion():
    global entry_id_factura, entry_id_venta, entry_id_tienda, entry_id_metodo_pago, entry_total_venta, entry_cantidad_productos, entry_iva

    for widget in panel_abajo.winfo_children():
        widget.destroy()

    fuente = Font(family="Code New Roman", size=11)

    # Crear entradas para facturación
    campos = [
        "ID de Factura", "ID de Venta", "ID de Tienda", "ID de Método de Pago",
        "Total de Venta", "Cantidad de Productos", "IVA (%)"
    ]
    entradas = {}

    for campo in campos:
        label = tk.Label(panel_abajo, text=f"{campo}:", font=fuente, bg="lightgray")
        label.pack(pady=5)
        entrada = tk.Entry(panel_abajo)
        entrada.pack(pady=5)
        entradas[campo] = entrada

    # Asignar variables globales
    entry_id_factura = entradas["ID de Factura"]
    entry_id_venta = entradas["ID de Venta"]
    entry_id_tienda = entradas["ID de Tienda"]
    entry_id_metodo_pago = entradas["ID de Método de Pago"]
    entry_total_venta = entradas["Total de Venta"]
    entry_cantidad_productos = entradas["Cantidad de Productos"]
    entry_iva = entradas["IVA (%)"]

    # Botón para ingresar los datos
    boton_ingresar = tk.Button(panel_abajo, text="Ingresar", font=fuente, command=insertar_facturacion)
    boton_ingresar.pack(pady=10)

# Función para manejar la inserción de datos en la tabla producto
def insertar_producto():
    global entry_sku_producto, entry_nombre_producto, entry_descripcion, entry_precio, entry_stock, entry_id_categoria, entry_id_proveedor

    sku_producto = entry_sku_producto.get()
    nombre_producto = entry_nombre_producto.get()
    descripcion = entry_descripcion.get()
    precio = entry_precio.get()
    stock = entry_stock.get()
    id_categoria = entry_id_categoria.get()
    id_proveedor = entry_id_proveedor.get()

    # Validaciones
    if not sku_producto.isdigit():
        messagebox.showwarning("Advertencia", "El SKU del producto debe ser un número.")
        return
    if not nombre_producto.strip():
        messagebox.showwarning("Advertencia", "El nombre del producto no puede estar vacío.")
        return
    if len(nombre_producto) > 100:
        messagebox.showwarning("Advertencia", "El nombre del producto no debe exceder los 100 caracteres.")
        return
    if len(descripcion) > 120:
        messagebox.showwarning("Advertencia", "La descripción no debe exceder los 120 caracteres.")
        return

    # Validar precio
    try:
        float_precio = float(precio)
        if float_precio <= 0:
            messagebox.showwarning("Advertencia", "El precio debe ser mayor a 0.")
            return
    except ValueError:
        messagebox.showwarning("Advertencia", "El precio debe ser un número válido.")
        return

    # Validar stock
    try:
        int_stock = int(stock)
        if int_stock < 0:
            messagebox.showwarning("Advertencia", "El stock no puede ser negativo.")
            return
    except ValueError:
        messagebox.showwarning("Advertencia", "El stock debe ser un número entero.")
        return

    if not id_categoria.isdigit():
        messagebox.showwarning("Advertencia", "El ID de categoría debe ser un número.")
        return
    if not id_proveedor.isdigit():
        messagebox.showwarning("Advertencia", "El ID de proveedor debe ser un número.")
        return

    # Insertar datos en la base de datos
    query = """
    INSERT INTO producto (sku_producto, nombre_producto, descripcion, precio, stock, id_categoria, id_proveedor) 
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    params = (
        int(sku_producto), nombre_producto, descripcion, float_precio,
        int_stock, int(id_categoria), int(id_proveedor)
    )
    ejecutar_consulta(query, params)
    messagebox.showinfo("Éxito", "Producto insertado correctamente.")

# Función para mostrar el formulario de producto
def mostrar_formulario_producto():
    global entry_sku_producto, entry_nombre_producto, entry_descripcion, entry_precio, entry_stock, entry_id_categoria, entry_id_proveedor

    for widget in panel_abajo.winfo_children():
        widget.destroy()

    fuente = Font(family="Code New Roman", size=11)

    # Crear entradas para producto
    campos = [
        "SKU de Producto", "Nombre de Producto", "Descripción", "Precio", "Stock",
        "ID de Categoría", "ID de Proveedor"
    ]
    entradas = {}

    for campo in campos:
        label = tk.Label(panel_abajo, text=f"{campo}:", font=fuente, bg="lightgray")
        label.pack(pady=5)
        entrada = tk.Entry(panel_abajo)
        entrada.pack(pady=5)
        entradas[campo] = entrada

    # Asignar variables globales
    entry_sku_producto = entradas["SKU de Producto"]
    entry_nombre_producto = entradas["Nombre de Producto"]
    entry_descripcion = entradas["Descripción"]
    entry_precio = entradas["Precio"]
    entry_stock = entradas["Stock"]
    entry_id_categoria = entradas["ID de Categoría"]
    entry_id_proveedor = entradas["ID de Proveedor"]

    # Botón para ingresar los datos
    boton_ingresar = tk.Button(panel_abajo, text="Ingresar", font=fuente, command=insertar_producto)
    boton_ingresar.pack(pady=10)

# Función botón continuar() 
def continuar():    
    global combo_tablas
    seleccion = combo_tablas.get()
    if seleccion == "persona":
        mostrar_formulario_persona()
    elif seleccion == "categoria_producto":
        mostrar_formulario_categoria_producto()
    elif seleccion == "venta":
        mostrar_formulario_venta()
    elif seleccion == "tienda":
        mostrar_formulario_tienda()
    elif seleccion == "metodo_pago":
        mostrar_formulario_metodo_pago()
    elif seleccion == "inventario":
        mostrar_formulario_inventario()
    elif seleccion == "facturacion":
        mostrar_formulario_facturacion()
    elif seleccion == "empleado":
        mostrar_formulario_empleado()
    elif seleccion == "cliente":
        mostrar_formulario_cliente()
    elif seleccion == "proveedor":
        mostrar_formulario_proveedor()
    elif seleccion == "producto":
        mostrar_formulario_producto()
    elif seleccion == "usuarios":
        mostrar_formulario_usuario()