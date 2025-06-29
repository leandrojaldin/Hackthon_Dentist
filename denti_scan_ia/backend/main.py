from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from datetime import datetime
import os

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

# MongoDB connection (skeleton)
MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB_NAME = "dentiscan_db"

try:
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB_NAME]
    dental_scans_collection = db["dental_scans"]
    print("Connected to MongoDB")
except Exception as e:
    print(f"Could not connect to MongoDB: {e}")
    client = None # Ensure client is None if connection fails

@app.get("/health")
async def health_check():
    return {"status": "ok"}

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
        print(f"Recibiendo datos - Nombre: {name}, Email: {email}, Fecha de Nacimiento: {birthDate}")
        print(f"Archivo recibido: {dentalImage.filename}, tipo: {dentalImage.content_type}")

        # Leer el contenido de la imagen
        image_data = await dentalImage.read()
        
        # Crear un nombre único para el archivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name.replace(' ', '_')}_{timestamp}_{dentalImage.filename}"
        
        # Guardar la imagen en el sistema de archivos (opcional)
        os.makedirs("uploads", exist_ok=True)
        file_path = os.path.join("uploads", filename)
        with open(file_path, "wb") as f:
            f.write(image_data)

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

        # Insertar en MongoDB
        if client is not None:
            result = dental_scans_collection.insert_one(patient_data)
            print(f"Datos guardados en MongoDB con ID: {result.inserted_id}")
        else:
            print("Advertencia: No se pudo conectar a MongoDB")

        # Simular respuesta del modelo de IA
        response_data = {
            "status": "success",
            "message": "Imagen procesada correctamente",
            "data": {
                "patient_name": name,
                "analysis_id": str(result.inserted_id) if client else "none",
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
        print(f"Error al procesar la solicitud: {str(e)}")
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
    image_bytes = await imagen.read()
    image_filename = f"{nombre}{apellido}{datetime.now().strftime('%Y%m%d_%H%M%S')}_{imagen.filename}"
    with open(image_filename, "wb") as f:
        f.write(image_bytes)

    if client:
        dental_scans_collection.insert_one({
            "nombre": nombre,
            "apellido": apellido,
            "email": email,
            "fecha_nacimiento": fecha_nacimiento,
            "image_filename": image_filename,
            "fecha": datetime.now()
        })
        return {"status": "ok", "nombre": nombre, "apellido": apellido, "email": email, "fecha_nacimiento": fecha_nacimiento, "filename": image_filename}
    else:
        return {"status": "error", "message": "No se pudo conectar a MongoDB"}