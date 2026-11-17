import os
import flet as ft
from controllers.auth_controller import AuthController
from controllers.categoria_controller import CategoriaController
from controllers.manga_controller import MangaController
from views.login_view import login_view
from views.home_view import home_view
from views.categorias_view import categorias_view
from views.mangas_view import mangas_view

def main(page: ft.Page):
    page.title = "MangaStore"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    auth = AuthController()
    cat_ctrl = CategoriaController(auth.client, auth)
    manga_ctrl = MangaController(auth.client, auth)

    def ir_login():
        login_view(page, auth, on_login_success=ir_home)

    def ir_home():
        if not auth.esta_logado():
            ir_login()
            return
        home_view(page, auth, on_logout=ir_login, ir_para_categorias=ir_categorias, ir_para_mangas=ir_mangas)

    def ir_categorias():
        if not auth.esta_logado():
            ir_login()
            return
        categorias_view(page, auth, cat_ctrl, voltar_home=ir_home)

    def ir_mangas():
        if not auth.esta_logado():
            ir_login()
            return
        mangas_view(page, auth, manga_ctrl, cat_ctrl, voltar_home=ir_home)

    ir_login()

if __name__ == "__main__":
    porta = int(os.environ.get("PORT", 8080))
    ft.run(main, view=ft.AppView.WEB_BROWSER, host="127.0.0.1", port=porta)