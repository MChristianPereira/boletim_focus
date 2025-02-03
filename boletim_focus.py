from bcb import Expectativas
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter, FuncFormatter
import locale
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
plt.style.use('Solarize_Light2')

def dados_boletim_focus(data_inicial, data_referencia_inicial, data_referencia_final):

    em = Expectativas()
    ep = em.get_endpoint('ExpectativasMercadoAnuais')

    indicadores = ['IPCA', 'PIB Total', 'Câmbio', 'Selic']

    lista_dfs = []
    for indicador in indicadores:
        data = ep.query().filter(ep.Indicador == f'{indicador}').collect()
        data = data[['Indicador', 'Data', 'DataReferencia', 'Mediana']]
        lista_dfs.append(data)

    boletim_focus = pd.concat(lista_dfs, axis = 0)
    boletim_focus = boletim_focus[(boletim_focus['Data'] >= data_inicial)
                                  & (boletim_focus['DataReferencia'] <= data_referencia_final)
                                  & (boletim_focus['DataReferencia'] >= data_referencia_inicial)]
    return boletim_focus

def gerando_grafico(df):

    df['Data'] = pd.to_datetime(df['Data'])

    for indicador in df['Indicador'].unique():
        fig, ax = plt.subplots(figsize=(10, 6))

        dados_indicador = df[df['Indicador'] == indicador]

        for referencia in dados_indicador['DataReferencia'].unique():
            dados_referencia = dados_indicador[dados_indicador['DataReferencia'] == referencia]
            ax.plot(dados_referencia['Data'], dados_referencia['Mediana'], label = f'Data {referencia}', linewidth=0.75)

        ax.set_title(f'Expectativas de Mercado - {indicador}')
        ax.set_ylabel('Mediana')
        ax.legend()

        ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%b %Y'))
        ax.xaxis.set_major_locator(plt.MaxNLocator(nbins = len(dados_indicador['Data'].dt.month.unique())))
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: f'R${x:,.2f}')) if indicador == 'Câmbio' else ax.yaxis.set_major_formatter(PercentFormatter())

        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.savefig(f'{indicador}.png')
        plt.close()

if __name__ == '__main__':
    ano_passado = datetime.now() - relativedelta(years = 1)
    ano_atual = datetime.now().year
    ano_final = (datetime.now() + relativedelta(years = 3)).year
    df = dados_boletim_focus(data_inicial = ano_passado, data_referencia_inicial = f'{ano_atual}', data_referencia_final = f'{ano_final}')
    gerando_grafico(df)