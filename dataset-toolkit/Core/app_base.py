# core/app_base.py
import customtkinter as ctk
import json
import os

class BaseApp(ctk.CTk):
    def __init__(self, config_path):
        super().__init__()
        
        self.config = self._load_config(config_path)
        self.system_prompt = self._load_system_prompt()
        self.dataset_file = self.config.get("dataset_file", "dataset.jsonl")
        self.dataset = self._load_dataset()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

    def _load_config(self, config_path):
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"El archivo de configuración no se encontró en: {config_path}")
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _load_system_prompt(self):
        prompt_file = self.config.get("system_prompt_file")
        if prompt_file and os.path.exists(prompt_file):
            with open(prompt_file, 'r', encoding='utf-8') as f:
                return f.read()
        return self.config.get("default_system_prompt", "System prompt por defecto.")

    def _load_dataset(self):
        data = []
        if not os.path.exists(self.dataset_file): return data
        try:
            with open(self.dataset_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip(): data.append(json.loads(line))
        except Exception as e:
            print(f"Error al cargar el dataset: {e}")
        return data

    def _save_dataset(self):
        try:
            with open(self.dataset_file, 'w', encoding='utf-8') as f:
                for entry in self.dataset:
                    f.write(json.dumps(entry, ensure_ascii=False) + '\n')
            return True
        except Exception as e:
            print(f"Error al guardar el dataset: {e}")
            return False

    def run(self):
        self.mainloop()
