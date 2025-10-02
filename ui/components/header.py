import flet as ft
from core.file_manager import FileManager as fm

class Header(ft.Container):
    def __init__(self, file_manager:fm, refresh_callback):
        super().__init__()
        self.file_manager = file_manager
        self.refresh_callback = refresh_callback

        self.content_navigation = ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK_SHARP,
                    on_click=self.go_back
                ),
                ft.IconButton(
                    icon=ft.Icons.ARROW_FORWARD_SHARP,
                    on_click=self.go_forward
                ),
                ft.Container(
                    expand=True,
                    border = ft.border.all(0.5, "grey"),
                    padding=10,
                    border_radius=5,
                    content=ft.Row(
                        expand=True,
                        controls= [
                            ft.Text(f"Ruta: {self.file_manager.current_path}", weight="bold"),
                        ]
                    )
                ),
                ft.IconButton(
                    icon=ft.Icons.NOTE_ADD,
                    tooltip="Crear archivo"
                ),
                ft.IconButton(
                    icon=ft.Icons.CREATE_NEW_FOLDER,
                    tooltip="Crear carpeta"
                )
                
            ]
        )

        self.content = self.content_navigation

    def go_back(self, e):
        if self.file_manager.go_back():
            self.refresh_callback()

    def go_forward(self, e):
        if self.file_manager.go_forward():
            self.refresh_callback()


    def update_path(self):
        self.content_navigation.controls[2].content.controls[0].value = f"Ruta: {self.file_manager.current_path}"