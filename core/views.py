import json
import mimetypes
import os

from django.http import HttpResponse
from django.shortcuts import render, redirect
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

import manage
from classes.Admin import Admin
from classes.Aluno import Aluno
from classes.Exercicio import Exercicio
from classes.Pessoa import Pessoa
from classes.Professor import Professor
from classes.Treino import Treino
from classes.Utils import Utils

# cred = credentials.Certificate('sistema-academia-db-auth.json')
cred = credentials.Certificate({
    "type": "service_account",
    "project_id": "sistema-academia-aee3a",
    "private_key_id": "3456745efd700455ebd52e35c24f7974694249b5",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDSHZA1Se7RRNWi\n6bQIn70njBa9xQ2TeNX0gM2ts3QM2tr2K3nHAUhjjbMcjbXNHysbnDHDnLcLpkMl\n8jgqiXAQIUTtl4Dr3gBJ/34otxOgsv2MYJuh4YXLgouWW3MzWLma+IIvNOMTzai1\n0HgJXJWG+pqdJWYOSfrbc00PbBdpwwnqU5pDuHYVmjtEIBn5iqQDr81xPU1wrZdM\nIcluYbtwPnyScR3ZPBrHgNlpKZCT2+v0Jdfhkn42kPCubVWGoLQVSnbxDq0cBxIK\n7YWbD543c1ghLBiqK8rC1+cG5APXgoIBtVsEM+3A4DX0ylXxp/x2CdwjtwKeFKNA\nwEmpDtLVAgMBAAECggEAFpsdp84ThqpcPdHdD8x34mhdDf/EbShkBJFTD6wuATAO\nvMuCp5mIu0VEjv7kH3SKA8dzRzN2MieqM8vypQjyaJnbu6BAO6A/8bYuUZ0Y3IJF\nazP9qpYD+hhKglvGcjDKj1TLVN7gy4Gl9CHAuGkgoUwXFG8worrs5W1rTgx4HGWw\nbnWIkVqgtGv1gduXke88vqQ8Kw2eMBuloujOsm3gj5lyD4ycyMJQA8CsfkGy2ae/\nUXF/3dZGnapEUN5Vo6SAy1i+1S+1+mtj1uCyytBHDfiMqzfujns2nIvX+Xn9jBEE\nWgl55xR/0SnMij0hgkJ8RUQ8/NuGKRCD/Pr6sKRYYQKBgQD+Rjc3UkYKQUAdCliW\neHNggAiHLIhrmYwbj6VKIh3ulEQsMq9YhQt+zlF8fnfp7rcyHwsrtJMFN2X5Xyyb\nVGRCZxShMmwSsHYLax1JNQ8vThiF3ead+ARN0NtgEJgBLYV5EJ3a3sIMB2zFSt1B\nfjLR0pvtnHOez6zpA1DX69WwuQKBgQDTip/s6doJ+wf1RzWUqIb0lmN1yJ4JUN+0\nWtdHYG4+TRLVXc7m3OsNryqiVo4HrjwbyBOeJirFNQPmh+eAuSW8g7YsYBvKKLZN\nvWJPg3r5TfB0htphz4jutBpaQbUng3JBNyud5dIP/d35r0Zwup6Sz9nBCEeHOG7g\nx6gq6wqM/QKBgQDBrbwbMFjXMNJkDGBj5MWFSKC2Ta5vvxpgV+7/47LG6jpvLAAx\nvc1+viqFWFOAZWs3CzxYAwhFXegXpW31trdTeO7WxfBZ3/1aPzGkdHznfGXjeZ1S\nz/p/R0oCB0GxC/pxt711XF2UCgfI03hqjXSqK/DHcXcEDY3YQsVOYn13SQKBgQCD\nlqTa27EdKkGOCwjCe37PoMkn2G6uPteZOjTWGp8ZNBp2DU+J/nxc28y6hPr+vhx3\n76J8ayOJ3uuZOIsCYKmftZLZ0cMXovGcNCV2bsRNVnUwFz67Pzzft7r40AzfEn49\nIROJug9MkU/GZIh90SiZDKBY2kycSbd3LdtnLyQ2BQKBgQDlfo/R0ew4KUW5j4KE\nCvqaratRdJqd3Dw3Uh55NJA8FyrMp4Z7U90NM0nG0TQWQJWD1X6U8a3Z4ZHsOB6g\ndqkyh4ABAVOC2ybDDTZX6QB5nLVEevxm+fj11AT0BHznF3Ml0OOI46uENMtFBTN+\nE1qv5uTpQzrdPiT1FgeHtT4elw==\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-f70fk@sistema-academia-aee3a.iam.gserviceaccount.com",
    "client_id": "110051915874166408877",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-f70fk%40sistema-academia-aee3a.iam.gserviceaccount.com"
})
firebase_admin.initialize_app(cred)

