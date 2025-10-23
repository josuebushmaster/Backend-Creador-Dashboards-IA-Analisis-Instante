"""
Test con logging detallado para identificar dónde se pierde el almacenamiento
"""
import requests
import json

print("\n🔍 DEBUG DEL ALMACENAMIENTO")
print("="*60)

def test_con_debug():
    # Agregar un endpoint temporal para debuggear
    print("\n1️⃣ Verificando almacenamiento después del upload...")
    
    # Upload
    with open("test_data/ventas_ejemplo.csv", "rb") as f:
        files = {"file": ("ventas.csv", f, "text/csv")}
        response = requests.post("http://localhost:8000/upload", files=files, timeout=30)
    
    if response.status_code != 200:
        print(f"❌ Upload falló: {response.status_code}")
        return
    
    data = response.json()
    id_archivo = data["id_archivo"]
    print(f"✅ Upload exitoso, ID: {id_archivo}")
    
    # Intentar acceder directamente al almacenamiento vía un endpoint debug
    print(f"\n2️⃣ Verificando si el archivo está en almacenamiento...")
    
    # Crear petición a chart-data con debug
    sugerencia = data["analisis"]["sugerencias_graficos"][0]
    
    print(f"📊 Sugerencia a probar:")
    print(f"   Título: {sugerencia.get('titulo')}")
    print(f"   Tipo: {sugerencia.get('tipo_grafico')}")
    print(f"   Ejes: {sugerencia['parametros']['eje_x']} vs {sugerencia['parametros']['eje_y']}")
    
    payload = {
        "id_archivo": id_archivo,
        "tipo_grafico": sugerencia["tipo_grafico"],
        "eje_x": sugerencia["parametros"]["eje_x"],
        "eje_y": sugerencia["parametros"]["eje_y"],
        "titulo": sugerencia.get("titulo"),
        "agregacion": "suma"
    }
    
    print(f"\n3️⃣ Payload para chart-data:")
    print(json.dumps(payload, indent=2))
    
    response = requests.post(
        "http://localhost:8000/chart-data",
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=10
    )
    
    print(f"\n4️⃣ Respuesta de chart-data:")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        chart_data = response.json()
        print(f"✅ Éxito! Datos: {len(chart_data.get('datos', []))} puntos")
    else:
        print(f"❌ Falló con status {response.status_code}")

if __name__ == "__main__":
    test_con_debug()