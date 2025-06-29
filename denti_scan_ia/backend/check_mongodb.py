#!/usr/bin/env python3
"""
Script para verificar el estado de MongoDB
"""

import subprocess
import sys
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

def check_mongodb_installation():
    """Verificar si MongoDB está instalado"""
    print("🔍 Verificando instalación de MongoDB...")
    
    # Verificar si mongod está en el PATH
    try:
        result = subprocess.run(['mongod', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ MongoDB está instalado")
            print(f"   Versión: {result.stdout.strip()}")
            return True
        else:
            print("❌ MongoDB no está instalado o no está en el PATH")
            return False
    except FileNotFoundError:
        print("❌ MongoDB no está instalado o no está en el PATH")
        return False
    except subprocess.TimeoutExpired:
        print("⚠️ Timeout al verificar MongoDB")
        return False

def check_mongodb_service():
    """Verificar si el servicio de MongoDB está ejecutándose"""
    print("\n🔍 Verificando si MongoDB está ejecutándose...")
    
    # En Windows, verificar el servicio
    if os.name == 'nt':  # Windows
        try:
            result = subprocess.run(['sc', 'query', 'MongoDB'], 
                                  capture_output=True, text=True, timeout=10)
            if 'RUNNING' in result.stdout:
                print("✅ Servicio de MongoDB está ejecutándose")
                return True
            else:
                print("❌ Servicio de MongoDB no está ejecutándose")
                print("   Para iniciar MongoDB en Windows:")
                print("   1. Abre PowerShell como administrador")
                print("   2. Ejecuta: net start MongoDB")
                return False
        except FileNotFoundError:
            print("⚠️ No se pudo verificar el servicio de MongoDB")
            return False
    else:  # Linux/Mac
        try:
            result = subprocess.run(['systemctl', 'is-active', 'mongod'], 
                                  capture_output=True, text=True, timeout=10)
            if result.stdout.strip() == 'active':
                print("✅ Servicio de MongoDB está ejecutándose")
                return True
            else:
                print("❌ Servicio de MongoDB no está ejecutándose")
                print("   Para iniciar MongoDB en Linux/Mac:")
                print("   sudo systemctl start mongod")
                return False
        except FileNotFoundError:
            print("⚠️ No se pudo verificar el servicio de MongoDB")
            return False

def check_mongodb_connection():
    """Verificar conexión a MongoDB"""
    print("\n🔍 Verificando conexión a MongoDB...")
    
    try:
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        print("✅ Conexión exitosa a MongoDB")
        
        # Listar bases de datos
        databases = client.list_database_names()
        print(f"   Bases de datos disponibles: {databases}")
        
        # Verificar si existe nuestra base de datos
        db_name = "DentiScan-AI--Proyect"
        if db_name in databases:
            print(f"✅ Base de datos '{db_name}' existe")
            db = client[db_name]
            collections = db.list_collection_names()
            print(f"   Colecciones: {collections}")
        else:
            print(f"⚠️ Base de datos '{db_name}' no existe (se creará automáticamente)")
        
        client.close()
        return True
        
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        print(f"❌ No se pudo conectar a MongoDB: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def main():
    print("=" * 50)
    print("DIAGNÓSTICO DE MONGODB")
    print("=" * 50)
    
    # Verificar instalación
    installed = check_mongodb_installation()
    
    if installed:
        # Verificar servicio
        running = check_mongodb_service()
        
        if running:
            # Verificar conexión
            connected = check_mongodb_connection()
            
            if connected:
                print("\n🎉 MongoDB está funcionando correctamente!")
                print("   Tu aplicación debería poder guardar datos sin problemas.")
            else:
                print("\n⚠️ MongoDB está instalado y ejecutándose, pero hay problemas de conexión.")
                print("   Verifica que el puerto 27017 esté disponible.")
        else:
            print("\n⚠️ MongoDB está instalado pero no está ejecutándose.")
            print("   Inicia el servicio de MongoDB antes de usar la aplicación.")
    else:
        print("\n❌ MongoDB no está instalado.")
        print("   Para instalar MongoDB:")
        print("   - Windows: Descarga desde https://www.mongodb.com/try/download/community")
        print("   - Linux: sudo apt-get install mongodb-org")
        print("   - Mac: brew install mongodb-community")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main() 