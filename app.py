import math
import flet as ft
from logic.data_handler import DataHandler
from styles.style import apply_styles

def main(page: ft.Page):
    apply_styles(page)

    # Configuración general de la página
    page.title = "Sistema SENAMECF"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.padding = 50
    page.scroll = ft.ScrollMode.AUTO
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
    logo_container = ft.Container(
        width=80,
        height=80,
        alignment=ft.alignment.center,
        border=ft.border.all(1, ft.Colors.BLACK),
        content=ft.Text("LOGO", size=14)
    )

    enunciado_text = ft.Text(
        "ENUNCIADO",
        size=24,
        weight=ft.FontWeight.BOLD,
    )
    subenunciado_text = ft.Text(
        "AQUÍ VA A IR MÁS TEXTO.",
        size=16,
    )

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
        ],
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.START,
        spacing=20
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

    show_form_button = ft.ElevatedButton("Agregar registro", on_click=open_modal)

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
            border_color="#cccccc",
            text_style=ft.TextStyle(color=ft.Colors.BLACK),
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
                edit_button = ft.ElevatedButton("Editar", on_click=lambda e, row=row: edit_row(row))
                delete_button = ft.ElevatedButton("Eliminar", on_click=lambda e, row=row: delete_row(row))
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
        refresh_table()  # Llamar a refresh_table después de definirla

    # --------------------------------------------------------------------------
    # DATATABLE
    # --------------------------------------------------------------------------
    records_table = ft.DataTable(
        border=ft.border.all(1, ft.Colors.BLACK),
        columns=[
            ft.DataColumn(ft.Container(width=100, content=ft.Text("N° de experticia"))),
            ft.DataColumn(ft.Container(width=100, content=ft.Text("Fecha"))),
            ft.DataColumn(ft.Container(width=150, content=ft.Text("Apellido y nombre"))),
            ft.DataColumn(ft.Container(width=100, content=ft.Text("Salida"))),
            ft.DataColumn(ft.Container(width=200, content=ft.Text("Días de incapacidad/Recuperación"))),
            ft.DataColumn(ft.Container(width=150, content=ft.Text("Fecha de entrega"))),
            ft.DataColumn(ft.Container(width=80,  content=ft.Text("Edad"))),
            ft.DataColumn(ft.Container(width=150, content=ft.Text("Motivo de la experticia"))),
            ft.DataColumn(ft.Container(width=100, content=ft.Text("Médico"))),
            ft.DataColumn(ft.Container(width=100, content=ft.Text("Organismo"))),
            ft.DataColumn(ft.Container(width=150, content=ft.Text("Expediente/causa"))),
            ft.DataColumn(ft.Container(width=100, content=ft.Text("Acciones"))),
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
        border=ft.border.all(1, ft.Colors.BLACK),
    )

    # --------------------------------------------------------------------------
    # PAGINACIÓN
    # --------------------------------------------------------------------------
    pagination_info = ft.Text(value="Página 1 de 1")
    prev_page_button = ft.ElevatedButton("Página anterior", on_click=lambda e: go_to_page(current_page - 1))
    next_page_button = ft.ElevatedButton("Página siguiente", on_click=lambda e: go_to_page(current_page + 1))

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
    btn_agregar = ft.ElevatedButton("Agregar Datos", disabled=True)
    btn_refrescar = ft.ElevatedButton("Refrescar vista")
    btn_cerrar = ft.ElevatedButton("Cerrar")

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

    dialog_title_text = ft.Text("Agregar registro", size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
    dialog_title = ft.Row(
        [dialog_title_text],
        alignment=ft.MainAxisAlignment.CENTER
    )

    modal_content = ft.Container(
        content=formulario,
        width=700,
        height=400,
        bgcolor=ft.Colors.WHITE,
        border_radius=ft.border_radius.all(10),
        padding=20,
        alignment=ft.alignment.center
    )

    modal_dialog = ft.AlertDialog(
        modal=False,
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
        title=ft.Text("Confirmar eliminación"),
        content=ft.Text("¿Estás seguro de que deseas eliminar este registro?"),
        actions=[
            ft.ElevatedButton("Sí", on_click=lambda e: confirm_delete(e)),
            ft.ElevatedButton("No", on_click=lambda e: cancel_delete(e)),
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
            expand=True
        )
    )

    # --------------------------------------------------------------------------
    # CARGA INICIAL DE DATOS
    # --------------------------------------------------------------------------
    load_and_sort_data()
    apply_filter()
    go_to_page(1)

if __name__ == "__main__":
    ft.app(target=main)