import os
import flet as ft
import base64
import webbrowser

import utils.json_util as jsu
import utils.installMods as installer
import utils.updater as updater
import utils.server_status as status

version = "v2.3"

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

    def SaveBytes(bytes:str):
        format = bytes[bytes.find(",")+1:].encode()
        with open("icon.png","wb") as file:
            file.write(base64.decodebytes(format))
        return "icon.png"

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

        
    def RedirVersion(e):
        updateAler.open = False
        page.update()
        webbrowser.open("https://github.com/Mixgyt/ModInstaller/releases/download/"+updater.GetVersion()+"/ModInstaller.exe",0,autoraise=True)
    
    def CancelUpdate(e):
        updateAler.open = False
        page.update()

    def NameList(lista:dict):
        rlista:str = "Jugadores:"
        for l in lista:
            rlista += "\n"+l["name"]
        return rlista

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
        content=ft.Text("El instalador se ha actualizado ¿deseas atualizarlo?"),
        actions=[
            ft.ElevatedButton(text="Descargar Actualizacion",color="green",on_click=RedirVersion),
            ft.ElevatedButton(text="Cancelar",color="red",on_click=CancelUpdate)
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )

    folderPiker = ft.FilePicker(on_result=PickFolder)
    page.overlay.append(folderPiker)

    Sname = status.ServerName()
    SInfo = status.ServerInfo()
    if SInfo["online"]:
        Ico = SaveBytes(SInfo["icon"])
        contenedorSup = ft.Container(
            bgcolor=ft.colors.GREEN_800,
            width=400,
            height=110,
            border_radius=10,
            margin=10,
            padding=20,
            tooltip=Sname+" Online "+str(SInfo["ip"])+":"+str(SInfo["port"]),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Image(src=Ico),
                    ft.Column(
                        controls=[
                            ft.Text(Sname,weight="bold",size=25,color=ft.colors.GREEN_100),
                            ft.Text("::"+SInfo["motd"]["clean"][0]+"::",size=15,color="yellow")
                    ]),
                    ft.VerticalDivider(width=50),
                    ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[ft.Text("Online",color=ft.colors.GREEN_100,text_align=ft.alignment.center,tooltip="Jugadores activos: "+str(SInfo["players"]["online"]),),
                                  ft.Text(str(SInfo["players"]["online"])+"/"+str(SInfo["players"]["max"]),color=ft.colors.GREEN_100,text_align=ft.alignment.center,tooltip=NameList(SInfo["players"]["list"]))]
                    )
                ]
            )
        )
    else:
        contenedorSup = ft.Container(
            bgcolor=ft.colors.RED_800,
            width=400,
            height=120,
            border_radius=10,
            margin=10,
            padding=20,
            tooltip=Sname+" Offline "+str(SInfo["ip"])+":"+str(SInfo["port"]),
            content=ft.Row(
                controls=[
                    ft.Icon(ft.icons.ERROR_ROUNDED),
                    ft.Column(
                    controls=[
                        ft.Text(Sname,weight="bold",size=25,color=ft.colors.RED_100),
                        ft.Text("::"+"SERVIDOR OFFLINE"+"::",size=15,color="yellow")
                    ]),
                    ft.VerticalDivider(width=50),
                    ft.Text("Offline",color=ft.colors.RED_100)
                ]
            )
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

    page.add(TituloText,contenedorSup,contenedorMed,InstalarBt,ContenerdorDeCarga)

    if(updater.CheckVersion(version)):
        page.dialog = updateAler
        updateAler.open = True
        page.update()

ft.app(target=main)
try:
    os.remove("icon.png")
except:
    print("el icono no fue creado previamente")
    quit()