db = firestore.client()
utils = Utils()

dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]


# current_user = None
# Create your views here.
def login_page(request):
    return render(request, 'login_page.html')


def submit_login(request):
    if request.POST:
        matricula = request.POST.get('username')
        password = request.POST.get('password')

        if matricula.startswith('alu'):
            users_collection = db.collection('Aluno')
        elif matricula.startswith('adm'):
            users_collection = db.collection('Admin')
        else:
            users_collection = db.collection('Professor')

        query = users_collection.where('matricula', '==', matricula).get()

        if len(query) == 1:
            for doc in query:
                if doc.get('matricula') == matricula and doc.get('senha') == password:
                    manage.current_user = set_current_user(doc, doc.get('permissao'), doc.id)
                    return redirect('/principal/')
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
                pessoa = Professor(nome=name, cpf=cpf, email=email, senha=password, username=username,
                                   matricula=username + '.professor')
            elif db_collection == 'Admin':
                pessoa = Admin(nome=name, cpf=cpf, email=email, senha=password, username=username, matricula='adm_' + username)
            else:
                pessoa = Aluno(nome=name, cpf=cpf, email=email, senha=password, username=username, matricula='alu' + utils.criar_matricula())
            obj = pessoa.converter_objeto()
            doc_ref = db.collection(db_collection).document()
            doc_ref.set(obj)
        else:
            raise Exception("erro de senha")

    return redirect('/')


def logout_user(request):
    manage.current_user = None
    return redirect('/')


def set_current_user(data, permissao, id):
    usuario = Pessoa(
        username=data.get('username'),
        senha=data.get('senha'),
        cpf=data.get('cpf'),
        email=data.get('email'),
        nome=data.get('nome'),
        matricula=data.get('matricula'),
    )
    usuario.permissao = permissao
    usuario.id = id
    return usuario


def cadastrar_aluno(request):
    dados = {
        'tipo_usuario': 'aluno'
    }
    return render(request, 'create_new_user_page.html', dados)


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
            email=doc.get('email'),
            matricula=doc.get('matricula'),
        )
        temp.id = doc.id
        lista.append(temp)
    dados = {
        'student_list': lista,
    }
    print(manage.current_user)
    return render(request, 'search_student.html', dados)


def buscar_aluno(request, id_aluno):
    doc_ref = db.collection('Aluno').document(id_aluno).get()
    if doc_ref is None:
        return redirect('/')
    dados = {}
    temp = Aluno(
        username=doc_ref.get('username'),
        nome=doc_ref.get('nome'),
        senha=doc_ref.get('senha'),
        cpf=doc_ref.get('cpf'),
        email=doc_ref.get('email'),
        matricula=doc_ref.get('matricula')
    )
    temp.id = doc_ref.id

    try:
        temp.treinamento = doc_ref.get('treinamento')
    except:
        pass
    dados['aluno'] = temp
    dados['dias_semana'] = dias_semana
    dados['current_user'] = manage.current_user
    return render(request, 'student_page.html', dados)


def criar_treino(request, id_aluno):
    doc_ref = db.collection('Aluno').document(id_aluno).get()
    temp = Pessoa(
        username=doc_ref.get('username'),
        nome=doc_ref.get('nome'),
        senha=doc_ref.get('senha'),
        cpf=doc_ref.get('cpf'),
        email=doc_ref.get('email'),
        matricula=doc_ref.get('matricula')
    )
    temp.id = doc_ref.id
    exercicios = db.collection('Exercicio').get()
    lista_exercicios = []
    for doc in exercicios:
        exercicio = Exercicio(nome=doc.get('Nome'))
        lista_exercicios.append(exercicio)
    dados = {
        'aluno': temp,
        'exercicios': lista_exercicios,
        'dias_semana': dias_semana
    }
    return render(request, 'add_practice.html', dados)


