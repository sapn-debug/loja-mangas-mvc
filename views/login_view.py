import flet as ft

def login_view(page: ft.Page, auth, on_login_success):
    page.clean()
    page.title = "MangaStore - Login"

    email = ft.TextField(label="E-mail", width=350, autofocus=True)
    senha = ft.TextField(label="Senha", password=True, can_reveal_password=True, width=350)
    nome = ft.TextField(label="Nome (apenas no cadastro)", width=350)
    msg = ft.Text(color=ft.Colors.RED_400, size=13)

    def fazer_login(e):
        ok, texto = auth.login(email.value, senha.value)
        if ok:
            on_login_success()
        else:
            msg.value = texto
            msg.color = ft.Colors.RED_400
            page.update() # A atualização manual ainda é necessária para o campo de erro

    def fazer_cadastro(e):
        ok, texto = auth.cadastrar(email.value, senha.value, nome.value)
        if ok:
            on_login_success()
        else:
            msg.value = texto
            msg.color = ft.Colors.RED_400
            page.update()

    card = ft.Container(
        content=ft.Column(
            [
                ft.Text("📚 MangaStore", size=32, weight=ft.FontWeight.BOLD),
                ft.Text("Gerencie sua loja de mangás", size=14, color=ft.Colors.GREY_600),
                ft.Divider(height=20, color="transparent"),
                email, senha, nome,
                ft.Row(
                    [
                        ft.Button("Entrar", on_click=fazer_login, width=160, bgcolor=ft.Colors.PURPLE_400, color="white"),
                        ft.OutlinedButton("Cadastrar", on_click=fazer_cadastro, width=160),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=15,
                ),
                msg,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12,
        ),
        padding=35,
        bgcolor=ft.Colors.WHITE,
        border_radius=15,
        shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.BLACK_12),
    )

    page.add(ft.Row([card], alignment=ft.MainAxisAlignment.CENTER))
    page.update()