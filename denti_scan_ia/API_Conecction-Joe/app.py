import streamlit as st
from PIL import Image
from datetime import datetime
import requests

st.title("🦷 DentiScan IA - Demo Web")

usuario = st.text_input("👤 Nombre completo:")
correo = st.text_input("📧 Correo electrónico:")
fecha_nacimiento = st.text_input("📅 Fecha de nacimiento (dd/mm/aaaa):")
uploaded_file = st.file_uploader("📷 Sube una imagen de tu boca", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file and usuario and correo and fecha_nacimiento:
    imagen = Image.open(uploaded_file)
    imagen.save("temp.jpg")
    # Separar nombre y apellido si es posible
    partes_nombre = usuario.strip().split()
    nombre = partes_nombre[0] if len(partes_nombre) > 0 else ""
    apellido = " ".join(partes_nombre[1:]) if len(partes_nombre) > 1 else ""
    with open("temp.jpg", "rb") as img_file:
        files = {"imagen": img_file}
        data = {
            "nombre": nombre,
            "apellido": apellido,
            "email": correo,
            "fecha_nacimiento": fecha_nacimiento
        }
        try:
            response = requests.post("http://localhost:8000/registro", data=data, files=files)
            if response.status_code == 200:
                res = response.json()
                diagnostico = "Registro exitoso"
                recomendacion = f"Usuario guardado: {res.get('nombre', '')} {res.get('apellido', '')}"
            else:
                diagnostico = "Error al registrar usuario"
                recomendacion = "Intenta nuevamente más tarde."
        except Exception as e:
            diagnostico = "No se pudo conectar con la API"
            recomendacion = str(e)

    st.image(imagen, caption="✅ Imagen cargada", use_column_width=True)
    st.markdown(f"**🩺 Diagnóstico:** {diagnostico}")
    st.markdown(f"**📌 Recomendación:** {recomendacion}")
