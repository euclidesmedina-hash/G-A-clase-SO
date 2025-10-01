import flet as ft

class ShowContent(ft.Container):
    def __init__(self, page:ft.Page = None):
        super().__init__()
        self.page = page
        # self.border = ft.border.all(1, "red")
        self.col = self.col = {"xs":7, "sm":8, "md":9, "lg":10}

        self.content = ft.Column(
            # expand=True,
            controls=[
                # ft.Text("Show Content")
            ]
        )