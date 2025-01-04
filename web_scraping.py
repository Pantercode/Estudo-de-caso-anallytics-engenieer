from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from time import sleep
# Configura o web
service = Service(ChromeDriverManager().install())
# Abre o Chrome e acessa a página
driver = webdriver.Chrome(service=service)
#ir para o site do ibge
driver.get("https://coinmarketcap.com/pt-br/")

cabecalhotexto = driver.find_elements(By.CLASS_NAME,'stickyTop')
for i in range(len(cabecalhotexto)):
    print(cabecalhotexto[i].text)
