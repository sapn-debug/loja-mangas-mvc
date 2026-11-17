class MangaModel:
    def __init__(self, client):
        self.client = client

    def listar(self, user_id: str):
        try:
            resp = self.client.table("mangas").select(
                "*, categorias(nome)"
            ).eq("user_id", user_id).order("titulo").execute()
            return resp.data or []
        except Exception:
            return []

    def criar(self, user_id: str, categoria_id, titulo, autor, preco, estoque, status):
        try:
            return self.client.table("mangas").insert({
                "user_id": user_id,
                "categoria_id": categoria_id,
                "titulo": titulo.strip(),
                "autor": autor.strip(),
                "preco": preco,
                "estoque": estoque,
                "status": status
            }).execute()
        except Exception:
            return None

    def atualizar(self, manga_id, categoria_id, titulo, autor, preco, estoque, status):
        try:
            return self.client.table("mangas").update({
                "categoria_id": categoria_id,
                "titulo": titulo.strip(),
                "autor": autor.strip(),
                "preco": preco,
                "estoque": estoque,
                "status": status
            }).eq("id", manga_id).execute()
        except Exception:
            return None

    def excluir(self, manga_id):
        try:
            return self.client.table("mangas").delete().eq("id", manga_id).execute()
        except Exception:
            return None