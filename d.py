from telebot import types, TeleBot

bot = TeleBot('1335664866:AAG0OSHMeb9PM4lua5s-Imn5lonrt52KBkY')
@bot.message_handler(content_types = ['text'])
def send_text(message):

    if message.text.lower() == 'users':
        if message.from_user.id == 671337340:
            bot.send_message(message.chat.id, f'✅ Загрузка пользователей ...')
            f = open('help_files/users_id.txt', 'rb')
            bot.send_document(message.chat.id, f)

        else:
            pass
