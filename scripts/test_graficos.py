"""
Test directo - verifica cuántos gráficos genera el backend
"""
import sys
import os
import requests
import json

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/..")

print("\n" + "="*80)
print("🔍 TEST: ¿Cuántos gráficos está generando el backend?")
print("="*80)

try:
    print("\n📤 Subiendo archivo test_data/ventas_ejemplo.csv...")
    
    with open("test_data/ventas_ejemplo.csv", "rb") as f:
        files = {"file": ("ventas.csv", f, "text/csv")}
        response = requests.post("http://localhost:8000/upload", files=files, timeout=30)
    
    if response.status_code != 200:
        print(f"\n❌ ERROR {response.status_code}")
        print(response.text[:500])
        sys.exit(1)
    
    data = response.json()
    
    print(f"✅ Upload exitoso!")
    print(f"\n📊 Información del archivo:")
    print(f"   - ID: {data['id_archivo'][:30]}...")
    print(f"   - Filas: {data['metadatos']['filas']}")
    print(f"   - Columnas: {data['metadatos']['columnas']}")
    
    # AQUÍ ESTÁ LA CLAVE: cuántas sugerencias hay?
    sugerencias = data["analisis"]["sugerencias_graficos"]
    num_sugerencias = len(sugerencias)
    
    print(f"\n🎯 SUGERENCIAS DE GRÁFICOS GENERADAS: {num_sugerencias}")
    print("="*80)
    
    for i, sug in enumerate(sugerencias, 1):
        print(f"\n   {i}. {sug.get('titulo', 'Sin título')}")
        print(f"      Tipo: {sug.get('tipo_grafico', 'N/A')}")
        print(f"      Eje X: {sug.get('parametros', {}).get('eje_x', 'N/A')}")
        print(f"      Eje Y: {sug.get('parametros', {}).get('eje_y', 'N/A')}")
    
    print("\n" + "="*80)
    if num_sugerencias >= 3:
        print(f"✅ CORRECTO: Se generaron {num_sugerencias} sugerencias")
        print("   El backend está funcionando correctamente.")
        print("   Si solo ves 1 gráfico en el frontend, el problema está ahí.")
    else:
        print(f"⚠️  ADVERTENCIA: Solo {num_sugerencias} sugerencia(s)")
        print("   El sistema debería generar 3-5 sugerencias")
    
    print("="*80)
    
    # Guardar respuesta completa para debugging
    with open("debug_respuesta_upload.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print("\n💾 Respuesta completa guardada en: debug_respuesta_upload.json")
    print()
    
except FileNotFoundError:
    print("\n❌ ERROR: No se encontró test_data/ventas_ejemplo.csv")
    print("   Ejecuta este script desde el directorio Backend/")
    sys.exit(1)
except requests.exceptions.ConnectionError:
    print("\n❌ ERROR: No se pudo conectar al servidor en localhost:8000")
    print("   Asegúrate de que el servidor esté corriendo con: python main.py")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
