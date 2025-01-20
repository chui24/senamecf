import pandas as pd

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

    def save_data(self):
        """Guardar los datos en el archivo Excel"""
        self.data.to_excel(self.file_path, index=False)

    def get_data(self):
        """Obtener los datos como una lista de filas"""
        # Convertir cada fila del DataFrame en una lista
        return self.data.values.tolist()
