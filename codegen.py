import os, re
import tkinter as tk
from tkinter import ttk, font, filedialog
import shutil
from PIL import Image


################################## SCRIPT ###########################################

def generate(tipo_extension_seleccionado, codigo_catalogo, id_catalogo, catalog_name, extension_id, webpage, email, phone, brandText, header, logo, productName=None, partnumber=None, prodimg=None):

    # crear variables para diferentes tipos de nombre
    catalog_name_min = catalog_name.lower().replace(" ", "")
    catalog_name_may = catalog_name_min.capitalize()

    # Obtener la ubicación del script actual
    script_dir = os.path.dirname(os.path.abspath(__file__))

    #elegir carpeta estatica segun tipo de extension

    if tipo_extension_seleccionado == "shell":
        carpeta = os.path.join(script_dir, "staticExtensionShell")

    if tipo_extension_seleccionado == "hybrid":
        carpeta = os.path.join(script_dir, "staticExtensionHybrid")


    nueva_carpeta = r'C:\CetDev\version15.5\extensions\custom\%s' % catalog_name_min

    # Verificar si la carpeta nueva ya existe
    if os.path.exists(nueva_carpeta):
        shutil.rmtree(nueva_carpeta)

    # Copiar la carpeta existente a la nueva carpeta
    shutil.copytree(carpeta, nueva_carpeta)

    # crea una lista de los archivos y subdirectorios dentro de la carpeta
    contenido_carpeta = os.listdir(nueva_carpeta)


    # remover archivos no iterables de la lista
    if 'images' in contenido_carpeta:
        contenido_carpeta.remove('images')

    if 'secondTab' in contenido_carpeta:
        contenido_carpeta.remove('secondTab')

    # iterar sobre la lista creada anteriormente (firsttab)
    for archivo in contenido_carpeta:
        ruta_archivo = os.path.join(nueva_carpeta, archivo) #crear ruta completa (newExtension\archivo.cm)
        
        changeLine(ruta_archivo, "ExtensionName", catalog_name)
        changeLine(ruta_archivo, "ExtensionMayusName", catalog_name_may)
        changeLine(ruta_archivo, "extensionnamemin", catalog_name_min)
        changeLine(ruta_archivo, "catalogLetters", codigo_catalogo)


        ###### modificar extension.cm ... ######
        if ruta_archivo == r"C:\CetDev\version15.5\extensions\custom\%s\extension.cm" % catalog_name_min:
            changeLine(ruta_archivo, "//generateExtensionId", extension_id)

        ##### modificar Header.cm ######
        if ruta_archivo == r"C:\CetDev\version15.5\extensions\custom\%s\header.cm" % catalog_name_min:
            changeLine(ruta_archivo, "portafolioIdNumbers", id_catalogo)
            changeLine(ruta_archivo, "catalogLetters", codigo_catalogo)

        ###### modificar library.cm  ########
        if ruta_archivo == r"C:\CetDev\version15.5\extensions\custom\%s\library.cm" % catalog_name_min:
            changeLine(ruta_archivo, "catalogLetters", codigo_catalogo)
            
            cant_chars = len(brandText)
            if cant_chars > 37 :
                fragmentos = [brandText[i:i+37] for i in range(0, len(brandText), 37)]
                format_brandText = "\\n".join(fragmentos)
                 
            changeLine(ruta_archivo, "brandText", format_brandText)
            changeLine(ruta_archivo, "webpage", webpage)
            changeLine(ruta_archivo, "telefono", phone)
            changeLine(ruta_archivo, "correo", email)

        ###### modificar localize.rs  ########
        if ruta_archivo == r"C:\CetDev\version15.5\extensions\custom\%s\localize.rs" % catalog_name_min:
            changeLine(ruta_archivo, "webpage", webpage)
            changeLine(ruta_archivo, "telefono", phone)
            changeLine(ruta_archivo, "correo", email)

        ###### modificar lazy.xml  ########
        if ruta_archivo == r"C:\CetDev\version15.5\extensions\custom\%s\lazy.xml" % catalog_name_min:
            changeLine(ruta_archivo, "catalogLetters", codigo_catalogo)

        ###### modificar logo.png  ########
        carpeta_destino = r"C:\CetDev\version15.5\extensions\custom\%s" % catalog_name_min
        shutil.copy(logo, carpeta_destino)
        ruta_archivo_logo = os.path.join(carpeta_destino, os.path.basename(logo))
        nuevo_nombre_archivo = os.path.join(carpeta_destino, f"{catalog_name_min}Library.png")
        if os.path.exists(nuevo_nombre_archivo):
            os.remove(nuevo_nombre_archivo)
        os.rename(ruta_archivo_logo, nuevo_nombre_archivo)


    # SECOND TAB
    carpeta_secondtab = nueva_carpeta + "\secondTab"
    contenido_carpeta_st = os.listdir(carpeta_secondtab)

    for archivo in contenido_carpeta_st:
        ruta_archivo = os.path.join(carpeta_secondtab, archivo)
        changeLine(ruta_archivo, "ExtensionName", catalog_name)
        changeLine(ruta_archivo, "ExtensionMayusName", catalog_name_may)
        changeLine(ruta_archivo, "extensionnamemin", catalog_name_min)
        changeLine(ruta_archivo, "catalogLetters", codigo_catalogo)
        print(ruta_archivo)
        # Renombrar archivos
        if "ExtensionMayusName" in archivo:
            nuevo_nombre = archivo.replace("ExtensionMayusName", catalog_name_may)
            ruta_nuevo_archivo = os.path.join(carpeta_secondtab, nuevo_nombre)
            os.rename(ruta_archivo, ruta_nuevo_archivo)

        ###### modificar logo.png  ########
        carpeta_destino = r"C:\CetDev\version15.5\extensions\custom\%s\secondTab" % catalog_name_min
        shutil.copy(logo, carpeta_destino)
        ruta_archivo_logo = os.path.join(carpeta_destino, os.path.basename(logo))
        nuevo_nombre_archivo = os.path.join(carpeta_destino, f"products{codigo_catalogo}Library.png")
        if os.path.exists(nuevo_nombre_archivo):
            os.remove(nuevo_nombre_archivo) 
        os.rename(ruta_archivo_logo, nuevo_nombre_archivo)

        ###### buscar archivos de Hybrid #######
        if tipo_extension_seleccionado == "hybrid":
            
            product_name_min = productName.lower().replace(" ", "")
            product_name_may = productName.capitalize()

            # Renombrar archivos
            product_class = codigo_catalogo + product_name_may
            if "catalogLettersProductNameMay" in archivo:
                changeLine(ruta_archivo, "productName", productName)
                changeLine(ruta_archivo, "partnumber", partnumber)
                changeLine(ruta_archivo, "ProductNameMay", product_name_may)
                nuevo_nombre = archivo.replace("catalogLettersProductNameMay", product_class)
                ruta_nuevo_archivo = os.path.join(carpeta_secondtab, nuevo_nombre)
                os.rename(ruta_archivo, ruta_nuevo_archivo)

            if ruta_archivo == r"C:\CetDev\version15.5\extensions\custom\%s\secondTab\prdctFilteredVisibility.cm" % catalog_name_min:
                changeLine(ruta_archivo, "productnamemin", product_name_min)
            if ruta_archivo == r"C:\CetDev\version15.5\extensions\custom\%s\secondTab\prdctLibraryFilters.cm" % catalog_name_min:
                changeLine(ruta_archivo, "productnamemin", product_name_min)
            if ruta_archivo == r"C:\CetDev\version15.5\extensions\custom\%s\secondTab\productsHeader.cm" % catalog_name_min:
                changeLine(ruta_archivo, "productnamemin", product_name_min)
            if ruta_archivo == r"C:\CetDev\version15.5\extensions\custom\%s\secondTab\productsLibrary.cm" % catalog_name_min:
                changeLine(ruta_archivo, "partnumber", partnumber)
                changeLine(ruta_archivo, "productName", productName)
                changeLine(ruta_archivo, "productnamemin", product_name_min)
                changeLine(ruta_archivo, "ProductNameMay", product_name_may)
            if ruta_archivo == r"C:\CetDev\version15.5\extensions\custom\%s\secondTab\localize.rs" % catalog_name_min:
                changeLine(ruta_archivo, "productName", productName)
                changeLine(ruta_archivo, "productnamemin", product_name_min)

    # IMAGES
    carpeta_images = nueva_carpeta + "\images"

    # poner header #
    shutil.copy(header, carpeta_images) #copiar header dado a carpeta de destino
    # ruta completa del header actual
    ruta_archivo_header = os.path.join(carpeta_images, os.path.basename(header))
    # ruta completa del header a futuro
    nuevo_nombre_archivo = os.path.join(carpeta_images, "extensionHeader.png")
    if os.path.exists(nuevo_nombre_archivo):
        os.remove(nuevo_nombre_archivo)
    #cambiar nombre 
    os.rename(ruta_archivo_header, nuevo_nombre_archivo)
    if tipo_extension_seleccionado == "hybrid":
        # poner imagen producto #
        shutil.copy(prodimg, carpeta_images)

