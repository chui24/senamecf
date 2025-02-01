import math
import flet as ft
from logic.data_handler import DataHandler
from styles.style import apply_styles
import tkinter as tk
from tkinter import filedialog

def open_file_dialog():
    """Abrir un cuadro de diálogo para seleccionar un archivo."""
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal de tkinter
    file_path = filedialog.askopenfilename(
        title="Seleccionar archivo",
        filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
    )
    return file_path


def show_login_page(page: ft.Page):
    # Configuración general de la página
    page.title = "Sistema SENAMECF - Login"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 0
    page.bgcolor = "#f0f4f8"  # Color de fondo de la página

    # Imagen de fondo
    background_image = ft.Image(
        src="https://pazactiva.org.ve/wp-content/uploads/2017/09/Senamecd-Morgue-Bello-Monte.jpg",  # URL de la imagen de fondo
        width=page.width,
        height=page.height,
        fit=ft.ImageFit.COVER,
    )

    # Botón de "Importar archivo"
    importar_button = ft.ElevatedButton(
        "Importar archivo",
        on_click=lambda e: import_data_and_show_main_page(page),
        bgcolor=ft.colors.BLUE_700,
        color=ft.colors.WHITE,
        height=50,
        width=200,
    )

    # Contenedor para el botón, centrado en la pantalla
    button_container = ft.Container(
        content=importar_button,
        alignment=ft.alignment.center,
    )

    # Stack para superponer el botón sobre la imagen de fondo
    login_stack = ft.Stack(
        [
            background_image,
            button_container,
        ],
        expand=True,
    )

    # Agregar el stack a la página
    page.add(login_stack)

    # Manejador de evento para cuando la página se cierra
    def on_close(e):
        try:
            handler.save_data()  # Guardar los datos antes de cerrar
            page.snack_bar = ft.SnackBar(ft.Text("Datos guardados correctamente antes de cerrar."))
            page.snack_bar.open = True
            page.update()
        except Exception as e:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error al guardar los datos: {e}"))
            page.snack_bar.open = True
            page.update()

    # Asignar el manejador de eventos al evento on_close
    page.on_close = on_close

def import_data_and_show_main_page(page: ft.Page):
    """Función para importar un archivo y luego mostrar la pantalla principal."""
    import_path = open_file_dialog()
    if import_path:
        global handler
        handler = DataHandler(import_path)  # Crear un nuevo DataHandler con el archivo importado
        show_main_page(page)  # Mostrar la pantalla principal

def show_main_page(page: ft.Page):
    # Limpiar la página actual
    page.clean()

    # Llamar a la función principal que ya tienes definida
    main(page)

