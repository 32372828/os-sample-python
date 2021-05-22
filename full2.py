import smtplib
import subprocess
import sys
import os
import json
import smtplib
import time
from datetime import datetime

def install_Binance():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-binance"])

install_Binance()
#instalando bibliotecas
#!pip install python-binance

#@title
api_key = os.environ.get('KlE18YeWyGZWJLwi8Xsv33K9jHHZqnM1z5gAbdUGFjgHZv5HFae83qZEsagkWBEQ')
api_secret = os.environ.get('C80RihQtc7svxdRj1Kb15kyNh6IaE01YDxafA5nyt8NdY1PUIuYDBDxfoLr1De5C')
 
global client
from binance.client import Client
client = Client(api_key=api_key, api_secret=api_secret)
 
gmail_user = 'rcg.felipe@gmail.com'
gmail_password = 'mmsugiuawqtruete'
 
pares_new = client.get_all_tickers()
pares_old = client.get_all_tickers()

def RetMoeda(moeda):
  moeda_new = moeda
  moeda_new = moeda_new.replace("{\'symbol\': '","")
  moeda_new = moeda_new.replace("\'","")
  return (moeda_new.partition(",")[0])
 
def RetPreco(preco):
  price_new = preco
  price_new = price_new.partition(",")[-1]
  price_new = price_new.replace(" \'price\': \'","")
  price_new = price_new.replace("}","")
  price_new = float(price_new.replace("\'",""))
  return (price_new)
 
moeda_new = RetMoeda(str(pares_new[0]))
price_new = RetPreco(str(pares_new[0]))
print(moeda_new)
print(price_new)

def envia_email():
  sent_from = gmail_user
  to = ['rcg.felipe@gmail.com', 'gabrielcalderonsdpm@gmail.com']
  subject = 'Whale! ' + moeda_new + ' ' + str(dif_percentual) + '% ' + str(tempo_espera) + ' seg' 
  body = 'Hey, this is ' + moeda_new + ' ' + str(price_new)
  email_text = """\
From: %s
To: %s
Subject: %s
%s
""" % (sent_from, ", ".join(to), subject, body)
  try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to, email_text)
    server.close()
    print ('Email sent! Moeda: ' + moeda_new + ' ' + str(round(dif_percentual,2))+'% em ' + str(tempo_espera) +' segundos ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') )
  except Exception as error:
    print(error)
 
dif_percentual = 0.0
#envia_email()
print('Email carregado')

variacao_positiva = 5.0  ##positiva/negativa
#variacao_negativa = 3.0
tempo_espera = 10
 
print('Iniciado: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') )
 
pares_new = client.get_all_tickers()
pares_old = client.get_all_tickers()
 
while True:
    
  pares_old = pares_new
  pares_new = client.get_all_tickers()

  for index in range(len(pares_new)):
    #OLD
    moeda_old = RetMoeda(str(pares_old[index]))
    price_old = RetPreco(str(pares_old[index]))
    #print('Moeda velha: ' + moeda_old + ' Preço velho: ' + str(price_old))
 
    #NEW
    moeda_new = RetMoeda(str(pares_new[index]))
    price_new = RetPreco(str(pares_new[index]))
    #print('Moeda nova: ' + moeda_new + ' Preço novo: ' + str(price_new))
 
    #Variação Percentual = (VF/VI - 1) × 100
    dif_preco = price_new - price_old
    dif_percentual = round(((price_new/price_old) - 1) * 100,2)
    #print("Diferença preço: "+str(round(dif_preco,6))+' Diferença percentual: '+str(round(dif_percentual,2))+'%')
    #print('Moeda: ' + moeda_new + ' ' + str(round(dif_percentual,2))+'%' )
    
    if abs(dif_percentual) >= variacao_positiva:
      envia_email()
      #break
  #print('Tempo de espera: ' + str(tempo_espera) + ' segundos ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') )    
  time.sleep(tempo_espera)