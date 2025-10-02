import flet as ft
from core.file_manager import FileManager as fm

class Header(ft.Container):
    def __init__(self, file_maneger:fm, refresh_callback):
        super().__init__()
        # self.page = page
        self.file_manager = file_maneger
        self.refresh_callback = refresh_callback

        self.content = ft.Row(
            # spacing=0,
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
                    content=ft.Row(
                        expand=True,
                        controls= [
                            ft.Text(f"Ruta: {self.file_manager.current_path}", weight="bold")
                        ]
                    )
                ),
                
            ]
        )

    def go_back(self, e):
        if self.file_manager.go_back():
            self.refresh_callback()

    def go_forward(self, e):
        if self.file_manager.go_forward():
            self.refresh_callback()


    def update_path(self):
        self.content.controls[2].content.controls[0].value = f"Ruta: {self.file_manager.current_path}"