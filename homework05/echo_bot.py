import telebot


access_token = '1065394368:AAH7CHF7nd_OOgZewfCsapg3CQ-VaIGhNjs'
telebot.apihelper.proxy = {'https': 'https://117.1.16.131:8080'}

# Создание бота с указанным токеном доступа
bot = telebot.TeleBot(access_token)


# Бот будет отвечать только на текстовые сообщения
@bot.message_handler(content_types=['text'])
def echo(message: str) -> None:
    bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    bot.polling()