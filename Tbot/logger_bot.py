import telebot
from DataApplication.logger import DataLogger
import matplotlib.pyplot as plt

bot = telebot.TeleBot("5337445036:AAGQDYKj-MCSfgAIOsUytcUMhySBCdTR0qM", parse_mode=None)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id,"Howdy, how are you doing?")

@bot.message_handler(commands=["curr_situation"])
def send_info(message):
    try:
        logger = DataLogger()
        curr_data = logger.get_plot_time()
        curr_str = ""
        for i in range(4):
            curr_str+=curr_data[i+3]
            curr_str+="\n"
        bot.send_message(message.chat.id, curr_str)
        plt.figure(figsize=(10, 7))
        plt.plot(curr_data[0], label="Download time")
        plt.plot(curr_data[1], label="Converting time")
        plt.plot(curr_data[2], label="Summary time")
        plt.ylabel("Время, c")
        plt.xlabel("Номер песни")
        plt.grid()
        plt.legend()
        plt.savefig('tmp.png')
        img = open('tmp.png', 'rb')
        #bot.send_photo(message.chat_id, photo=('tmp.png'))
        bot.send_document(message.chat.id, img)
    except Exception as e:
        bot.send_message(message.chat.id, "Ошибка: "+str(e))

@bot.message_handler(commands=["logs"])
def send_logs(message):
    try:
        file = open("../logs/full_log.txt", "r")
        info = file.readlines()[-100:]
        file.close()
        curr_str = ""
        for line in info:
            curr_str+=line
        bot.send_message(message.chat.id, curr_str)
    except Exception as e:
        bot.send_message(message.chat.id, "Ошибка: "+str(e))

print("Бот поднят")
bot.polling()