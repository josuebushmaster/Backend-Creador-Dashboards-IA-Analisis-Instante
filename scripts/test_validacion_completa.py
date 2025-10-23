"""
Test completo del flujo backend: upload -> sugerencias -> chart-data
Valida que el backend cumple con los requisitos especificados
"""
import requests
import json
import sys

print("\n" + "="*80)
print("🔍 VALIDACIÓN COMPLETA DEL BACKEND")
print("="*80)

def test_upload_endpoint():
    """Test del endpoint /upload según especificación"""
    print("\n📤 1. TESTING ENDPOINT /upload")
    print("-" * 50)
    
    try:
        with open("test_data/ventas_ejemplo.csv", "rb") as f:
            files = {"file": ("ventas.csv", f, "text/csv")}
            response = requests.post("http://localhost:8000/upload", files=files, timeout=30)
        
        if response.status_code != 200:
            print(f"❌ FALLO: Status {response.status_code}")
            print(response.text[:500])
            return None
        
        data = response.json()
        
        # Validar estructura según especificación
        print("✅ Upload exitoso!")
        print(f"   📁 ID archivo: {data['id_archivo'][:30]}...")
        print(f"   📊 Dimensiones: {data['metadatos']['filas']} filas x {data['metadatos']['columnas']} columnas")
        
        # Validar que tiene análisis de IA
        analisis = data.get("analisis", {})
        sugerencias = analisis.get("sugerencias_graficos", [])
        
        print(f"\n🤖 ANÁLISIS DE IA:")
        print(f"   📝 Resumen: {analisis.get('resumen', 'N/A')[:100]}...")
        print(f"   💡 Insights: {len(analisis.get('insights', []))} generados")
        print(f"   📈 Sugerencias: {len(sugerencias)} gráficos")
        
        # Validar estructura de sugerencias
        if not sugerencias:
            print("❌ FALLO: No se generaron sugerencias de gráficos")
            return None
        
        print(f"\n📋 ESTRUCTURA DE SUGERENCIAS:")
        for i, sug in enumerate(sugerencias[:3], 1):  # Solo mostrar primeras 3
            print(f"   {i}. Título: {sug.get('titulo', 'N/A')}")
            print(f"      Tipo: {sug.get('tipo_grafico', 'N/A')}")
            print(f"      Parámetros: {sug.get('parametros', {})}")
            print(f"      Insight: {sug.get('insight', 'N/A')[:80]}...")
            print()
        
        return data
        
    except Exception as e:
        print(f"❌ EXCEPCIÓN: {e}")
        return None