def changeLine(ruta_archivo, last_line, new_line):
    #leer el contenido
    with open(ruta_archivo, "r") as readfile:
        contenido = readfile.readlines()

    #sobreescribir donde encuentre la linea // cambiar Nombre 
    with open(ruta_archivo, 'w') as writefile:
        for linea in contenido:
            linea_modificada = linea.replace(last_line, new_line)
            writefile.write(linea_modificada)
    
######################################## END SCRIPT ##########################################

######################################## FORMULARIO BACK ##########################################
id_example = "Ex: \n // ID1=5589525715858500640 \n // ID2=1755369451227214228 \n // ID3=5327118955185941208 \n extensionId.id0 = int64(0x4d91fc06, 0x24a82c20); \n extensionId.id1 = int64(0x185c5337, 0x2df87194); \n extensionId.id2 = int64(0x49edba77, 0x281baad8); \n extensionId.id3 = int64(0x26a5800d, 0x99f4cb45);"
def on_entry_focus_in(event):
    if entrada_codigo_catalogo.get() == "Ex: BPG":
        entrada_codigo_catalogo.delete(0, tk.END)
        entrada_codigo_catalogo.config(fg="black")
    if entrada_id_catalogo.get() == "Ex: 123456":
        entrada_id_catalogo.delete(0, tk.END)
        entrada_id_catalogo.config(fg="black")
    if entrada_catalog_name.get() == "Ex: Botton + Gardiner":
        entrada_catalog_name.delete(0, tk.END)
        entrada_catalog_name.config(fg="black")

