"""
Test simple y directo de los endpoints
"""
import requests
import time

print("\n🔍 TEST SIMPLE DE ENDPOINTS")
print("="*60)

# Esperar un segundo para asegurar que el servidor está listo
time.sleep(1)

# Test 1: Health check
print("\n1️⃣  Verificando servidor...")
try:
    r = requests.get("http://localhost:8000/docs", timeout=5)
    if r.status_code == 200:
        print("   ✅ Servidor activo y respondiendo")
    else:
        print(f"   ⚠️  Status: {r.status_code}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    exit(1)

# Test 2: Upload
print("\n2️⃣  Test de upload...")
try:
    with open("test_data/ventas_ejemplo.csv", "rb") as f:
        files = {"file": ("ventas.csv", f, "text/csv")}
        r = requests.post("http://localhost:8000/upload", files=files, timeout=30)
    
    print(f"   Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        print(f"   ✅ Upload exitoso!")
        print(f"   📁 ID: {data['id_archivo'][:20]}...")
        print(f"   📊 Filas: {data['metadatos']['filas']}")
        print(f"   📈 Sugerencias: {len(data['analisis']['sugerencias_graficos'])}")
        
        # Guardar para siguiente test
        id_archivo = data["id_archivo"]
        sugerencia = data["analisis"]["sugerencias_graficos"][0]
    else:
        print(f"   ❌ Error: {r.text[:200]}")
        exit(1)
except Exception as e:
    print(f"   ❌ Excepción: {e}")
    exit(1)

# Test 3: Chart data
print("\n3️⃣  Test de chart-data...")
try:
    payload = {
        "id_archivo": id_archivo,
        "tipo_grafico": sugerencia["tipo_grafico"],
        "eje_x": sugerencia["parametros"]["eje_x"],
        "eje_y": sugerencia["parametros"]["eje_y"],
        "agregacion": sugerencia["parametros"].get("agregacion", "suma")
    }
    
    r = requests.post(
        "http://localhost:8000/chart-data",
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=10
    )
    
    print(f"   Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        print(f"   ✅ Chart data generado!")
        print(f"   📊 Tipo: {data['tipo_grafico']}")
        print(f"   📈 Puntos: {len(data['datos'])}")
    elif r.status_code == 404:
        print(f"   ❌ ERROR 404: Endpoint no encontrado o datos no disponibles")
        print(f"   Response: {r.text[:200]}")
        exit(1)
    else:
        print(f"   ❌ Error {r.status_code}: {r.text[:200]}")
        exit(1)
except Exception as e:
    print(f"   ❌ Excepción: {e}")
    exit(1)

print("\n" + "="*60)
print("✅ ¡TODOS LOS TESTS PASARON!")
print("="*60)
print("\n📋 RESUMEN:")
print("   • Servidor funcionando ✓")
print("   • Upload de archivos ✓")
print("   • Análisis con IA ✓")
print("   • Generación de gráficos ✓")
print("   • Almacenamiento compartido ✓")
print()