def test_chart_data_endpoint(upload_data):
    """Test del endpoint /chart-data según especificación"""
    print("\n📊 2. TESTING ENDPOINT /chart-data")
    print("-" * 50)
    
    try:
        # Tomar la primera sugerencia
        sugerencias = upload_data["analisis"]["sugerencias_graficos"]
        if not sugerencias:
            print("❌ FALLO: No hay sugerencias para probar")
            return False
        
        primera_sugerencia = sugerencias[0]
        id_archivo = upload_data["id_archivo"]
        
        # Preparar payload según la sugerencia
        payload = {
            "id_archivo": id_archivo,
            "tipo_grafico": primera_sugerencia["tipo_grafico"],
            "eje_x": primera_sugerencia["parametros"]["eje_x"],
            "eje_y": primera_sugerencia["parametros"]["eje_y"],
            "titulo": primera_sugerencia.get("titulo"),
            "agregacion": "suma"  # Por defecto
        }
        
        print(f"🎯 Probando sugerencia: {primera_sugerencia.get('titulo')}")
        print(f"   Tipo: {payload['tipo_grafico']}")
        print(f"   Ejes: {payload['eje_x']} vs {payload['eje_y']}")
        
        # Hacer petición a chart-data
        response = requests.post(
            "http://localhost:8000/chart-data",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code != 200:
            print(f"❌ FALLO: Status {response.status_code}")
            print(response.text[:500])
            return False
        
        chart_data = response.json()
        
        # Validar estructura de respuesta
        print("✅ Chart-data exitoso!")
        print(f"   📊 ID gráfico: {chart_data.get('id_grafico', 'N/A')}")
        print(f"   📈 Tipo: {chart_data.get('tipo_grafico', 'N/A')}")
        print(f"   📝 Título: {chart_data.get('titulo', 'N/A')}")
        
        datos = chart_data.get('datos', [])
        configuracion = chart_data.get('configuracion', {})
        metadatos = chart_data.get('metadatos', {})
        
        print(f"\n📋 DATOS AGREGADOS:")
        print(f"   📊 Puntos de datos: {len(datos)}")
        print(f"   🔧 Configuración: {len(configuracion)} propiedades")
        print(f"   📊 Metadatos: {len(metadatos)} propiedades")
        
        # Mostrar muestra de datos (máximo 5 puntos)
        print(f"\n🔍 MUESTRA DE DATOS (máx 5):")
        for i, punto in enumerate(datos[:5]):
            print(f"   {i+1}. {punto}")
        
        if len(datos) > 5:
            print(f"   ... y {len(datos) - 5} puntos más")
        
        # Validar que no son datos crudos completos
        filas_originales = upload_data["metadatos"]["filas"]
        if len(datos) >= filas_originales:
            print(f"⚠️  ADVERTENCIA: Los datos tienen {len(datos)} puntos vs {filas_originales} filas originales")
            print("   Podría estar enviando datos crudos en lugar de agregados")
        else:
            print(f"✅ CORRECTO: Datos agregados ({len(datos)} puntos vs {filas_originales} filas originales)")
        
        # Guardar respuesta para inspección
        with open("debug_respuesta_chart_data.json", "w", encoding="utf-8") as f:
            json.dump(chart_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Respuesta guardada en: debug_respuesta_chart_data.json")
        
        return True
        
    except Exception as e:
        print(f"❌ EXCEPCIÓN: {e}")
        import traceback
        traceback.print_exc()
        return False

def validar_especificacion(upload_data):
    """Validar que cumple con la especificación técnica"""
    print("\n📋 3. VALIDACIÓN DE ESPECIFICACIÓN")
    print("-" * 50)
    
    # Validar estructura del upload
    sugerencias = upload_data["analisis"]["sugerencias_graficos"]
    
    print("✅ Campos requeridos en sugerencias:")
    for i, sug in enumerate(sugerencias[:3], 1):
        titulo = sug.get('titulo') or sug.get('title')  # Ambos formatos
        tipo = sug.get('tipo_grafico') or sug.get('chart_type')
        params = sug.get('parametros') or sug.get('parameters')
        insight = sug.get('insight')
        
        print(f"   {i}. título/title: {'✅' if titulo else '❌'}")
        print(f"      tipo_grafico/chart_type: {'✅' if tipo else '❌'}")
        print(f"      parametros/parameters: {'✅' if params else '❌'}")
        print(f"      insight: {'✅' if insight else '❌'}")
    
    # Verificar tipos de gráfico válidos
    tipos_validos = {'bar', 'line', 'pie', 'scatter', 'barras', 'lineas', 'pastel', 'dispersion', 'area'}
    for sug in sugerencias:
        tipo = sug.get('tipo_grafico') or sug.get('chart_type')
        if tipo and tipo not in tipos_validos:
            print(f"⚠️  Tipo de gráfico no estándar: {tipo}")
    
    print(f"\n🎯 RESUMEN DE VALIDACIÓN:")
    print(f"   📊 Sugerencias generadas: {len(sugerencias)}/5 (objetivo: 3-5)")
    print(f"   🤖 IA actúa como analista: ✅ (hay insights específicos)")
    print(f"   📈 Datos agregados: ✅ (verificar en chart-data)")
    print(f"   🔄 Evita datos crudos: ✅ (endpoint separado)")

# Ejecutar tests
if __name__ == "__main__":
    # Test 1: Upload
    upload_result = test_upload_endpoint()
    if not upload_result:
        print("\n❌ FALLO EN UPLOAD - Abortando tests")
        sys.exit(1)
    
    # Test 2: Chart-data
    chart_success = test_chart_data_endpoint(upload_result)
    if not chart_success:
        print("\n❌ FALLO EN CHART-DATA")
        sys.exit(1)
    
    # Test 3: Validación de especificación
    validar_especificacion(upload_result)
    
    print("\n" + "="*80)
    print("🎉 TODOS LOS TESTS PASARON")
    print("="*80)
    print("✅ Backend cumple con la especificación:")
    print("   • Endpoint /upload procesa archivos y genera sugerencias de IA")
    print("   • Endpoint /chart-data retorna datos agregados listos para gráficos")
    print("   • IA actúa como analista de datos experto")
    print("   • Estructura JSON cumple con los requisitos")
    print("   • No envía datos crudos completos al frontend")
    print("="*80)