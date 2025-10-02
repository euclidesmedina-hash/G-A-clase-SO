import flet as ft
import os
from core.file_manager import FileManager as fm
from .custom_button import CustomButton

class Sidebar(ft.Container):
    def __init__(self, file_manager:fm, refresh_callback):
        super().__init__()
        self.file_manager = file_manager
        self.refresh_callback = refresh_callback

        self.border = ft.border.only(right=ft.border.BorderSide(0.5, "grey"))
        self.col = {"xs":5, "sm":4, "md":3, "lg":2}

        home = self.file_manager.current_path
        # Diccionario simple de carpetas comunes (en español e inglés)
        self.common_paths = {
            "Escritorio": [os.path.join(home, "Desktop"), os.path.join(home, "Escritorio")],
            "Descargas": [os.path.join(home, "Downloads"), os.path.join(home, "Descargas")],
            "Documentos": [os.path.join(home, "Documents"), os.path.join(home, "Documentos")],
            "Imágenes": [os.path.join(home, "Pictures"), os.path.join(home, "Imágenes")],
            "Música": [os.path.join(home, "Music"), os.path.join(home, "Música")],
            "Videos": [os.path.join(home, "Videos"), os.path.join(home, "Vídeos")],
        }

        self.content = ft.Column(
            spacing=0,
            controls=[
                ft.Text("Explorar", weight="bold"),
                CustomButton(
                    text="Escritorio", 
                    icon=ft.Icons.DESKTOP_WINDOWS_ROUNDED, 
                    onClick=lambda e: self.navigate("Escritorio")
                ),
                CustomButton(
                    text="Descargas", 
                    icon=ft.Icons.FILE_DOWNLOAD_SHARP,
                    onClick=lambda e: self.navigate("Descargas")
                ),
                CustomButton(
                    text="Documentos", 
                    icon=ft.Icons.EDIT_DOCUMENT,
                    onClick=lambda e: self.navigate("Documentos")
                ),
                CustomButton(
                    text="Imágenes", 
                    icon=ft.Icons.IMAGE_ROUNDED,
                    onClick=lambda e: self.navigate("Imágenes")
                ),
                CustomButton(
                    text="Música", 
                    icon=ft.Icons.LIBRARY_MUSIC_ROUNDED,
                    onClick=lambda e: self.navigate("Música")
                ),
                CustomButton(
                    text="Videos", 
                    icon=ft.Icons.MOVIE_ROUNDED,
                    onClick=lambda e: self.navigate("Videos")
                ),
            ]
        )

    def navigate(self, key):
        # Busca la primera ruta que exista
        for path in self.common_paths[key]:
            if os.path.isdir(path):
                self.file_manager.current_path = path
                self.file_manager.update_history(path)
                self.refresh_callback()
                return
        print(f"No se encontró la carpeta: {key}")