import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from classes.Pessoa import Pessoa

cred = credentials.Certificate('sistema-academia-db-auth.json')
firebase_admin.initialize_app(cred)

db = firestore.client()


# Create your views here.
def login_page(request):
    return render(request, 'login_page.html')


def teste_db(request):
    #doc_ref = db.collection(u'users').document(u'nomenovo')
    #doc_ref.set({
    #    u'username': u'adad',
    #    u'lastname': u'123',
    #    u'born': 4567
    #})
    users_ref = db.collection(u'users')
    docs = users_ref.stream()

    for doc in docs:
        print(f'{doc.id} => {doc.to_dict()}')
    return render(request, 'added_file.html')


def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        doc_ref = db.collection('users').document('doc1')
        doc = doc_ref.get()
        if doc.exists:
            print(f'Document data: {doc.to_dict()}')
    return redirect('/')


def main_page(request):
    return render(request, 'add_user_page.html')


def add_user(request):
    return render(request, 'create_new_user_page.html')


def submit_user(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        pessoa = Pessoa(nome=username, cpf=password, email='')

        teste = pessoa.converter_objeto()
        doc_ref = db.collection('Pessoa').document()
        doc_ref.set(teste)
    return redirect('/')