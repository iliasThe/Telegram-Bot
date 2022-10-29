import telebot
from datemsg import gen_qr_code
from path import Path



token = "5404650116:AAHFKuX9poF-wUm52eQZuOzna7UL2xLW-a0"
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет ✌ \n Я умею делать QR с твоей картинкой(JPG,PNG) на фоне")

@bot.message_handler(content_types=['document'])
def handle_docs_photo(message):
    global path_to_download
    try:
        chat_id = message.chat.id
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        src = 'C:/sample/files/' + message.document.file_name;
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        path_to_download = Path().joinpath(src)
        bot.reply_to(message, "Пожалуй, я сохраню это. Отправь теперь ссылку")
    except Exception as e:
        bot.reply_to(message, e)

@bot.message_handler()
def send_text_based_qr(message):
    global path_to_download
    try:
        path_to_save = Path().joinpath("qr_code.png")
        print('path_to_save', path_to_save)
        gen_qr_code(message.text, path_to_download, path_to_save)
        bot.reply_to(message, 'Ща, пять сек!\nЖди.')
        with open('qr_code.png', 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
            bot.send_message(message.chat.id, 'QR-Code готов!')
    except Exception:
        bot.reply_to(message, "Сначала картинку, потом link----")

bot.infinity_polling()