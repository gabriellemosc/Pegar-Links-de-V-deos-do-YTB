#importar bibliotecas
import time, urllib
from IPython.display import display
from selenium import webdriver 
import pandas as pd 
import numpy as np
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from tkinter import * #interage com o usuário
import tkinter.filedialog
from tkinter import messagebox
import time

#ler csv

janela = Tk()

arquivo = tkinter.filedialog.askopenfilename(title= 'Selecione os canais do Youtube à serem mapeadaos')

janela.destroy()

buscas_df = pd.read_csv(r'C:\Users\gabri\Downloads\Python para executar programas mais complexos\Canais Youtube.csv', encoding = 'ISO-8859-1', sep=';')

buscas_df = buscas_df.rename(columns={'ÿCanais': 'Canais'})

display(buscas_df.head())

buscas_canais = buscas_df['Canais'].unique()
# ler videos de todas as buscas
driver = webdriver.Chrome() 

hrefs = []
delay = 5
    
# pegando os itens dos canais
for canal in buscas_canais:
    if canal is np.nan:
        break
    print('Iniciando a coleta de dados')
    hrefs.append(canal)
    driver.get(canal)
    time.sleep(3)
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'style-scope ytd-logo')))
    time.sleep(2)
    tab = driver.find_element(By.XPATH,'//*[@id="tabsContent"]/yt-tab-group-shape/div[1]/yt-tab-shape[2]/div[1]').click()
    time.sleep(2)
    altura = 0
    nova_altura = 1
    while nova_altura > altura:
            altura = driver.execute_script("return document.documentElement.scrollHeight")
            driver.execute_script("window.scrollTo(0, " + str(altura) + ");")
            time.sleep(3)
            nova_altura = driver.execute_script("return document.documentElement.scrollHeight")
    videos = driver.find_elements(By.ID, 'thumbnail')
    try:
        for video in videos:
            meu_link = video.get_attribute('href')
            if meu_link:
                if not 'googleadservices' in meu_link: 
                    hrefs.append(meu_link)
    except StaleElementReferenceException:
        time.sleep(2)
        videos = driver.find_elements(By.ID, 'thumbnail')
        for video in videos:
            meu_link = video.get_attribute('href')
            if meu_link:
                if not 'googleadservices' in meu_link: 
                    hrefs.append(meu_link)
    print('Pegamos {} vídeos do Canal {}'.format(len(videos), canal))

driver.quit()

#salvando o resultado em um csv
hrefs_df = pd.DataFrame(hrefs)
hrefs_df.to_csv(r'Canais Prontos.csv', sep=',', encoding='utf-8')

janela = Tk()

messagebox.showinfo('Programa executado com sucesso','Pegue o arquivo na pasta do programa')

janela.destroy()
