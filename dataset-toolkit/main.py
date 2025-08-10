# main.py
# Punto de entrada para lanzar las herramientas del Dataset Toolkit.

import argparse
import os
import sys

# Añadimos las carpetas 'core' y 'tools' a la ruta de Python
# para que podamos importar desde ellas sin problemas.
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'tools'))

from tools.creator import DatasetCreatorTool
from tools.viewer import DatasetViewerTool

def main():
    """
    Función principal que parsea los argumentos de la línea de comandos
    y lanza la herramienta correspondiente.
    """
    parser = argparse.ArgumentParser(
        description="Herramientas para crear y gestionar datasets de IA.",
        formatter_class=argparse.RawTextHelpFormatter # Para un texto de ayuda más bonito
    )
    
    parser.add_argument(
        "tool", 
        choices=["creator", "viewer"], 
        help="La herramienta que quieres ejecutar:\n"
             "  creator - Abre la interfaz para crear nuevas entradas.\n"
             "  viewer  - Abre la interfaz para visualizar y editar el dataset existente."
    )
                        
    parser.add_argument(
        "project", 
        type=str,
        help="El nombre de la carpeta del proyecto que se encuentra dentro de la carpeta 'projects'."
    )

    args = parser.parse_args()

    # Construir la ruta al archivo de configuración del proyecto especificado
    config_path = os.path.join("projects", args.project, "config.json")
    
    # Comprobar si el proyecto y su configuración existen
    if not os.path.exists(config_path):
        print(f"\n--- ERROR ---")
        print(f"No se encontró el proyecto '{args.project}'.")
        print(f"Asegúrate de que existe la siguiente ruta y archivo: {config_path}")
        print(f"-------------\n")
        return

    # Lanzar la herramienta seleccionada con la configuración del proyecto
    print(f"Lanzando la herramienta '{args.tool}' para el proyecto '{args.project}'...")
    
    app = None
    if args.tool == "creator":
        app = DatasetCreatorTool(config_path)
    elif args.tool == "viewer":
        app = DatasetViewerTool(config_path)
    
    if app:
        app.run()

if __name__ == "__main__":
    main()
