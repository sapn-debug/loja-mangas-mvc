from models.supabase_client import get_client
from models.perfil_model import PerfilModel

class AuthController:
    def __init__(self):
        self.client = get_client()
        self.usuario_atual = None
        self.perfil = None
        self.perfil_model = PerfilModel(self.client)

    def cadastrar(self, email: str, senha: str, nome: str):
        email = (email or "").strip()
        nome = (nome or "").strip()

        # Validações básicas
        if "@" not in email or len(email) < 5:
            return False, "Informe um e-mail válido."
        if len(senha) < 6:
            return False, "A senha deve ter no mínimo 6 caracteres."
        if len(nome) < 3 or len(nome) > 80:
            return False, "O nome deve ter entre 3 e 80 caracteres."

        try:
            # 1. Tenta criar o usuário no Supabase Auth
            resp = self.client.auth.sign_up({"email": email, "password": senha})
            
            if resp.user is None:
                return False, "Não foi possível criar a conta."

            # 2. Tenta fazer o login automático
            try:
                login_resp = self.client.auth.sign_in_with_password({"email": email, "password": senha})
                user = login_resp.user
            except Exception as e_login:
                print(f"\n[Aviso] Conta criada, mas o login automático falhou: {e_login}")
                return True, "Conta criada! Verifique seu e-mail para confirmar e depois faça login."
            
            # 3. Tenta salvar o perfil na tabela 'perfis' separadamente
            # Se der erro aqui, não cancela o cadastro do usuário.
            try:
                self.perfil_model.criar_perfil(user.id, nome)
            except Exception as e_perfil:
                print(f"\n[Aviso] Usuário criado, mas erro ao salvar perfil: {e_perfil}")
                # Mesmo sem o perfil, o login foi feito, então deixamos passar

            self.usuario_atual = {"id": user.id, "email": user.email}
            self.perfil = {"nome": nome}
            
            return True, "Conta criada e login realizado com sucesso!"

        except Exception as e:
            print("\n" + "="*40)
            print("--- ERRO REAL DO SUPABASE AO CADASTRAR ---")
            print(e)
            print("="*40 + "\n")
            
            erro_str = str(e).lower()
            if "already registered" in erro_str or "already exists" in erro_str:
                return False, "Este e-mail já está cadastrado."
            elif "rate limit" in erro_str:
                return False, "Muitas tentativas. Aguarde um minuto e tente novamente."
            elif "api key" in erro_str or "invalid" in erro_str:
                return False, "Erro de configuração no servidor (chave do Supabase)."
            else:
                return False, "Não foi possível cadastrar. Verifique os dados."

    def login(self, email: str, senha: str):
        email = (email or "").strip()
        if not email or not senha:
            return False, "E-mail ou senha inválidos."

        try:
            resp = self.client.auth.sign_in_with_password({"email": email, "password": senha})
            if resp.user is None:
                return False, "E-mail ou senha inválidos."
            self.usuario_atual = {"id": resp.user.id, "email": resp.user.email}
            self.perfil = self.perfil_model.buscar_por_user_id(resp.user.id) or {"nome": "Usuário"}
            return True, "Login realizado com sucesso!"
        except Exception as e:
            print(f"\n--- ERRO AO FAZER LOGIN --- \n{e}\n")
            return False, "E-mail ou senha inválidos."

    def logout(self):
        try:
            self.client.auth.sign_out()
        except Exception:
            pass
        self.usuario_atual = None
        self.perfil = None

    def esta_logado(self) -> bool:
        return self.usuario_atual is not None