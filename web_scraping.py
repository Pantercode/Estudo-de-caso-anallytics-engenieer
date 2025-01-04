import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep

# 1. Configurações do Selenium
opcoes_chrome = Options()
opcoes_chrome.add_argument("--headless")  # Executar sem janela do navegador
servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=servico, options=opcoes_chrome)

# 2. Acessa a página em português do CoinMarketCap
url = "https://coinmarketcap.com/pt-br/"
navegador.get(url)
sleep(5)  # Ajuste conforme a velocidade de carregamento

# 3. Localiza a tabela principal
# OBS: Caso o XPATH ou a classe "cmc-table" mudem, será necessário adaptar.
xpath_tabela = '//table[contains(@class,"cmc-table")]'
tabela = navegador.find_element(By.XPATH, xpath_tabela)

# 4. Captura todas as linhas do corpo da tabela (tbody)
linhas = tabela.find_elements(By.XPATH, './/tbody/tr')

# 5. Lista para armazenar os dados
dados = []

# 6. Itera sobre cada linha para extrair as colunas
for linha in linhas:
    colunas = linha.find_elements(By.TAG_NAME, 'td')
    
    # Garante que haja colunas suficientes (mínimo 10 colunas para ter a de 7 dias)
    if len(colunas) < 10:
        continue

    # Cada coluna (ajuste conforme necessário se o site mudar a posição das colunas)
    posicao = colunas[0].text
    nome_sigla = colunas[1].text
    preco = colunas[2].text
    porcentagem_1h = colunas[3].text
    porcentagem_24h = colunas[4].text
    porcentagem_7d = colunas[5].text
    capitalizacao_mercado = colunas[6].text
    volume_24h = colunas[7].text
    fornecimento_circulante = colunas[8].text
    ultimos_7_dias = colunas[9].text  # Geralmente é um mini-gráfico, pode vir vazio

    # Monta dicionário com os dados da linha
    linha_dados = {
        "Posição": posicao,
        "Nome (Sigla)": nome_sigla,
        "Preço": preco,
        "1h (%)": porcentagem_1h,
        "24h (%)": porcentagem_24h,
        "7d (%)": porcentagem_7d,
        "Capitalização de Mercado": capitalizacao_mercado,
        "Volume (24h)": volume_24h,
        "Fornecimento Circulante": fornecimento_circulante,
        "Últimos 7 Dias": ultimos_7_dias
    }
    
    dados.append(linha_dados)

# 7. Converte a lista de dicionários em DataFrame
df = pd.DataFrame(dados)

# Exibe ou salva em CSV, Excel, etc.
print(df)
df = df.to_excel('teste.xlsx')

navegador.quit()
