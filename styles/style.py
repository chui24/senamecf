import flet as ft

def apply_styles(page: ft.Page):
    # Configurar tema oscuro o claro
    page.theme_mode = "light"  # Cambiar a "dark" si prefieres el tema oscuro
    
    # Configuración adicional de colores
    page.theme = ft.Theme(color_scheme_seed=ft.colors.BLUE)
    
    # Alineación de la página
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
