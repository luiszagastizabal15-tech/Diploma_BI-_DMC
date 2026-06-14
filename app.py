# Librerías usadas
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# ==============================
# FUNCIONES REUTILIZABLES
# ==============================

# Devuelve la lista de columnas numéricas
def obtener_columnas_numericas(df):
    return df.select_dtypes(include="number").columns.tolist()

# Devuelve la lista de columnas categóricas
def obtener_columnas_categoricas(df):
    return df.select_dtypes(include=["object", "category"]).columns.tolist()

# Devuelve la lista de columnas de tipo fecha
def obtener_columnas_fecha(df):
    return df.select_dtypes(include=["datetime", "datetime64[ns]"]).columns.tolist()

# Calcula los outliers usando la regla IQR
def detectar_outliers_iqr(serie):
    Q1 = serie.quantile(0.25)              # Primer cuartil
    Q3 = serie.quantile(0.75)              # Tercer cuartil
    IQR = Q3 - Q1                          # Rango intercuartílico
    limite_inferior = Q1 - 1.5 * IQR       # Límite inferior
    limite_superior = Q3 + 1.5 * IQR       # Límite superior
    # Filtramos los valores que están fuera de los límites
    outliers = serie[(serie < limite_inferior) | (serie > limite_superior)]
    return outliers, limite_inferior, limite_superior

# ==============================
# CONFIGURACIÓN DE SESSION STATE
# ==============================

# Para guardar el dataset cargado
if "data" not in st.session_state:
    st.session_state.data = None

# Para guardar el nombre del dataset cargado
if "nombre_archivo" not in st.session_state:
    st.session_state.nombre_archivo = None

# ==============================
# TÍTULO E IMÁGENES
# ==============================

# Título principal 
st.title("Proyecto Final Diploma BI")

# Título en la barra lateral
st.sidebar.title("Parámetros")

# Imagen en página principal
st.image("Pythonlogo.png", width=150)

# Imagen en barra lateral
st.sidebar.image("DMCLogo.png", width=200)

# ==============================
# MENÚ DE MÓDULOS
# ==============================

modulos = st.sidebar.selectbox("Seleccione un módulo",
                               ["Home", "Carga y perfil del dataset", "Procesamiento de datos", "Análisis visual"])

# ==============================
# MÓDULO HOME
# ==============================

if modulos == "Home":

    st.subheader("App analizadora de datasets con Streamlit")

    # Datos del autor y año
    st.write("**Creado por:** Gustavo Rodriguez")
    st.write("**Año:** 2026")

    # Objetivo del proyecto
    st.markdown("### Objetivo del proyecto")
    st.write(
        "Construir una aplicación en Streamlit capaz de cargar, validar, procesar "
        "y visualizar cualquiera de los cuatro datasets propuestos, mostrando un "
        "análisis exploratorio claro y dinámico. El objetivo NO es crear un modelo "
        "predictivo, sino una herramienta analítica funcional y ordenada."
    )

    # Tecnologías usadas
    st.markdown("### Tecnologías usadas")
    st.write("Python, Pandas, NumPy, Streamlit, Plotly, Matplotlib, Seaborn y GitHub.")

    # Nota de uso responsable
    st.markdown("### Nota de uso responsable")
    st.info("Los resultados de esta aplicación son exploratorios y no reemplazan una "
            "validación técnica o profesional.")

    # Seteo del estado del dataset (Si se subió o no)
    st.markdown("---")
    if st.session_state.data is not None:
        st.success(f"Dataset cargado: {st.session_state.nombre_archivo}")
    else:
        st.info("Aún no se ha cargado ningún dataset.")

# ==============================
# MÓDULO CARGA Y PERFIL
# ==============================

