import flet as ft

def mangas_view(page: ft.Page, auth, manga_ctrl, cat_ctrl, voltar_home):
    if not auth.esta_logado():
        voltar_home()
        return

    page.clean()
    page.title = "MangaStore - Mangás"
    lista_col = ft.Column(spacing=8)
    editando_id = {"valor": None}

    cats = cat_ctrl.listar()
    opcoes = [ft.DropdownOption(key="", text="— Sem categoria —")] + [ft.DropdownOption(key=c["id"], text=c["nome"]) for c in cats]

    titulo_in = ft.TextField(label="Título", width=250)
    autor_in = ft.TextField(label="Autor", width=200)
    cat_in = ft.Dropdown(label="Categoria", width=200, options=opcoes, value="")
    preco_in = ft.TextField(label="Preço (R$)", width=130)
    estoque_in = ft.TextField(label="Estoque", width=110)
    
    status_in = ft.Dropdown(
        label="Status", width=160, value="disponivel", 
        options=[ft.DropdownOption("disponivel", "Disponível"), ft.DropdownOption("esgotado", "Esgotado"), ft.DropdownOption("pre_venda", "Pré-venda")]
    )
    msg = ft.Text(size=13)

    def render_lista():
        lista_col.controls.clear()
        dados = manga_ctrl.listar()
        if not dados:
            lista_col.controls.append(ft.Text("Nenhum mangá cadastrado.", italic=True, color=ft.Colors.GREY_600))
        else:
            for m in dados:
                cat_nome = (m.get("categorias") or {}).get("nome") or "Sem categoria"
                lista_col.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Column([ft.Text(f'{m["titulo"]}  —  {m.get("autor") or "—"}', weight=ft.FontWeight.BOLD, size=15), ft.Text(f'Categoria: {cat_nome}  •  R$ {m.get("preco", 0):.2f}  •  Estoque: {m.get("estoque", 0)}  •  {m.get("status","")}', size=12, color=ft.Colors.GREY_600)], expand=True),
                            ft.IconButton(ft.Icons.EDIT, icon_color=ft.Colors.BLUE_400, on_click=lambda e, mg=m: preparar_edicao(mg)),
                            ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED_400, on_click=lambda e, mg=m: pedir_exclusao(mg)),
                        ]),
                        padding=10, bgcolor=ft.Colors.GREY_100, border_radius=8,
                    )
                )
        page.update()

    def preparar_edicao(m):
        editando_id["valor"] = m["id"]
        titulo_in.value = m["titulo"]
        autor_in.value = m.get("autor") or ""
        cat_in.value = m.get("categoria_id") or ""
        preco_in.value = str(m.get("preco", 0))
        estoque_in.value = str(m.get("estoque", 0))
        status_in.value = m.get("status", "disponivel")
        msg.value = "Editando mangá..."
        msg.color = ft.Colors.BLUE_400
        page.update()

    def salvar(e):
        ok, texto = manga_ctrl.salvar(cat_in.value or None, titulo_in.value, autor_in.value, preco_in.value, estoque_in.value, status_in.value, editando_id["valor"])
        msg.value = texto
        msg.color = ft.Colors.GREEN_600 if ok else ft.Colors.RED_400
        if ok:
            titulo_in.value = ""
            autor_in.value = ""
            cat_in.value = ""
            preco_in.value = ""
            estoque_in.value = ""
            status_in.value = "disponivel"
            editando_id["valor"] = None
            render_lista()
        page.update()

    def pedir_exclusao(m):
        def confirmar(e):
            ok, texto = manga_ctrl.excluir(m["id"])
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
            content=ft.Text(f'Deseja excluir o mangá "{m["titulo"]}"?'), 
            actions=[ft.TextButton("Cancelar", on_click=cancelar), ft.TextButton("Excluir", on_click=confirmar)]
        )
        page.show_dialog(dlg)

    page.add(ft.Column([
        ft.Row([ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: voltar_home()), ft.Text("📖 Cadastro de Mangás", size=22, weight=ft.FontWeight.BOLD)]),
        ft.Divider(), ft.Row([titulo_in, autor_in, cat_in], spacing=10, wrap=True),
        ft.Row([preco_in, estoque_in, status_in, ft.Button("Salvar", on_click=salvar, bgcolor=ft.Colors.PURPLE_500, color="white")], spacing=10, wrap=True),
        msg, ft.Divider(), ft.Text("Seus mangás:", weight=ft.FontWeight.BOLD), lista_col,
    ], spacing=15))
    render_lista()