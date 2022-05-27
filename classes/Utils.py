import datetime
import core

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