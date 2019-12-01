import telebot
import json

with open('config.json') as con:
    config = json.load(con)
telebot.apihelper.proxy = {'https': 'https://54.37.131.235:3128'}
bot = telebot.TeleBot(config["access_token"])
# Бот будет отвечать только на текстовые сообщения
@bot.message_handler(content_types=['text'])
def echo(message: str) -> None:
    bot.send_message(message.chat.id, message.text)

if __name__ == '__main__':
    bot.polling()