elif modulos == "Carga y perfil del dataset":

    st.subheader("Carga y perfil del dataset")

    # Cargador de archivos en formatos Excel o CSV
    archivo = st.file_uploader(
        "Cargue el archivo Excel o CSV",
        type=["csv", "xlsx"]
    )

    # Validación si el usuario cargó un archivo
    if archivo is not None:
        # Guardar nombre del archivo en session_state
        st.session_state.nombre_archivo = archivo.name

        # Validación de formato de archivo .csv
        if archivo.name.endswith(".csv"):
            # Abrir el archivo CSV 
            st.session_state.data = pd.read_csv(archivo)

        # Validación de formato de archivo .xlsx
        elif archivo.name.endswith(".xlsx"):
            # Abrir el archivo CSV  Excel 
            st.session_state.data = pd.read_excel(archivo)

        # Mensaje de error si no es ninguno de los 2 formatos
        else:
            st.error("Formato no válido")

        # Confirmación de que el archivo fue cargado
        st.success("Archivo cargado correctamente")

    # Si se cargó, se muestra de esta manera
    if st.session_state.data is not None:

        # Guardamos el dataset en una variable corta para usarlo más fácil
        data = st.session_state.data

        st.write(f"Archivo actual: **{st.session_state.nombre_archivo}**")

        st.subheader("Vista previa del dataset")
        # Mostramos solo las primeras filas con head()
        st.dataframe(data.head())

        # ----- MÉTRICAS RÁPIDAS -----
        st.subheader("Métricas Generals")

        # Calculo de valores
        num_filas = data.shape[0]
        num_columnas = data.shape[1]
        num_numericas = len(obtener_columnas_numericas(data))
        num_categoricas = len(obtener_columnas_categoricas(data))
        total_nulos = int(data.isnull().sum().sum())
        total_duplicados = int(data.duplicated().sum())

        # Métrcas con st.columns y st.metric
        col1, col2, col3 = st.columns(3)
        col1.metric("Filas", num_filas)
        col2.metric("Columnas", num_columnas)
        col3.metric("Variables numéricas", num_numericas)

        col4, col5, col6 = st.columns(3)
        col4.metric("Variables categóricas", num_categoricas)
        col5.metric("Valores nulos", total_nulos)
        col6.metric("Duplicados", total_duplicados)

        # ----- CARACTERÍSTICAS BÁSICAS -----
        st.subheader("Características del dataset")

        # Nombres de columnas
        st.write("Columnas del dataset:")
        st.write(data.columns.tolist())

        # Tipos de datos
        st.write("Tipos de datos:")
        st.write(data.dtypes)

        # Recuento de valores nulos por columna
        st.write("Valores nulos por columna:")
        st.write(data.isnull().sum())

        # Estadística descriptiva
        st.write("Estadística descriptiva:")
        st.write(data.describe())

        # ----- DETALLE DE VARIABLES RELEVANTES -----
        st.subheader("VISUALIZAR DETALLES DE VARIABLE")
        columnas_elegidas = st.multiselect(
            "Elija la/s varuables que desea revisar:",
            data.columns.tolist()
        )
        # Mostrar solo las columnas elegidas 
        if columnas_elegidas:
            st.dataframe(data[columnas_elegidas].head())

        # Opción para eliminar el dataset cargado
        if st.button("Eliminar dataset"):
            st.session_state.data = None
            st.session_state.nombre_archivo = None
            st.rerun()

    else:
        st.write("Por favor cargue su archivo.")

# ==============================
# MÓDULO PROCESAMIENTO DE DATOS
# ==============================

