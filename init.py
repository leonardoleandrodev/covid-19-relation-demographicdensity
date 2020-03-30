import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import requests as rq
#arquivo csv baixado em https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv
txt = rq.get("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv").text
f = open(os.path.dirname(__file__) + "/time_series_covid19_confirmed_global.csv",'w').write(txt)

df = pd.read_csv(os.path.dirname(__file__) + "/time_series_covid19_confirmed_global.csv")
#ordena os paises
res = df.sort_values(by="Country/Region")
#remove as colunas desnecessarias
res = res.drop(["Province/State","Lat","Long"],axis=1)
#agrupa os paises somando seus valores de infectados
res = res.groupby("Country/Region").sum()
#paises selecionados para analise
#alinhar os paises com as suas respectivas densidades demograficas
paises               = ['Brazil','Italy','Spain', 'US','United Kingdom','France','China']
densidadeDemografica = [   24.96, 200.64, 150.51,33.67,          279.98,  119.15, 151.02]
#fonte da densidade demografica https://www.populationpyramid.net/pt/densidades-populacionais/2020/

#lista as datas
dates =  list(res)[:-1]

#busca os paises conforme solicitado
listaPaises = []
for pais in paises:
    pais = res.loc[[pais]]
    listaPaises.append(pais.iloc[0,:-1])


dframe = {'date':dates}

#relaciona os paises selecionados com as suas informacoes de densidade demografica
i = 0
for dadosPais in listaPaises:
    dframe['Dens. Dem. de Infectados ' + paises[i][0:3] + ' .']=(dadosPais/densidadeDemografica[i])
    i += 1

#prepara os dados para serem apresentados no grafico
dframeResult = pd.DataFrame(dframe)
#altera o formato das datas
dframeResult['date'] = pd.to_datetime(dframeResult['date'])

#prepara a exibicao do grafico
fig = plt.figure()
ax = plt.axes()

#lista as informacoes dos graficos
for dfresultitem in dframeResult:
    if dfresultitem.find('Dem.')>-1:
        dframeResult.set_index('date')[dfresultitem].plot(legend=True,grid=True,label=dfresultitem)


plt.title('data')
plt.xlabel('')
plt.ylabel('densidade de infecção por km2')
plt.show()
