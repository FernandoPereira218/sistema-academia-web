import datetime
from io import BytesIO

from django.http import HttpResponse
from django.template.loader import get_template, render_to_string
from xhtml2pdf import pisa

import core
from classes.Aluno import Aluno


class Utils:
    def criar_matricula(self):
        matricula = self.buscar_ano_semestre()
        doc_ref = core.views.db.collection('ID_Matricula').get()
        valor_nova_matricula = doc_ref[0].get('nova_matricula')
        matricula_final = f'{matricula}{valor_nova_matricula}'
        valor_nova_matricula += 1
        obj = core.views.db.collection('ID_Matricula').document(doc_ref[0].id)
        obj.set({
            'nova_matricula': valor_nova_matricula
        })
        return matricula_final

    def buscar_ano_semestre(self):
        data_atual = datetime.datetime.now()
        semestre = 0
        if data_atual.month <= 6:
            semestre = 1
        else:
            semestre = 2
        ano = data_atual.year
        ano_semestre = f'{ano}{semestre}'
        return ano_semestre

    def html_pdf(self, template_src, context_dict={}):
        template = get_template(template_src)
        html = template.render(context_dict)
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        return None

    def gerar_pdf(self, request, id_aluno):
        aluno_ref = core.views.db.collection('Aluno').document(id_aluno).get()
        aluno = Aluno(
            nome=aluno_ref.get('nome'),
            cpf=aluno_ref.get('cpf'),
            matricula=aluno_ref.get('matricula'),
            senha=aluno_ref.get('senha'),
            username=aluno_ref.get('username'),
            email=aluno_ref.get('email'),
        )
        aluno.treinamento = aluno_ref.get('treinamento')
        dados = {}
        dados['aluno'] = aluno
        dados['dias_semana'] = core.views.dias_semana
        open('templates/temp.html', "w", encoding="UTF-8").write(render_to_string('student_practice_pdf_template.html', dados))
        pdf = self.html_pdf('temp.html')

        return pdf
