import pandas as pd
from datetime import datetime
import flet as ft
import os 


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
        self.save_data()  # Guardar automáticamente después de agregar una fila

    def update_row(self, n_experticia, new_data):
        """Actualizar una fila existente en el DataFrame"""
        # Buscar la fila que coincida con el número de experticia
        index = self.data[self.data["N de experticia"] == n_experticia].index
        if not index.empty:
            # Actualizar los valores de la fila
            for key, value in new_data.items():
                self.data.at[index[0], key] = value
            self.save_data()  # Guardar automáticamente después de actualizar una fila

    def delete_row(self, n_experticia):
        """Eliminar una fila existente en el DataFrame"""
        # Buscar la fila que coincida con el número de experticia
        index = self.data[self.data["N de experticia"] == n_experticia].index
        if not index.empty:
            # Eliminar la fila
            self.data = self.data.drop(index)
            self.save_data()  # Guardar automáticamente después de eliminar una fila

    def save_data(self, custom_path=None):
        """
        Guardar los datos en el archivo Excel.
        :param custom_path: Ruta personalizada para guardar el archivo (opcional).
        """
        if custom_path:
            save_path = custom_path
        else:
            save_path = self.file_path

        # Crear la carpeta si no existe
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        self.data.to_excel(save_path, index=False)



    def get_data(self):
        """Obtener los datos como una lista de filas"""
        # Convertir cada fila del DataFrame en una lista
        return self.data.values.tolist()

    def import_data(self, file_path):
        """Importar datos desde un archivo Excel."""
        try:
            new_data = pd.read_excel(file_path)
            self.data = new_data  # Reemplazar los datos actuales con los nuevos
            self.save_data()  # Guardar los datos importados en el archivo actual
            print(f"Datos importados correctamente desde {file_path}")
        except Exception as e:
            print(f"Error al importar datos: {e}")


    def _generate_backup_path(self):
        """
        Generar una ruta única para el backup del archivo actual.
        :return: Ruta del archivo de backup.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.file_path.replace(".xlsx", f"_backup_{timestamp}.xlsx")
        return backup_path
    
    def export_data(self, file_path):
        """Guarda los datos en un archivo Excel en la ubicación especificada."""
        try:
            self.data.to_excel(file_path, index=False)  
            print(f"✅ Archivo exportado a: {file_path}")  # Debug en consola
        except Exception as e:
            print(f"❌ Error al exportar archivo: {e}")


def open_save_file_dialog(page: ft.Page, on_file_selected):
    """Abrir un cuadro de diálogo para seleccionar la ubicación de guardado."""
    file_picker = ft.FilePicker(on_result=on_file_selected)
    page.overlay.append(file_picker)
    page.update()
    file_picker.save_file(allowed_extensions=["xlsx"])