def submit_treino(request, id_aluno):
    if request.POST:
        dias = request.POST.getlist('dia_semana')
        aluno = db.collection('Aluno').document(id_aluno).get()
        temp = Aluno(
            username=aluno.get('username'),
            nome=aluno.get('nome'),
            senha=aluno.get('senha'),
            cpf=aluno.get('cpf'),
            email=aluno.get('email'),
            matricula=aluno.get('matricula')
        )
        try:
            temp.treinamento = aluno.get('treinamento')
        except:
            pass
        for dia in dias:
            temp.treinamento[dia] = []
            exercicios = request.POST.getlist('exercicios_' + dia)
            series = request.POST.getlist('series_' + dia)
            repeticoes = request.POST.getlist('repeticoes_' + dia)
            for i in range(len(exercicios)):
                if i == 0:
                    continue
                temp.treinamento[dia].append({
                    'Exercicio': exercicios[i],
                    'Series': series[i],
                    'Repeticoes': repeticoes[i],
                })
    objeto = temp.converter_objeto()
    doc_ref = db.collection('Aluno').document(id_aluno)
    doc_ref.set(objeto)
    return redirect('/consulta_aluno/' + id_aluno)


def alterar_treino(request, id_aluno):
    aluno = db.collection('Aluno').document(id_aluno).get()
    temp = Aluno(
        username=aluno.get('username'),
        nome=aluno.get('nome'),
        cpf=aluno.get('cpf'),
        email=aluno.get('email'),
        senha=aluno.get('senha'),
        matricula=aluno.get('matricula'),
    )
    temp.treinamento = aluno.get('treinamento')

    exercicios = db.collection('Exercicio').get()
    lista_exercicios = []
    for doc in exercicios:
        exercicio = Exercicio(nome=doc.get('Nome'))
        lista_exercicios.append(exercicio)
    dados = {}
    dados['aluno'] = temp
    dados['dias_semana'] = dias_semana
    dados['exercicios'] = lista_exercicios
    return render(request, 'alter_practice.html', dados)


def submit_alterar_treino(request, id_aluno):
    submit_treino(request, id_aluno)
    return redirect('/consulta_aluno/' + id_aluno)


def deletar_treino(request, id_aluno):
    doc_ref = db.collection('Aluno').document(id_aluno).get()
    aluno = Aluno(
        username=doc_ref.get('username'),
        nome=doc_ref.get('nome'),
        cpf=doc_ref.get('cpf'),
        email=doc_ref.get('email'),
        senha=doc_ref.get('senha'),
        matricula=doc_ref.get('matricula')
    )
    aluno.permissao = 'aluno'
    aluno.treinamento = doc_ref.get('treinamento')
    aluno.treinamento = Treino().treinamentos

    objeto = aluno.converter_objeto()
    updated_doc = db.collection('Aluno').document(id_aluno)
    updated_doc.set(objeto)
    return redirect('/consulta_aluno/' + id_aluno)


def consultar_exercicios(request):
    exercicios_ref = db.collection('Exercicio').get()
    exercicios = []
    for ex in exercicios_ref:
        temp = Exercicio(nome=ex.get('Nome'))
        exercicios.append(temp)

    dados = {
        'exercicios': exercicios
    }
    return render(request, 'manage_exercises.html', dados)


def submit_exercicios(request):
    if request.POST:
        exercicios_atualizados = request.POST.getlist('nome_exercicio')
        exercicios_no_banco = db.collection('Exercicio').get()
        lista_exercicios_no_banco = []

        for ex in exercicios_no_banco:
            lista_exercicios_no_banco.append(ex.get('Nome'))

        for exercicio in exercicios_atualizados:
            if exercicio == '' or exercicio in lista_exercicios_no_banco:
                continue

            temp = Exercicio(nome=exercicio).converter_objeto()
            doc_ref = db.collection('Exercicio').document()
            doc_ref.set(temp)

        for exercicio in lista_exercicios_no_banco:
            if exercicio not in exercicios_atualizados:
                query = db.collection('Exercicio').where('Nome', '==', exercicio).get()
                if len(query) != 0:
                    db.collection('Exercicio').document(query[0].id).delete()

    return redirect('/principal')


