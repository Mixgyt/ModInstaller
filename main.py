import os
import flet as ft
import asyncio

import utils.json_util as jsu
import utils.verifymc as verify

def verifyDir():
    data = jsu.ConfigReader("mcdir")
    if not(data != None and os.path.exists(data)):
        return False
    return True

def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    path_text = ft.TextField(value=jsu.ConfigReader("mcdir"),width=350)

    def PickFolder(e: ft.FilePickerResultEvent):
        if(e.path != None):
            jsu.ConfigEdit("mcdir",e.path)
            path_text.value = jsu.ConfigReader("mcdir")
            page.update()


    selectDir = ft.AlertDialog(
        modal=True,
        title=ft.Text("Selecciona la carpeta de minecraft"),
        content=ft.Text("Necesitas buscar la carpeta donde se encuentra la version de minecraft que usaras"),
        actions=[
            ft.TextButton("Buscar carpeta",on_click=None)
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda e: print("cerrado")
    )

    folderPiker = ft.FilePicker(on_result=PickFolder)
    page.overlay.append(folderPiker)

    contenedorSup = ft.Column(
        alignment=ft.alignment.center,
        controls=[
            ft.Text("Servidor"),
            ft.Text("motd",text_align=ft.TextAlign.CENTER)
        ]
    )

    contenedorMed = ft.Container(
        alignment=ft.alignment.center,
        border_radius=10,
        margin=10,
        padding=10,
        bgcolor=ft.colors.BLUE_600,
        width=500,
        height=200,
        content = ft.Column(
            controls=[ft.Text("Carpeta de minecraft"),
                ft.Row(controls=[path_text,ft.IconButton(ft.icons.FOLDER,on_click=lambda _: folderPiker.get_directory_path("Directorio de Minecraft",jsu.ConfigReader("userPath")))])],
            alignment="center"
        )
    )

    page.add(contenedorMed)


ft.app(target=main)