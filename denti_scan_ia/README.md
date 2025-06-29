# 🦷 DentiScan IA

Sistema de análisis dental basado en IA para la detección temprana de problemas bucodentales a través de imágenes.

## 🚀 Características Principales

- 📸 Carga de imágenes dentales
- 🤖 Análisis automático de imágenes mediante IA
- 💾 Almacenamiento seguro de registros médicos
- 📊 Visualización de resultados detallados
- 🔄 Interfaz de usuario intuitiva y responsiva

## 🏗️ Estructura del Proyecto

```
denti_scan_ia/
├── backend/                  # Código del servidor
│   ├── uploads/             # Imágenes subidas por los usuarios
│   ├── main.py              # Aplicación principal de FastAPI
│   ├── requirements.txt     # Dependencias de Python
│   └── .env                # Variables de entorno (crear manualmente)
├── frontend/               # Aplicación React
│   ├── public/             # Archivos estáticos
│   ├── src/                # Código fuente
│   │   ├── components/     # Componentes de React
│   │   ├── pages/          # Páginas de la aplicación
│   │   ├── App.jsx         # Componente principal
│   │   └── main.jsx        # Punto de entrada
│   ├── package.json        # Dependencias de Node.js
│   └── vite.config.js      # Configuración de Vite
└── README.md               # Este archivo
```

## 🛠️ Requisitos Previos

- Python 3.8+
- Node.js 16+
- MongoDB 6.0+
- npm o yarn

## 🚀 Instalación y Configuración

### 1. Configuración del Backend

```bash
# Navegar al directorio del backend
cd backend

# Crear y activar entorno virtual (Windows)
python -m venv venv
.\venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno (crear archivo .env)
echo "MONGO_URI=mongodb://localhost:27017/" > .env
echo "MONGO_DB_NAME=dentiscan_db" >> .env

# Iniciar servidor de desarrollo
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Configuración del Frontend

```bash
# Navegar al directorio del frontend
cd frontend

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev
```

### 3. Configuración de MongoDB

1. Descargar e instalar MongoDB Community Server desde [aquí](https://www.mongodb.com/try/download/community)
2. Iniciar el servicio de MongoDB:
   - Windows: Buscar "Services" y asegurarse que el servicio "MongoDB" esté en ejecución
   - macOS: `brew services start mongodb-community`
   - Linux: `sudo systemctl start mongod`

## 📚 API Endpoints

### Análisis de Imagen Dental
```
POST /analyze_dental_image
Content-Type: multipart/form-data

Parámetros:
- name: string (requerido)
- email: string (requerido)
- birthDate: string (formato YYYY-MM-DD)
- dentalImage: file (imagen)
```

### Verificar Estado del Servicio
```
GET /health
```

## 🌐 Despliegue

### Backend (Producción)
```bash
# Instalar gunicorn
pip install gunicorn

# Ejecutar con gunicorn (producción)
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend (Producción)
```bash
# Construir para producción
npm run build

# Servir archivos estáticos
npm install -g serve
serve -s dist
```

## 🐛 Solución de Problemas

### Error de Conexión a MongoDB
- Verificar que el servicio de MongoDB esté en ejecución
- Comprobar que la URL de conexión sea correcta en el archivo `.env`

### Problemas de CORS
- Asegurarse que los orígenes permitidos en `main.py` incluyan la URL del frontend
- Verificar que las credenciales CORS estén configuradas correctamente

### Errores de Dependencias
- Asegurarse de tener todas las dependencias instaladas
- Reinstalar dependencias si es necesario: `pip install -r requirements.txt`

## 🤝 Contribución

1. Hacer fork del repositorio
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Hacer commit de tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Hacer push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## ✉️ Contacto

¿Preguntas o comentarios? Por favor abre un issue en el repositorio.