elif modulos == "Procesamiento de datos":

    st.subheader("Procesamiento de datos")

    # Validación si se subió un dataset
    if st.session_state.data is not None:

        # Hacer una copia del dataset original
        data = st.session_state.data.copy()

        # ----- ESTANDARIZAR NOMBRES DE COLUMNAS -----
        st.markdown("### 1. Nombres de columnas")
        # Opción para limpiar nombres con checkbox
        if st.checkbox("Estandarizar nombres de columnas (minúsculas y sin espacios)"):
            data.columns = (
                data.columns
                .str.strip()           # Quitamos espacios al inicio y final
                .str.lower()           # Pasamos todo a minúsculas
                .str.replace(" ", "_") # Reemplazamos espacios por guion bajo
            )
            # Guardamos el cambio en session_state
            st.session_state.data = data
            st.success("Nombres de columnas estandarizados.")
        st.write(data.columns.tolist())

        # ----- CLASIFICACIÓN AUTOMÁTICA DE VARIABLES -----
        st.markdown("### 2. Clasificación automática de variables")
        columnas_num = obtener_columnas_numericas(data)
        columnas_cat = obtener_columnas_categoricas(data)
        columnas_fecha = obtener_columnas_fecha(data)

        st.write("**Numéricas:**", columnas_num if columnas_num else "No hay")
        st.write("**Categóricas:**", columnas_cat if columnas_cat else "No hay")
        st.write("**Fechas:**", columnas_fecha if columnas_fecha else "No hay")

        # ----- CONVERSIÓN DE FECHAS -----
        st.markdown("### 3. Conversión de fechas")
        # Opción de seleccionar columnas a convertir a en formato fecha
        posibles_fechas = st.multiselect(
            "Seleccione columnas que deban convertirse a fecha:",
            columnas_cat
        )
        for col in posibles_fechas:
            # Usando errors='coerce' para no romper la app con formatos distintos
            data[col] = pd.to_datetime(data[col], errors="coerce")
        if posibles_fechas:
            st.session_state.data = data
            st.success("Columnas convertidas a fecha.")

        # ----- VALORES NULOS Y DUPLICADOS -----
        st.markdown("### 4. Valores nulos y duplicados")
        # Recuento de valores nulos
        nulos = data.isnull().sum()
        porcentaje_nulos = (nulos / len(data) * 100).round(2)
        tabla_nulos = pd.DataFrame({
            "Nulos": nulos,
            "Porcentaje (%)": porcentaje_nulos
        })
        st.write("Valores faltantes por columna:")
        st.dataframe(tabla_nulos)

        # Recuento cantidad de duplicados
        duplicados = data.duplicated().sum()
        st.write(f"Filas duplicadas: **{duplicados}**")

        # ----- OUTLIERS POR IQR -----
        st.markdown("### 5. Detección de outliers (regla IQR)")
        if columnas_num:
            columna_outlier = st.selectbox(
                "Seleccione una columna numérica:",
                columnas_num
            )
            # Función reutilizable
            outliers, lim_inf, lim_sup = detectar_outliers_iqr(data[columna_outlier])
            st.write(f"Límite inferior: {round(lim_inf, 2)} | Límite superior: {round(lim_sup, 2)}")
            st.write(f"Cantidad de outliers encontrados: **{len(outliers)}**")
        else:
            st.info("El dataset no tiene columnas numéricas para analizar outliers.")

        # ----- FILTRO DINÁMICO -----
        st.markdown("### 6. Filtro dinámico")
        if columnas_cat:
            columna_filtro = st.selectbox(
                "Filtrar por una columna categórica:",
                columnas_cat
            )
            # Mostrar valores únicos a elegir
            valores = st.multiselect(
                "Seleccione los valores a mostrar:",
                data[columna_filtro].dropna().unique().tolist()
            )
            if valores:
                data_filtrada = data[data[columna_filtro].isin(valores)]
                st.write(f"Filas resultantes: {data_filtrada.shape[0]}")
                st.dataframe(data_filtrada.head())
        else:
            st.info("El dataset no tiene columnas categóricas para filtrar.")

    else:
        st.warning(
            "Primero debe cargar un dataset en el módulo "
            "'Carga y perfil del dataset'."
        )


# ==============================
# MÓDULO ANÁLISIS VISUAL
# ==============================