def on_entry_focus_out(event):
    if entrada_id_catalogo.get() == "":
        entrada_id_catalogo.insert(0, "Ex: 123456")
        entrada_id_catalogo.config(fg="gray")
    if entrada_codigo_catalogo.get() == "":
        entrada_codigo_catalogo.insert(0, "Ex: BPG")
        entrada_codigo_catalogo.config(fg="gray")
    if entrada_catalog_name.get() == "":
        entrada_catalog_name.insert(0, "Ex: Botton + Gardiner")
        entrada_catalog_name.config(fg="gray")

def on_text_focus_in(event):
    if entrada_extension_id.get("1.0", "end-1c") == id_example:
        entrada_extension_id.delete("1.0", "end-1c")
        entrada_extension_id.config(fg="black")

def on_text_focus_out(event):
    if entrada_extension_id.get("1.0", "end-1c") == "":
        entrada_extension_id.insert("1.0", id_example)
        entrada_extension_id.config(fg="gray")

# Función para seleccionar una imagen desde una ruta
def seleccionar_header():
    ruta_imagen = filedialog.askopenfilename(filetypes=[("Archivos de imagen", "*.jpg;*.jpeg;*.png")])
    entrada_ruta_header.delete(0, tk.END)
    entrada_ruta_header.insert(0, ruta_imagen)

def seleccionar_logo():
    ruta_imagen = filedialog.askopenfilename(filetypes=[("Archivos de imagen", "*.jpg;*.jpeg;*.png")])
    entrada_ruta_logo.delete(0, tk.END)
    entrada_ruta_logo.insert(0, ruta_imagen)

def seleccionar_prodimg(entrada_ruta_prodimg):
    ruta_imagen = filedialog.askopenfilename(filetypes=[("Archivos de imagen", "*.jpg;*.jpeg;*.png")])
    entrada_ruta_prodimg.delete(0, tk.END)
    entrada_ruta_prodimg.insert(0, ruta_imagen)


def desactivar_tabs(notebook):
    s = ttk.Style()
    s.layout('TNotebook.Tab', [])  # Eliminar el estilo de los tabs
    s.configure('TNotebook', tabposition='nw')  # Establecer la posición de los tabs en 'nw'
    notebook.enable_traversal()  # Desactivar la navegación por teclado en los tabs

