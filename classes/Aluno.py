import firebase_admin
from firebase_admin import firestore, credentials
from django.template.defaulttags import register

import core
from classes.Pessoa import Pessoa


class Aluno(Pessoa):
    def __init__(self, username, nome, cpf, email, senha, matricula):
        self.username = username
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.senha = senha
        self.treinamento = {
            "Segunda": [],
            "Terça": [],
            "Quarta": [],
            "Quinta": [],
            "Sexta": [],
            "Sábado": [],
            "Domingo": [],
        }
        self.permissao = 'aluno'
        self.matricula = matricula

    @register.filter
    def get_treino(self, dia_semana):
        temp = core.views.db.collection('Aluno').document(self.id).get()
        treinamento = temp.get('treinamento')
        treino_dia = treinamento[dia_semana]
        return {
            "treino": treino_dia
        }

    @register.filter
    def get_exercicio(self, dia_semana):
        temp = core.views.db.collection('Aluno').document(self.id).get()
        treinamento = temp.get('treinamento')
        treino_dia = treinamento[dia_semana]
        return {
            "treino": treino_dia
        }

    def converter_objeto(self):
        return {
            "nome": self.nome,
            "cpf": self.cpf,
            "email": self.email,
            "senha": self.senha,
            "username": self.username,
            "treinamento": self.treinamento,
            "permissao": self.permissao,
            "matricula": self.matricula,
        }