import flet as ft
import os
from core.file_manager import FileManager as fm

class Header(ft.Container):
    def __init__(self, file_manager:fm, refresh_callback):
        super().__init__()
        self.file_manager = file_manager
        self.refresh_callback = refresh_callback

        self.editing = True #flag saber si estamos editando

        self.path_text = ft.Text(f"Ruta: {self.file_manager.current_path}") #text con la ruta

        #input oculto inicialmente
        self.path_input = ft.TextField(
            value=self.file_manager.current_path,
            expand=True,
            visible=False,
            height=40,
            on_submit=self.on_submit_path,
            on_blur=self.on_cancel_edit
        )

        self.path_container = ft.Container(
            expand=True,
            border=ft.border.all(0.5, "grey"),
            padding=10,
            border_radius=5,
            content=ft.Row(
                expand=True,
                controls=[self.path_text, self.path_input]
            ),
            on_click=self.enable_edit #habilitar edicion
        )

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
                self.path_container,

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

    def enable_edit(self, e):
        self.editing = True
        self.path_text.visible = False
        self.path_input.visible = True
        self.path_input.value = self.file_manager.current_path
        self.path_container.padding = 0
        self.path_input.focus()
        self.update()
    
    def on_submit_path(self, e):
        new_path = self.path_input.value.strip()
        if os.path.isdir(new_path):
            self.file_manager.current_path = new_path
            self.file_manager.update_history(new_path)
            self.refresh_callback()
        else:
            print(f"ruta invalidad {new_path}")
        self.exit_edit_mode()
    
    def on_cancel_edit(self, e):
        """Salir de edición si se pierde el foco"""
        self.exit_edit_mode()

    def exit_edit_mode(self):
        """Volver a mostrar solo el texto"""
        self.editing = False
        self.path_text.visible = True
        self.path_input.visible = False
        self.path_container.padding = 10
        self.update()