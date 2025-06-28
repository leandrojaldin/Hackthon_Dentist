# DentiScan IA

## Estructura del Proyecto

```
denti_scan_ia/
├── backend/
│   ├── venv/
│   ├── main.py
│   ├── requirements.txt
│   ├── database_config.py
│   ├── ia_integration.py
├── frontend/
│   ├── public/
│   │   └── mock_images/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── index.css
│   │   ├── main.jsx
│   │   └── components/
│   │       ├── FileUpload.jsx
│   │       └── ResultDisplay.jsx
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── package.json
│   ├── vite.config.js
└── README.md
```

## Instrucciones básicas

### Backend
1. Crear y activar un entorno virtual en `backend/venv`.
2. Instalar dependencias: `pip install -r requirements.txt`
3. Ejecutar el backend: `uvicorn main:app --reload`

### Frontend
1. Instalar dependencias: `npm install`
2. Ejecutar el frontend: `npm run dev`

