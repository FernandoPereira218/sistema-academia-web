class Pessoa:
    def __init__(self, nome, cpf, email):
        self.nome = nome
        self.cpf = cpf
        self.email = email

    def converter_objeto(self):
        return {
            "nome": self.nome,
            "cpf": self.cpf,
            "email": self.email
        }
