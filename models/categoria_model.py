class CategoriaModel:
    def __init__(self, client):
        self.client = client

    def listar(self, user_id: str):
        try:
            resp = self.client.table("categorias").select("*").eq("user_id", user_id).order("nome").execute()
            return resp.data or []
        except Exception:
            return []

    def criar(self, user_id: str, nome: str, descricao: str):
        try:
            return self.client.table("categorias").insert({
                "user_id": user_id,
                "nome": nome.strip(),
                "descricao": descricao.strip()
            }).execute()
        except Exception:
            return None

    def atualizar(self, cat_id: str, nome: str, descricao: str):
        try:
            return self.client.table("categorias").update({
                "nome": nome.strip(),
                "descricao": descricao.strip()
            }).eq("id", cat_id).execute()
        except Exception:
            return None

    def excluir(self, cat_id: str):
        try:
            return self.client.table("categorias").delete().eq("id", cat_id).execute()
        except Exception:
            return None