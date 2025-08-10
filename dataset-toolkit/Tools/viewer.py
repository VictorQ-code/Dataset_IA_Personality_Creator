# tools/viewer.py
import customtkinter as ctk
import json
import os
import textwrap
from core.app_base import BaseApp

class DatasetViewerTool(BaseApp):
    def __init__(self, config_path):
        super().__init__(config_path)

        self.title(self.config["ui_titles"].get("viewer", "Visualizador de Dataset"))
        self.geometry("1400x800") 

        self.current_index = -1
        self.list_buttons = []
        
        self.default_button_color = ctk.CTkButton(self).cget("fg_color")
        self.highlight_button_color = ("#1F6AA5", "#14456D")

        self._create_widgets()
        self._populate_entry_list()
        
    def _create_widgets(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        left_frame = ctk.CTkFrame(self, fg_color="transparent")
        left_frame.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky="ns")
        left_frame.grid_rowconfigure(1, weight=1)

        list_label = ctk.CTkLabel(left_frame, text="Entradas del Dataset", font=ctk.CTkFont(size=16, weight="bold"))
        list_label.grid(row=0, column=0, padx=10, pady=10)

        self.scrollable_list_frame = ctk.CTkScrollableFrame(left_frame, label_text="", width=450)
        self.scrollable_list_frame.grid(row=1, column=0, sticky="ns")
        self.scrollable_list_frame.grid_columnconfigure(0, weight=1)

        right_frame = ctk.CTkFrame(self, fg_color="transparent")
        right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_rowconfigure(3, weight=1)

        user_label = ctk.CTkLabel(right_frame, text=self.config["ui_labels"].get("user_prompt", "User:"), font=ctk.CTkFont(size=16, weight="bold"))
        user_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        self.user_text = ctk.CTkTextbox(right_frame, height=150, wrap="word", font=("Calibri", 14))
        self.user_text.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        assistant_label = ctk.CTkLabel(right_frame, text=self.config["ui_labels"].get("assistant_response", "Assistant:"), font=ctk.CTkFont(size=16, weight="bold"))
        assistant_label.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="w")
        self.assistant_text = ctk.CTkTextbox(right_frame, wrap="word", font=("Calibri", 14))
        self.assistant_text.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")

        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=1, column=1, padx=10, pady=10, sticky="sew")
        button_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.update_button = ctk.CTkButton(button_frame, text="Actualizar Entrada", command=self.update_entry)
        self.update_button.grid(row=0, column=0, padx=10, pady=5)
        
        self.delete_button = ctk.CTkButton(button_frame, text="Eliminar Entrada", command=self.delete_entry, fg_color="#D10000", hover_color="#A30000")
        self.delete_button.grid(row=0, column=1, padx=10, pady=5)

        self.save_button = ctk.CTkButton(button_frame, text="GUARDAR TODO AL ARCHIVO", command=self._save_and_notify)
        self.save_button.grid(row=0, column=2, padx=10, pady=5)
        
        self.status_label = ctk.CTkLabel(self, text="Selecciona una entrada de la lista para verla o editarla.")
        self.status_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="s")

    def _populate_entry_list(self):
        for button in self.list_buttons:
            button.destroy()
        self.list_buttons = []

        for i, entry in enumerate(self.dataset):
            entry_id = f"Entrada_{i+1}" # Usamos un contador simple para IDs visuales
            user_content = entry.get("messages", [{}, {"content": ""}])[1].get("content", "[VACÍO]")
            full_text = f"{entry_id}: {user_content}"
            wrapped_text = "\n".join(textwrap.wrap(full_text, width=60))

            button = ctk.CTkButton(self.scrollable_list_frame, text=wrapped_text, command=lambda index=i: self._select_entry(index), anchor="w")
            button.grid(row=i, column=0, padx=5, pady=2, sticky="ew")
            self.list_buttons.append(button)

    def _select_entry(self, index):
        self.current_index = index

        for i, btn in enumerate(self.list_buttons):
            btn.configure(fg_color=self.highlight_button_color if i == index else self.default_button_color)

        entry = self.dataset[index]
        user_content = entry.get("messages", [{}, {"content": ""}])[1].get("content", "ERROR")
        assistant_content = entry.get("messages", [{}, {}, {"content": ""}])[2].get("content", "ERROR")
        self.user_text.delete("1.0", "end"); self.user_text.insert("1.0", user_content)
        self.assistant_text.delete("1.0", "end"); self.assistant_text.insert("1.0", assistant_content)
        self.status_label.configure(text=f"Mostrando Entrada_{index+1}", text_color="white")

    def update_entry(self):
        if self.current_index == -1: return
        
        self.dataset[self.current_index]["messages"][1]["content"] = self.user_text.get("1.0", "end-1c").strip()
        self.dataset[self.current_index]["messages"][2]["content"] = self.assistant_text.get("1.0", "end-1c").strip()
        
        user_content = self.dataset[self.current_index].get("messages")[1].get("content")
        full_text = f"Entrada_{self.current_index+1}: {user_content}"
        wrapped_text = "\n".join(textwrap.wrap(full_text, width=60))
        self.list_buttons[self.current_index].configure(text=wrapped_text)

        self.status_label.configure(text="Entrada actualizada en memoria. No olvides GUARDAR.", text_color="#FFFF77")

    def delete_entry(self):
        if self.current_index == -1: return
        
        del self.dataset[self.current_index]
        self.user_text.delete("1.0", "end")
        self.assistant_text.delete("1.0", "end")
        self.current_index = -1
        self._populate_entry_list()
        self.status_label.configure(text=f"Entrada eliminada de la memoria. No olvides GUARDAR.", text_color="#FF8888")

    def _save_and_notify(self):
        if self._save_dataset():
            self.status_label.configure(text="¡Dataset guardado con éxito!", text_color="lightgreen")
        else:
            self.status_label.configure(text="Error al guardar el archivo.", text_color="red")
