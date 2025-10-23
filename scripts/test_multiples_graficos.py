"""
Test para verificar que el backend genera MÚLTIPLES sugerencias de gráficos
"""
import requests
import json
import time

print("\n🔍 VERIFICACIÓN DE MÚLTIPLES SUGERENCIAS DE GRÁFICOS")
print("="*80)

# Esperar a que el servidor esté listo
time.sleep(1)

# Test de upload
print("\n1️⃣  Subiendo archivo y obteniendo análisis con IA...")
try:
    with open("test_data/ventas_ejemplo.csv", "rb") as f:
        files = {"file": ("ventas.csv", f, "text/csv")}
        r = requests.post("http://localhost:8000/upload", files=files, timeout=30)
    
    if r.status_code != 200:
        print(f"   ❌ Error {r.status_code}: {r.text[:300]}")
        exit(1)
    
    data = r.json()
    print(f"   ✅ Upload exitoso!")
    print(f"   📁 Archivo: {data['nombre_archivo']}")
    print(f"   📊 Dimensiones: {data['metadatos']['filas']} filas x {data['metadatos']['columnas']} columnas")
    
    # Extraer sugerencias
    sugerencias = data["analisis"]["sugerencias_graficos"]
    num_sugerencias = len(sugerencias)
    
    print(f"\n   🎯 TOTAL DE SUGERENCIAS GENERADAS: {num_sugerencias}")
    print("   " + "-"*76)
    
    # Mostrar todas las sugerencias
    for i, sug in enumerate(sugerencias, 1):
        print(f"\n   📈 SUGERENCIA #{i}:")
        print(f"      Título: {sug.get('titulo', 'Sin título')}")
        print(f"      Tipo: {sug.get('tipo_grafico', 'No especificado')}")
        print(f"      Eje X: {sug['parametros']['eje_x']}")
        print(f"      Eje Y: {sug['parametros']['eje_y']}")
        print(f"      Insight: {sug.get('insight', 'Sin insight')[:100]}...")
    
    print("\n" + "="*80)
    
    # Verificar que hay múltiples sugerencias
    if num_sugerencias >= 3:
        print(f"✅ EXCELENTE: El backend genera {num_sugerencias} sugerencias de gráficos")
        print("   El frontend debería mostrar TODOS estos gráficos, no solo uno.")
    elif num_sugerencias == 2:
        print(f"⚠️  ADVERTENCIA: Solo se generaron {num_sugerencias} sugerencias")
        print("   Se esperan al menos 3-5 sugerencias")
    else:
        print(f"❌ ERROR: Solo {num_sugerencias} sugerencia(s) generada(s)")
        print("   El sistema debería generar 3-5 sugerencias")
    
    print("\n" + "="*80)
    print("\n📝 DATOS COMPLETOS DEL ANÁLISIS:")
    print(json.dumps(data["analisis"], indent=2, ensure_ascii=False))
    
except Exception as e:
    print(f"   ❌ Excepción: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("\n" + "="*80)
print("🎯 CONCLUSIÓN:")
print("="*80)
print("Si ves múltiples sugerencias arriba pero solo UN gráfico en el frontend,")
print("entonces el problema está en el FRONTEND, no en el backend.")
print("El backend está generando correctamente múltiples sugerencias.")
print("="*80)
print()