def consultar_professor(request):
    doc_professores = db.collection('Professor').get()
    lista_professores = []
    for doc in doc_professores:
        temp = Professor(
            nome=doc.get('nome'),
            cpf=doc.get('cpf'),
            username=doc.get('username'),
            senha=doc.get('senha'),
            matricula=doc.get('matricula'),
            email=doc.get('email')
        )
        temp.id = doc.id
        lista_professores.append(temp)
    dados = {}
    dados['professores'] = lista_professores
    return render(request, 'manage_teachers.html', dados)


def deletar_professor(request, id_professor):
    doc_professores = db.collection('Professor').get()
    lista_professores = []
    for doc in doc_professores:
        if doc.id == id_professor:
            db.collection('Professor').document(id_professor).delete()
        else:
            temp = Professor(
                nome=doc.get('nome'),
                cpf=doc.get('cpf'),
                username=doc.get('username'),
                senha=doc.get('senha'),
                matricula=doc.get('matricula'),
                email=doc.get('email')
            )
            temp.id = doc.id
            lista_professores.append(temp)
    dados = {
        'professores': lista_professores
    }
    return redirect('/gerenciar_professores')


def consultar_admin(request):
    doc_admins = db.collection('Admin').get()
    lista_admins = []
    for doc in doc_admins:
        temp = Professor(
            nome=doc.get('nome'),
            cpf=doc.get('cpf'),
            username=doc.get('username'),
            senha=doc.get('senha'),
            matricula=doc.get('matricula'),
            email=doc.get('email')
        )
        temp.id = doc.id
        lista_admins.append(temp)
    dados = {}
    dados['admins'] = lista_admins
    return render(request, 'manage_admin.html', dados)


def cadastrar_professor(request):
    dados = {
        'tipo_usuario': 'professor'
    }
    return render(request, 'create_new_user_page.html', dados)


def submit_professor(request):
    submit_user(request, 'Professor')
    return redirect('/')


def deletar_aluno(request, id_aluno):
    doc_alunos = db.collection('Aluno').get()
    lista_alunos = []
    for doc in doc_alunos:
        if doc.id == id_aluno:
            db.collection('Aluno').document(id_aluno).delete()
        else:
            temp = Aluno(
                nome=doc.get('nome'),
                cpf=doc.get('cpf'),
                username=doc.get('username'),
                senha=doc.get('senha'),
                matricula=doc.get('matricula'),
                email=doc.get('email')
            )
            temp.id = doc.id
            lista_alunos.append(temp)
    dados = {
        'student_list': lista_alunos
    }
    return redirect('/consulta_aluno')


def cadastrar_admin(request):
    dados = {
        'tipo_usuario': 'admin'
    }
    return render(request, 'create_new_user_page.html', dados)


def submit_admin(request):
    submit_user(request, 'Admin')
    return redirect('/')


def deletar_admin(request, id_admin):
    doc_admins = db.collection('Admin').get()
    lista_admins = []
    for doc in doc_admins:
        if doc.id == id_admin:
            db.collection('Admin').document(id_admin).delete()
        else:
            temp = Admin(
                nome=doc.get('nome'),
                cpf=doc.get('cpf'),
                username=doc.get('username'),
                senha=doc.get('senha'),
                matricula=doc.get('matricula'),
                email=doc.get('email')
            )
            temp.id = doc.id
            lista_admins.append(temp)
    dados = {
        'admins': lista_admins
    }
    return redirect('/gerenciar_admin')


def download_pdf(request, id_aluno):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = 'test.txt'
    filepath = BASE_DIR + '/Files/' + filename
    path = open(filepath, 'r')
    mime_type, _ = mimetypes.guess_type(filepath)
    response = HttpResponse(path, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response

def converter_pdf(request, id_aluno):
    pdf = utils.gerar_pdf(request, id_aluno)
    return HttpResponse(pdf, content_type='application/pdf')