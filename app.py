import streamlit as st
import google.generativeai as genai
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import io

# Configuración de página
st.set_page_config(page_title="Asistente de Trámites UNAL")

# Título con color institucional
st.markdown("<h1 style='color:#C8102E;'>Asistente de Trámites UNAL</h1>", unsafe_allow_html=True)

st.write("Genera cartas formales siguiendo lineamientos institucionales.")

# Campo para API Key
api_key = st.text_input("Ingresa tu API Key de Gemini", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    st.subheader("Datos del estudiante")

    nombre = st.text_input("Nombre completo")
    documento = st.text_input("Número de documento")
    programa = st.text_input("Programa académico")
    facultad = st.text_input("Facultad")
    sede = st.text_input("Sede")
    motivo = st.text_area("Describe el motivo del trámite")

    if st.button("Generar carta formal"):

        prompt = f"""
        Redacta una carta formal dirigida a la Universidad Nacional de Colombia.
        Usa tono institucional.
        No inventes información.
        No agregues datos que no fueron proporcionados.

        Nombre: {nombre}
        Documento: {documento}
        Programa: {programa}
        Facultad: {facultad}
        Sede: {sede}
        Motivo: {motivo}
        """

        respuesta = model.generate_content(prompt)
        carta = respuesta.text

        st.subheader("Vista previa")
        st.write(carta)

        # Crear PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        elementos = []
        elementos.append(Paragraph(carta.replace("\n", "<br/>"), styles["Normal"]))
        elementos.append(Spacer(1, 0.5 * inch))
        doc.build(elementos)
        buffer.seek(0)

        st.download_button(
            label="Descargar PDF",
            data=buffer,
            file_name="Carta_UNAL.pdf",
            mime="application/pdf"
        )
