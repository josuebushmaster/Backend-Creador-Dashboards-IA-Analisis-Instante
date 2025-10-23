"""
Script de prueba para verificar endpoints del backend
"""
import requests
import json
from pathlib import Path

BASE_URL = "http://localhost:8000"

def test_upload():
    """Test del endpoint de upload"""
    print("\n" + "="*80)
    print("TEST 1: Upload de archivo CSV")
    print("="*80)
    
    csv_file = Path("test_data/ventas_ejemplo.csv")
    if not csv_file.exists():
        print(f"❌ Archivo no encontrado: {csv_file}")
        return None
    
    with open(csv_file, 'rb') as f:
        files = {'file': ('ventas_ejemplo.csv', f, 'text/csv')}
        response = requests.post(f"{BASE_URL}/upload", files=files)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Upload exitoso!")
        print(f"   ID Archivo: {data['id_archivo']}")
        print(f"   Filas: {data['metadatos']['filas']}")
        print(f"   Columnas: {data['metadatos']['columnas']}")
        print(f"   Sugerencias de gráficos: {len(data['analisis']['sugerencias_graficos'])}")
        
        if data['analisis']['sugerencias_graficos']:
            print(f"\n   Primera sugerencia:")
            primera = data['analisis']['sugerencias_graficos'][0]
            print(f"      - Título: {primera.get('titulo')}")
            print(f"      - Tipo: {primera.get('tipo_grafico')}")
            print(f"      - Parámetros: {primera.get('parametros')}")
        
        return data
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"   {response.text}")
        return None

def test_chart_data(upload_data):
    """Test del endpoint de chart-data"""
    print("\n" + "="*80)
    print("TEST 2: Generación de datos de gráfico")
    print("="*80)
    
    if not upload_data or not upload_data['analisis']['sugerencias_graficos']:
        print("❌ No hay datos de upload o sugerencias de gráficos")
        return False
    
    id_archivo = upload_data['id_archivo']
    sugerencia = upload_data['analisis']['sugerencias_graficos'][0]
    
    request_data = {
        "id_archivo": id_archivo,
        "tipo_grafico": sugerencia['tipo_grafico'],
        "eje_x": sugerencia['parametros']['eje_x'],
        "eje_y": sugerencia['parametros']['eje_y'],
        "agregacion": sugerencia['parametros'].get('agregacion', 'suma')
    }
    
    print(f"Request data:")
    print(f"  {json.dumps(request_data, indent=2, ensure_ascii=False)}")
    
    response = requests.post(
        f"{BASE_URL}/chart-data",
        json=request_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"\nStatus: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Chart data generado exitosamente!")
        print(f"   ID Gráfico: {data.get('id_grafico')}")
        print(f"   Tipo: {data.get('tipo_grafico')}")
        print(f"   Total de puntos: {len(data.get('datos', []))}")
        print(f"   Primeros 3 puntos:")
        for punto in data.get('datos', [])[:3]:
            print(f"      {punto}")
        return True
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"   {response.text}")
        return False

def main():
    print("\n🔍 INICIANDO PRUEBAS DE ENDPOINTS")
    print("="*80)
    
    # Test 1: Upload
    upload_result = test_upload()
    
    # Test 2: Chart data
    if upload_result:
        chart_result = test_chart_data(upload_result)
        
        if chart_result:
            print("\n" + "="*80)
            print("✅ ¡TODOS LOS TESTS PASARON EXITOSAMENTE!")
            print("="*80)
            print("\n📊 El backend está funcionando correctamente:")
            print("   1. Upload de archivos ✓")
            print("   2. Análisis con IA ✓")
            print("   3. Generación de datos de gráficos ✓")
            print("   4. Almacenamiento compartido entre routers ✓")
        else:
            print("\n" + "="*80)
            print("❌ FALLÓ: Chart data endpoint")
            print("="*80)
    else:
        print("\n" + "="*80)
        print("❌ FALLÓ: Upload endpoint")
        print("="*80)

if __name__ == "__main__":
    main()
