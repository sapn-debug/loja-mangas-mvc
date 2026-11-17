from models.categoria_model import CategoriaModel
from controllers.auth_controller import AuthController

class CategoriaController:
    def __init__(self, client, auth: AuthController):
        self.auth = auth
        self.model = CategoriaModel(client)

    def _user_id(self):
        if not self.auth.esta_logado():
            return None
        return self.auth.usuario_atual["id"]

    def listar(self):
        uid = self._user_id()
        if not uid:
            return []
        return self.model.listar(uid)

    def salvar(self, nome, descricao, cat_id=None):
        uid = self._user_id()
        if not uid:
            return False, "Sessão expirada. Faça login novamente."

        nome = (nome or "").strip()
        descricao = (descricao or "").strip()

        if len(nome) < 2 or len(nome) > 50:
            return False, "O nome deve ter entre 2 e 50 caracteres."
        if len(descricao) > 200:
            return False, "A descrição deve ter no máximo 200 caracteres."

        if cat_id:
            r = self.model.atualizar(cat_id, nome, descricao)
        else:
            r = self.model.criar(uid, nome, descricao)

        if r is None:
            return False, "Não foi possível salvar a categoria."
        return True, "Categoria salva com sucesso!"

    def excluir(self, cat_id):
        if not self._user_id():
            return False, "Sessão expirada."
        if not cat_id:
            return False, "Categoria inválida."
        r = self.model.excluir(cat_id)
        if r is None:
            return False, "Não foi possível excluir."
        return True, "Categoria excluída."