# senamecf

Este repositorio contiene la aplicación de escritorio para gestionar registros de datos del sistema SENAMECF. La aplicación permite registrar, actualizar y visualizar datos médicos, utilizando un archivo de Excel para almacenar la información. Está desarrollada en Python con la biblioteca Flet para la interfaz gráfica.

## Descripción

La aplicación permite realizar las siguientes operaciones:

- **Registrar nuevos datos** en el sistema, como N° de experticia, fecha, nombre, motivo de la experticia, médico, entre otros.
- **Visualizar los registros** almacenados en una tabla, con la opción de ordenar los registros por N° de experticia.
- **Refrescar la vista** para ver los registros más recientes.

## Requisitos previos

Antes de ejecutar la aplicación, asegúrate de tener los siguientes programas instalados:

- **Python 3.10 o superior**
- **Pip** (gestor de paquetes de Python)

## Instalación

### Clonar el repositorio

1. Clona el repositorio en tu máquina local utilizando el siguiente comando:

   ```bash
   git clone https://github.com/chui24/senamecf.git
   ```

2. Entra al directorio del proyecto:

   ```bash
   cd senamecf
   ```

### Crear un entorno virtual (opcional pero recomendado)

Es recomendable crear un entorno virtual para gestionar las dependencias del proyecto. Para crear y activar un entorno virtual, sigue estos pasos:

1. Crea un entorno virtual:

   ```bash
   python3 -m venv env
   ```

2. Activa el entorno virtual:

   - En **Linux/macOS**:

     ```bash
     source env/bin/activate
     ```

   - En **Windows**:

     ```bash
     .\env\Scripts\activate
     ```

### Instalar dependencias

Con el entorno virtual activado (si es que lo estás usando), instala las dependencias desde el archivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Ejecutar la aplicación

Una vez que hayas instalado las dependencias, puedes ejecutar la aplicación con el siguiente comando:

```bash
python app.py
```

Esto abrirá la interfaz gráfica de la aplicación, donde podrás agregar y ver los registros de datos.

## Estructura del proyecto

El proyecto tiene la siguiente estructura de directorios:

```
senamecf/
│
├── app.py                  # Archivo principal para ejecutar la aplicación
├── logic/                  # Lógica para el manejo de datos
│   └── data_handler.py     # Lógica para agregar, guardar y obtener datos
├── styles/                 # Estilos de la aplicación
│   └── style.py            # Definición de estilos utilizados
├── data/                   # Carpeta para almacenar los datos (archivos Excel)
│   └── datos.xlsx          # Archivo de datos de ejemplo
├── requirements.txt        # Archivo de dependencias
└── README.md               # Este archivo
```

## Contribuciones

Si deseas contribuir al proyecto, sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature-nueva-funcion`).
3. Realiza tus cambios y haz commit (`git commit -am 'Agregada nueva funcionalidad'`).
4. Haz push a tu rama (`git push origin feature-nueva-funcion`).
5. Abre un Pull Request en GitHub.

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.

## Repositorio en GitHub

Puedes acceder al repositorio en GitHub en el siguiente enlace:

[https://github.com/chui24/senamecf.git](https://github.com/chui24/senamecf.git)