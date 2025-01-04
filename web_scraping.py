import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep

# 1. Configurações do Selenium (SEM headless para ver o navegador)
opcoes_chrome = Options()
# opcoes_chrome.add_argument("--headless")  # Comente ou remova para ver a janela
servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=servico, options=opcoes_chrome)

# 2. Acessar o site em português
url = "https://coinmarketcap.com/pt-br/"
navegador.get(url)
sleep(5)  # Ajuste se necessário

# 3. Localiza a tabela principal
xpath_tabela = '//table[contains(@class,"cmc-table")]'
tabela = navegador.find_element(By.XPATH, xpath_tabela)

# 4. Captura todas as linhas do <tbody>
linhas = tabela.find_elements(By.XPATH, './/tbody/tr')

# 5. Lista final para armazenar
dados = []

for linha in linhas:
    colunas = linha.find_elements(By.TAG_NAME, 'td')
    
    # Se o site tiver menos colunas em alguma linha, pule
    if len(colunas) < 10:
        continue

    # --- TESTE: imprime cada coluna para conferir a ordem ---
    # for i, col in enumerate(colunas):
    #     print(f"Coluna {i} -> {col.text}")
    # print("------")

    # Ajuste AQUI conforme descobrir a ordem exata:
    posicao = colunas[0].text            # Geralmente "#"
    nome_sigla = colunas[1].text         # Geralmente "Nome + Sigla"
    preco = colunas[2].text             # Geralmente "Preço"
    porcentagem_1h = colunas[3].text     # Geralmente "1h (%)"
    porcentagem_24h = colunas[4].text    # Geralmente "24h (%)"
    porcentagem_7d = colunas[5].text     # Geralmente "7d (%)"
    capitalizacao_mercado = colunas[6].text  # Geralmente "Cap. de Mercado"
    volume_24h = colunas[7].text         # Geralmente "Volume (24h)"
    fornecimento_circulante = colunas[8].text  # Geralmente "Fornecimento Circulante"
    

    # Monta um dicionário
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

# 7. Monta o DataFrame
df = pd.DataFrame(dados)

# 8. Se quiser, pode reordenar explicitamente as colunas:
ordem = [
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
df = df[ordem]
df = df.rename(columns={"Nome (Sigla)": "Ranking", "Preço": "Nome Moeda"})

# 9. Exibe
print(df)

# 10. Exporta para Excel
df.to_excel("teste.xlsx", index=False)

navegador.quit()
