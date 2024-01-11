import openai
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
            "content":f"faça o resumo com 1200 caracteres da seguinte sentença: {message}"
        }]
    }

    body_mensagem = json.dumps(body_mensagem)

    requisicao = requests.post(link,headers=headers,data=body_mensagem)

    resposta = requisicao.json()

    mensagem = resposta['choices'][0]['message']['content']

    return mensagem if requisicao.status_code == 200 else message

print(getResumo('quanto é 1 +1'))