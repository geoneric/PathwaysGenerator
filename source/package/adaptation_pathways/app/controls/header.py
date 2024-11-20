import flet as ft
import theme

class Header(ft.Container):
    def __init__(
        self, 
        icon=None, 
        text="", 
        size=16, 
        expand=True,
        color=theme.colors.primary_dark,
        padding=0, 
        border_radius=0, 
        border: ft.Border | None = None,
        bgcolor:str | None = None
    ):
        super().__init__(
            height=(size + 2*padding),
            padding=padding,
            expand=expand,
            bgcolor=bgcolor,
            border_radius=border_radius,
            border=border
        )
        
        header_text_style = ft.TextStyle(
            size=size,
            height=1,
            color=color,
            weight=ft.FontWeight.W_600,
        )

        if icon is not None:
            self.content = ft.Row(
                expand=expand,
                controls=[
                    ft.Image(icon, width=size, height=size, color=color),
                    ft.Text(text, style=header_text_style)
                ], 
                spacing=4,            
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            )
        else:
            self.content=ft.Row(
                expand=True,
                controls=[
                    ft.Text(text, style=header_text_style)
                ]
            )

