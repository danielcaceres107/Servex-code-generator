import os, re
import tkinter as tk
from tkinter import ttk, font, filedialog
import shutil
from PIL import Image


################################## SCRIPT ###########################################

def generate(tipo_extension_seleccionado, codigo_catalogo, id_catalogo, catalog_name, extension_id, webpage, email, phone, brandText, header, logo):

    # crear variables para diferentes tipos de nombre
    catalog_name_min = catalog_name.lower().replace(" ", "")
    catalog_name_may = catalog_name_min.capitalize()

    #elegir carpeta estatica segun tipo de extension

    if tipo_extension_seleccionado == "shell":
        carpeta = r'C:\CetDev\version14.0\extensions\custom\staticExtension'

    if tipo_extension_seleccionado == "hybrid":
        carpeta = r'C:\CetDev\version14.0\extensions\custom\staticExtension2'


    nueva_carpeta = r'C:\CetDev\version14.0\extensions\custom\%s' % catalog_name_min

    # Verificar si la carpeta nueva ya existe
    if os.path.exists(nueva_carpeta):
        shutil.rmtree(nueva_carpeta)

    # Copiar la carpeta existente a la nueva carpeta
    shutil.copytree(carpeta, nueva_carpeta)

    #TO-DO: hacer que las rutas sean dinamicas para donde quiera que se ejecute el script(?)

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

        ###### modificar extension.cm ... ######
        if ruta_archivo == r"C:\CetDev\version14.0\extensions\custom\%s\extension.cm" % catalog_name_min:
            changeLine(ruta_archivo, "//generateExtensionId", extension_id)
            changeLine(ruta_archivo, "catalogLetters", codigo_catalogo)

        ##### modificar Header.cm ######
        if ruta_archivo == r"C:\CetDev\version14.0\extensions\custom\%s\header.cm" % catalog_name_min:
            changeLine(ruta_archivo, "portafolioIdNumbers", id_catalogo)
            changeLine(ruta_archivo, "catalogLetters", codigo_catalogo)

        ###### modificar library.cm  ########
        if ruta_archivo == r"C:\CetDev\version14.0\extensions\custom\%s\library.cm" % catalog_name_min:
            changeLine(ruta_archivo, "catalogLetters", codigo_catalogo)
            
            cant_chars = len(brandText)
            if cant_chars > 37 :
                fragmentos = [brandText[i:i+37] for i in range(0, len(brandText), 37)]
                print(fragmentos)
                format_brandText = "\\n".join(fragmentos)
                print(format_brandText)
                 
            changeLine(ruta_archivo, "brandText", format_brandText)
            changeLine(ruta_archivo, "webpage", webpage)
            changeLine(ruta_archivo, "telefono", phone)
            changeLine(ruta_archivo, "correo", email)

        ###### modificar localize.rs  ########
        if ruta_archivo == r"C:\CetDev\version14.0\extensions\custom\%s\localize.rs" % catalog_name_min:
            changeLine(ruta_archivo, "webpage", webpage)
            changeLine(ruta_archivo, "telefono", phone)
            changeLine(ruta_archivo, "correo", email)

        ###### modificar lazy.xml  ########
        if ruta_archivo == r"C:\CetDev\version14.0\extensions\custom\%s\lazy.xml" % catalog_name_min:
            changeLine(ruta_archivo, "catalogLetters", codigo_catalogo)

        ###### modificar logo.png  ########
        carpeta_destino = r"C:\CetDev\version14.0\extensions\custom\%s" % catalog_name_min
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

        # Renombrar archivos
        if "ExtensionMayusName" in archivo:
            nuevo_nombre = archivo.replace("ExtensionMayusName", catalog_name_may)
            ruta_nuevo_archivo = os.path.join(carpeta_secondtab, nuevo_nombre)
            os.rename(ruta_archivo, ruta_nuevo_archivo)

        ###### modificar EXTENSION.CM... ######
        if ruta_archivo == r"C:\CetDev\version14.0\extensions\custom\%s\secondTab\extension.cm" % catalog_name_min:
            changeLine(ruta_archivo, "catalogLetters", codigo_catalogo)
        ###### modificar library.cm  ########
        if ruta_archivo == r"C:\CetDev\version14.0\extensions\custom\%s\secondTab\library.cm" % catalog_name_min:
            changeLine(ruta_archivo, "catalogLetters", codigo_catalogo)

        ###### modificar lazy.xml  ########
        if ruta_archivo == r"C:\CetDev\version14.0\extensions\custom\%s\secondTab\lazy.xml" % catalog_name_min:
            changeLine(ruta_archivo, "catalogLetters", codigo_catalogo)

        ###### modificar logo.png  ########
        carpeta_destino = r"C:\CetDev\version14.0\extensions\custom\%s\secondTab" % catalog_name_min
        shutil.copy(logo, carpeta_destino)
        ruta_archivo_logo = os.path.join(carpeta_destino, os.path.basename(logo))
        nuevo_nombre_archivo = os.path.join(carpeta_destino, f"products{codigo_catalogo}Library.png")
        if os.path.exists(nuevo_nombre_archivo):
            os.remove(nuevo_nombre_archivo) 
        os.rename(ruta_archivo_logo, nuevo_nombre_archivo)

        ###### buscar archivos de Hybrid #######
        if tipo_extension_seleccionado == "hybrid":
            if ruta_archivo == r"C:\CetDev\version14.0\extensions\custom\%s\secondTab\prdctLibraryFilters.cm" % catalog_name_min:
                changeLine(ruta_archivo, "catalogLetters", codigo_catalogo)
            if ruta_archivo == r"C:\CetDev\version14.0\extensions\custom\%s\secondTab\prdctFilteredLibraryLimb.cm" % catalog_name_min:
                changeLine(ruta_archivo, "catalogLetters", codigo_catalogo)
            if ruta_archivo == r"C:\CetDev\version14.0\extensions\custom\%s\secondTab\prdctFilteredVisibility.cm" % catalog_name_min:
                changeLine(ruta_archivo, "catalogLetters", codigo_catalogo)


    # IMAGES
    carpeta_images = nueva_carpeta + "\images"
    shutil.copy(header, carpeta_images) #copiar header dado a carpeta de destino
    # ruta completa del header actual
    ruta_archivo_header = os.path.join(carpeta_images, os.path.basename(header))
    # ruta completa del header a futuro
    nuevo_nombre_archivo = os.path.join(carpeta_images, "extensionHeader.png")
    if os.path.exists(nuevo_nombre_archivo):
        os.remove(nuevo_nombre_archivo)
    #cambiar nombre 
    os.rename(ruta_archivo_header, nuevo_nombre_archivo)


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

