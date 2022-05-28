from classes.Pessoa import Pessoa


class Admin(Pessoa):
    def __init__(self, username, nome, cpf, email, senha, matricula):
        self.username = username
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.senha = senha
        self.permissao = 'admin'
        self.matricula = matricula

    def converter_objeto(self):
        return {
            "nome": self.nome,
            "cpf": self.cpf,
            "email": self.email,
            "senha": self.senha,
            "username": self.username,
            "permissao": self.permissao,
            "matricula": self.matricula,
        }