elif modulos == "Análisis visual":

    st.subheader("Análisis visual")

    # Validación si se subió dataset
    if st.session_state.data is not None:

        # Guardamos el dataset en una variable corta
        data = st.session_state.data

        # Obtenemos las listas de columnas 
        columnas_num = obtener_columnas_numericas(data)
        columnas_cat = obtener_columnas_categoricas(data)
        columnas_fecha = obtener_columnas_fecha(data)

        # Creación de pestañas para el análisis
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "Resumen", "Univariado", "Bivariado",
            "Multivariado", "Temporal", "Insights"
        ])

        # ----- TAB 1: RESUMEN -----
        with tab1:
            st.markdown("#### Resumen")
            col1, col2, col3 = st.columns(3)
            col1.metric("Filas", data.shape[0])
            col2.metric("Columnas", data.shape[1])
            col3.metric("Nulos", int(data.isnull().sum().sum()))

            st.write("Tipos de datos:")
            st.write(data.dtypes)

            st.write("Resumen estadístico:")
            st.write(data.describe())

        # ----- TAB 2: ANÁLISIS UNIVARIADO -----
        with tab2:
            st.markdown("#### Análisis univariado")

            # Analizador de variable numérica
            if columnas_num:
                variable_num = st.selectbox(
                    "Seleccione una columna numérica:",
                    columnas_num,
                    key="uni_num"
                )
                # Organización de histograma y boxplot en dos columnas
                col1, col2 = st.columns(2)
                with col1:
                    fig_hist = px.histogram(data, x=variable_num,
                                            title=f"Histograma de {variable_num}")
                    st.plotly_chart(fig_hist, use_container_width=True)
                with col2:
                    fig_box = px.box(data, y=variable_num,
                                     title=f"Boxplot de {variable_num}")
                    st.plotly_chart(fig_box, use_container_width=True)
            else:
                st.info("El dataset no tiene columnas numéricas.")

            # Analizar variable categórica
            if columnas_cat:
                variable_cat = st.selectbox(
                    "Seleccione una columna categórica:",
                    columnas_cat,
                    key="uni_cat"
                )
                # Contao y grafico de barras
                conteo = data[variable_cat].value_counts().reset_index()
                conteo.columns = [variable_cat, "conteo"]
                fig_barras = px.bar(conteo, x=variable_cat, y="conteo",
                                    title=f"Conteo de {variable_cat}")
                st.plotly_chart(fig_barras, use_container_width=True)
            else:
                st.info("El dataset no tiene columnas categóricas.")

        # ----- TAB 3: ANÁLISIS BIVARIADO -----
        with tab3:
            st.markdown("#### Análisis bivariado")

            # Condicional de mínimo para el scatter
            if len(columnas_num) >= 2:
                col1, col2 = st.columns(2)
                with col1:
                    var_x = st.selectbox("Variable X:", columnas_num, key="bi_x")
                with col2:
                    var_y = st.selectbox("Variable Y:", columnas_num, key="bi_y")
                fig_scatter = px.scatter(data, x=var_x, y=var_y,
                                         title=f"{var_x} vs {var_y}")
                st.plotly_chart(fig_scatter, use_container_width=True)
            else:
                st.info("Se necesitan al menos dos columnas numéricas.")

            # Boxplot de  variable numérica / categórica
            if columnas_num and columnas_cat:
                var_num_bi = st.selectbox("Variable numérica:", columnas_num, key="bi_num")
                var_cat_bi = st.selectbox("Variable categórica:", columnas_cat, key="bi_cat")
                fig_box_cat = px.box(data, x=var_cat_bi, y=var_num_bi,
                                     title=f"{var_num_bi} por {var_cat_bi}")
                st.plotly_chart(fig_box_cat, use_container_width=True)

        # ----- TAB 4: ANÁLISIS MULTIVARIADO -----
        with tab4:
            st.markdown("#### Análisis multivariado")

            # Heatmap de correlación con Seaborn
            if len(columnas_num) >= 2:
                st.write("Mapa de calor de correlaciones:")
                # Matriz de correlación
                correlacion = data[columnas_num].corr()
                # Figura usando Matplotlib/Seaborn
                fig, ax = plt.subplots()
                sns.heatmap(correlacion, annot=True, cmap="Blues", ax=ax)
                st.pyplot(fig)
            else:
                st.info("Se necesitan al menos dos columnas numéricas para la correlación.")

        # ----- TAB 5: ANÁLISIS TEMPORAL -----
        with tab5:
            st.markdown("#### Análisis temporal")

            # Condicion para solo mostrar si existen fechas para el análisis
            if columnas_fecha and columnas_num:
                col_fecha = st.selectbox("Columna de fecha:", columnas_fecha, key="temp_fecha")
                col_valor = st.selectbox("Variable numérica:", columnas_num, key="temp_valor")
                # Ordenar fechas y graficar línea de tiempo
                data_orden = data.sort_values(by=col_fecha)
                fig_linea = px.line(data_orden, x=col_fecha, y=col_valor,
                                    title=f"Evolución de {col_valor} en el tiempo")
                st.plotly_chart(fig_linea, use_container_width=True)
            else:
                st.info("El dataset no tiene columnas de fecha. "
                        "Conviértalas primero en el módulo de Procesamiento.")

        # ----- TAB 6: INSIGHTS -----
        with tab6:
            st.markdown("#### Insights y conclusiones")
            st.write("Aquí se presentan algunos hallazgos exploratorios automáticos:")

            # Mostramos algunos hallazgos simples calculados con los datos
            if columnas_num:
                col_mas_nula = data.isnull().sum().idxmax()
                st.write(f"- La columna con más valores nulos es: **{col_mas_nula}**")
                st.write(f"- El dataset tiene **{data.duplicated().sum()}** filas duplicadas.")
                st.write(f"- Hay **{len(columnas_num)}** variables numéricas y "
                         f"**{len(columnas_cat)}** categóricas.")

            st.info("Estas conclusiones son exploratorias y deben "
                    "interpretarse con cuidado, sin afirmaciones exageradas.")

    else:
        st.warning(
            "Primero debe cargar un dataset en el módulo "
            "'Carga y perfil del dataset'."
        )
