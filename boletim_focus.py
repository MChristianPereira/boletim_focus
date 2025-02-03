from bcb import Expectativas
import pandas as pd

def dados_boletim_focus(data_inicial, data_final):

    em = Expectativas()
    ep = em.get_endpoint('ExpectativasMercadoAnuais')

    indicadores = ['IPCA', 'PIB Total', 'Selic']

    lista_dfs = []
    for indicador in indicadores:
        data = ep.query().filter(ep.Indicador == f'{indicador}').collect()
        data = data[['Indicador', 'Data', 'DataReferencia', 'Mediana']]
        lista_dfs.append(data)

    boletim_focus = pd.concat(lista_dfs, axis = 0)
    boletim_focus = boletim_focus[(boletim_focus['Data'] >= data_inicial) & (boletim_focus['DataReferencia'] <= data_final)]
    boletim_focus.to_excel('boletim_focus.xlsx', index = False)
    print(boletim_focus)

dados_boletim_focus(data_inicial = '2025-01-24', data_final = '2028')