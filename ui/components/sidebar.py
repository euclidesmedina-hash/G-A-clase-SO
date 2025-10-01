import flet as ft
from .custom_button import CustomButton

class Sidebar(ft.Container):
    def __init__(self, page:ft.Page = None):
        super().__init__()
        self.page = page
        self.border = ft.border.only(right=ft.border.BorderSide(0.5, "grey"))
        self.col = {"xs":5, "sm":4, "md":3, "lg":2}

        self.content = ft.Column(
            spacing=0,
            controls=[
                ft.Text("Explorar", weight="bold"),
                CustomButton(
                    text="Escritorio", 
                    icon=ft.Icons.DESKTOP_WINDOWS_ROUNDED, 
                    onClick=lambda e:print("hola")
                ),
                CustomButton(
                    text="Descargas", 
                    icon=ft.Icons.FILE_DOWNLOAD_SHARP
                ),
                CustomButton(
                    text="Documentos", 
                    icon=ft.Icons.EDIT_DOCUMENT
                ),
                CustomButton(
                    text="Imágenes", 
                    icon=ft.Icons.IMAGE_ROUNDED
                ),
                CustomButton(
                    text="Música", 
                    icon=ft.Icons.LIBRARY_MUSIC_ROUNDED
                ),
                CustomButton(
                    text="Videos", 
                    icon=ft.Icons.MOVIE_ROUNDED
                ),
            ]
        )