# Función para cambiar de página
def ir_a_pagina_siguiente(notebook):
    # Obtener el índice de la página actual
    indice_actual = notebook.index(notebook.select())
    
    # Calcular el índice de la página siguiente (sumando 1)
    indice_siguiente = min(notebook.index('end'), indice_actual + 1)  # no ir más allá de la última página
    
    # Seleccionar la página siguiente
    notebook.select(indice_siguiente)

def ir_a_pagina_anterior(notebook):
    # Obtener el índice de la página actual
    indice_actual = notebook.index(notebook.select())

    # Calcular el índice de la página anterior (restando 1)
    indice_anterior = max(0, indice_actual - 1)  # no ir por debajo de 0

    # Seleccionar la página anterior
    notebook.select(indice_anterior)

def abrir_pagina_hybrid():
    #crear pagina 3
    page3 = tk.Frame(notebook, bg="#939494")
    page3.pack(fill="both", expand=True)

    # Agregar las páginas al notebook
    notebook.add(page3, text="Página 3")

    notebook.select(page3)

    # titulo pagina 3
    etiqueta_title3 = tk.Label(page3, text="AÑADE UN ITEM", bg="#939494", fg="white", font= font.Font(family="Roboto", size=12, weight='bold'))
    etiqueta_title3.pack(pady=4)
    
    # label partnumber
    etiqueta_partnumber = tk.Label(page3, text="PN:", bg="#939494", fg="white", font=("Roboto", 12))
    etiqueta_partnumber.pack(pady=4)
    
    entrada_partnumber = tk.Entry(page3, width=40, font=("Roboto", 12))
    entrada_partnumber.pack(pady=10)

    #label productName
    etiqueta_productName = tk.Label(page3, text="Product Name:", bg="#939494", fg="white", font=("Roboto", 12))
    etiqueta_productName.pack(pady=4)
    
    entrada_productName = tk.Entry(page3, width=40, font=("Roboto", 12))
    entrada_productName.pack(pady=10)

    # Campo seleccionar imagen producto
    etiqueta_ruta_prodimg = tk.Label(page3, text="Seleccionar imagen (60X60)", bg="#939494", fg="white", font=("Roboto", 12))
    etiqueta_ruta_prodimg.pack()

    entrada_ruta_prodimg = tk.Entry(page3, width=40, font=("Roboto", 12))
    entrada_ruta_prodimg.pack(pady=5)

    # Botón para seleccionar imagen producto
    boton_seleccionar_prodimg = tk.Button(page3, text="Seleccionar imagen", command=lambda: seleccionar_prodimg(entrada_ruta_prodimg), bg="#7E8D8D", fg="black", font=fuente_title)
    boton_seleccionar_prodimg.pack(pady=10)

    # Botón para enviar
    boton_enviar = tk.Button(page3, text="Enviar", command=lambda: enviar(entrada_productName.get(), entrada_partnumber.get(), entrada_ruta_prodimg.get()), bg="#7E8D8D", fg="black", font=fuente_title)
    boton_enviar.pack(pady=20)

def enviar(entrada_productName=None, entrada_partnumber=None, entrada_ruta_prodimg=None):
    tipo_extension_seleccionado = combo_tipo_extension.get()
    codigo_catalogo = entrada_codigo_catalogo.get()
    id_catalogo = entrada_id_catalogo.get()
    catalog_name = entrada_catalog_name.get()
    extension_id = entrada_extension_id.get("1.0", "end-1c")
    webpage = entrada_webpage.get()
    email = entrada_email.get()
    phone = entrada_phone.get()            
    brandText = entrada_brand_text.get("1.0", "end-1c")
    header = entrada_ruta_header.get()
    logo = entrada_ruta_logo.get()

    if tipo_extension_seleccionado == "hybrid":
        productName = entrada_productName
        partnumber = entrada_partnumber
        prodimg = entrada_ruta_prodimg
    else:
        productName = None
        partnumber = None
        prodimg = None
    
    generate(tipo_extension_seleccionado, codigo_catalogo, id_catalogo, catalog_name, extension_id, webpage, email, phone, brandText, header, logo, productName, partnumber, prodimg)
    print("GENERACION EXITOSA: Tipo de extensión seleccionado:", tipo_extension_seleccionado, 
          "Codigo catalogo:", codigo_catalogo, ",",
          "ID catalogo:", id_catalogo, ",",
          "Nombre del catalogo", catalog_name)
    
######################################## FORMULARIO DESIGN ##########################################
# Crear ventana principal
myWindow = tk.Tk()
myWindow.geometry("650x690")
myWindow.title("CET CODE GENERATOR")
myWindow.resizable(True, True)
myWindow.config(background="#7E8D8D")

