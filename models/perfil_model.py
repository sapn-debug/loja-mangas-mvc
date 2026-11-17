class PerfilModel:
    def __init__(self, client):
        self.client = client
        self.tabela = "perfis"

    def criar_perfil(self, user_id: str, nome: str):
        # Cria o perfil vinculado ao ID do usuário do Auth
        return self.client.table(self.tabela).insert({
            "id": user_id,
            "nome": nome
        }).execute()

    def buscar_por_user_id(self, user_id: str):
        # Busca o perfil pelo ID
        resp = self.client.table(self.tabela).select("*").eq("id", user_id).execute()
        if resp.data and len(resp.data) > 0:
            return resp.data[0]
        return None