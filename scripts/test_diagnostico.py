"""
Test diagnóstico: verificar dónde se pierde el almacenamiento
"""
import requests
import json
import time

print("\n🔍 DIAGNÓSTICO DEL ALMACENAMIENTO")
print("="*60)

def test_con_logs():
    # Test 1: Upload
    print("\n1️⃣ Subiendo archivo...")
    with open("test_data/ventas_ejemplo.csv", "rb") as f:
        files = {"file": ("ventas.csv", f, "text/csv")}
        response = requests.post("http://localhost:8000/upload", files=files, timeout=30)
    
    if response.status_code != 200:
        print(f"❌ Upload falló: {response.status_code}")
        print(response.text)
        return
    
    data = response.json()
    id_archivo = data["id_archivo"]
    print(f"✅ Upload exitoso, ID: {id_archivo}")
    
    # Test 2: Inmediatamente intentar chart-data
    print(f"\n2️⃣ Intentando chart-data inmediatamente...")
    sugerencia = data["analisis"]["sugerencias_graficos"][0]
    
    payload = {
        "id_archivo": id_archivo,
        "tipo_grafico": sugerencia["tipo_grafico"],
        "eje_x": sugerencia["parametros"]["eje_x"],
        "eje_y": sugerencia["parametros"]["eje_y"],
        "titulo": sugerencia.get("titulo"),
        "agregacion": "suma"
    }
    
    response = requests.post(
        "http://localhost:8000/chart-data",
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=10
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ Chart-data exitoso!")
        chart_data = response.json()
        print(f"Datos: {len(chart_data.get('datos', []))} puntos")
    else:
        print(f"❌ Chart-data falló")
        print(f"Response: {response.text}")
    
    # Test 3: Esperar un poco e intentar de nuevo
    print(f"\n3️⃣ Esperando 2 segundos e intentando de nuevo...")
    time.sleep(2)
    
    response = requests.post(
        "http://localhost:8000/chart-data",
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=10
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ Chart-data exitoso después de esperar!")
    else:
        print(f"❌ Chart-data aún falla después de esperar")
        print(f"Response: {response.text}")

if __name__ == "__main__":
    test_con_logs()