######################################## FORMULARIO ##########################################
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


def desactivar_tabs(notebook):
    s = ttk.Style()
    s.layout('TNotebook.Tab', [])  # Eliminar el estilo de los tabs
    s.configure('TNotebook', tabposition='nw')  # Establecer la posición de los tabs en 'nw'
    notebook.enable_traversal()  # Desactivar la navegación por teclado en los tabs

# Función para cambiar de página
def cambiar_pagina():
    if notebook.index(notebook.select()) == 0:
        notebook.hide(0)
        notebook.select(1)
        boton_cambiar_pagina.config(text="Siguiente")
    else:
        notebook.hide(1)
        notebook.select(0)
        boton_cambiar_pagina.config(text="Cambiar página")

def enviar():
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
    
    generate(tipo_extension_seleccionado, codigo_catalogo, id_catalogo, catalog_name, extension_id, webpage, email, phone, brandText, header, logo)
    print("GENERACION EXITOSA: Tipo de extensión seleccionado:", tipo_extension_seleccionado, 
          "Codigo catalogo:", codigo_catalogo, ",",
          "ID catalogo:", id_catalogo, ",",
          "Nombre del catalogo", catalog_name)
    

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
boton_cambiar_pagina = tk.Button(page1, text="Siguiente", command=cambiar_pagina, bg="#7E8D8D", fg="black", font=fuente_title)
boton_cambiar_pagina.pack(pady=20)

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

# Botón para enviar
boton_tipo_extension = tk.Button(page2, text="Enviar", command=enviar, bg="#7E8D8D", fg="black", font=fuente_title)
boton_tipo_extension.pack(pady=20)

# Configurar la barra de desplazamiento
scrollbar.config(command=canvas.yview)

# Ejecutar bucle de eventos
myWindow.mainloop()