class SearchHandler:
    def __init__(self, data_handler):
        self.data_handler = data_handler

    def search_by_column(self, column_name, value):
        df = self.data_handler.get_data()
        return df[df[column_name] == value]