# Crear frame para el formulario
formulario_frame = tk.Frame(myWindow, bg="#7E8D8D")
formulario_frame.pack(fill="both", expand=True, padx=0, pady=0)

# Crear scrollbar
scrollbar = ttk.Scrollbar(formulario_frame)
scrollbar.pack(side="right", fill="y")

# Crear lienzo (canvas) para el formulario
canvas = tk.Canvas(formulario_frame, bg="#939494", yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.config(command=canvas.yview)

# Configurar el lienzo para que se ajuste a los cambios en el contenido
canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Crear notebook para las páginas del formulario
notebook = ttk.Notebook(canvas, width=650, height=750)
notebook.pack(padx=1)

# Crear página 1
page1 = tk.Frame(notebook, bg="#939494")
page1.pack(fill="both", expand=True)

# fuente del titulo
fuente_title = font.Font(family="Roboto", size=12, weight="bold")

# Título principal
main_title = tk.Label(page1, text="CET CODE GENERATOR", font=fuente_title, bg="#5C6262", fg="white", width=65, height=4)
main_title.pack(pady=(0,10))

# código del catálogo
etiqueta_codigo_catalogo = tk.Label(page1, text="Codigo del catálogo:", bg="#939494", fg="white", font=("Roboto", 12))
etiqueta_codigo_catalogo.pack(pady=10)

entrada_codigo_catalogo = tk.Entry(page1, width=40, font=("Roboto", 12))
entrada_codigo_catalogo.insert(0, 'Ex: BPG')
entrada_codigo_catalogo.config(fg="gray")
entrada_codigo_catalogo.bind("<FocusIn>", on_entry_focus_in)
entrada_codigo_catalogo.bind("<FocusOut>", on_entry_focus_out)

entrada_codigo_catalogo.pack(pady=10)

# id del catálogo
etiqueta_id_catalogo = tk.Label(page1, text="Id del catálogo:", bg="#939494", fg="white", font=("Roboto", 12))
etiqueta_id_catalogo.pack()

entrada_id_catalogo = tk.Entry(page1, width=40, font=("Roboto", 12))
entrada_id_catalogo.insert(0, 'Ex: 123456')
entrada_id_catalogo.config(fg="gray")
entrada_id_catalogo.bind("<FocusIn>", on_entry_focus_in)
entrada_id_catalogo.bind("<FocusOut>", on_entry_focus_out)

entrada_id_catalogo.pack(pady=10)

# Nombre del catalogo
etiqueta_catalog_name = tk.Label(page1, text="Nombre del catálogo:", bg="#939494", fg="white", font=("Roboto", 12))
etiqueta_catalog_name.pack()

entrada_catalog_name = tk.Entry(page1, width=40, font=("Roboto", 12))
entrada_catalog_name.pack(pady=10)
entrada_catalog_name.insert(0, 'Ex: Botton + Gardiner')
entrada_catalog_name.config(fg="gray")
entrada_catalog_name.bind("<FocusIn>", on_entry_focus_in)
entrada_catalog_name.bind("<FocusOut>", on_entry_focus_out)

# Tipo de extensión
etiqueta_tipo_extension = tk.Label(page1, text="Tipo de extensión:", bg="#939494", fg="white", font=("Roboto", 12))
etiqueta_tipo_extension.pack()

tipo_extension = tk.StringVar()
combo_tipo_extension = ttk.Combobox(page1, textvariable=tipo_extension, values=["hybrid", "shell"], state="readonly", font=("Roboto", 12))
combo_tipo_extension.current(0)
combo_tipo_extension.pack(pady=10)

# Extension Id
etiqueta_extension_id = tk.Label(page1, text="Extension ids:", bg="#939494", fg="white", font=("Roboto", 12))
etiqueta_extension_id.pack()

entrada_extension_id = tk.Text(page1, height=8, width=58, font=("Monaco", 9))
entrada_extension_id.pack(pady=10)

# Asociar eventos de enfoque a las funciones correspondientes
entrada_extension_id.insert(0.0 , id_example)
entrada_extension_id.config(fg="gray")
entrada_extension_id.bind("<FocusIn>", on_text_focus_in)
entrada_extension_id.bind("<FocusOut>", on_text_focus_out)

# Crear página 2
page2 = tk.Frame(notebook, bg="#939494")
page2.pack(fill="both", expand=True)

# Agregar las páginas al notebook
notebook.add(page1, text="Página 1")
notebook.add(page2, text="Página 2")

# Ocultar la barra de pestañas del notebook
notebook.hide(1)

# Botón "Cambiar página"
boton_cambiar_pagina = tk.Button(page1, text="Siguiente", command=lambda: ir_a_pagina_siguiente(notebook), bg="#7E8D8D", fg="black", font=fuente_title)
boton_cambiar_pagina.pack(pady=20)

# Botón atrás
boton_atras = tk.Button(page2, text="←", command=lambda: ir_a_pagina_anterior(notebook), bg="#7E8D8D", fg="black", font=fuente_title)
boton_atras.pack(side="left", anchor="nw", padx=0, pady=0)

# webpage
etiqueta_webpage = tk.Label(page2, text="Webpage:", bg="#939494", fg="white", font=("Roboto", 12))
etiqueta_webpage.pack(pady=4)

entrada_webpage = tk.Entry(page2, width=40, font=("Roboto", 12))
entrada_webpage.pack(pady=10)

# phone
etiqueta_phone = tk.Label(page2, text="Phone:", bg="#939494", fg="white", font=("Roboto", 12))
etiqueta_phone.pack()

entrada_phone = tk.Entry(page2, width=40, font=("Roboto", 12))
entrada_phone.pack(pady=10)

# email
etiqueta_email = tk.Label(page2, text="Email:", bg="#939494", fg="white", font=("Roboto", 12))
etiqueta_email.pack()

entrada_email = tk.Entry(page2, width=40, font=("Roboto", 12))
entrada_email.pack(pady=10)

# Brand Text
etiqueta_brand_text = tk.Label(page2, text="Brand Text:", bg="#939494", fg="white", font=("Roboto", 12))
etiqueta_brand_text.pack()

entrada_brand_text = tk.Text(page2, height=8, width=58, font=("Monaco", 9))
entrada_brand_text.pack(pady=10)


# Campo seleccionar imagen header
etiqueta_ruta_header = tk.Label(page2, text="Seleccionar header (150x50)", bg="#939494", fg="white", font=("Roboto", 12))
etiqueta_ruta_header.pack()

entrada_ruta_header = tk.Entry(page2, width=40, font=("Roboto", 12))
entrada_ruta_header.pack(pady=5)

# Botón para seleccionar imagen header
boton_seleccionar_header = tk.Button(page2, text="Seleccionar imagen", command=seleccionar_header, bg="#7E8D8D", fg="black", font=fuente_title)
boton_seleccionar_header.pack(pady=10)

# Campo seleccionar imagen logo
etiqueta_ruta_logo = tk.Label(page2, text="Seleccionar logo (30x20):", bg="#939494", fg="white", font=("Roboto", 12))
etiqueta_ruta_logo.pack()

entrada_ruta_logo = tk.Entry(page2, width=40, font=("Roboto", 12))
entrada_ruta_logo.pack(pady=5)

# Botón para seleccionar imagen logo
boton_seleccionar_logo = tk.Button(page2, text="Seleccionar imagen", command=seleccionar_logo, bg="#7E8D8D", fg="black", font=fuente_title)
boton_seleccionar_logo.pack(pady=10)

def actualizar_boton():
    tipo_extension_seleccionado = combo_tipo_extension.get()
    print(tipo_extension_seleccionado)
    if tipo_extension_seleccionado == "hybrid":
        boton_enviar.pack_forget()  # Oculta el botón "Enviar"
        boton_siguiente.pack()  # Muestra el botón "Siguiente"
    else:
        boton_siguiente.pack_forget()  # Oculta el botón "Siguiente"
        boton_enviar.pack()  # Muestra el botón "Enviar"

# Crea el botón "Enviar"
boton_enviar = tk.Button(page2, text="Enviar", command=enviar, bg="#7E8D8D", fg="black", font=fuente_title)

# Crea el botón "Siguiente"
boton_siguiente = tk.Button(page2, text="Siguiente", command=abrir_pagina_hybrid, bg="#7E8D8D", fg="black", font=fuente_title)

actualizar_boton()

# Conectar la función `actualizar_boton` con el evento de selección en el combo_box
combo_tipo_extension.bind("<<ComboboxSelected>>", lambda e: actualizar_boton())

# Configurar la barra de desplazamiento
scrollbar.config(command=canvas.yview)

# Ejecutar bucle de eventos
myWindow.mainloop()