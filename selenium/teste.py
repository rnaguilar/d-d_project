from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# Configurar o WebDriver usando webdriver_manager
driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# Inicializa o webdriver Chrome
driver = webdriver.Chrome(ChromeDriverManager().install())

# A partir daqui, é possível utilizar o webdriver normalmente
driver.get("https://www.exemplo.com")

# Lista de URLs das páginas HTML que você deseja capturar
urls = ["C:\\PROJETOS\\D&D\\htmls\\Adivinhação.html"]

for url in urls:
    # Abrir a página
    driver.get(url)

    # Tirar uma captura de tela da página
    screenshot_path = f'screenshot_{urls.index(url) + 1}.png'
    driver.save_screenshot(screenshot_path)
    print(f"Captura de tela salva em: {screenshot_path}")

# Fechar o navegador
driver.quit()
