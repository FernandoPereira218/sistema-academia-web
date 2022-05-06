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
from classes.Pessoa import Pessoa
from classes.Professor import Professor

cred = credentials.Certificate('sistema-academia-db-auth.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

#current_user = None
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
                    #login(request, doc)

                    manage.current_user = set_current_user(doc)
                    #return render(request, 'main_page.html', dados)
                    return redirect('/principal/')
    # doc = doc_ref.get()
    # if doc.exists:
    #    print(f'Document data: {doc.to_dict()}')
    return redirect('/')


def main_page(request):
    dados = {}
    dados['current_user'] = manage.current_user
    return render(request, 'main_page.html', dados)


def add_user(request):
    return render(request, 'create_new_user_page.html')


def submit_user(request):
    if request.POST:
        username = request.POST.get('username')
        name = request.POST.get('fullname')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        cpf = request.POST.get('cpf')
        email = request.POST.get('email')
        users_collection = db.collection('Professor')
        query = users_collection.where('username', '==', username).get()
        if len(query) != 0:
            return redirect('/')

        if password == confirm_password:
            pessoa = Professor(nome=name, cpf=cpf, email=email, senha=password, username=username)
            obj = pessoa.converter_objeto()
            doc_ref = db.collection('Professor').document()
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