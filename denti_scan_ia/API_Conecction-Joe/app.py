import streamlit as st
from PIL import Image
from datetime import datetime
from mongo_utils import guardar_imagen_dentiscan_local
import requests

st.title("🦷 DentiScan IA - Demo Web")

usuario = st.text_input("👤 Nombre de usuario:")
uploaded_file = st.file_uploader("📷 Sube una imagen de tu boca", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file and usuario:
    imagen = Image.open(uploaded_file)
    imagen.save("temp.jpg")
    # Llamada a la API
    with open("temp.jpg", "rb") as img_file:
        files = {"image_file": img_file}
        try:
            response = requests.post("http://localhost:8000/analyze_dental_image", files=files)
            if response.status_code == 200:
                data = response.json()
                diagnostico = data.get("diagnosis_result", "Sin diagnóstico")
                recomendacion = data.get("recommendations", "Sin recomendación")
            else:
                diagnostico = "Error al analizar la imagen"
                recomendacion = "Intenta nuevamente más tarde."
        except Exception as e:
            diagnostico = "No se pudo conectar con la API"
            recomendacion = str(e)

    st.image(imagen, caption="✅ Imagen cargada", use_column_width=True)
    st.markdown(f"**🩺 Diagnóstico:** {diagnostico}")
    st.markdown(f"**📌 Recomendación:** {recomendacion}")

    if st.button("💾 Guardar diagnóstico"):
        nombre_img = f"{usuario}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        guardar_imagen_dentiscan_local("temp.jpg", nombre_img, usuario, diagnostico, recomendacion)
        st.success("🎉 Guardado correctamente en MongoDB local.")
