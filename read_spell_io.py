import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
# import imgkit
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import json


def getResumo(message):
    # Configure a sua chave da API da OpenAI
    API_KEY = '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'
    headers = {"Authorization":f"Bearer {API_KEY}", "Content-Type": "application/json"}
    link = "https://api.openai.com/v1/chat/completions"
    id_modelo = 'gpt-3.5-turbo'

    body_mensagem = {
        "model":id_modelo,
        "messages":[{
            "role":"user",
            "content":f"faça o resumo com 1000 caracteres da seguinte sentença: {message}"
        }]
    }

    body_mensagem = json.dumps(body_mensagem)

    requisicao = requests.post(link,headers=headers,data=body_mensagem)

    resposta = requisicao.json()

    mensagem = resposta['choices'][0]['message']['content']

    return mensagem if requisicao.status_code == 200 else message

def instanceOptions()->Options():
    options = Options()
    options.add_argument('window-size=640,890')
    # 120
    # 77
    # ideal 620 x 877
    options.add_argument("--headless") 

    prefs = {"download.default_directory" : "C:\\PROJETOS\\D&D\\selenium\\"}
    options.add_experimental_option("prefs",prefs)
    return options


def createHtml(path, name,string):
     # Escrever a string HTML no arquivo
    with open(f'{path}\\{name}.html', 'w', encoding='utf-8') as arquivo_html:
        arquivo_html.write(string)

