class Exercicio:
    def __init__(self, nome):
        self.nome = nome


    def converter_objeto(self):
        return {
            "Nome": self.nome,
        }