import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.linear_model import LinearRegression

# Configuración de página
st.set_page_config(page_title="LP - Dashboard Citas Médicas", layout="wide")

# Cargar dataset con prefijo LP
LP_df = pd.read_csv('LP_citas_medicas.csv')
LP_df['LP_fecha'] = pd.to_datetime(LP_df['LP_fecha'])
LP_df['LP_mes'] = LP_df['LP_fecha'].dt.month

st.title('LP - Dashboard de Gestión de Citas Médicas (Hospital Lima Norte)')

# --- KPIs SUPERIORES ---
LP_total_citas = len(LP_df)
LP_tasa_cancelacion = (LP_df['LP_estado'] == 'Cancelada').mean() * 100
LP_tasa_ausencia = (LP_df['LP_estado'] == 'No asistió').mean() * 100
LP_esp_top = LP_df['LP_especialidad'].value_counts().idxmax()

LP_col1, LP_col2, LP_col3, LP_col4 = st.columns(4)
LP_col1.metric("Total de Citas", f"{LP_total_citas:,}")
LP_col2.metric("Especialidad Top", LP_esp_top)
LP_col3.metric("% Cancelaciones", f"{LP_tasa_cancelacion:.2f}%")
LP_col4.metric("% No Asistió", f"{LP_tasa_ausencia:.2f}%")

st.divider()

# --- GRÁFICOS PRINCIPALES ---
LP_c1, LP_c2 = st.columns(2)

with LP_c1:
    st.subheader('Citas por Especialidad')
    LP_conteo_esp = LP_df['LP_especialidad'].value_counts().reset_index()
    LP_conteo_esp.columns = ['Especialidad', 'Cantidad']
    LP_fig1 = px.bar(
        LP_conteo_esp,
        x='Especialidad',
        y='Cantidad',
        color='Especialidad',
        text_auto=True
    )
    st.plotly_chart(LP_fig1, use_container_width=True)

with LP_c2:
    st.subheader('Estado de las Citas')
    LP_fig2 = px.pie(
        LP_df,
        names='LP_estado',
        hole=0.4
    )
    st.plotly_chart(LP_fig2, use_container_width=True)

# --- SERIE TEMPORAL POR MES ---
LP_citas_mes = LP_df.groupby('LP_mes').size().reset_index(name='LP_cantidad')

st.subheader('Evolución de Citas por Mes')
LP_fig3 = px.line(
    LP_citas_mes,
    x='LP_mes',
    y='LP_cantidad',
    markers=True,
    labels={'LP_mes': 'Mes', 'LP_cantidad': 'Cantidad de Citas'}
)
st.plotly_chart(LP_fig3, use_container_width=True)