def main(page: ft.Page):
    apply_styles(page)

    # Configuración general de la página
    page.title = "Sistema SENAMECF"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    page.bgcolor = "#f0f4f8"  # Color de fondo de la página
    page.update()

    # ------------- ESTADOS GLOBALES -------------
    current_page = 1
    items_per_page = 5
    all_data = []
    filtered_data = []
    current_filter = ""
    is_editing = False  # Para saber si estamos editando o agregando

    # --------------------------------------------------------------------------
    # SECCIÓN SUPERIOR: LOGO + ENUNCIADOS
    # --------------------------------------------------------------------------
    logo_container = ft.Image(
        width=80,
        height=80,
        border_radius=10,
        src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRq8-JJDDAeO5iI5w3K3lDkGnHlNoFYPTCsVQ&s"
    )

    enunciado_text = ft.Text(
        "Evaluaciones medico-legales",
        size=24,
        weight=ft.FontWeight.BOLD,
        color=ft.colors.BLUE_900,
    )
    subenunciado_text = ft.Text(
        "SENAMECF - Núcleo Mérida",
        size=16,
        color=ft.colors.GREY_700,
    )

    # Menú desplegable para importar y exportar
    def import_data(e):
        import_path = open_file_dialog()
        if import_path:
            handler.import_data(import_path)
            load_and_sort_data()
            apply_filter()
            go_to_page(1)
            page.update()

    def export_data(e):
        """Guardar los datos actuales sobrescribiendo el archivo actual."""
        try:
            handler.save_data()  # Sobrescribir el archivo actual
            page.snack_bar = ft.SnackBar(ft.Text("Archivo guardado correctamente"))
            page.snack_bar.open = True
            page.update()
        except Exception as e:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error al guardar el archivo: {e}"))
            page.snack_bar.open = True
            page.update()

    menu_items = [
        ft.PopupMenuItem(text="Importar", on_click=import_data),
        ft.PopupMenuItem(text="Exportar", on_click=export_data),
    ]

    menu = ft.PopupMenuButton(
        items=menu_items,
        icon=ft.icons.MENU,
        tooltip="Opciones",
    )
    
    # Función para exportar el archivo
    def export_data_as(e):
        """Exportar el archivo a una ubicación específica."""
        root = tk.Tk()
        root.withdraw()  # Ocultar la ventana principal de tkinter
        file_path = filedialog.asksaveasfilename(
            title="Guardar como",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            defaultextension=".xlsx"
        )
        if file_path:
            try:
                handler.export_data(file_path)  # Exportar el archivo a la ubicación seleccionada
                page.snack_bar = ft.SnackBar(ft.Text(f"Archivo guardado en: {file_path}"))
                page.snack_bar.open = True
                page.update()
            except Exception as e:
                page.snack_bar = ft.SnackBar(ft.Text(f"Error al guardar el archivo: {e}"))
                page.snack_bar.open = True
                page.update()
                
    # Ícono de exportar (guardar como)
    export_icon = ft.IconButton(
        icon=ft.icons.UPLOAD,  # Cambiar a un ícono que represente mejor la exportación
        on_click=export_data_as,  # Llamar a la función export_data_as
        tooltip="Exportar archivo a otra ubicación",  # Tooltip más descriptivo
        icon_color=ft.colors.BLUE_700,
    )
    
    # Ícono de guardar (exportar)
    save_icon = ft.IconButton(
        icon=ft.icons.SAVE,
        on_click=export_data,  # Llamar a la función export_data
        tooltip="Guardar archivo",
        icon_color=ft.colors.BLUE_700,
    )
    # Contenedor para los íconos, alineado a la derecha
    icons_container = ft.Container(
        content=ft.Row([save_icon, export_icon], spacing=10),
        alignment=ft.alignment.top_right,
        expand=True,  # Ocupar todo el espacio disponible
    )

    # Sección superior con el logo, enunciado y los íconos
    top_section = ft.Row(
        [
            logo_container,
            ft.Column(
                [
                    enunciado_text,
                    subenunciado_text,
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.START
            ),
            icons_container,  # Contenedor de los íconos
        ],
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.START,
        spacing=10,
        expand=True,  # Asegurar que el Row ocupe todo el ancho disponible
    )
    # --------------------------------------------------------------------------
    # FILTRO (TextField) Y BOTÓN PARA MOSTRAR FORMULARIO
    # --------------------------------------------------------------------------
    def do_filter(e):
        nonlocal current_filter
        current_filter = filter_field.value
        apply_filter()
        go_to_page(1)

    filter_field = ft.TextField(
        label="Filtro",
        width=400,
        height=45,
        border_radius=25,
        filled=True,
        bgcolor=ft.colors.WHITE,
        border_color=ft.colors.GREY_400,
        on_change=do_filter,  # Filtra mientras escribes
    )

    # Botón para mostrar el formulario
    def open_modal(e):
        nonlocal is_editing
        is_editing = False  # Estamos en modo "agregar"
        reset_form()
        dialog_title_text.value = "Agregar registro"
        btn_agregar.text = "Agregar Datos"
        btn_agregar.on_click = add_data
        page.overlay.append(modal_dialog)
        modal_dialog.open = True
        page.update()

    show_form_button = ft.ElevatedButton(
        "Agregar registro",
        on_click=open_modal,
        bgcolor=ft.colors.BLUE_700,
        color=ft.colors.WHITE,
        height=45,
        width=150,
    )

    filter_layout = ft.Row(
        [
            filter_field,
            show_form_button,  # Botón para abrir el formulario
        ],
        alignment=ft.MainAxisAlignment.START,
        spacing=10
    )

    # --------------------------------------------------------------------------
    # DATA HANDLER
    # --------------------------------------------------------------------------
    handler = DataHandler("data/datos.xlsx")

    # --------------------------------------------------------------------------
    # CAMPOS DEL FORMULARIO
    # --------------------------------------------------------------------------
    def crear_campo(etiqueta: str) -> ft.TextField:
        return ft.TextField(
            label=etiqueta,
            height=45,
            border_radius=25,
            filled=True,
            bgcolor=ft.colors.WHITE,
            border_color=ft.colors.GREY_400,
            text_style=ft.TextStyle(color=ft.colors.BLACK),
            expand=1,
        )

    n_experticia_field = crear_campo("N° de experticia")
    fecha_field = crear_campo("Fecha")
    apellido_field = crear_campo("Apellido y nombre")

    salida_field = crear_campo("Salida")
    incapacidad_field = crear_campo("Días incap./Recup.")
    fecha_entrega_field = crear_campo("Fecha entrega")

    edad_field = crear_campo("Edad")
    motivo_field = crear_campo("Motivo")
    medico_field = crear_campo("Médico")

    organismo_field = crear_campo("Organismo")
    expediente_field = crear_campo("Expediente/causa")

    form_fields = [
        n_experticia_field, fecha_field, apellido_field,
        salida_field, incapacidad_field, fecha_entrega_field,
        edad_field, motivo_field, medico_field,
        organismo_field, expediente_field
    ]

    # --------------------------------------------------------------------------
    # FUNCIONES DE TABLA Y FILTRO
    # --------------------------------------------------------------------------
    def load_and_sort_data():
        nonlocal all_data
        # Cargar los datos y luego invertir el orden
        all_data = handler.get_data()[::-1]  # Invertir el orden para mostrar el más reciente primero
        # Asegurar que cada fila tenga 11 elementos
        all_data = [row + [""] * (11 - len(row)) if len(row) < 11 else row for row in all_data]

    def apply_filter():
        nonlocal filtered_data
        text = current_filter.strip().lower()
        if not text:
            filtered_data = all_data[:]
        else:
            filtered_data = []
            for row in all_data:
                row_strs = [str(cell).lower() for cell in row]
                if any(text in cell_str for cell_str in row_strs):
                    filtered_data.append(row)
        # Asegurar que cada fila tenga 11 elementos
        filtered_data = [row + [""] * (11 - len(row)) if len(row) < 11 else row for row in filtered_data]

    def get_total_pages():
        return max(1, math.ceil(len(filtered_data) / items_per_page))

    def refresh_table():
        records_table.rows.clear()
        total_pages = get_total_pages()
        start_idx = (current_page - 1) * items_per_page
        end_idx = start_idx + items_per_page
        page_rows = filtered_data[start_idx:end_idx]

        for row in page_rows:
            # Verificar si la fila contiene valores None o cadenas vacías
            if not any(value is None or value == "" for value in row):
                # Crear las celdas para cada columna
                cells = [ft.DataCell(ft.Text(str(value))) for value in row]
                
                # Agregar los botones de "Editar" y "Eliminar" como una celda adicional
                edit_button = ft.ElevatedButton(
                    "Editar",
                    on_click=lambda e, row=row: edit_row(row),
                    bgcolor=ft.colors.BLUE_700,
                    color=ft.colors.WHITE,
                    height=30,
                )
                delete_button = ft.ElevatedButton(
                    "Eliminar",
                    on_click=lambda e, row=row: delete_row(row),
                    bgcolor=ft.colors.RED_700,
                    color=ft.colors.WHITE,
                    height=30,
                )
                actions_cell = ft.DataCell(ft.Row([edit_button, delete_button], spacing=5))
                
                # Asegurar que haya exactamente 12 celdas (11 columnas de datos + 1 de acciones)
                if len(cells) == 11:  # Si hay 11 celdas de datos
                    cells.append(actions_cell)  # Agregar la celda de acciones
                else:
                    # Si no hay 11 celdas, completar con celdas vacías
                    cells.extend([ft.DataCell(ft.Text(""))] * (11 - len(cells)))
                    cells.append(actions_cell)
                
                # Agregar la fila a la tabla
                records_table.rows.append(ft.DataRow(cells=cells))

        pagination_info.value = f"Página {current_page} de {total_pages}"
        page.update()

    def go_to_page(page_num: int):
        nonlocal current_page
        total_pages = get_total_pages()
        if page_num < 1:
            page_num = 1
        elif page_num > total_pages:
            page_num = total_pages
        current_page = page_num
        refresh_table()

    # --------------------------------------------------------------------------
    # DATATABLE
    # --------------------------------------------------------------------------
    records_table = ft.DataTable(
        border=ft.border.all(1, ft.colors.GREY_400),
        columns=[
            ft.DataColumn(ft.Container(width=100, content=ft.Text("N° de experticia", color=ft.colors.BLUE_900))),
            ft.DataColumn(ft.Container(width=100, content=ft.Text("Fecha", color=ft.colors.BLUE_900))),
            ft.DataColumn(ft.Container(width=150, content=ft.Text("Apellido y nombre", color=ft.colors.BLUE_900))),
            ft.DataColumn(ft.Container(width=100, content=ft.Text("Salida", color=ft.colors.BLUE_900))),
            ft.DataColumn(ft.Container(width=200, content=ft.Text("Días de incapacidad/Recuperación", color=ft.colors.BLUE_900))),
            ft.DataColumn(ft.Container(width=150, content=ft.Text("Fecha de entrega", color=ft.colors.BLUE_900))),
            ft.DataColumn(ft.Container(width=80,  content=ft.Text("Edad", color=ft.colors.BLUE_900))),
            ft.DataColumn(ft.Container(width=150, content=ft.Text("Motivo de la experticia", color=ft.colors.BLUE_900))),
            ft.DataColumn(ft.Container(width=100, content=ft.Text("Médico", color=ft.colors.BLUE_900))),
            ft.DataColumn(ft.Container(width=100, content=ft.Text("Organismo", color=ft.colors.BLUE_900))),
            ft.DataColumn(ft.Container(width=150, content=ft.Text("Expediente/causa", color=ft.colors.BLUE_900))),
            ft.DataColumn(ft.Container(width=100, content=ft.Text("Acciones", color=ft.colors.BLUE_900))),
        ],
        rows=[]
    )

    scrollable_table = ft.Row(
        controls=[records_table],
        scroll=ft.ScrollMode.AUTO 
    )

    table_container = ft.Container(
        content=scrollable_table,
        width='100%',
        height='100%',
        border=ft.border.all(1, ft.colors.GREY_400),
        border_radius=10,
        bgcolor=ft.colors.WHITE,
        padding=10,
    )

    # --------------------------------------------------------------------------
    # PAGINACIÓN
    # --------------------------------------------------------------------------
    pagination_info = ft.Text(value="Página 1 de 1", color=ft.colors.BLUE_900)
    prev_page_button = ft.ElevatedButton(
        "Página anterior",
        on_click=lambda e: go_to_page(current_page - 1),
        bgcolor=ft.colors.BLUE_700,
        color=ft.colors.WHITE,
        height=40,
    )
    next_page_button = ft.ElevatedButton(
        "Página siguiente",
        on_click=lambda e: go_to_page(current_page + 1),
        bgcolor=ft.colors.BLUE_700,
        color=ft.colors.WHITE,
        height=40,
    )

    pagination_layout = ft.Row(
        [
            prev_page_button,
            pagination_info,
            next_page_button,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=50
    )

    # --------------------------------------------------------------------------
    # BOTONES DEL FORMULARIO
    # --------------------------------------------------------------------------
    btn_agregar = ft.ElevatedButton(
        "Agregar Datos",
        disabled=True,
        bgcolor=ft.colors.BLUE_700,
        color=ft.colors.WHITE,
        height=40,
    )
    btn_refrescar = ft.ElevatedButton(
        "Refrescar vista",
        bgcolor=ft.colors.GREY_700,
        color=ft.colors.WHITE,
        height=40,
    )
    btn_cerrar = ft.ElevatedButton(
        "Cerrar",
        bgcolor=ft.colors.RED_700,
        color=ft.colors.WHITE,
        height=40,
    )

    def add_data(e):
        handler.add_row({
            "N de experticia": n_experticia_field.value,
            "Fecha": fecha_field.value,
            "Apellido y nombre": apellido_field.value,
            "Salida": salida_field.value,
            "Días de incapacidad/Recuperación": incapacidad_field.value,
            "Fecha de entrega": fecha_entrega_field.value,
            "Edad": edad_field.value,
            "Motivo de la experticia": motivo_field.value,
            "Médico": medico_field.value,
            "Organismo": organismo_field.value,
            "Expediente/causa": expediente_field.value
        })
        handler.save_data()
        load_and_sort_data()
        apply_filter()
        go_to_page(1)
        modal_dialog.open = False
        page.update()

    def reload_data(e):
        # Limpiar todos los campos del formulario
        reset_form()
        page.update()

    def close_modal(e):
        modal_dialog.open = False
        page.update()

    btn_agregar.on_click = add_data
    btn_refrescar.on_click = reload_data
    btn_cerrar.on_click = close_modal

    # --------------------------------------------------------------------------
    # HABILITAR "AGREGAR DATOS" SI TODOS LOS CAMPOS ESTÁN LLENOS
    # --------------------------------------------------------------------------
    def validar_campos(e):
        todos_llenos = all(c.value and c.value.strip() != "" for c in form_fields)
        btn_agregar.disabled = not todos_llenos
        page.update()

    for c in form_fields:
        c.on_change = validar_campos

    # --------------------------------------------------------------------------
    # FORMULARIO EN ALERTDIALOG
    # --------------------------------------------------------------------------
    formulario = ft.Column(
        [
            ft.Row([n_experticia_field, fecha_field, apellido_field], spacing=15, expand=True),
            ft.Row([salida_field, incapacidad_field, fecha_entrega_field], spacing=15, expand=True),
            ft.Row([edad_field, motivo_field, medico_field], spacing=15, expand=True),
            ft.Row([organismo_field, expediente_field], spacing=15, expand=True),
            ft.Row(
                [btn_agregar, btn_refrescar, btn_cerrar],
                spacing=25,
                alignment=ft.MainAxisAlignment.CENTER
            ),
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    dialog_title_text = ft.Text("Agregar registro", size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, color=ft.colors.BLUE_900)
    dialog_title = ft.Row(
        [dialog_title_text],
        alignment=ft.MainAxisAlignment.CENTER
    )

    modal_content = ft.Container(
        content=formulario,
        width=700,
        height=400,
        bgcolor=ft.colors.WHITE,
        border_radius=ft.border_radius.all(10),
        padding=20,
        alignment=ft.alignment.center
    )

    modal_dialog = ft.AlertDialog(
        modal=True,  # Cambiado a True para evitar interacción con el fondo
        title=dialog_title,
        content=modal_content,
        on_dismiss=close_modal
    )

    # --------------------------------------------------------------------------
    # FUNCIÓN PARA EDITAR UNA FILA
    # --------------------------------------------------------------------------
    def edit_row(row):
        nonlocal is_editing
        is_editing = True  # Estamos en modo "editar"
        n_experticia_field.value = row[0]
        fecha_field.value = row[1]
        apellido_field.value = row[2]
        salida_field.value = row[3]
        incapacidad_field.value = row[4]
        fecha_entrega_field.value = row[5]
        edad_field.value = row[6]
        motivo_field.value = row[7]
        medico_field.value = row[8]
        organismo_field.value = row[9]
        expediente_field.value = row[10]

        def save_edit(e):
            handler.update_row(row[0], {
                "N de experticia": n_experticia_field.value,
                "Fecha": fecha_field.value,
                "Apellido y nombre": apellido_field.value,
                "Salida": salida_field.value,
                "Días de incapacidad/Recuperación": incapacidad_field.value,
                "Fecha de entrega": fecha_entrega_field.value,
                "Edad": edad_field.value,
                "Motivo de la experticia": motivo_field.value,
                "Médico": medico_field.value,
                "Organismo": organismo_field.value,
                "Expediente/causa": expediente_field.value
            })
            handler.save_data()
            load_and_sort_data()
            apply_filter()
            go_to_page(current_page)
            modal_dialog.open = False
            page.update()

        dialog_title_text.value = "Editar registro"
        btn_agregar.text = "Guardar Cambios"
        btn_agregar.on_click = save_edit
        page.overlay.append(modal_dialog)
        modal_dialog.open = True
        page.update()

    # --------------------------------------------------------------------------
    # FUNCIÓN PARA ELIMINAR UNA FILA
    # --------------------------------------------------------------------------
    delete_id = None  # Variable para almacenar el ID del registro a eliminar

    confirm_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmar eliminación", color=ft.colors.BLUE_900),
        content=ft.Text("¿Estás seguro de que deseas eliminar este registro?", color=ft.colors.GREY_700),
        actions=[
            ft.ElevatedButton(
                "Sí",
                on_click=lambda e: confirm_delete(e),
                bgcolor=ft.colors.BLUE_700,
                color=ft.colors.WHITE,
            ),
            ft.ElevatedButton(
                "No",
                on_click=lambda e: cancel_delete(e),
                bgcolor=ft.colors.RED_700,
                color=ft.colors.WHITE,
            ),
        ],
    )

    def confirm_delete(e):
        """Eliminar el registro después de confirmar"""
        global delete_id
        if delete_id is not None:
            handler.delete_row(delete_id)
            handler.save_data()
            load_and_sort_data()
            apply_filter()
            go_to_page(current_page)
            page.update()
        confirm_dialog.open = False
        page.update()

    def cancel_delete(e):
        """Cancelar la eliminación"""
        global delete_id
        delete_id = None
        confirm_dialog.open = False
        page.update()

    def delete_row(row):
        """Mostrar el cuadro de diálogo de confirmación antes de eliminar"""
        global delete_id
        delete_id = row[0]  # Obtener el ID del registro a eliminar
        page.overlay.append(confirm_dialog)
        confirm_dialog.open = True
        page.update()

    # --------------------------------------------------------------------------
    # FUNCIÓN PARA RESETEAR EL FORMULARIO
    # --------------------------------------------------------------------------
    def reset_form():
        for field in form_fields:
            field.value = ""
        btn_agregar.disabled = True

    # --------------------------------------------------------------------------
    # ESTRUCTURA PRINCIPAL DE LA PÁGINA
    # --------------------------------------------------------------------------
    page.add(
        ft.Column(
            [
                top_section,       # Logo + Enunciado
                filter_layout,     # Filtro y botón para mostrar formulario
                table_container,   # Contenedor con scroll horizontal
                pagination_layout  # Paginación
            ],
            expand=True,
            spacing=20,
        )
    )

    # --------------------------------------------------------------------------
    # CARGA INICIAL DE DATOS
    # --------------------------------------------------------------------------
    load_and_sort_data()
    apply_filter()
    go_to_page(1)

if __name__ == "__main__":
    ft.app(target=show_login_page)