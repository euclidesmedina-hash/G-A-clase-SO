import flet as ft
from ui.layout.Layout import Layout

def main(page:ft.Page):
    page.title = "Gestor simple de archivos"
    page.window.min_width = 500
    page.window.min_height = 400

    layout = Layout()
    page.add(layout)

if __name__ == "__main__":
    ft.app(target=main)
