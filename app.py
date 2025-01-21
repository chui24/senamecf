import flet as ft
from logic.data_handler import DataHandler
from styles.style import apply_styles

def main(page: ft.Page):
    # Aplicar estilos
    apply_styles(page)

    # Título de bienvenida
    title = ft.Text("Bienvenido al sistema de registros de datos del SENAMECF", size=50)
    page.add(title)

    # Crear campos de entrada para los datos
    n_experticia_field = ft.TextField(label="N° de experticia", width=150)
    fecha_field = ft.TextField(label="Fecha", width=150)
    apellido_field = ft.TextField(label="Apellido y nombre", width=150)
    salida_field = ft.TextField(label="Salida", width=150)
    incapacidad_field = ft.TextField(label="Días de incapacidad/Recuperación", width=150)
    fecha_entrega_field = ft.TextField(label="Fecha de entrega", width=150)
    edad_field = ft.TextField(label="Edad", width=150)
    motivo_field = ft.TextField(label="Motivo de la experticia", width=150)
    medico_field = ft.TextField(label="Médico", width=150)
    organismo_field = ft.TextField(label="Organismo", width=150)
    expediente_field = ft.TextField(label="Expediente/causa", width=150)

    # Crear instancia de DataHandler
    handler = DataHandler("data/datos.xlsx")

    # Botón para agregar datos
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
        handler.save_data()  # Guardar los datos en el archivo
        refresh_table()  # Refrescar la vista de la tabla

    # Botón para limpiar campos
    def clear_fields(e):
        n_experticia_field.value = ""
        fecha_field.value = ""
        apellido_field.value = ""
        salida_field.value = ""
        incapacidad_field.value = ""
        fecha_entrega_field.value = ""
        edad_field.value = ""
        motivo_field.value = ""
        medico_field.value = ""
        organismo_field.value = ""
        expediente_field.value = ""
        page.update()

    def refresh_table(filter_column=None, filter_value=None):
        # Obtener los datos actualizados
        rows = handler.get_data()

        # Filtrar los datos si se proporciona un filtro
        if filter_column and filter_value:
            column_index = [
                "N de experticia", "Fecha", "Apellido y nombre", "Salida",
                "Días de incapacidad/Recuperación", "Fecha de entrega", "Edad",
                "Motivo de la experticia", "Médico", "Organismo", "Expediente/causa"
            ].index(filter_column)

            rows = [row for row in rows if str(row[column_index]).lower() == filter_value.lower()]

        # Limpiar la tabla actual
        records_table.rows.clear()

        # Ordenar los registros en orden descendente según el campo "N de experticia"
        rows_sorted = sorted(rows, key=lambda x: float(str(x[0]).replace('.', '', 1)) if str(x[0]).replace('.', '', 1).isdigit() else float('-inf'), reverse=True)

        # Agregar los datos ordenados a la tabla
        for row in rows_sorted:
            records_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(str(cell))) for cell in row]))

        # Actualizar la tabla
        page.update()

    # Crear campos para el filtro
    filter_dropdown = ft.Dropdown(
        label="Filtrar por", 
        options=[
            ft.dropdown.Option("N de experticia"),
            ft.dropdown.Option("Fecha"),
            ft.dropdown.Option("Apellido y nombre"),
            ft.dropdown.Option("Salida"),
            ft.dropdown.Option("Días de incapacidad/Recuperación"),
            ft.dropdown.Option("Fecha de entrega"),
            ft.dropdown.Option("Edad"),
            ft.dropdown.Option("Motivo de la experticia"),
            ft.dropdown.Option("Médico"),
            ft.dropdown.Option("Organismo"),
            ft.dropdown.Option("Expediente/causa")
        ],
        width=200
    )

    filter_value_field = ft.TextField(label="Valor a buscar", width=200)

    def apply_filter(e):
        refresh_table(filter_dropdown.value, filter_value_field.value)

    filter_button = ft.ElevatedButton("Buscar", on_click=apply_filter)

    # Crear un botón de refrescar vista
    refresh_button = ft.ElevatedButton("Refrescar vista", on_click=lambda e: refresh_table())

    # Crear un layout con los campos organizados en filas
    fields_layout = ft.Column(
        [
            ft.Row([n_experticia_field, fecha_field, apellido_field, salida_field, incapacidad_field], spacing=70),
            ft.Row([fecha_entrega_field, edad_field, motivo_field, medico_field, organismo_field], spacing=70),
            ft.Row([expediente_field], spacing=70),
            add_button := ft.ElevatedButton("Agregar Datos", on_click=add_data),
            ft.ElevatedButton("Limpiar Datos", on_click=clear_fields),
            ft.Row([filter_dropdown, filter_value_field, filter_button], spacing=20),
            refresh_button,
        ],
        alignment=ft.MainAxisAlignment.START,
        scroll=ft.ScrollMode.AUTO,
        spacing=20,
    )

    # Agregar el layout con los campos y el botón
    page.add(fields_layout)

    # Crear la tabla de registros sin scroll
    records_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("N° de experticia")),
            ft.DataColumn(ft.Text("Fecha")),
            ft.DataColumn(ft.Text("Apellido y nombre")),
            ft.DataColumn(ft.Text("Salida")),
            ft.DataColumn(ft.Text("Días de incapacidad/Recuperación")),
            ft.DataColumn(ft.Text("Fecha de entrega")),
            ft.DataColumn(ft.Text("Edad")),
            ft.DataColumn(ft.Text("Motivo de la experticia")),
            ft.DataColumn(ft.Text("Médico")),
            ft.DataColumn(ft.Text("Organismo")),
            ft.DataColumn(ft.Text("Expediente/causa")),
        ],
        rows=[],
    )

    # Añadir la tabla al layout sin scroll
    page.add(records_table)

    # Cargar los datos existentes y mostrar en la tabla
    refresh_table()

if __name__ == "__main__":
    # Iniciar la aplicación
    ft.app(target=main)
