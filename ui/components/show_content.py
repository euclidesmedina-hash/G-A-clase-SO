import flet as ft
import os
import platform
from core.file_manager import FileManager as fm

class ShowContent(ft.Container):
    def __init__(self, file_maneger:fm, refresh_callback):
        super().__init__()
        # self.page = page
        self.file_manager = file_maneger
        self.refresh_callback = refresh_callback
        # self.border = ft.border.all(1, "red")
        self.col = self.col = {"xs":7, "sm":8, "md":9, "lg":10}
        self.column = ft.ListView()
        
        self.content = self.column

    # Se ejecuta automáticamente cuando ya está en la page  
    def did_mount(self):
        self.refresh()

    def refresh(self):
        self.column.controls.clear()

        for item in self.file_manager.list_dir():
            path = os.path.join(self.file_manager.current_path, item)
            icon = ft.Icons.FOLDER if os.path.isdir(path) else ft.Icons.DESCRIPTION
            is_dir = os.path.isdir(path)

            self.column.controls.append(
                ft.Container(
                    content=ft.Row([ft.Icon(icon), ft.Text(item, expand=True)]),
                    on_click= lambda e, f=item, d=is_dir: self.on_click_item(f,d),
                    ink=True
                )
            )
        self.update()

    def on_click_item(self, item, is_dir):
        if is_dir and self.file_manager.navigate_to(item):
            self.refresh_callback()
        else:
            self.file_manager.open_file(item)