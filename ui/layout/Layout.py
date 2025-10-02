import flet as ft
from ..components.header import Header
from ..components.sidebar import Sidebar
from ..components.show_content import ShowContent
from core.file_manager import FileManager

class Layout(ft.Container):
    def __init__(self, page:ft.Page = None):
        super().__init__()
        self.page = page
        self.expand = True
        self.file_manager = FileManager()

        #components
        self.header = Header(self.file_manager, self.refresh)
        self.sidebar = Sidebar(self.file_manager, self.refresh)
        self.show_content = ShowContent(self.file_manager, self.refresh)

        self.content = ft.Column(
            spacing=0,
            expand=True,
            controls=[
                self.header,
                ft.ResponsiveRow(
                    expand=True,
                    controls=[
                        self.sidebar,
                        self.show_content
                    ]
                )
            ]
        )

    def refresh(self):
        self.header.update_path()
        self.show_content.refresh()
        self.page.update()