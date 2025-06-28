from pymongo import MongoClient
from PIL import Image
from io import BytesIO
import base64

def mostrar_imagen(nombre_imagen,
                   uri='mongodb://localhost:27017/',
                   db_name='DentiScan-AI--Proyect',
                   coleccion_nombre='imagenes'):
    client = MongoClient(uri)
    db = client[db_name]
    coleccion = db[coleccion_nombre]

    documento = coleccion.find_one({"nombre": nombre_imagen})

    if documento:
        print(f"👤 Usuario: {documento.get('usuario')}")
        print(f"🩺 Diagnóstico: {documento.get('diagnostico')}")
        print(f"📌 Recomendación: {documento.get('recomendacion')}")
        print(f"📅 Fecha: {documento.get('fecha_subida')}")

        imagen_base64 = documento['imagen']
        imagen_bytes = base64.b64decode(imagen_base64)
        imagen = Image.open(BytesIO(imagen_bytes))
        imagen.save('imagen_recuperada.jpg')
        imagen.show()
        print("✅ Imagen recuperada y mostrada.")
    else:
        print("⚠️ Imagen no encontrada.")

if __name__ == "__main__":
    mostrar_imagen("juan123_20250628_220000")  # cambia por el nombre exacto
