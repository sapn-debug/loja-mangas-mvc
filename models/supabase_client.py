import os
from supabase import create_client, Client

def get_client() -> Client:
    # Pega as variáveis de ambiente configuradas no Render
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    
    # Validação para evitar erro se esquecer de configurar no Render
    if not url or not key:
        raise ValueError("ERRO: As variáveis SUPABASE_URL e SUPABASE_KEY não estão configuradas no ambiente.")
        
    return create_client(url, key)