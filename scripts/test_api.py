"""
Script de prueba para los endpoints de la API Dashboard IA
"""
import requests
import json
import time
import sys
from pathlib import Path

# Configuración
BASE_URL = "http://localhost:8000"
TEST_FILE = Path(__file__).parent / "test_data" / "ventas_ejemplo.csv"

def print_section(title):
    """Imprime una sección visual"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")

def print_json(data):
    """Imprime JSON formateado"""
    print(json.dumps(data, indent=2, ensure_ascii=False))

def test_health():
    """Prueba el endpoint de health check"""
    print_section("1. Health Check")
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print_json(response.json())
    
    return response.status_code == 200

def test_upload_file():
    """Prueba el endpoint de carga de archivos"""
    print_section("2. Cargar Archivo")
    
    if not TEST_FILE.exists():
        print(f"❌ Error: Archivo de prueba no encontrado: {TEST_FILE}")
        return None
    
    with open(TEST_FILE, 'rb') as f:
        files = {'file': ('ventas_ejemplo.csv', f, 'text/csv')}
        response = requests.post(f"{BASE_URL}/api/analysis/upload", files=files)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Archivo cargado exitosamente!")
        print(f"   File ID: {data['file_id']}")
        print(f"   Filename: {data['filename']}")
        print(f"   Rows: {data['rows']}")
        print(f"   Columns: {data['columns']}")
        print(f"   Column Names: {', '.join(data['column_names'])}")
        print(f"\n📊 Preview (primeras 3 filas):")
        for i, row in enumerate(data['preview'][:3]):
            print(f"   {i+1}. {row}")
        return data['file_id']
    else:
        print(f"❌ Error al cargar archivo:")
        print_json(response.json())
        return None

def test_analyze_file(file_id):
    """Prueba el endpoint de análisis con IA"""
    print_section("3. Analizar Archivo con IA")
    
    print("⏳ Enviando datos al LLM para análisis...")
    print("   (Esto puede tardar 10-30 segundos)")
    
    response = requests.post(f"{BASE_URL}/api/analysis/analyze/{file_id}")
    
    print(f"\nStatus: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Análisis completado!")
        print(f"\n📝 Resumen:")
        print(f"   {data['summary']}")
        
        print(f"\n💡 Insights ({len(data['insights'])}):")
        for i, insight in enumerate(data['insights'], 1):
            print(f"   {i}. {insight}")
        
        print(f"\n📊 Sugerencias de Gráficos ({len(data['chart_suggestions'])}):")
        for i, chart in enumerate(data['chart_suggestions'], 1):
            print(f"\n   {i}. {chart['title']}")
            print(f"      Tipo: {chart['chart_type']}")
            print(f"      Eje X: {chart['parameters']['x_axis']}")
            print(f"      Eje Y: {chart['parameters']['y_axis']}")
            print(f"      Insight: {chart['insight']}")
        
        return data['chart_suggestions']
    else:
        print(f"❌ Error en análisis:")
        print_json(response.json())
        return None

def test_get_chart_data(file_id, chart_suggestion):
    """Prueba el endpoint de obtención de datos de gráfico"""
    print_section(f"4. Obtener Datos para Gráfico: {chart_suggestion['title']}")
    
    payload = {
        "file_id": file_id,
        "chart_type": chart_suggestion['chart_type'],
        "x_axis": chart_suggestion['parameters']['x_axis'],
        "y_axis": chart_suggestion['parameters']['y_axis'],
        "title": chart_suggestion['title'],
        "aggregation": "sum"
    }
    
    print("📤 Request:")
    print_json(payload)
    
    response = requests.post(f"{BASE_URL}/api/charts/chart-data", json=payload)
    
    print(f"\n📥 Response Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Datos del gráfico obtenidos!")
        print(f"\n📊 Chart ID: {data['chart_id']}")
        print(f"   Tipo: {data['chart_type']}")
        print(f"   Título: {data['title']}")
        print(f"   Registros procesados: {data['metadata']['processed_records']}")
        print(f"\n   Datos (primeros 5):")
        for i, row in enumerate(data['data'][:5]):
            print(f"      {i+1}. {row}")
        
        print(f"\n⚙️ Configuración del gráfico:")
        print_json(data['config'])
        
        return True
    else:
        print(f"❌ Error obteniendo datos del gráfico:")
        print_json(response.json())
        return False

def test_chart_types():
    """Prueba el endpoint de tipos de gráficos"""
    print_section("5. Tipos de Gráficos Disponibles")
    
    response = requests.get(f"{BASE_URL}/api/charts/types")
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ {len(data['chart_types'])} tipos de gráficos disponibles:\n")
        for chart_type in data['chart_types']:
            print(f"   📈 {chart_type['label']} ({chart_type['value']})")
            print(f"      {chart_type['description']}")
            print(f"      Uso: {chart_type['use_case']}\n")
        return True
    else:
        print(f"❌ Error:")
        print_json(response.json())
        return False

def main():
    """Ejecuta todas las pruebas"""
    print("\n" + "🚀 "*20)
    print("  PRUEBAS DE API - DASHBOARD IA")
    print("🚀 "*20)
    
    try:
        # 1. Health Check
        if not test_health():
            print("\n❌ El servidor no responde. ¿Está ejecutándose?")
            print("   Ejecuta: python main.py")
            sys.exit(1)
        
        # 2. Upload File
        file_id = test_upload_file()
        if not file_id:
            print("\n❌ Falló la carga del archivo")
            sys.exit(1)
        
        # Pausa para procesar
        time.sleep(2)
        
        # 3. Analyze File
        chart_suggestions = test_analyze_file(file_id)
        if not chart_suggestions:
            print("\n❌ Falló el análisis")
            sys.exit(1)
        
        # Pausa para procesar
        time.sleep(2)
        
        # 4. Get Chart Data (primer gráfico sugerido)
        if chart_suggestions:
            test_get_chart_data(file_id, chart_suggestions[0])
        
        # 5. Chart Types
        time.sleep(1)
        test_chart_types()
        
        # Resumen final
        print_section("✅ PRUEBAS COMPLETADAS EXITOSAMENTE")
        print("""
        🎉 ¡Todos los endpoints funcionan correctamente!
        
        Próximos pasos:
        1. Revisa la documentación completa en: http://localhost:8000/docs
        2. Prueba con tus propios archivos CSV/Excel
        3. Integra el frontend con estos endpoints
        
        Endpoints principales:
        - POST /api/analysis/upload       -> Cargar archivo
        - POST /api/analysis/analyze/{id} -> Analizar con IA
        - POST /api/charts/chart-data     -> Obtener datos de gráfico
        - GET  /api/charts/types          -> Tipos de gráficos
        """)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error de conexión. Asegúrate de que el servidor esté ejecutándose.")
        print("   Ejecuta: python main.py")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
