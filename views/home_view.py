import flet as ft

def home_view(page: ft.Page, auth, on_logout, ir_para_categorias, ir_para_mangas):
    if not auth.esta_logado():
        on_logout()
        return

    page.clean()
    page.title = "MangaStore - Início"
    nome = (auth.perfil or {}).get("nome", "Usuário")

    def sair(e):
        auth.logout()
        on_logout()

    page.add(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(f"📚 Olá, {nome}!", size=24, weight=ft.FontWeight.BOLD),
                        ft.Container(expand=True),
                        ft.OutlinedButton("Sair", icon=ft.Icons.LOGOUT, on_click=sair),
                    ]
                ),
                ft.Divider(),
                ft.Text("O que deseja fazer?", size=16),
                ft.Row(
                    [
                        ft.Button("📂 Gerenciar Categorias", width=250, height=60, on_click=lambda e: ir_para_categorias(), bgcolor=ft.Colors.PURPLE_300, color="white"),
                        ft.Button("📖 Gerenciar Mangás", width=250, height=60, on_click=lambda e: ir_para_mangas(), bgcolor=ft.Colors.PURPLE_500, color="white"),
                    ],
                    spacing=20,
                ),
            ],
            spacing=20,
        )
    )
    page.update()