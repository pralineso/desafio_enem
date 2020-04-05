# -*- coding: utf-8 -*-
"""DesafioEnemRLS

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jJjtTFAnTya_CqOWROBS9l2SvQlc1MD6
"""


%matplotlib inline
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
from google.colab import files


url_teste = "https://raw.githubusercontent.com/pralineso/desafio_enem/master/test.csv"
url_treino = "https://raw.githubusercontent.com/pralineso/desafio_enem/master/train.csv"
dados_teste_of = pd.read_csv(url_teste)
dados_treino_of = pd.read_csv(url_treino)


#FUNÇAO PRA CALCULAR A NOTA DO ENEM
##o q tem mais correlação é  repetido na nota de matematica quando for 0
def calcula_nota(matematica, c_natureza, l_codigos, c_humanas, redacao): #recebe a string com a resposta e a string com o gabarito
    nota_enem = ((matematica*3)+(c_natureza*2)+(l_codigos*(1.5))+(c_humanas*1)+(redacao*3))/(10.5)
    return round(nota_enem,2)



#FUNÇAÕ PRA PERCORRER LINHAS DA TABELA DE TREINO
def preenche_tabela_treino_df(tabela_base):

  for i in tabela_base.index:
    #PEGA A LINHA
    linha = tabela_base.loc[[i]]
    insc = linha.loc[i,'NU_INSCRICAO']
    mat = linha.loc[i,'NU_NOTA_MT']
    ciencia_natureza = linha.loc[i,'NU_NOTA_CN']
    linguagens_codigos = linha.loc[i,'NU_NOTA_LC']
    ciencias_humanas = linha.loc[i,'NU_NOTA_CH']
    red = linha.loc[i,'NU_NOTA_REDACAO']

    #CHAMANDO FUNCAO conta_acertos
    nota_enem = calcula_nota(mat,ciencia_natureza,linguagens_codigos,ciencias_humanas,red)

    #SALVANDO NA NOVA TABELA OS DADOS
    tabela_base.loc[i, 'NOTA_ENEM'] = nota_enem


#FUNÇAO PRA PERCORRER LINHAS DA TABELA DE TESTE
def preenche_tabela_teste_df(tabela_base):
  #se for a de teste ai nao tem a coluna coma nota, entao repete a nota da ciencia da natureza
  for i in tabela_base.index:
    #PEGA A LINHA
    linha = tabela_base.loc[[i]]
    insc = linha.loc[i,'NU_INSCRICAO']
    ciencia_natureza = linha.loc[i,'NU_NOTA_CN']
    linguagens_codigos = linha.loc[i,'NU_NOTA_LC']
    ciencias_humanas = linha.loc[i,'NU_NOTA_CH']
    red = linha.loc[i,'NU_NOTA_REDACAO']

    #CHAMANDO FUNCAO conta_acertos
    nota_enem = calcula_nota(ciencia_natureza,ciencia_natureza,linguagens_codigos,ciencias_humanas,red)#repete a nota de ciencia da natureza no lugar da de matematica

    #SALVANDO NA NOVA TABELA OS DADOS
    tabela_base.loc[i, 'NOTA_ENEM'] = nota_enem


#GERANDO TABELA DE TREINO
#PEGANDO SO AS COLUNAS QUE VAI USAR
#MONTANDO A TABELA SO COM ALGUNS REGISTROS
tabela_of = dados_treino_of[['NU_INSCRICAO','NU_NOTA_CN','NU_NOTA_CH','NU_NOTA_LC','NU_NOTA_REDACAO','NU_NOTA_MT']]
#tabela_of
#print(tabela_of.NU_NOTA_MT.isnull().sum())
tabela_of = tabela_of.loc[0:13730] #13730 pq é a qtd de linhas da tabela

#REMOVENDO LINHAS COM NU_NOTA_MT
tabela_of.dropna(how='any', inplace=True)
#tabela_of

#ADICIONANDO A COLUNA
tabela_of['NOTA_ENEM'] = 0
#tabela_of

#CHAMANDO A FUNCAO PRA GERAR A COLUNA COM OS ACERTOS
preenche_tabela_treino_df(tabela_of)
#tabela_of

#QTD TBL TEST = 10097 
#QTD TBL TRAIN = 13730 
#QTD DE NAN NA TBL TRAIN = 3597
#QTD SEM NAN = 10133 
#QTD TBL TEST = 4576

#GERANDO TABELA DE TESTE
tabela_para_testar = dados_teste_of[['NU_INSCRICAO','NU_NOTA_CN','NU_NOTA_CH','NU_NOTA_LC','NU_NOTA_REDACAO']]
#print(tabela_para_testar.columns.size)

tabela_para_testar = tabela_para_testar.loc[0:10097]
#print(tabela_teste_of.TX_GABARITO_MT.isnull().sum())

#REMOVENDO LINHAS COM NU_NOTA_MT
tabela_para_testar.dropna(how='any', inplace=True)
#tabela_para_testar

#ADICIONANDO A COLUNA
tabela_para_testar['NOTA_ENEM'] = 0
#tabela_para_testar

#CHAMANDO A FUNCAO PRA GERAR A COLUNA COM A NOTA 
preenche_tabela_teste_df(tabela_para_testar)


#MODELA
#y=ax+b

#PASSADO VALORES PARA X E Y
x = tabela_of[["NU_NOTA_CN","NU_NOTA_CH","NU_NOTA_LC","NU_NOTA_REDACAO","NOTA_ENEM"]]
y = tabela_of["NU_NOTA_MT"]

lm = LinearRegression()

#TREINO
lm.fit(x,y)

#COMANDOS USADOS PRA DECIDIR QUAL CAMPO REPETIR NA NOTA DE MATEMATICA
#print('coeficiente:',lm.intercept_)
#print('num coeficiente:',len(lm.coef_))
#pd.DataFrame(zip(X.columns, lm.coef_), columns=['colunas','coeficientesEstimados'])

#PREVISAO
x_teste = tabela_para_testar[["NU_NOTA_CN","NU_NOTA_CH","NU_NOTA_LC","NU_NOTA_REDACAO","NOTA_ENEM"]]


#FAZENDO A PREVISAO COM OS VALORES DO TEST
previsao = lm.predict(x_teste)
#previsao

#GERA A TABELA COM OS RESULTADOS
tabela_resultado = tabela_para_testar[['NU_INSCRICAO']]
tabela_resultado['NU_NOTA_MT'] = np.around(previsao,2)
#EXPORTANDO
tabela_resultado.to_csv('answer.csv', index=False, header=True)

#COMANDO PRA FAZER O DOWNLOAD DO COLAB
#files.download("answer.csv")
