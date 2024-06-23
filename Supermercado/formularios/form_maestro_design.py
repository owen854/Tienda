import tkinter as tk
from tkinter import font, ttk, messagebox
from config import COLOR_BARRA_SUPERIOR, COLOR_MENU_LATERAL, COLOR_CUERPO_PRINCIPAL, COLOR_MENU_CURSOR_ENCIMA
import util.util_ventana as util_ventana
import util.util_imagenes as util_img

class FormularioMaestroDesign(tk.Tk):

    def __init__(self):
        super().__init__()
        self.logo = util_img.leer_imagen("./imagenes/logo.png", (900, 650))
        self.perfil = util_img.leer_imagen("./imagenes/mercado.png", (100, 100))
        self.config_window()
        self.paneles()
        self.controles_barra_superior()
        self.controles_menu_lateral()
        self.controles_cuerpo()
        self.nombre_cliente = ""
        self.apellido_cliente = ""
        self.ordenes = []  # Lista para almacenar las órdenes del cliente
        self.cesta = []  # Lista para almacenar los productos seleccionados en la cesta
    
    def config_window(self):
        # Configuración inicial de la ventana
        self.title('Mercado')
        self.iconbitmap("./imagenes/piña.ico")
        w, h = 1024, 600
        util_ventana.centrar_ventana(self, w, h)

    def paneles(self):
        # Crear paneles: barra superior, menú lateral y cuerpo principal
        self.barra_superior = tk.Frame(self, bg=COLOR_BARRA_SUPERIOR, height=50)
        self.barra_superior.pack(side=tk.TOP, fill='both')

        self.menu_lateral = tk.Frame(self, bg=COLOR_MENU_LATERAL, width=150)
        self.menu_lateral.pack(side=tk.LEFT, fill='both', expand=False)
        
        self.cuerpo_principal = tk.Frame(self, bg=COLOR_CUERPO_PRINCIPAL)
        self.cuerpo_principal.pack(side=tk.RIGHT, fill='both', expand=True)
    
    def controles_barra_superior(self):
        # Configuración de la barra superior
        font_awesome = font.Font(family='FontAwesome', size=12)

        # Etiqueta de título
        self.labelTitulo = tk.Label(self.barra_superior, text="Mercado")
        self.labelTitulo.config(fg="#fff", font=("Roboto", 15), bg=COLOR_BARRA_SUPERIOR, pady=10, width=16)
        self.labelTitulo.pack(side=tk.LEFT)

        # Botón del menú lateral
        self.buttonMenuLateral = tk.Button(self.barra_superior, text="\uf0c9", font=font_awesome, command=self.toggle_panel, bd=0, bg=COLOR_BARRA_SUPERIOR, fg="white")
        self.buttonMenuLateral.pack(side=tk.LEFT)

        # Etiqueta de información
        self.labelUsuario = tk.Label(self.barra_superior, text="Owen Fuentes")
        self.labelUsuario.config(fg="#fff", font=("Roboto", 10), bg=COLOR_BARRA_SUPERIOR, padx=10, width=20)
        self.labelUsuario.pack(side=tk.RIGHT)
    
    def controles_menu_lateral(self):
        # Configuración del menú lateral
        ancho_menu = 20
        alto_menu = 2
        font_awesome = font.Font(family='FontAwesome', size=15)
        
        # Etiqueta de perfil
        self.labelPerfil = tk.Label(self.menu_lateral, image=self.perfil, bg=COLOR_MENU_LATERAL)
        self.labelPerfil.pack(side=tk.TOP, pady=10)

        # Botones del menú lateral
        self.buttoncliente = tk.Button(self.menu_lateral, command=self.pedir_nombre_apellido_cliente)
        self.buttonProductos = tk.Button(self.menu_lateral, command=self.mostrar_productos)
        self.buttonOrdenes = tk.Button(self.menu_lateral, command=self.verificar_cliente)

        buttons_info = [
            ("Cliente","\uf179", self.buttoncliente),
            ("Productos","\uf179", self.buttonProductos),
            ("Ordenes","\uf179", self.buttonOrdenes),
        ]

        for text, icon, button in buttons_info:
            self.configurar_boton_menu(button, text, icon, font_awesome, ancho_menu, alto_menu)                    
    
    def controles_cuerpo(self):
        # Imagen en el cuerpo principal
        self.label_logo = tk.Label(self.cuerpo_principal, image=self.logo, bg=COLOR_CUERPO_PRINCIPAL)
        self.label_logo.place(x=0, y=0, relwidth=1, relheight=1)

    def configurar_boton_menu(self, button, text, icon, font_awesome, ancho_menu, alto_menu):
        button.config(text=f"  {icon}    {text}", anchor="w", font=font_awesome, bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=ancho_menu, height=alto_menu)
        button.pack(side=tk.TOP)
        self.bind_hover_events(button)

    def bind_hover_events(self, button):
        # Asociar eventos Enter y Leave con la función dinámica
        button.bind("<Enter>", lambda event: self.on_enter(event, button))
        button.bind("<Leave>", lambda event: self.on_leave(event, button))

    def on_enter(self, event, button):
        # Cambiar estilo al pasar el ratón por encima
        button.config(bg=COLOR_MENU_CURSOR_ENCIMA, fg='white')

    def on_leave(self, event, button):
        # Restaurar estilo al salir el ratón
        button.config(bg=COLOR_MENU_LATERAL, fg='white')

    def toggle_panel(self):
        # Alternar visibilidad del menú lateral
        if self.menu_lateral.winfo_ismapped():
            self.menu_lateral.pack_forget()
        else:
            self.menu_lateral.pack(side=tk.LEFT, fill='y')        

    def mostrar_productos(self):
        # Limpiar la imagen del logo si existe
        if hasattr(self, 'label_logo'):
            self.label_logo.destroy()

        # Limpiar el cuerpo principal antes de agregar la tabla
        for widget in self.cuerpo_principal.winfo_children():
            widget.destroy()

        # Crear una tabla para mostrar los productos
        columns = ('Nombre', 'Precio', 'Categoría')
        self.tree = ttk.Treeview(self.cuerpo_principal, columns=columns, show='headings', selectmode='extended')

        # Definir los encabezados
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor='center')

        # Agregar datos de productos (ejemplo)
        productos = [
            ("Manzana", 1.00, "Frutas"),
            ("Leche", 0.80, "Lácteos"),
            ("Pan", 1.20, "Panadería"),
            ("Tomate", 0.50, "Verduras"),
            ("Carne", 5.00, "Carnes"),
            ("Pescado", 4.50, "Pescados"),
            ("Arroz", 2.00, "Granos"),
            ("Cereal", 3.00, "Cereales"),
            ("Queso", 2.50, "Lácteos"),
            ("Yogur", 1.50, "Lácteos"),
            ("Zanahoria", 0.70, "Verduras"),
            ("Papas", 1.00, "Verduras")
        ]

        for producto in productos:
            self.tree.insert('', tk.END, values=producto)

        # Empacar el treeview en el cuerpo principal
        self.tree.pack(side=tk.TOP, fill='both', expand=True)

        # Agregar scrollbar vertical
        scrollbar_vertical = ttk.Scrollbar(self.cuerpo_principal, orient="vertical", command=self.tree.yview)
        scrollbar_vertical.pack(side='right', fill='y')
        self.tree.configure(yscroll=scrollbar_vertical.set)

        # Agregar scrollbar horizontal
        scrollbar_horizontal = ttk.Scrollbar(self.cuerpo_principal, orient="horizontal", command=self.tree.xview)
        scrollbar_horizontal.pack(side='bottom', fill='x')
        self.tree.configure(xscroll=scrollbar_horizontal.set)

        # Botón para añadir productos seleccionados a la orden
        self.boton_ordenar = tk.Button(self.cuerpo_principal, text="Hacer Orden", command=self.confirmar_orden, bg=COLOR_BARRA_SUPERIOR, fg="white")
        self.boton_ordenar.pack(side=tk.BOTTOM, pady=10)

        # Botón para regresar a la vista inicial
        self.boton_volver = tk.Button(self.cuerpo_principal, text="Salir", command=self.volver_vista_inicial, bg=COLOR_BARRA_SUPERIOR, fg="white")
        self.boton_volver.pack(side=tk.BOTTOM, pady=10)

    def volver_vista_inicial(self):
        # Limpiar los widgets actuales
        for widget in self.cuerpo_principal.winfo_children():
            widget.destroy()

        # Restaurar la imagen del logo
        self.label_logo = tk.Label(self.cuerpo_principal, image=self.logo, bg=COLOR_CUERPO_PRINCIPAL)
        self.label_logo.place(x=0, y=0, relwidth=1, relheight=1)

    def pedir_nombre_apellido_cliente(self):
        # Limpiar los widgets actuales
        for widget in self.cuerpo_principal.winfo_children():
            widget.destroy()

        # Crear etiquetas y campos de entrada para el nombre y apellido
        label_nombre = tk.Label(self.cuerpo_principal, text="Nombre:", bg=COLOR_CUERPO_PRINCIPAL)
        label_nombre.pack(pady=5)
        self.entry_nombre = tk.Entry(self.cuerpo_principal)
        self.entry_nombre.pack(pady=5)

        label_apellido = tk.Label(self.cuerpo_principal, text="Apellido:", bg=COLOR_CUERPO_PRINCIPAL)
        label_apellido.pack(pady=5)
        self.entry_apellido = tk.Entry(self.cuerpo_principal)
        self.entry_apellido.pack(pady=5)

        # Botón para guardar la información del cliente
        boton_guardar = tk.Button(self.cuerpo_principal, text="Guardar", command=self.guardar_cliente, bg=COLOR_BARRA_SUPERIOR, fg="white")
        boton_guardar.pack(pady=10)

    def guardar_cliente(self):
        self.nombre_cliente = self.entry_nombre.get()
        self.apellido_cliente = self.entry_apellido.get()

        # Mostrar mensaje de confirmación
        messagebox.showinfo("Cliente Guardado", f"Cliente: {self.nombre_cliente} {self.apellido_cliente} guardado correctamente.")
        self.volver_vista_inicial()

    def verificar_cliente(self):
        if not self.nombre_cliente or not self.apellido_cliente:
            messagebox.showerror("Error", "Debe ingresar el nombre y apellido del cliente antes de realizar una orden.")
        else:
            self.mostrar_ordenes()

    def mostrar_ordenes(self):
        # Limpiar los widgets actuales
        for widget in self.cuerpo_principal.winfo_children():
            widget.destroy()

        # Crear una tabla para mostrar las órdenes
        columns = ('Nombre del Cliente', 'Apellido del Cliente', 'Productos')
        self.tree_ordenes = ttk.Treeview(self.cuerpo_principal, columns=columns, show='headings', selectmode='extended')

        # Definir los encabezados
        for col in columns:
            self.tree_ordenes.heading(col, text=col)
            self.tree_ordenes.column(col, anchor='center')

        # Agregar datos de órdenes (ejemplo)
        for orden in self.ordenes:
            self.tree_ordenes.insert('', tk.END, values=orden)

        # Empacar el treeview en el cuerpo principal
        self.tree_ordenes.pack(side=tk.TOP, fill='both', expand=True)

        # Botón para regresar a la vista inicial
        self.boton_volver = tk.Button(self.cuerpo_principal, text="Volver", command=self.volver_vista_inicial, bg=COLOR_BARRA_SUPERIOR, fg="white")
        self.boton_volver.pack(side=tk.BOTTOM, pady=10)

    def confirmar_orden(self):
        # Obtener los productos seleccionados
        productos_seleccionados = [self.tree.item(item)['values'] for item in self.tree.selection()]

        if not productos_seleccionados:
            messagebox.showerror("Error", "Debe seleccionar al menos un producto para hacer una orden.")
        else:
            self.cesta.extend(productos_seleccionados)  # Agregar productos seleccionados a la cesta
            self.mostrar_confirmacion_orden()

    def mostrar_confirmacion_orden(self):
        # Crear una ventana emergente personalizada
        self.popup_confirmacion = tk.Toplevel(self)
        self.popup_confirmacion.title("Confirmación de Orden")
        self.popup_confirmacion.geometry("300x300")
        
        # Calcular el subtotal y el total
        subtotal = sum(float(producto[1]) for producto in self.cesta)
        total = subtotal * 1.16  # Asumiendo un 16% de impuestos

        # Etiqueta de mensaje
        mensaje = f"¿Desea terminar la compra o agregar más productos?\n\nProductos seleccionados:"
        label_mensaje = tk.Label(self.popup_confirmacion, text=mensaje, wraplength=250, justify="left")
        label_mensaje.pack(pady=10)

        # Mostrar productos seleccionados
        for producto in self.cesta:
            producto_label = tk.Label(self.popup_confirmacion, text=f"{producto[0]} - ${float(producto[1]):.2f}")
            producto_label.pack()

        # Mostrar subtotal y total
        label_subtotal = tk.Label(self.popup_confirmacion, text=f"\nSubtotal: ${subtotal:.2f}")
        label_subtotal.pack()
        label_total = tk.Label(self.popup_confirmacion, text=f"Total (con impuestos): ${total:.2f}")
        label_total.pack()

        # Botones personalizados
        boton_terminar = tk.Button(self.popup_confirmacion, text="Terminar Compra", command=self.terminar_compra, bg=COLOR_BARRA_SUPERIOR, fg="white")
        boton_terminar.pack(pady=10)

        boton_agregar_mas = tk.Button(self.popup_confirmacion, text="Agregar Más Productos", command=self.agregar_mas_productos, bg=COLOR_BARRA_SUPERIOR, fg="white")
        boton_agregar_mas.pack(pady=10)

    def terminar_compra(self):
        # Guardar la orden del cliente
        orden = (self.nombre_cliente, self.apellido_cliente, ", ".join(producto[0] for producto in self.cesta))
        self.ordenes.append(orden)

        # Vaciar la cesta
        self.cesta.clear()

        # Cerrar la ventana emergente
        self.popup_confirmacion.destroy()

        # Mostrar mensaje de confirmación
        messagebox.showinfo("Compra Finalizada", "La compra ha sido finalizada con éxito.")
        self.volver_vista_inicial()

    def agregar_mas_productos(self):
        # Cerrar la ventana emergente
        self.popup_confirmacion.destroy()

        # Volver a mostrar los productos para agregar más
        self.mostrar_productos()
