from datetime import datetime

import telebot
import requests

# Chaves e URLs
WEATHER_API_KEY = "4c08e1777043477e9d9114107231408"
WEATHER_BASE_URL = "http://api.weatherapi.com/v1/current.json"
TELEGRAM_BOT_TOKEN = "6372031764:AAHC-klH3R6UH7eKY2WGkAooMYh6ISNKq94"

# Inicializar o bot do Telegram
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Manipulador do comando /previsao
@bot.message_handler(commands=["tempo"])
def obter_previsao(mensagem):
    try:
        provincia = mensagem.text.split("/tempo ", 1)[1]
        cidade = f"{provincia}"

        params = {
            "key": WEATHER_API_KEY,
            "q": cidade,
            "aqi": "yes"
        }

        response = requests.get(WEATHER_BASE_URL, params=params)

        if response.status_code == 200:
            data = response.json()
            data_hora = datetime.strptime(data['location']['localtime'], "%Y-%m-%d %H:%M")
            data_hora_formatada = data_hora.strftime("%H:%M %d/%m/%Y")

            resposta = f"Condições atuais em {cidade}:\n"
            resposta += f"Tempo: {data['current']['condition']['text']}\n"
            resposta += f"Max : {data['current']['temp_c']}°C\n"
            resposta += f""
            resposta += f"Velocidade do ar: {data['current']['wind_kph']} km/h\n"
            resposta += f"Índice de qualidade do ar (AQI): {data['current']['air_quality']['us-epa-index']}\n"
            resposta += f"Humidade: {data['current']['humidity']}%\n"
            resposta += f"Data e Hora da cidade: {data_hora_formatada}"
            bot.reply_to(mensagem, resposta)
        else:
            bot.reply_to(mensagem, f"Erro na solicitação: {response.status_code}")
    except IndexError:
        bot.reply_to(mensagem, "Por favor, forneça o nome da província após o comando.")

# Função para verificar mensagens
def verificar(mensagem):
    return True

# Manipulador para responder a todas as mensagens
@bot.message_handler(func=verificar)
def responder_padrao(mensagem):
    bot.reply_to(mensagem, 'Olá, aqui é o Bot do Jossias.')

# Iniciar o bot
bot.polling()
