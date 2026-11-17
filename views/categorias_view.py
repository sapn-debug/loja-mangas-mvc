import flet as ft

def categorias_view(page: ft.Page, auth, cat_ctrl, voltar_home):
    if not auth.esta_logado():
        voltar_home()
        return

    page.clean()
    page.title = "MangaStore - Categorias"
    lista_col = ft.Column(spacing=8)
    editando_id = {"valor": None}

    nome_in = ft.TextField(label="Nome da categoria", width=300)
    desc_in = ft.TextField(label="Descrição", width=300)
    msg = ft.Text(size=13)

    def render_lista():
        lista_col.controls.clear()
        dados = cat_ctrl.listar()
        if not dados:
            lista_col.controls.append(ft.Text("Nenhuma categoria cadastrada.", italic=True, color=ft.Colors.GREY_600))
        else:
            for c in dados:
                lista_col.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Column([ft.Text(c["nome"], weight=ft.FontWeight.BOLD, size=15), ft.Text(c.get("descricao") or "—", size=12, color=ft.Colors.GREY_600)], expand=True),
                            ft.IconButton(ft.Icons.EDIT, icon_color=ft.Colors.BLUE_400, on_click=lambda e, cat=c: preparar_edicao(cat)),
                            ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED_400, on_click=lambda e, cat=c: pedir_exclusao(cat)),
                        ]),
                        padding=10, bgcolor=ft.Colors.GREY_100, border_radius=8,
                    )
                )
        page.update()

    def preparar_edicao(cat):
        editando_id["valor"] = cat["id"]
        nome_in.value = cat["nome"]
        desc_in.value = cat.get("descricao") or ""
        msg.value = "Editando categoria..."
        msg.color = ft.Colors.BLUE_400
        page.update()

    def salvar(e):
        ok, texto = cat_ctrl.salvar(nome_in.value, desc_in.value, editando_id["valor"])
        msg.value = texto
        msg.color = ft.Colors.GREEN_600 if ok else ft.Colors.RED_400
        if ok:
            nome_in.value = ""
            desc_in.value = ""
            editando_id["valor"] = None
            render_lista()
        page.update()

    def pedir_exclusao(cat):
        def confirmar(e):
            ok, texto = cat_ctrl.excluir(cat["id"])
            page.pop_dialog()
            msg.value = texto
            msg.color = ft.Colors.GREEN_600 if ok else ft.Colors.RED_400
            render_lista()
            page.update()
            
        def cancelar(e):
            page.pop_dialog()
            page.update()

        dlg = ft.AlertDialog(
            title=ft.Text("Confirmar exclusão"), 
            content=ft.Text(f'Deseja excluir a categoria "{cat["nome"]}"?'), 
            actions=[ft.TextButton("Cancelar", on_click=cancelar), ft.TextButton("Excluir", on_click=confirmar)]
        )
        page.show_dialog(dlg)

    page.add(ft.Column([
        ft.Row([ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: voltar_home()), ft.Text("📂 Categorias de Mangá", size=22, weight=ft.FontWeight.BOLD)]),
        ft.Divider(), ft.Row([nome_in, desc_in, ft.Button("Salvar", on_click=salvar, bgcolor=ft.Colors.PURPLE_400, color="white")], spacing=10),
        msg, ft.Divider(), ft.Text("Suas categorias:", weight=ft.FontWeight.BOLD), lista_col,
    ], spacing=15))
    render_lista()