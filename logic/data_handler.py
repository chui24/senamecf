import pandas as pd
from datetime import datetime

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
            self.data.to_excel(custom_path, index=False)
        else:
            self.data.to_excel(self.file_path, index=False)

    def get_data(self):
        """Obtener los datos como una lista de filas"""
        # Convertir cada fila del DataFrame en una lista
        return self.data.values.tolist()

    def import_data(self, import_path):
        """
        Importar datos desde otro archivo Excel.
        :param import_path: Ruta del archivo Excel a importar.
        """
        try:
            # Guardar el archivo actual antes de importar
            self.save_data()
            print(f"Archivo actual guardado en: {self.file_path}")

            # Leer el archivo Excel a importar
            new_data = pd.read_excel(import_path)
            # Reemplazar los datos actuales con los nuevos
            self.data = new_data
            # Guardar los datos reemplazados en el archivo original
            self.save_data()
            print(f"Datos importados correctamente desde {import_path}")
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