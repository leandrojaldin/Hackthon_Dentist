from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from datetime import datetime

app = FastAPI()

# CORS configuration
origins = [
    "http://localhost:3000",  # Allow frontend origin
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
async def analyze_dental_image(image_file: UploadFile = File(...)):
    """
    Endpoint preparado para integrar el modelo de IA entrenado.
    Recibe una imagen dental, la procesa y retorna el diagnóstico.
    """
    # Aquí se integrará la lógica para cargar el modelo y hacer la predicción
    # Por ahora, solo simula la recepción y respuesta
    print(f"Received image file: {image_file.filename}, content type: {image_file.content_type}")

    # Simulación de respuesta del modelo IA
    mock_diagnosis = {
        "diagnosis_result": "Posible Caries",
        "confidence_score": 0.88,
        "recommendations": "Se recomienda visitar al odontólogo para una revisión profesional lo antes posible.",
        "highlighted_image_url": "/mock_images/caries_highlighted.png",
        "warning_message": "Esta detección es solo una herramienta de cribado inicial y no reemplaza un diagnóstico médico profesional."
    }

    # Aquí se podría guardar el resultado en la base de datos si se desea

    return JSONResponse(content=mock_diagnosis)

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

# To run this application:
# 1. Make sure you have uvicorn installed: pip install uvicorn
# 2. Run from your terminal: uvicorn main:app --reload --port 8000