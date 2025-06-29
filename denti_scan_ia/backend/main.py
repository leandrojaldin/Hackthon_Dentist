from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from datetime import datetime
import os
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS configuration
origins = [
    "http://localhost:5173",  # Frontend development server
    "http://localhost:3000",  # Otro puerto común para desarrollo
    "http://127.0.0.1:5173",  # Alternativa a localhost
    "http://127.0.0.1:3000"   # Alternativa a localhost
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# MongoDB connection
MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB_NAME = "DentiScan-AI--Proyect"

client = None
db = None
dental_scans_collection = None

def connect_to_mongodb():
    global client, db, dental_scans_collection
    try:
        logger.info("Intentando conectar a MongoDB...")
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        # Verificar conexión
        client.admin.command('ping')
        db = client[MONGO_DB_NAME]
        dental_scans_collection = db["imagenes"]
        logger.info("✅ Conectado exitosamente a MongoDB")
        return True
    except Exception as e:
        logger.error(f"❌ Error conectando a MongoDB: {e}")
        client = None
        db = None
        dental_scans_collection = None
        return False

# Intentar conectar al inicio
connect_to_mongodb()

@app.get("/health")
async def health_check():
    mongodb_status = "connected" if client else "disconnected"
    return {
        "status": "ok", 
        "mongodb": mongodb_status,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/analyze_dental_image")
async def analyze_dental_image(
    dentalImage: UploadFile = File(...),
    name: str = Form(...),
    email: str = Form(...),
    birthDate: str = Form(...)
):
    """
    Endpoint para procesar imágenes dentales y guardar los datos del paciente.
    """
    try:
        logger.info(f"📝 Recibiendo datos - Nombre: {name}, Email: {email}, Fecha de Nacimiento: {birthDate}")
        logger.info(f"📁 Archivo recibido: {dentalImage.filename}, tipo: {dentalImage.content_type}")

        # Leer el contenido de la imagen
        image_data = await dentalImage.read()
        
        # Crear un nombre único para el archivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name.replace(' ', '_')}_{timestamp}_{dentalImage.filename}"
        
        # Guardar la imagen en el sistema de archivos
        os.makedirs("uploads", exist_ok=True)
        file_path = os.path.join("uploads", filename)
        with open(file_path, "wb") as f:
            f.write(image_data)
        logger.info(f"💾 Imagen guardada en: {file_path}")

        # Crear documento para MongoDB
        patient_data = {
            "name": name,
            "email": email,
            "birth_date": birthDate,
            "image_filename": filename,
            "file_path": file_path,
            "upload_date": datetime.now(),
            "status": "processed"
        }

        # Intentar insertar en MongoDB
        mongo_result = None
        if client is not None and dental_scans_collection is not None:
            try:
                result = dental_scans_collection.insert_one(patient_data)
                mongo_result = str(result.inserted_id)
                logger.info(f"✅ Datos guardados en MongoDB con ID: {mongo_result}")
            except Exception as mongo_error:
                logger.error(f"❌ Error al guardar en MongoDB: {mongo_error}")
                # Intentar reconectar
                if connect_to_mongodb():
                    try:
                        result = dental_scans_collection.insert_one(patient_data)
                        mongo_result = str(result.inserted_id)
                        logger.info(f"✅ Datos guardados en MongoDB después de reconectar: {mongo_result}")
                    except Exception as retry_error:
                        logger.error(f"❌ Error al guardar después de reconectar: {retry_error}")
        else:
            logger.warning("⚠️ No se pudo conectar a MongoDB - los datos no se guardaron")

        # Simular respuesta del modelo de IA
        response_data = {
            "status": "success",
            "message": "Imagen procesada correctamente",
            "data": {
                "patient_name": name,
                "analysis_id": mongo_result if mongo_result else "none",
                "mongodb_status": "connected" if mongo_result else "disconnected",
                "diagnosis": "Caries detectada",
                "confidence": 0.92,
                "recommendations": [
                    "Visita a un odontólogo en los próximos 7 días",
                    "Realiza una limpieza dental profesional"
                ]
            }
        }

        return JSONResponse(content=response_data)

    except Exception as e:
        logger.error(f"❌ Error al procesar la solicitud: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "DentiScan IA Backend funcionando"}

@app.post("/registro")
async def registro(
    nombre: str = Form(...),
    apellido: str = Form(...),
    email: str = Form(...),
    fecha_nacimiento: str = Form(...),
    imagen: UploadFile = File(...)
):
    try:
        logger.info(f"📝 Registro - Nombre: {nombre} {apellido}, Email: {email}, Fecha: {fecha_nacimiento}")
        
        image_bytes = await imagen.read()
        image_filename = f"{nombre}{apellido}{datetime.now().strftime('%Y%m%d_%H%M%S')}_{imagen.filename}"
        
        # Guardar la imagen en el sistema de archivos
        os.makedirs("uploads", exist_ok=True)
        file_path = os.path.join("uploads", image_filename)
        with open(file_path, "wb") as f:
            f.write(image_bytes)
        logger.info(f"💾 Imagen guardada en: {file_path}")

        # Crear documento para MongoDB
        patient_data = {
            "nombre": nombre,
            "apellido": apellido,
            "email": email,
            "fecha_nacimiento": fecha_nacimiento,
            "image_filename": image_filename,
            "file_path": file_path,
            "fecha": datetime.now(),
            "status": "registered"
        }

        # Intentar insertar en MongoDB
        mongo_result = None
        if client is not None and dental_scans_collection is not None:
            try:
                result = dental_scans_collection.insert_one(patient_data)
                mongo_result = str(result.inserted_id)
                logger.info(f"✅ Registro guardado en MongoDB con ID: {mongo_result}")
            except Exception as mongo_error:
                logger.error(f"❌ Error al guardar registro en MongoDB: {mongo_error}")
                # Intentar reconectar
                if connect_to_mongodb():
                    try:
                        result = dental_scans_collection.insert_one(patient_data)
                        mongo_result = str(result.inserted_id)
                        logger.info(f"✅ Registro guardado en MongoDB después de reconectar: {mongo_result}")
                    except Exception as retry_error:
                        logger.error(f"❌ Error al guardar registro después de reconectar: {retry_error}")
        else:
            logger.warning("⚠️ No se pudo conectar a MongoDB - el registro no se guardó")

        if mongo_result:
            return {
                "status": "ok", 
                "nombre": nombre, 
                "apellido": apellido, 
                "email": email, 
                "fecha_nacimiento": fecha_nacimiento, 
                "filename": image_filename,
                "mongodb_id": mongo_result
            }
        else:
            return {
                "status": "error", 
                "message": "No se pudo conectar a MongoDB",
                "nombre": nombre, 
                "apellido": apellido, 
                "email": email, 
                "fecha_nacimiento": fecha_nacimiento, 
                "filename": image_filename
            }
            
    except Exception as e:
        logger.error(f"❌ Error en el registro: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))