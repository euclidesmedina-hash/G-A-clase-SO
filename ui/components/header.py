import flet as ft

class Header(ft.Container):
    def __init__(self, page:ft.Page = None):
        super().__init__()
        self.page = page
        # self.height = 50
        # self.border = ft.border.only(bottom=ft.border.BorderSide(1, "grey"))

        self.content = ft.Row(
            # spacing=0,
            controls=[
                ft.IconButton(icon=ft.Icons.ARROW_BACK_SHARP),
                ft.IconButton(icon=ft.Icons.ARROW_FORWARD_SHARP),
                ft.Container(
                    expand=True,
                    border = ft.border.all(0.5, "grey"),
                    padding=10,
                    content=ft.Row(
                        expand=True,
                        controls= [
                            ft.Text("Ruta: ", weight="bold")
                        ]
                    )
                ),
                
            ]
        )