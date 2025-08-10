# tools/creator.py

import customtkinter as ctk
import json
from core.app_base import BaseApp

class DatasetCreatorTool(BaseApp):
    def __init__(self, config_path):
        super().__init__(config_path)
        
        self.title(self.config["ui_titles"].get("creator", "Creador de Dataset"))
        self.geometry("900x800")
        
        self._create_widgets()

    def _create_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1) # Damos peso a la fila de la respuesta

        # Obtener los textos de las etiquetas desde el archivo de configuración
        user_label_text = self.config["ui_labels"].get("user_prompt", "User Prompt:")
        assistant_label_text = self.config["ui_labels"].get("assistant_response", "Assistant Response:")
        
        # --- Campo de Pregunta (User) ---
        user_label = ctk.CTkLabel(self, text=user_label_text, font=ctk.CTkFont(size=16, weight="bold"))
        user_label.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")
        self.user_text = ctk.CTkTextbox(self, height=150, wrap="word", font=("Calibri", 14))
        self.user_text.grid(row=1, column=0, padx=20, pady=5, sticky="ew")

        # --- Campo de Respuesta (Assistant) ---
        assistant_label = cturplek.CTkLabel(self, text=assistant_label_text, font=ctk.CTkFont(size=16, weight="bold"))
        assistant_label.grid(row=2, column=0, padx=20, pady=(20, 5), sticky="w")
        self.assistant_text = ctk.CTkTextbox(self, wrap="word", font=("Calibri", 14))
        self.assistant_text.grid(row=3, column=0, padx=20, pady=5, sticky="nsew")

        # --- Botón y Etiqueta de Estado ---
        self.save_button = ctk.CTkButton(self, text="Añadir Entrada y Guardar en Archivo", command=self._add_entry_and_save, height=40, font=ctk.CTkFont(size=16, weight="bold"))
        self.save_button.grid(row=4, column=0, padx=20, pady=20, sticky="ew")
        
        self.status_label = ctk.CTkLabel(self, text=f"Listo para añadir entradas a '{os.path.basename(self.dataset_file)}'")
        self.status_label.grid(row=5, column=0, padx=20, pady=10)

    def _add_entry_and_save(self):
        user_input = self.user_text.get("1.0", "end-1c").strip()
        assistant_input = self.assistant_text.get("1.0", "end-1c").strip()

        if not user_input or not assistant_input:
            self.status_label.configure(text="Ambos campos son obligatorios.", text_color="orange")
            return

        # Creamos la nueva entrada usando el system_prompt cargado por BaseApp
        new_entry = {
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_input},
                {"role": "assistant", "content": assistant_input}
            ]
        }
        self.dataset.append(new_entry)
        
        # Usamos el método de guardado heredado de BaseApp
        if self._save_dataset():
            self.status_label.configure(text=f"¡Entrada #{len(self.dataset)} guardada con éxito!", text_color="lightgreen")
            # Limpiamos los campos para la siguiente entrada
            self.user_text.delete("1.0", "end")
            self.assistant_text.delete("1.0", "end")
            self.user_text.focus() # Ponemos el cursor en el primer campo
        else:
            # Si el guardado falla, revertimos la adición a la lista en memoria
            self.dataset.pop()
            self.status_label.configure(text="Error al guardar el archivo. La entrada no fue añadida.", text_color="red")
