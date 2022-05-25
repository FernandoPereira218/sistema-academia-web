from classes.Pessoa import Pessoa


class Professor(Pessoa):
    def __init__(self, username, nome, cpf, email, senha):
        self.username = username
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.senha = senha
        self.permissao = 'professor'