def implementPNG(path:str, df:pd.DataFrame):

    driver = webdriver.Chrome(options=instanceOptions())

    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <!-- Vincula o arquivo CSS -->
        {css}
        <title>Document</title>
    </head>
    <body>

        <div class="card-container">
            <p class="card-title">{Magia}</p>
            <div class="card-status">
                <div class="card-status-container">
                    <img class="status-img" src="img/action.png">
                    <div class="status-text">{Action}</div>
                </div>
                <div class="card-status-container">
                    <img class="status-img" src="img/range.png">
                    <div class="status-text">{Range}</div>
                </div>
                <div class="card-status-container">
                    <img class="status-img" src="img/flag.png">
                    <div class="status-text">{Flag}</div>
                </div>
                <div class="card-status-container">
                    <img class="status-img" src="img/duration.png">
                    <div class="status-text">{Duration}</div>
                </div>
            </div>

            <hr>

            <div class="description-container">
                <div class="description-title">Material</div> 
                <div class="description-material">
                    {Material}
                <div>
                <br>
                <div class="description-title">Descrição</div> 
                <div class="description">
                    {Description}
                </div>
            </div>
            
            <footer>
                    <div class="school">{School}</div>
                    <div class="level">{Level}</div>
            </footer>

        </div>
        
    </body>
    </html>
    """

    for linha in df.index:
        print(f"Magia: {df.loc[linha,'nome']}")
        css = '<link rel="stylesheet" href="css/style2.css">' if  df.loc[linha,'aoe']  else '<link rel="stylesheet" href="css/style.css">'
        description = f"<p>{df.loc[linha,'descricao'][:900]} </p>"
        
        # for dp in df.loc[linha,'descricao']:
        #     description = f"""{description}\n {dp}"""

        # description = f"<p> {getResumo(description)} </p>"
        
        html_content =  html.format(
            css = css,
            Magia = df.loc[linha,'nome'],
            Material = df.loc[linha,'material'],
            Description = description,
            Level = df.loc[linha,'level'],
            School = df.loc[linha,'school'],
            Action = df.loc[linha,'cast'],
            Range = df.loc[linha,'range'],
            Flag = df.loc[linha,'components'],
            Duration = df.loc[linha,'duration']
        )

        createHtml(path=f"{path}\\htmls",name=df.loc[linha,'nome'],string= html_content)

        

        # Tirar uma captura de tela da página
        driver.get(f"{path}\\htmls\\{df.loc[linha,'nome']}.html")
        screenshot_path = f"{path}\\cards\\{df.loc[linha,'nome']}.png"
        driver.save_screenshot(screenshot_path)


def extrair_numeros_iterativo(texto):
    numeros = [c if c.isdigit() else ' ' for c in texto]
    numeros_str = ''.join(numeros).split()
    n_numeros = ''
    for numero in numeros_str:
        n_numeros = f"{n_numeros}{numero}"
    return n_numeros

def getSpells()->pd.DataFrame:

    url = "https://avribacki.gitlab.io/magias5e/spells.js"

    # Baixa o conteúdo da URL
    response = requests.get(url)

    html_content = response.text

    soup = BeautifulSoup(html_content[30:-1], 'html.parser')

    # Encontrar todas as divs com a classe "spell-item"
    spell_items = soup.find_all('div', class_='spell-item')

    data = []

    for spell_item in spell_items:
        

        name = spell_item.find('div', class_='name').find('p').text.strip()
        
        # Encontrar a tag <strong> dentro da div com a classe "description"
        strong_material = spell_item.find('div', class_='description').find('p').find('strong', text='Material')
        level = spell_item.find('div', class_='level').text.strip()
        school_tag = spell_item.find('div', class_='name').find('p', class_='school')
        school_text = school_tag.text.strip() if school_tag else None
        
        # Use expressão regular para extrair o texto
        match = re.match(r'(\D+)', school_text)

        # Verifica se houve correspondência e extrai o texto
        school = match.group(1).strip().capitalize() if match else None


        # Encontrar a div com a classe "description"
        description_div = spell_item.find('div', class_='description')

        # Inicializar as variáveis
        material = None
        descricao = []
        flag_aoe = False

        # Palavras-chave para verificar na descrição
        palavras_chave = ['alvos', 'grupo']

        if description_div:
            # Iterar pelos parágrafos dentro da div "description"
            for paragraph in description_div.find_all('p'):
                # Verificar se o parágrafo contém a tag <strong>
                if paragraph.strong and paragraph.strong.get_text(strip=True) == 'Material':
                    # Se contém a tag <strong>, atribuir o texto ao material
                    material = str(paragraph.get_text(strip=True)).replace('Material:','')
                else:
                    # Se não contém a tag <strong>, adicionar o texto à descrição
                    descricao.append(str(paragraph.get_text(strip=True)).replace('\n',''))
                    # Verificar se as palavras-chave estão presentes na descrição
                    if any(palavra in paragraph.get_text().lower() for palavra in palavras_chave) and flag_aoe == False:
                        flag_aoe = True

        # Inicializa as variáveis
        cast = None
        range_ = None
        components = None
        duration = None

        

        # Verifica a presença da imagem e atribui os valores correspondentes
        meta_items = spell_item.find_all('div', class_='meta-item')
        for meta_item in meta_items:
            img_duration = meta_item.find('img', src='img/duration.svg')
            img_concentration = meta_item.find('img', src='img/concentration.svg')
            img_range = meta_item.find('img', src='img/range.svg')
            img_components = meta_item.find('img', src='img/components.svg')
            img_cast = meta_item.find('img', src='img/cast.svg')

            if img_duration:
                duration = meta_item.find('div', class_='meta-content').text.strip()
            elif img_concentration:
                # You can handle concentration logic here if needed
                pass
            elif img_range:
                range_ = meta_item.find('div', class_='meta-content').text.strip()
            elif img_components:
                components = meta_item.find('div', class_='meta-content').text.strip()
            elif img_cast:
                cast = meta_item.find('div', class_='meta-content').text.strip()


        spell_data = {}

        # Encontrar o nome da magia
        spell_data['nome'] = str(name).replace('/',' ou ')
        spell_data['material'] = str(material).replace('\n','')[:100]
        spell_data['descricao'] = '\n'.join(descricao)
        spell_data['level'] =  extrair_numeros_iterativo(str(level)) 
        spell_data['school'] = str(school).replace('\n','')
        spell_data['cast'] = str(cast).replace('\n','')
        spell_data['range'] = str(range_).replace('\n','')
        spell_data['components'] = str(components).replace('\n','')
        spell_data['duration'] = str(duration).replace('\n','')
        spell_data['aoe'] = flag_aoe

        data.append(spell_data)

    # Criar um DataFrame com os dados
    df = pd.DataFrame(data)

    df.to_excel('C:\\PROJETOS\\D&D\\magias.xlsx')

    return df

# getSpells()
df =  pd.read_excel('C:\\PROJETOS\\D&D\\magias.xlsx')

# exit()


path = 'C:\\PROJETOS\\D&D'

implementPNG(path=path,df=df)