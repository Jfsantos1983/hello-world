from datetime import datetime, date
from conectar import conexao
from workalendar.america import Brazil
#from util import extract_element_from_json
from xlrd import open_workbook
from xlutils.copy import copy
import xlrd
import json
import unicodedata
import re

def get_prazo_inicial_final_intimacao(data_disponibilizacao, prazo):

    print(data_disponibilizacao, prazo)

    # primeiro faço um cálculo de qual o prazo final adicionando o prazo informado na planilha à data do início do prazo, em dias úteis
    cal = Brazil()

    # separei em dia, mês e ano para utilizar depois como integer
    day = datetime.strptime(data_disponibilizacao, "%d-%m-%Y %H:%M:%S").strftime('%d')
    month = datetime.strptime(data_disponibilizacao, "%d-%m-%Y %H:%M:%S").strftime('%m')
    year = datetime.strptime(data_disponibilizacao, "%%d-%m-%Y %H:%M:%S").strftime('%Y')

    print(day, month, year)

    # aqui eu faço a soma do prazo à data inicial, já transformando em AAAA-MM-DD, conforme exige o SAPIENS
    prazo_final = cal.add_working_days(date(int(year), int(month), int(day)), prazo).strftime('%Y-%m-%d')

    # aqui eu apenas transformo a data inicial no formato AAAA-MM-DD
    prazo_inicial = datetime.strptime(data_disponibilizacao, '%d-%m-%Y').strftime('%Y-%m-%d')

    # aqui eu incluo o formato de hora exigido pelo SAPIENS, colocando no início do prazo o primeiro segundo do dia e no fim o último minuto

    prazo_inicial_convertido = prazo_inicial + " 00:01:00"
    prazo_final_convertido = prazo_final + " 23:59:59"

    return prazo_inicial_convertido, prazo_final_convertido


def get_unidade_id():

    cpf = "21631424858"
    senha = "Giobru2020"
    conexao.seta_usuario({'uss': re.sub("\D", "", cpf), 'pass': senha})
    sessao1 = conexao.testa_conexao()
    sessao = conexao.obtem_Sessao()

    tid = conexao.obtem_tid()
    descricao_Setor = "PROCURADORIA SECCIONAL DA UNIÃO EM PRESIDENTE PRUDENTE"


    dic_post = {"action": "SapiensMain_Setor",
                "method": "getSetor",
                "data": [{"fetch": ["unidade"],
                          "query": descricao_Setor,
                          "page": 1,
                          "start": 0,
                          "limit": 500}],
                "type": "rpc",
                "tid": int(tid)}

    m = sessao.post('https://sapiens.agu.gov.br/route', json=dic_post)

    valor = m.json()

    unidade_id_json = extract_element_from_json(valor, ['result', 'records', 'unidade_id'])

    unidade_id = unidade_id_json[0][0]

    return unidade_id

def get_name():

    cjto_postit_tarefa = "PRONTO EXECUÇÃO INVERTIDA {GUSTAVO AURÉLIO FAUSTINO} JJJA"
    proc_name_inicio = cjto_postit_tarefa.find('{') + 1
    proc_name_fim = cjto_postit_tarefa.find('}')
    proc_name = cjto_postit_tarefa[proc_name_inicio:proc_name_fim]

    print(proc_name_inicio, proc_name_fim, proc_name)


#get_unidade_id()
get_name()