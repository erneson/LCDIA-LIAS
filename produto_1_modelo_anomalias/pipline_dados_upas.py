####################################
### IMPORTANDO MÓDULOS E FUNÇÕES ###
####################################

### CARREGANDO MODULOS ###
import pandas as pd
import numpy as np
import unidecode
import matplotlib as mpl
import matplotlib.pyplot as plt
import datetime as dt
### CARREGANDO MODULOS ###

### CERCA DE TUKEY ###
def calcula_cerca(janela):
  Q1, Q3 = np.quantile(np.sort(janela), [0.25, 0.75])
  IQR = Q3 - Q1

  sensibilidade = 1.5

  limite_inferior = Q1 - (IQR * sensibilidade)
  limite_superior = Q3 + (IQR * sensibilidade)

  return limite_inferior, limite_superior
### CERCA DE TUKEY ###

### IDENTIFICA ANOMALIAS ###
def identifica_anomalias(tamanho_janela, array):
  N = len(array)
  anomalias = np.full(N, np.nan)

  for i in range(tamanho_janela, N):
    janela = array[i - tamanho_janela : i]
    limite_inferior, limite_superior = calcula_cerca(janela)
    if array[i] > limite_superior:
      anomalias[i] = 1
    if array[i] < limite_inferior:
      anomalias[i] = 2
      
  return anomalias
### IDENTIFICA ANOMALIAS ###

### DIFERENÇAS FINITAS ###
def dif_fin(array):
  array_saida = np.full(len(array), np.nan)

  for i in range(2, len(array)):
    dfdx = ((3 * array[i]) - (4 * array[i-1]) + (array[i-2])) / 2
    array_saida[i] = dfdx

  return array_saida
### DIFERENÇAS FINITAS ###

### PLOT ###
def plot(anomalias, modelo):
  mycolors = [(1., 0., 0.), (0., 1., 0.)]

  mymap = mpl.colors.LinearSegmentedColormap.from_list('mymap', mycolors, N = 2)

  fig, ax = plt.subplots(figsize = (20,14))

  ax.scatter(df_corr.index, df_corr['media_movel_suspeitos'], c = anomalias, s = 60, zorder = 2, cmap = mymap)
  ax.plot(df_corr['media_movel_suspeitos'], lw = 2, zorder = 1, marker = 'o', markersize = 4, markerfacecolor = 'white')
  ax.set_ylabel('Suspeitos', fontsize = 32)
  ax.legend(['Suspeitos'], loc = (0.35, 0.90), fontsize = 32)
  twinplot = ax.twinx()
  twinplot.plot(df_corr['media_movel_confirmados'], color = '#D55E00')
  twinplot.set_ylabel('Confirmados', fontsize = 32)
  twinplot.legend(['Confirmados'], loc = (0.35, 0.80), fontsize = 32)

  ax.tick_params(labelsize = 24)
  twinplot.tick_params(labelsize = 24)
  
  if modelo == 'janela':
    ax.annotate('Janela de 28 dias', fontsize = 32, xycoords = 'figure fraction', xy = (0.70, 0.895))
    plt.savefig('imgs/anomalias_janela.pdf')

  elif modelo == 'derivada':
    
    ax.annotate('Derivada 2° ordem', fontsize = 32, xycoords = 'figure fraction', xy = (0.68, 0.895))
    plt.savefig('imgs/derivada_2ordem_anomalias.pdf')

### PLOT ###

####################################
### IMPORTANDO MÓDULOS E FUNÇÕES ###
####################################

### INPUTS ###
dados_upas = 'datasets/base_atendimentos_upas_20221128-001.csv' # CARREGANDO BASE DE DADOS DAS UPAS
dados_confirmados = 'datasets/casos-confirmados-integrasus-2022-07-13-07-30-38.csv' # CARREGANDO BASE DE DADOS DE CONFIRMADOS
tamanho_janela = 7 # MÉDIAS MÓVEIS DAS SÉRIES TEMPORAIS
janela_em_dias = 28 # PLOTANDO JANELA MÓVEL
### INPUTS ###

### CARREGANDO BASE DE DADOS DAS UPAS ###
colunas = ["upa","paciente","data_atendimento","hor_chegada","data_classificao_risco",
           "hora_classificao_risco","data_nascimento","anos","meses","dsc_endereco","dsc_risco",
           "dsc_queixa","dsc_discriminador","sinais_sintomas_anamnese","cod_cid10","dsc_cid10","dsc_detalhe"]

df_upas = pd.read_csv(dados_upas,
                      sep = ';',
                      header = None,
                      names = colunas,
                      encoding = 'latin1',
                      dtype = str)
### CARREGANDO BASE DE DADOS DAS UPAS ###

### TRATANDO BASE DE DADOS DAS UPAS ###
df_upas.drop_duplicates(inplace = True, ignore_index = True)
df_upas = df_upas.drop(columns=['paciente', 'dsc_endereco'])
df_upas['data_atendimento'] = pd.to_datetime(df_upas['data_atendimento'], format='%Y/%m/%d')
### TRATANDO BASE DE DADOS DAS UPAS ###

### CRIANDO SÉRIE TEMPORAL DE SUSPEITOS ###
existe_suspeita = np.zeros(len(df_upas))
sinonimos = ['falta de ar', 'dispineia', 'desconforto respiratorio']
sintomas = ['febre', 'tosse']

