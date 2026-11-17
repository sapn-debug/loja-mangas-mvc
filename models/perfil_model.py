class PerfilModel:
    def __init__(self, client):
        self.client = client

    def criar_perfil(self, user_id: str, nome: str):
        try:
            return self.client.table("perfis").insert({
                "user_id": user_id,
                "nome": nome.strip()
            }).execute()
        except Exception:
            return None

    def buscar_por_user_id(self, user_id: str):
        try:
            resp = self.client.table("perfis").select("*").eq("user_id", user_id).execute()
            return resp.data[0] if resp.data else None
        except Exception:
            return None