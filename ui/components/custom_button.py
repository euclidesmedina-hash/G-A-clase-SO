import flet as ft

class CustomButton(ft.Container):
    def __init__(self, text="", onClick=None, icon=None):
        super().__init__()
        self.on_click = onClick
        self.ink = True
        self.padding = 5
        self.border_radius = 5

        self.content = ft.Row(
            controls=[
                ft.Icon(icon),
                ft.Text(text, weight="bold")
            ]
        )