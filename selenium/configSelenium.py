from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def instanceOptions()->Options():
    options = Options()
    options.add_argument('window-size=525,990')
    options.add_argument("--headless") 

    prefs = {"download.default_directory" : "C:\\PROJETOS\\D&D\\selenium\\"}
    options.add_experimental_option("prefs",prefs)
    return options

# options.add_argument('--headless')
driver = webdriver.Chrome(options=instanceOptions())

# Configurar o caminho do webdriver do Selenium (neste exemplo, usando o Chrome)
# webdriver_path = 'C:\\PROJETOS\\D&D\\selenium\\chromedriver.exe'
# driver = webdriver.Chrome(executable_path=webdriver_path)

# Lista de URLs das páginas HTML que você deseja capturar
urls = ["C:\\PROJETOS\\D&D\\htmls\\Adivinhação.html"]

for url in urls:
    # Abrir a página
    driver.get(url)

    # Tirar uma captura de tela da página
    screenshot_path = f'C:\\PROJETOS\\D&D\\cards\\screenshot_{urls.index(url) + 1}.png'
    driver.save_screenshot(screenshot_path)
    print(f"Captura de tela salva em: {screenshot_path}")

# Fechar o navegador
driver.quit()
