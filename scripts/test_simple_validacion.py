"""
Test simplificado para identificar el error específico
"""
import requests
import json

def test_simple():
    print("🔍 Test simplificado")
    
    # Upload
    with open("test_data/ventas_ejemplo.csv", "rb") as f:
        files = {"file": ("ventas.csv", f, "text/csv")}
        response = requests.post("http://localhost:8000/upload", files=files, timeout=30)
    
    if response.status_code != 200:
        print(f"❌ Upload falló: {response.status_code}")
        print(response.text)
        return
    
    data = response.json()
    print("✅ Upload exitoso")
    
    # Verificar estructura básica
    print(f"ID archivo: {data.get('id_archivo', 'N/A')}")
    print(f"Análisis presente: {bool(data.get('analisis'))}")
    
    analisis = data.get("analisis", {})
    sugerencias = analisis.get("sugerencias_graficos", [])
    print(f"Sugerencias: {len(sugerencias)}")
    
    if sugerencias:
        primera = sugerencias[0]
        print(f"Primera sugerencia: {primera.get('titulo', 'N/A')}")
        print(f"Tipo: {primera.get('tipo_grafico', 'N/A')}")
        print(f"Parámetros: {primera.get('parametros', {})}")
        
        # Chart-data
        payload = {
            "id_archivo": data["id_archivo"],
            "tipo_grafico": primera["tipo_grafico"],
            "eje_x": primera["parametros"]["eje_x"],
            "eje_y": primera["parametros"]["eje_y"],
            "titulo": primera.get("titulo"),
            "agregacion": "suma"
        }
        
        response = requests.post(
            "http://localhost:8000/chart-data",
            json=payload,
            timeout=10
        )
        
        print(f"Chart-data status: {response.status_code}")
        if response.status_code == 200:
            chart_data = response.json()
            print(f"Datos: {len(chart_data.get('datos', []))} puntos")
            print("✅ Backend validado completamente")
        else:
            print(f"Chart-data error: {response.text[:200]}")

if __name__ == "__main__":
    test_simple()