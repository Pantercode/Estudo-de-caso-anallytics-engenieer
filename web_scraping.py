import pandas as pd
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# 1. Configurações Selenium
opcoes_chrome = Options()
# Se quiser rodar sem abrir janela, descomente:
# opcoes_chrome.add_argument("--headless")  

servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=servico, options=opcoes_chrome)

# 2. Acessar o site (pt-BR)
url = "https://coinmarketcap.com/pt-br/"
navegador.get(url)

# Aguarda alguns segundos para a página carregar totalmente
time.sleep(5)

# 3. Localiza a tabela principal
xpath_tabela = '//table[contains(@class, "cmc-table")]'
tabela = navegador.find_element(By.XPATH, xpath_tabela)

# 4. Pega todas as linhas do <tbody>
linhas = tabela.find_elements(By.XPATH, './/tbody/tr')

dados = []
for linha in linhas:
    colunas = linha.find_elements(By.TAG_NAME, 'td')
    
    # Se o site tiver menos colunas do que o esperado, pule
    if len(colunas) < 9:
        continue

    # (Opcional) Debug para verificar o conteúdo de cada coluna:
    # for i, c in enumerate(colunas):
    #     print(i, repr(c.text))
    # print("-----")

    # Ajuste aqui conforme a ordem real que você observar no debug
    posicao                = colunas[0].text
    nome_sigla             = colunas[1].text
    preco                  = colunas[2].text
    porcentagem_1h         = colunas[3].text
    porcentagem_24h        = colunas[4].text
    porcentagem_7d         = colunas[5].text
    capitalizacao_mercado  = colunas[6].text
    
    # Tentar extrair Volume(24h) e Fornecimento Circulante
    # De vez em quando, ambos vêm em uma única coluna com "\n"
    volume_fornecimento_text = colunas[7].text
    partes = volume_fornecimento_text.split('\n')
    
    if len(partes) == 2:
        # Se tem duas partes, presumimos que a primeira seja Volume e a segunda Fornecimento
        volume_24h = partes[0].strip()
        fornecimento_circulante = partes[1].strip()
    else:
        # Se não tem quebra de linha, tentamos pegar o Volume dessa própria coluna
        volume_24h = volume_fornecimento_text
        # E ver se existe uma 9ª coluna (índice 8) com o Fornecimento
        if len(colunas) > 8:
            fornecimento_circulante = colunas[8].text.strip()
        else:
            fornecimento_circulante = None

    # Monta o dicionário que representará uma linha do DataFrame
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
    }
    dados.append(linha_dados)

# 5. Constrói o DataFrame
df = pd.DataFrame(dados)

# 6. (Opcional) Reordena colunas
ordem_colunas = [
    "Posição",
    "Nome (Sigla)",
    "Preço",
    "1h (%)",
    "24h (%)",
    "7d (%)",
    "Capitalização de Mercado",
    "Volume (24h)",
    "Fornecimento Circulante"
]
df = df[ordem_colunas]

df = df.rename(columns={
    "Nome (Sigla)": "Ranking",
    "Preço": "Nome Moeda",
    "1h (%)": "Preço",
    "24h (%)": "1h (%)",
    "7d (%)": "24h (%)",
    "Capitalização de Mercado": "7d (%)"
})
df = df.drop(columns=['Posição'])
# Exibe no console
print(df)



print(df)
df.to_excel("teste.xlsx", index=False)
navegador.quit()
