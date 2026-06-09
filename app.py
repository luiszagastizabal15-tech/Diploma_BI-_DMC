# Importamos Streamlit para crear la aplicación web
import streamlit as st

# Importamos Pandas para leer archivos CSV y Excel
import pandas as pd

# Creamos el título principal de la aplicación
st.title("Proyecto Final Diploma BI")

# Creamos un título en la barra lateral
st.sidebar.title("Parámetros")

# Mostramos una imagen en la página principal con un ancho de 500 píxeles
st.image("Pythonlogo.png", width=150)

# Mostramos una imagen en la barra lateral con un ancho de 100 píxeles
st.sidebar.image("DMCLogo.png", width=200)

# Mostramos un texto indicando el autor del proyecto
st.write("Elaborado por: Gustavo Rodriguez")

modulos = st.sidebar.selectbox('Seleccione un módulo',["Home", "Carga y perfil del dataset", "Procesamiento de datos", "Analisis visual"])

if modulos == "Home":
    st.write("Bienvenido a la aplicacion")

elif modulos == "Carga y perfil del dataset":
    # Creamos un cargador de archivos para subir archivos Excel o CSV
    archivo = st.file_uploader("Cargue el archivo excel o csv")
    
    # Validamos si el usuario cargó un archivo
    if archivo is not None:
    
        # Validamos si el archivo cargado tiene extensión .csv
        if archivo.name.endswith(".csv"):
    
            # Leemos el archivo CSV y lo guardamos en un DataFrame
            data = pd.read_csv(archivo)
    
            # Mostramos el DataFrame en la aplicación
            st.write(data)
    
        # Validamos si el archivo cargado tiene extensión .xlsx
        elif archivo.name.endswith(".xlsx"):
    
            # Leemos el archivo Excel y lo guardamos en un DataFrame
            data = pd.read_excel(archivo)
    
            # Mostramos el DataFrame en la aplicación
            st.write(data)
    
        # Si el archivo no es CSV ni Excel, mostramos un mensaje de error
        else:
            st.write("Formato no válido")
    
    # Si el usuario no ha cargado ningún archivo, mostramos un mensaje
    else:
        st.write("Por favor cargue su archivo")
    
