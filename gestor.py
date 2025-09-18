import os
import flet as ft
import platform
import stat

def main(page: ft.Page):
    page.title = "Gestor de Archivos"
    page.window_width = 700
    page.window_height = 550
    page.scroll = "auto"


    # Ruta inicial
    ruta_actual = ft.TextField(value=os.getcwd(), expand=True)

    # Lista de archivos
    lista_archivos = ft.ListView(expand=True, spacing=5, padding=10)

    # Base de comentarios en memoria
    comentarios = {}

    #abrir archivos carpeta
    def abrir_item(ruta):
        if os.path.isdir(ruta):
            ruta_actual.value = ruta
            listar_archivos()
        else:
            try:
                sistema = platform.system()
                if sistema == "Windows":
                    os.startfile(ruta)
                elif sistema == "Darwin":  # macOS
                    os.system(f"open '{ruta}'")
                else:  # Linux
                    os.system(f"xdg-open '{ruta}'")
            except Exception as ex:
                page.snack_bar = ft.SnackBar(ft.Text(f"No se pudo abrir: {ex}"), open=True)
                page.update()

    # Crear archivo
    def crear_archivo(e):
        nombre = nombre_input.value.strip()
        if nombre:
            ruta = os.path.join(ruta_actual.value, nombre)
            with open(ruta, "w") as f:
                f.write("")  # archivo vacío
            listar_archivos()

    # Crear directorio
    def crear_directorio(e):
        nombre = nombre_input.value.strip()
        if nombre:
            ruta = os.path.join(ruta_actual.value, nombre)
            os.makedirs(ruta, exist_ok=True)
            listar_archivos()

    # Eliminar
    def eliminar(ruta):
        try:
            if os.path.isdir(ruta):
                os.rmdir(ruta)  # elimina solo si está vacío
            else:
                os.remove(ruta)
            listar_archivos()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"), open=True)
            page.update()

    # Renombrar
    def renombrar(ruta):
        def confirmar(e):
            nuevo_nombre = nuevo_input.value.strip()
            if nuevo_nombre:
                nuevo_ruta = os.path.join(ruta_actual.value, nuevo_nombre)
                os.rename(ruta, nuevo_ruta)
                dlg.open = False
                listar_archivos()
                page.update()

        nuevo_input = ft.TextField(label="Nuevo nombre")
        dlg = ft.AlertDialog(
            title=ft.Text("Renombrar"),
            content=nuevo_input,
            actions=[ft.TextButton("Aceptar", on_click=confirmar)],
        )
        page.open(dlg)
    # cambiar permisos
    def cambiar_permisos(ruta):
        lectura = ft.Checkbox(label="Lectura", value=True)
        escritura = ft.Checkbox(label="Escritura", value=True)
        ejecucion = ft.Checkbox(label="Ejecución", value=False)

        def aplicar(e):
            permisos = 0
            if lectura.value:
                permisos |= stat.S_IREAD
            if escritura.value:
                permisos |= stat.S_IWRITE
            if ejecucion.value:
                permisos |= stat.S_IEXEC

            try:
                os.chmod(ruta, permisos)
                page.snack_bar = ft.SnackBar(ft.Text(f"Permisos aplicados a {os.path.basename(ruta)}"), open=True)
            except Exception as ex:
                page.snack_bar = ft.SnackBar(ft.Text(f"Error cambiando permisos: {ex}"), open=True)
            dlg.open = False
            page.update()

        dlg = ft.AlertDialog(
            title=ft.Text(f"Cambiar permisos: {os.path.basename(ruta)}"),
            content=ft.Column([lectura, escritura, ejecucion]),
            actions=[ft.TextButton("Aplicar", on_click=aplicar)],
        )
        page.open(dlg)



    # Refrescar listado
    def listar_archivos(e=None):
        lista_archivos.controls.clear()
        try:
            archivos = os.listdir(ruta_actual.value)
            for item in archivos:
                ruta_item = os.path.join(ruta_actual.value, item)
                icono = ft.Icons.FOLDER if os.path.isdir(ruta_item) else ft.Icons.DESCRIPTION

                acciones = []

                # solo el rol de editor puede eliminar o renombrar

                acciones.append(
                        ft.IconButton(ft.Icons.DELETE, on_click=lambda e, p=ruta_item: eliminar(p))
                    )
                acciones.append(
                        ft.IconButton(ft.Icons.EDIT, on_click=lambda e, p=ruta_item: renombrar(p))
                    )
                acciones.append(
                        ft.IconButton(ft.Icons.LOCK, on_click=lambda e, p=ruta_item: cambiar_permisos(p))
                    )



                lista_archivos.controls.append(
                    ft.Container(
                        content = ft.Row([ft.Icon(icono), ft.Text(item, expand=True)] + acciones),
                        on_click=lambda e, p=ruta_item: abrir_item(p),
                        ink=True,
                    )
                    
                )
        except Exception as ex:
            lista_archivos.controls.append(ft.Text(f"Error: {ex}", color="red"))
        page.update()

    # Barra de acciones
    nombre_input = ft.TextField(label="Nombre archivo/directorio", expand=True)
    acciones = ft.Row([
        nombre_input,
        ft.IconButton(
            ft.Icons.NOTE_ADD,
            tooltip="Crear archivo",
            on_click=crear_archivo,
        ),
        ft.IconButton(
            ft.Icons.CREATE_NEW_FOLDER,
            tooltip="Crear carpeta",
            on_click=crear_directorio,
        ),
        ft.IconButton(ft.Icons.REFRESH, tooltip="Refrescar", on_click=listar_archivos),
    ])


    # Layout
    page.add(ft.Row([ft.Text("Ruta:"), ruta_actual, ft.IconButton(ft.Icons.REFRESH, on_click=listar_archivos)]))
    page.add(acciones)
    page.add(lista_archivos)

    listar_archivos()

if __name__ == "__main__":
    ft.app(target=main)