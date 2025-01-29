import pandas as pd
import flet as ft


class DataHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        # Cargar los datos al inicializar el objeto
        try:
            self.data = pd.read_excel(file_path)
        except FileNotFoundError:
            # Si el archivo no existe, crear un DataFrame vacío con las columnas especificadas
            columns = [
                "N de experticia", "Fecha", "Apellido y nombre", "Salida", 
                "Días de incapacidad/Recuperación", "Fecha de entrega", "Edad", 
                "Motivo de la experticia", "Médico", "Organismo", "Expediente/causa"
            ]
            self.data = pd.DataFrame(columns=columns)

    def add_row(self, row):
        """Añadir una nueva fila de datos al DataFrame"""
        # Usar concat en lugar de append
        new_row = pd.DataFrame([row])
        self.data = pd.concat([self.data, new_row], ignore_index=True)

    def update_row(self, n_experticia, new_data):
        """Actualizar una fila existente en el DataFrame"""
        # Buscar la fila que coincida con el número de experticia
        index = self.data[self.data["N de experticia"] == n_experticia].index
        if not index.empty:
            # Actualizar los valores de la fila
            for key, value in new_data.items():
                self.data.at[index[0], key] = value

    def delete_row(self, n_experticia):
        """Eliminar una fila existente en el DataFrame"""
        # Buscar la fila que coincida con el número de experticia
        index = self.data[self.data["N de experticia"] == n_experticia].index
        if not index.empty:
            # Eliminar la fila
            self.data = self.data.drop(index)

    def save_data(self):
        """Guardar los datos en el archivo Excel"""
        self.data.to_excel(self.file_path, index=False)

    def get_data(self):
        """Obtener los datos como una lista de filas"""
        # Convertir cada fila del DataFrame en una lista
        return self.data.values.tolist()


    def export_data(self, page):
        """Exportar los datos a un archivo Excel usando FilePicker."""

        def save_file_result(e: ft.FilePickerResultEvent):
            if e.path:
                file_path = e.path if e.path.endswith(".xlsx") else e.path + ".xlsx"
                self.data.to_excel(file_path, index=False)
                print(f"Datos exportados a: {file_path}")
                page.snack_bar = ft.SnackBar(ft.Text(f"Archivo guardado en {file_path}"))
                page.snack_bar.open = True
                page.update()
            else:
                print("Exportación cancelada.")

        save_file_dialog = ft.FilePicker(on_result=save_file_result)
        page.overlay.append(save_file_dialog)
        page.update()

        # Mostrar diálogo de guardado
        save_file_dialog.save_file(allowed_extensions=["xlsx"])


    
    def import_data(self, page, refresh_callback):
        """Importar datos desde un archivo Excel usando el selector de archivos de Flet."""

        def handle_import_result(event):
            """Manejar la importación del archivo seleccionado."""
            if event.files:
                file_path = event.files[0].path  # Obtener la ruta del archivo seleccionado
                self.data = pd.read_excel(file_path)  # Leer el archivo Excel
                self.save_data()  # Guardar los datos cargados en el archivo
                refresh_callback()  # Llamar a la función de refresco de la tabla

        file_picker = ft.FilePicker(on_result=handle_import_result)  # Pasar la función corregida
        page.add(file_picker)  # Asegurar que el FilePicker se agregue a la página
        file_picker.pick_files(allow_multiple=False, file_type="*.xlsx")



    def handle_import_result(self, event):
        """Manejar la importación del archivo seleccionado."""
        if event.files:
            file_path = event.files[0].path  # Obtener la ruta del archivo seleccionado
            self.data = pd.read_excel(file_path)  # Leer el archivo Excel
            self.save_data()  # Guardar los datos cargados en el archivo
            
            # Actualizar los datos filtrados antes de refrescar la tabla
            global filtered_data
            filtered_data = self.get_data()  # Asegurar que filtered_data tenga los datos más recientes
    
            # Refrescar la vista
            refresh_callback()
