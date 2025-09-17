import os
import flet as ft

def main(page: ft.Page):
    page.title = "Gestor de Archivos"
    page.window_width = 700
    page.window_height = 550
    page.scroll = "auto"

    # Rol actual (por defecto editor)
    rol_usuario = ft.Dropdown(
        label="Selecciona rol",
        value="editor",
        options=[
            ft.dropdown.Option("lector"),
            ft.dropdown.Option("editor"),
            ft.dropdown.Option("comentador"),
        ],
        width=200,
    )

    # Ruta inicial
    ruta_actual = ft.TextField(value=os.getcwd(), expand=True)

    # Lista de archivos
    lista_archivos = ft.ListView(expand=True, spacing=5, padding=10)

    # Base de comentarios en memoria
    comentarios = {}

    # Crear archivo
    def crear_archivo(e):
        if rol_usuario.value != "editor":
            return
        nombre = nombre_input.value.strip()
        if nombre:
            ruta = os.path.join(ruta_actual.value, nombre)
            with open(ruta, "w") as f:
                f.write("")  # archivo vacío
            listar_archivos()

    # Crear directorio
    def crear_directorio(e):
        if rol_usuario.value != "editor":
            return
        nombre = nombre_input.value.strip()
        if nombre:
            ruta = os.path.join(ruta_actual.value, nombre)
            os.makedirs(ruta, exist_ok=True)
            listar_archivos()

    # Eliminar
    def eliminar(ruta):
        if rol_usuario.value != "editor":
            return
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
        if rol_usuario.value != "editor":
            return

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

    # Comentar
    def comentar(ruta):
        if rol_usuario.value != "comentador":
            return

        def guardar_comentario(e):
            if ruta not in comentarios:
                comentarios[ruta] = []
            comentarios[ruta].append(comentario_input.value.strip())
            dlg.open = False
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Comentario guardado para {os.path.basename(ruta)}"),
                open=True,
            )
            page.update()

        comentario_input = ft.TextField(
            label="Escribe un comentario", multiline=True, width=400
        )
        dlg = ft.AlertDialog(
            title=ft.Text(f"Comentar {os.path.basename(ruta)}"),
            content=comentario_input,
            actions=[ft.TextButton("Guardar", on_click=guardar_comentario)],
        )
        page.open(dlg)

    # Ver comentarios (fuera de comentar)
    def ver_comentarios(ruta):
        lista = comentarios.get(ruta, ["(No hay comentarios)"])
        def cerrar(e):
            dlg.open = False
            page.update()
        dlg = ft.AlertDialog(
            title=ft.Text(f"Comentarios de {os.path.basename(ruta)}"),
            content=ft.Column([ft.Text(c) for c in lista], scroll="auto", height=300),
            actions=[ft.TextButton("Cerrar", on_click=cerrar)],
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
                if rol_usuario.value == "editor":
                    acciones.append(
                        ft.IconButton(ft.Icons.DELETE, on_click=lambda e, p=ruta_item: eliminar(p))
                    )
                    acciones.append(
                        ft.IconButton(ft.Icons.EDIT, on_click=lambda e, p=ruta_item: renombrar(p))
                    )

                # solo rol comentador puede comentar
                if rol_usuario.value == "comentador":
                    acciones.append(
                        ft.IconButton(ft.Icons.COMMENT, on_click=lambda e, p=ruta_item: comentar(p))
                    )

                # cualquier rol puede ver comentarios
                acciones.append(
                    ft.IconButton(ft.Icons.VISIBILITY, on_click=lambda e, p=ruta_item: ver_comentarios(p))
                )

                lista_archivos.controls.append(
                    ft.Row([ft.Icon(icono), ft.Text(item, expand=True)] + acciones)
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

    # Cuando cambie el rol, refrescar listado
    def cambiar_rol(e):
        listar_archivos()
    rol_usuario.on_change = cambiar_rol

    # Layout
    page.add(ft.Row([ft.Text("Rol:"), rol_usuario]))
    page.add(ft.Row([ft.Text("Ruta:"), ruta_actual, ft.IconButton(ft.Icons.REFRESH, on_click=listar_archivos)]))
    page.add(acciones)
    page.add(lista_archivos)

    listar_archivos()

if __name__ == "__main__":
    ft.app(target=main)