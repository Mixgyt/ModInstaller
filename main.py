import os
import flet as ft

import utils.json_util as jsu
import utils.installMods as installer
import utils.updater as updater

version = "v2.2"

def verifyDir():
    data = jsu.ConfigReader("mcdir")
    if not(data != None and os.path.isdir(data)):
        return False
    return True

def main(page: ft.Page):
    page.title = "ChambaLand Mods Installer "+version+" by Mixgyt"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_height = 600
    page.window_width = 800
    path_text = ft.TextField(value=jsu.ConfigReader("mcdir"),width=500,tooltip="Aqui se muestra la direccion donde se instalan los mods en para ChambaLand")

    def PickFolder(e: ft.FilePickerResultEvent):
        if(e.path != None):
            jsu.ConfigAdd("mcdir",e.path.strip())
            path_text.value = jsu.ConfigReader("mcdir")
            page.update()

    def ModsInstaller(e):
        selectFolder.disabled = True
        usaTLauncher.disabled = True
        path_text.disabled = True
        InstalarBt.disabled = True
        ContenerdorDeCarga.visible = True
        page.update()
        result = installer.InstallMods(path_text.value.strip(),eliminarModsOld.value)
        if(result):
            page.dialog = exitoAlert
            barraDeDescarga.value = 1
            barraDeDescarga.color = ft.colors.GREEN_300
            exitoAlert.open = True
            page.update()
        else: 
            page.dialog = errorAlert
            barraDeDescarga.color = "red"
            errorAlert.open = True
            page.update()

        selectFolder.disabled = False
        usaTLauncher.disabled = False
        path_text.disabled = False
        InstalarBt.disabled = False
        page.update()

    def TLauncherUse(e):
        if(usaTLauncher.value):
            jsu.ConfigAdd("mcdir",jsu.ConfigReader("userPath")+"\\AppData\\Roaming\\.minecraft\\mods")
            path_text.value = jsu.ConfigReader("mcdir")
            page.update()
        else:
            jsu.ConfigAdd("mcdir",jsu.ConfigReader("userPath")+"\\")
            path_text.value = jsu.ConfigReader("mcdir")
            page.update()

    def ErrorProceso(e):
        ContenerdorDeCarga.visible = False
        barraDeDescarga.color = ft.colors.BLUE_300
        errorAlert.open = False
        page.update()

    def ExitoProceso(e):
        ContenerdorDeCarga.visible = False
        barraDeDescarga.value = None
        barraDeDescarga.color = ft.colors.BLUE_300
        exitoAlert.open = False
        page.update()

        
    def RemoverVersion(e):
        page.window_close()
        os.system("updater.exe")
        ##os.remove("ModInstaller"+version+".exe")
        ##print("Eliminado")

    errorAlert = ft.AlertDialog(
        modal=True,
        title=ft.Text("Error"),
        content=ft.Text("El directorio de instalacion no se ha encontrado"),
        actions=[
            ft.ElevatedButton(text="Aceptar",color="red",on_click=ErrorProceso)
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda e: print("cerrado")
    )

    exitoAlert = ft.AlertDialog(
        modal=True,
        title=ft.Text("Mods Instalados Correctamente"),
        content=ft.Text("Los mods han sido instalados correctamente"),
        actions=[
            ft.ElevatedButton(text="Aceptar",color="green",on_click=ExitoProceso)
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )

    updateAler = ft.AlertDialog(
        modal=True,
        title=ft.Text("El instalador se ha actualizado"),
        content=ft.Text("El instalador se ha actualizado por favor cierra esta version"),
        actions=[
            ft.ElevatedButton(text="Cerrar App",color="red",on_click=RemoverVersion)
        ],
        actions_alignment=ft.MainAxisAlignment.END
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

    eliminarModsOld = ft.Checkbox(
        label="Eliminar mods viejos",
        tooltip="Si marcas esta casilla los Mods antiguos que tengas en la carpeta seleccionada se eliminaran",
        label_position=ft.LabelPosition.RIGHT,
        check_color=ft.colors.WHITE,
        fill_color=ft.colors.BLUE_600,
        value=True
    )

    usaTLauncher = ft.Checkbox(
        label="Usas TLauncher",
        tooltip="Si usas TLauncher marca esta casilla para instalar los mods en la ubicación predeterminada",
        label_position=ft.LabelPosition.RIGHT,
        check_color=ft.colors.BLUE_900,
        fill_color=ft.colors.WHITE,
        value=True,
        on_change=TLauncherUse
    )

    selectFolder = ft.IconButton(
        ft.icons.FOLDER,
        tooltip="Selecciona la carpeta manualmente",
        on_click=lambda _: folderPiker.get_directory_path("Directorio de Minecraft",jsu.ConfigReader("userPath"))
    )

    contenedorMed = ft.Container(
        alignment=ft.alignment.center,
        border_radius=10,
        margin=10,
        padding=20,
        bgcolor=ft.colors.BLUE_900,
        width=600,
        height=200,
        content = ft.Column(
            controls=[
                ft.Text("Opciones extra:",weight=ft.FontWeight.BOLD),
                ft.Row(controls=[eliminarModsOld, usaTLauncher]),
                ft.Text("Carpeta de instalacion:"),
                ft.Row(controls=[path_text,selectFolder])],
            alignment="center"
        )
    )
        
    barraDeDescarga = ft.ProgressBar(
        width=500,
        color=ft.colors.BLUE_300,
        visible=True
    )

    ContenerdorDeCarga = ft.Container(
        content=ft.Column(
            controls=[ft.Text("Descargando e Instalando Mods..."),
                      barraDeDescarga]
        ),
        visible=False
    )

    InstalarBt = ft.ElevatedButton(
        width=150,
        height=50,
        tooltip="Instalar los mods de ChambaLand en la ubicacion seleccionada",
        text="Instalar Mods",
        color = ft.colors.WHITE,
        bgcolor=ft.colors.BLUE_600,
        on_click=ModsInstaller
    )

    TituloText = ft.Text(
        value="Instalador de Mods para ChambaLand",
        weight = ft.FontWeight.BOLD,
        style=ft.TextThemeStyle.HEADLINE_SMALL
    )

    if(page.platform != "windows"):
        usaTLauncher.visible = False
        page.update()
    
    if(jsu.ConfigReader("mcdir") != jsu.ConfigReader("userPath")+"\\AppData\\Roaming\\.minecraft\\mods"):
        usaTLauncher.value = False

    page.add(TituloText,contenedorMed,InstalarBt,ContenerdorDeCarga)
    jsu.ConfigAdd("version",version)

    if(updater.CheckVersion(version)):
        page.dialog = updateAler
        updateAler.open = True
        page.update()


ft.app(target=main)