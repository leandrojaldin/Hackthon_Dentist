from pymongo import MongoClient
from datetime import datetime, timezone
import base64
from PIL import Image
import os

def guardar_imagen_dentiscan_local(ruta_imagen, nombre_imagen, usuario, diagnostico, recomendacion,
                                    uri='mongodb://localhost:27017/',
                                    db_name='DentiScan-AI--Proyect',
                                    coleccion_nombre='imagenes'):
    cliente = MongoClient(uri)
    db = cliente[db_name]
    coleccion = db[coleccion_nombre]

    with Image.open(ruta_imagen) as im:
        im = im.convert("RGB")
        temp_path = "temp_convertida.jpg"
        im.save(temp_path, format="JPEG")

    with open(temp_path, 'rb') as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode('utf-8')

    os.remove(temp_path)

    documento = {
        "nombre": nombre_imagen,
        "imagen": encoded_string,
        "usuario": usuario,
        "diagnostico": diagnostico,
        "recomendacion": recomendacion,
        "fecha_subida": datetime.now(timezone.utc)
    }

    coleccion.insert_one(documento)
    print("✅ Imagen convertida a JPG y guardada en MongoDB local.")