for indice, linha in df_upas.iterrows():
  if isinstance(linha['dsc_queixa'], str):
    for sinonimo in sinonimos:
      if sinonimo in unidecode.unidecode(linha['dsc_queixa'].lower()):
        for sintoma in sintomas:
          if sintoma in unidecode.unidecode(linha['dsc_queixa'].lower()):
            existe_suspeita[indice] = 1

df_upas['existe_suspeita'] = existe_suspeita.astype(int)

suspeitos = df_upas[df_upas['existe_suspeita']==1].sort_values(by='data_atendimento')
suspeitos = suspeitos[['data_atendimento', 'existe_suspeita']].groupby('data_atendimento').size()
### CRIANDO SÉRIE TEMPORAL DE SUSPEITOS ###

### CARREGANDO BASE DE DADOS DE CONFIRMADOS ###
df_confirmados = pd.read_csv(dados_confirmados,
                              sep = ';',
                              dtype = str)
### CARREGANDO BASE DE DADOS DE CONFIRMADOS ###

### TRATANDO BASE DE DADOS DE CONFIRMADOS ###
df_confirmados['DATA NOTIFICACAO'] = pd.to_datetime(df_confirmados['DATA NOTIFICACAO'], format='%d/%m/%Y')

confirmados = df_confirmados.groupby('DATA NOTIFICACAO')['DATA NOTIFICACAO'].count()
### TRATANDO BASE DE DADOS DE CONFIRMADOS ###

### CRIANDO DF DE COMPARAÇÃO DAS SÉRIES TEMPORAIS ###
def lista_de_datas(data_inicial, data_final):
    n = (data_final - data_inicial).days + 1

    datas = []
    for i in range(n):
        datas.append(data_inicial + dt.timedelta(i))
    return datas

vetor_data = lista_de_datas(dt.date(2020,1,1), suspeitos.index[-1].date())

dict_suspeitos = suspeitos.to_dict()
dict_confirmados = confirmados.to_dict()

dict_suspeitos_ajuste = {}
dict_confirmados_ajuste = {}

for key, value in dict_suspeitos.items():
  dict_suspeitos_ajuste[key.date()] = value

for key, value in dict_confirmados.items():
  dict_confirmados_ajuste[key.date()] = value

lista_suspeitos = []
lista_confirmados = []

for indice, data in enumerate(vetor_data):
  if data in dict_suspeitos_ajuste:
    lista_suspeitos.append(dict_suspeitos_ajuste[data])
  else:
    lista_suspeitos.append(np.nan)
  
  if data in dict_confirmados_ajuste:
    lista_confirmados.append(dict_confirmados_ajuste[data])
  else:
    lista_confirmados.append(np.nan)

d = {'suspeitos': lista_suspeitos, 'confirmados': lista_confirmados}
df_corr = pd.DataFrame(data = d, index = vetor_data)
### CRIANDO DF DE COMPARAÇÃO DAS SÉRIES TEMPORAIS ###

### MÉDIAS MÓVEIS DAS SÉRIES TEMPORAIS ###
janela_suspeitos = df_corr['suspeitos'].rolling(tamanho_janela, min_periods = 1)
df_corr['media_movel_suspeitos'] = janela_suspeitos.mean()

janela_confirmados = df_corr['confirmados'].rolling(tamanho_janela, min_periods = 1)
df_corr['media_movel_confirmados'] = janela_confirmados.mean()
### MÉDIAS MÓVEIS DAS SÉRIES TEMPORAIS ###

########################################################
### MÉTODO DE DETECÇÃO DE ANOMALIAS POR JANELA MÓVEL ###
########################################################

### IDENTIFICA ANOMALIAS ###
anomalias = identifica_anomalias(janela_em_dias, np.array(df_corr['media_movel_suspeitos']))
### IDENTIFICA ANOMALIAS ###

### PLOTANDO JANELA MÓVEL ###
# plot(anomalias, 'janela')
### PLOTANDO JANELA MÓVEL ###

########################################################
### MÉTODO DE DETECÇÃO DE ANOMALIAS POR JANELA MÓVEL ###
########################################################

####################################################
### MÉTODO DE DETECÇÃO DE ANOMALIAS POR DERIVADA ###
####################################################

dif_fin_2_ord = dif_fin(np.array(df_corr['media_movel_suspeitos']))

### IDENTIFICA ANOMALIAS ###
limite_inferior, limite_superior = calcula_cerca(np.array(dif_fin_2_ord[2:]))

anom_diff = np.full(len(dif_fin_2_ord), np.nan)

for i, v in enumerate(np.array(dif_fin_2_ord)):
  if v > limite_superior:
    anom_diff[i] = 1
  elif v < limite_inferior:
    anom_diff[i] = 2
### IDENTIFICA ANOMALIAS ###

### PLOTANDO DERIVADA ###
# plot(anom_diff, 'derivada')
### PLOTANDO DERIVADA ###

####################################################
### MÉTODO DE DETECÇÃO DE ANOMALIAS POR DERIVADA ###
####################################################

### DATAFRAME GERAL DAS ANOMALIAS ###
df_anomalias_covid = pd.DataFrame({'media_movel_suspeitos': list(df_corr['media_movel_suspeitos']),
                        'anomalias_janela_movel': anomalias,
                        'anomalias_derivada': anom_diff})

df_anomalias_covid.to_csv('output/dataframe_anomalias_covid.csv',
                           index = False,
                           sep = ';')
### DATAFRAME GERAL DAS ANOMALIAS ###