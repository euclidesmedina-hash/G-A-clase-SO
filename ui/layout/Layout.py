import flet as ft
from ..components.header import Header
from ..components.sidebar import Sidebar
from ..components.show_content import ShowContent

class Layout(ft.Container):
    def __init__(self, page:ft.Page = None):
        super().__init__()
        self.page = page
        self.expand = True

        self.content = ft.Column(
            spacing=0,
            expand=True,
            controls=[
                Header(),
                ft.ResponsiveRow(
                    expand=True,
                    controls=[
                        Sidebar(),
                        ShowContent()
                    ]
                )
            ]
        )