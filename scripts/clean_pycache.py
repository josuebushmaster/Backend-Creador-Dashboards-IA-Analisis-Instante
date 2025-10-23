"""
Elimina recursivamente carpetas __pycache__ dentro del proyecto.
Uso:
  python scripts/clean_pycache.py [--path PATH] [--delete]
Opciones:
  --path  Ruta raíz donde buscar (por defecto: directorio actual)
  --delete  Realiza la eliminación. Si no se especifica, solo lista (dry-run).

Precaución: este script borra únicamente carpetas llamadas '__pycache__'.
"""

import argparse
import os
import shutil


def find_pycache_dirs(root):
    matches = []
    for dirpath, dirnames, filenames in os.walk(root):
        # make a copy of dirnames to avoid modifying the walk in place
        for d in list(dirnames):
            if d == "__pycache__":
                matches.append(os.path.join(dirpath, d))
    return matches


def main():
    parser = argparse.ArgumentParser(description="Eliminar carpetas __pycache__ (dry-run por defecto).")
    parser.add_argument("--path", default='.', help="Ruta raíz donde buscar")
    parser.add_argument("--delete", action='store_true', help="Borrar los directorios encontrados")
    args = parser.parse_args()

    root = os.path.abspath(args.path)
    print(f"Buscando '__pycache__' en: {root}")

    # Evitar borrar fuera de la ruta actual por accidente
    if not os.path.exists(root):
        print("La ruta indicada no existe.")
        return

    pyc_dirs = find_pycache_dirs(root)

    if not pyc_dirs:
        print("No se encontraron carpetas '__pycache__'.")
        return

    for d in pyc_dirs:
        if args.delete:
            try:
                shutil.rmtree(d)
                print(f"Eliminado: {d}")
            except Exception as e:
                print(f"Error eliminando {d}: {e}")
        else:
            print(f"[DRY-RUN] Encontrado: {d}")

    print("Hecho.")

if __name__ == '__main__':
    main()
