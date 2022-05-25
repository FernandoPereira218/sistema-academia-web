class Pessoa:
    def __init__(self, username, nome, cpf, email, senha):
        self.username = username
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.senha = senha

    def converter_objeto(self):
        return {
            "nome": self.nome,
            "cpf": self.cpf,
            "email": self.email,
            "senha": self.senha,
            "username": self.username,
            "treinamento": self.treinamento,
            "permissao": self.permissao,
        }

    def converter_json(self, dados):
        self.nome = dados.get('nome')
        self.cpf = dados.get('cpf')
        self.email = dados.get('email')
        self.senha = dados.get('senha')
        self.username = dados.get('username')
