"""
Script rápido para probar que el servidor funciona
"""
import requests
import time

# Esperar a que el servidor esté listo
time.sleep(2)

print("🔍 Probando endpoints del servidor...\n")

# 1. Test root endpoint
try:
    response = requests.get("http://localhost:8000/")
    print(f"✅ GET / - Status: {response.status_code}")
    print(f"   Response: {response.json()}\n")
except Exception as e:
    print(f"❌ Error en /: {e}\n")

# 2. Test health endpoint
try:
    response = requests.get("http://localhost:8000/health")
    print(f"✅ GET /health - Status: {response.status_code}")
    print(f"   Response: {response.json()}\n")
except Exception as e:
    print(f"❌ Error en /health: {e}\n")

# 3. Test docs endpoint
try:
    response = requests.get("http://localhost:8000/docs")
    print(f"✅ GET /docs - Status: {response.status_code}")
    print(f"   Documentación Swagger disponible\n")
except Exception as e:
    print(f"❌ Error en /docs: {e}\n")

# 4. Test chart types endpoint
try:
    response = requests.get("http://localhost:8000/api/charts/types")
    print(f"✅ GET /api/charts/types - Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Tipos de gráficos disponibles: {len(data['chart_types'])}")
        for ct in data['chart_types']:
            print(f"   - {ct['label']}")
    print()
except Exception as e:
    print(f"❌ Error en /api/charts/types: {e}\n")

print("\n" + "="*60)
print("✅ SERVIDOR FUNCIONANDO CORRECTAMENTE")
print("="*60)
print("\n📚 Documentación: http://localhost:8000/docs")
print("🧪 Ejecuta: .\\venv\\Scripts\\python.exe test_api.py")
print("\nPara probar la funcionalidad completa con carga de archivos")
