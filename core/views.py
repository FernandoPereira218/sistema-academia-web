import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

import manage
from classes.Aluno import Aluno
from classes.Exercicio import Exercicio
from classes.Pessoa import Pessoa
from classes.Professor import Professor

cred = credentials.Certificate('sistema-academia-db-auth.json')
firebase_admin.initialize_app(cred)

db = firestore.client()


# current_user = None
# Create your views here.
def login_page(request):
    return render(request, 'login_page.html')


def teste_db(request):
    # doc_ref = db.collection(u'users').document(u'nomenovo')
    # doc_ref.set({
    #    u'username': u'adad',
    #    u'lastname': u'123',
    #    u'born': 4567
    # })
    users_ref = db.collection(u'users')
    docs = users_ref.stream()

    for doc in docs:
        print(f'{doc.id} => {doc.to_dict()}')
    return render(request, 'added_file.html')


def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        users_collection = db.collection('Professor')
        query = users_collection.where('username', '==', username).get()

        if len(query) == 1:
            for doc in query:
                if doc.get('username') == username and doc.get('senha') == password:
                    # login(request, doc)

                    manage.current_user = set_current_user(doc)
                    # return render(request, 'main_page.html', dados)
                    return redirect('/principal/')
    # doc = doc_ref.get()
    # if doc.exists:
    #    print(f'Document data: {doc.to_dict()}')
    return redirect('/')


def main_page(request):
    dados = {'current_user': manage.current_user}
    return render(request, 'main_page.html', dados)


def add_user(request):
    return render(request, 'create_new_user_page.html')


def submit_user(request, db_collection='Professor'):
    if request.POST:
        username = request.POST.get('username')
        name = request.POST.get('fullname')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        cpf = request.POST.get('cpf')
        email = request.POST.get('email')
        users_collection = db.collection(db_collection)
        query = users_collection.where('username', '==', username).get()
        if len(query) != 0:
            return redirect('/')

        if password == confirm_password:
            if db_collection == 'Professor':
                pessoa = Professor(nome=name, cpf=cpf, email=email, senha=password, username=username)
            else:
                pessoa = Aluno(nome=name, cpf=cpf, email=email, senha=password, username=username)
            obj = pessoa.converter_objeto()
            doc_ref = db.collection(db_collection).document()
            doc_ref.set(obj)
        else:
            raise Exception("erro de senha")

    return redirect('/')


def logout_user(request):
    manage.current_user = None
    return redirect('/')


def set_current_user(data):
    usuario = Pessoa(
        username=data.get('username'),
        senha=data.get('senha'),
        cpf=data.get('cpf'),
        email=data.get('email'),
        nome=data.get('nome')
    )
    return usuario


def cadastrar_aluno(request):
    return render(request, 'register_student.html')


def submit_aluno(request):
    submit_user(request, 'Aluno')
    return redirect('/')


def consultar_aluno(request):
    teste = db.collection('Aluno').get()
    lista = []
    for doc in teste:
        temp = Pessoa(
            username=doc.get('username'),
            nome=doc.get('nome'),
            senha=doc.get('senha'),
            cpf=doc.get('cpf'),
            email=doc.get('email')
        )
        temp.id = doc.id
        lista.append(temp)
    dados = {'student_list': lista}
    return render(request, 'search_student.html', dados)


def buscar_aluno(request, id_aluno):
    doc_ref = db.collection('Aluno').document(id_aluno).get()
    if doc_ref is None:
        return redirect('/')
    dados = {}
    temp = Pessoa(
        username=doc_ref.get('username'),
        nome=doc_ref.get('nome'),
        senha=doc_ref.get('senha'),
        cpf=doc_ref.get('cpf'),
        email=doc_ref.get('email')
    )
    temp.id = doc_ref.id
    dados['aluno'] = temp
    return render(request, 'student_page.html', dados)


def criar_treino(request, id_aluno):
    doc_ref = db.collection('Aluno').document(id_aluno).get()
    temp = Pessoa(
        username=doc_ref.get('username'),
        nome=doc_ref.get('nome'),
        senha=doc_ref.get('senha'),
        cpf=doc_ref.get('cpf'),
        email=doc_ref.get('email')
    )
    temp.id = doc_ref.id
    exercicios = db.collection('Exercicio').get()
    lista_exercicios = []
    for doc in exercicios:
        exercicio = Exercicio()
        exercicio.nome = doc.get('Nome')
        lista_exercicios.append(exercicio)
    dados = {
        'aluno': temp,
        'exercicios': lista_exercicios
    }
    return render(request, 'add_practice.html', dados)


def submit_treino(request, id_aluno):
    if request.POST:
        exercicios = request.POST.getlist('exercicios')
        series = request.POST.getlist('series')
        repeticoes = request.POST.getlist('repeticoes')
        treinamento = []
        for i in range(len(exercicios)):
            treinamento.append({
                'Exercicio': exercicios[i],
                'Series': series[i],
                'Repeticoes': repeticoes[i],
            })

    aluno = db.collection('Aluno').document(id_aluno).get()
    temp = Pessoa(
        username=aluno.get('username'),
        nome=aluno.get('nome'),
        senha=aluno.get('senha'),
        cpf=aluno.get('cpf'),
        email=aluno.get('email')
    )
    temp.treinamento = treinamento
    objeto = temp.converter_objeto()
    doc_ref = db.collection('Aluno').document(id_aluno)
    doc_ref.set(objeto)
    return redirect('/consulta_aluno/' + id_aluno)
