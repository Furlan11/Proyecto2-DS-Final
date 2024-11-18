import streamlit as st
import pandas as pd
import numpy as np

# Título de la aplicación
st.title("Mi primera aplicación de Streamlit")

# Subtítulo o descripción
st.write("Esta es una aplicación sencilla de ejemplo")

# Generar algunos datos de muestra
data = pd.DataFrame(
    np.random.randn(100, 2),
    columns=['Columna 1', 'Columna 2']
)

# Mostrar el dataframe
st.write("Aquí hay un DataFrame aleatorio:")
st.dataframe(data)

# Mostrar un gráfico
st.line_chart(data)
