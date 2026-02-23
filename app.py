import streamlit as st
import google.generativeai as genai
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import io
from datetime import datetime

st.set_page_config(page_title="Asistente Normativo UNAL", layout="centered")

# Color institucional
st.markdown("<h1 style='color:#C8102E;'>Asistente Normativo UNAL</h1>", unsafe_allow_html=True)
st.markdown("Herramienta de orientación basada en normativa institucional vigente.")
st.markdown("---")

# API KEY
api_key = st.text_input("Ingresa tu API Key de Gemini", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Inicializar estado
    if "analisis_generado" not in st.session_state:
        st.session_state.analisis_generado = False
    if "respuesta_normativa" not in st.session_state:
        st.session_state.respuesta_normativa = ""
    if "carta_generada" not in st.session_state:
        st.session_state.carta_generada = ""

    st.subheader("Describe tu caso")

    caso_usuario = st.text_area("Explica detalladamente la situación académica o administrativa")

    if st.button("Analizar conforme a normativa UNAL"):

        prompt = f"""
        Actúa como asistente normativo de la Universidad Nacional de Colombia.

        Responde únicamente con base en normativa institucional vigente.
        No inventes artículos específicos si no estás seguro.
        No agregues normas inexistentes.
        Si falta información, indícalo claramente.

        Analiza el siguiente caso:
        {caso_usuario}

        1. Determina si el trámite podría ser procedente.
        2. Explica bajo qué tipo de disposición normativa se enmarca.
        3. Indica condiciones y posibles plazos.
        4. No redactes carta aún.
        """

        respuesta = model.generate_content(prompt)
        st.session_state.respuesta_normativa = respuesta.text
        st.session_state.analisis_generado = True

    if st.session_state.analisis_generado:
        st.subheader("Análisis normativo")
        st.write(st.session_state.respuesta_normativa)

        st.markdown("---")
        st.subheader("¿Deseas generar solicitud formal?")

        nombre = st.text_input("Nombre completo")
        documento = st.text_input("Número de documento")
        programa = st.text_input("Programa académico")
        facultad = st.text_input("Facultad")
        sede = st.text_input("Sede")

        if st.button("Generar solicitud formal en PDF"):

            prompt_carta = f"""
            Redacta una solicitud formal dirigida a la Universidad Nacional de Colombia.

            Usa tono institucional.
            No inventes información.
            Basarse en el siguiente análisis normativo:
            {st.session_state.respuesta_normativa}

            Datos del estudiante:
            Nombre: {nombre}
            Documento: {documento}
            Programa: {programa}
            Facultad: {facultad}
            Sede: {sede}
            """

            respuesta_carta = model.generate_content(prompt_carta)
            carta = respuesta_carta.text
            st.session_state.carta_generada = carta

            st.subheader("Vista previa de la solicitud")
            st.write(carta)

            # Generar PDF
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
                file_name="Solicitud_UNAL.pdf",
                mime="application/pdf"
            )
