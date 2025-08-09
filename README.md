# Dataset Toolkit para IA Conversacional

Un conjunto de herramientas gráficas construidas con Python y CustomTkinter para crear, visualizar y editar datasets para el fine-tuning de modelos de lenguaje.

## Características

- **Modular:** Diseñado para manejar múltiples proyectos de IA con configuraciones separadas.
- **Fácil de Usar:** Interfaces gráficas simples para la creación y edición de datos.
- **Configurable:** Define la personalidad de tu IA, los nombres de los archivos y los textos de la UI a través de un simple archivo `config.json`.

## Estructura del Proyecto

```
/dataset-toolkit/
├── core/             # Lógica base de la aplicación
├── tools/            # Herramientas (Creador, Visualizador)
├── projects/         # ¡Aquí es donde vives!
│   └── mi_proyecto/
│       ├── config.json
│       └── personality.txt
├── main.py           # Punto de entrada
└── README.md
```

## ¿Cómo Empezar?

1.  **Clona el repositorio:**
    ```bash
    git clone https://github.com/tu_usuario/dataset-toolkit.git
    cd dataset-toolkit
    ```

2.  **Instala las dependencias:**
    ```bash
    pip install customtkinter
    ```

3.  **Crea tu primer proyecto:**
    -   Dentro de la carpeta `projects/`, crea una nueva carpeta, por ejemplo, `my_assistant`.
    -   Dentro de `my_assistant/`, crea un archivo `personality.txt` y escribe el system prompt de tu IA.
    -   Crea un archivo `config.json` y configúralo. Puedes usar `projects/six/config.json` como plantilla.

4.  **Lanza las herramientas:**
    -   Para abrir el creador de dataset para tu proyecto:
        ```bash
        python main.py creator my_assistant
        ```
    -   Para abrir el visualizador/editor:
        ```bash
        python main.py viewer my_assistant
        ```

---
