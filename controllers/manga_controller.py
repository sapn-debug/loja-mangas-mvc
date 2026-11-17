from models.manga_model import MangaModel
from controllers.auth_controller import AuthController

class MangaController:
    def __init__(self, client, auth: AuthController):
        self.auth = auth
        self.model = MangaModel(client)

    def _user_id(self):
        if not self.auth.esta_logado():
            return None
        return self.auth.usuario_atual["id"]

    def listar(self):
        uid = self._user_id()
        return self.model.listar(uid) if uid else []

    def salvar(self, categoria_id, titulo, autor, preco_txt, estoque_txt, status, manga_id=None):
        uid = self._user_id()
        if not uid:
            return False, "Sessão expirada. Faça login novamente."

        titulo = (titulo or "").strip()
        autor = (autor or "").strip()

        if len(titulo) < 2 or len(titulo) > 100:
            return False, "Título deve ter entre 2 e 100 caracteres."
        if len(autor) > 80:
            return False, "Autor deve ter no máximo 80 caracteres."

        try:
            preco = float(str(preco_txt).replace(",", "."))
        except (ValueError, TypeError):
            return False, "Preço inválido."
        if preco < 0 or preco > 10000:
            return False, "Preço deve estar entre 0 e 10.000."

        try:
            estoque = int(estoque_txt)
        except (ValueError, TypeError):
            return False, "Estoque deve ser um número inteiro."
        if estoque < 0 or estoque > 100000:
            return False, "Estoque inválido."

        if status not in ("disponivel", "esgotado", "pre_venda"):
            return False, "Status inválido."

        if manga_id:
            r = self.model.atualizar(manga_id, categoria_id, titulo, autor, preco, estoque, status)
        else:
            r = self.model.criar(uid, categoria_id, titulo, autor, preco, estoque, status)

        if r is None:
            return False, "Não foi possível salvar o mangá."
        return True, "Mangá salvo com sucesso!"

    def excluir(self, manga_id):
        if not self._user_id():
            return False, "Sessão expirada."
        if not manga_id:
            return False, "Mangá inválido."
        r = self.model.excluir(manga_id)
        if r is None:
            return False, "Não foi possível excluir."
        return True, "Mangá excluído."