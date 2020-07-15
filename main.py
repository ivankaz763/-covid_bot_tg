import telebot
import COVID19Py
from telebot import types


covid19 = COVID19Py.COVID19()
bot = telebot.TeleBot('1198658250:AAEkU0jeal9i3JJJnydRdjHgiDJ-kBZc6ZI')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('США')
    btn2 = types.KeyboardButton('Украина')
    btn3 = types.KeyboardButton('Россия')
    btn4 = types.KeyboardButton('Беларусь')
    markup.add(btn1, btn2, btn3, btn4)
    
    send_message = f"<b>Привет, {message.from_user.first_name}!</b>\nЧтобы узнать как пользоваться ботом, введи /help"
    bot.send_message(message.chat.id, send_message, parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    final_message = ""
    k = 0
    i = 0
    get_messge_bot = message.text.strip().lower()
    if get_messge_bot == "информация" or get_messge_bot == "/info" or get_messge_bot == "/start" and k == 0:
        # Готовим кнопки
        keyboard = types.InlineKeyboardMarkup()
        # По очереди готовим текст и обработчик для каждого знака зодиака
        key_cov = types.InlineKeyboardButton(text='Что такое COVID', callback_data='covid')
        keyboard.add(key_cov)
        key_sim = types.InlineKeyboardButton(text='Симптомы', callback_data='sim')
        keyboard.add(key_sim)
        key_seb = types.InlineKeyboardButton(text='Если заметили симптомы у себя', callback_data='seb')
        keyboard.add(key_seb)
        key_mif = types.InlineKeyboardButton(text='Мифы о короновирусе', callback_data='mif')
        keyboard.add(key_mif)
        # Показываем все кнопки сразу и пишем сообщение о выборе
        bot.send_message(message.from_user.id, text='Что конкретно тебя интересует?', reply_markup=keyboard)
    elif get_messge_bot == "/help":
        bot.send_message(message.from_user.id, """Привет, я могу рассказать тебе информацию о COVID-19 или показать статистику заболевания.

Для того чтобы узнать информацию о COVID, напиши сообщение "Информация" или команду /info 

Если хочешь узнать статистику, то можешь написать "Статистика" или ввести команду
/stat """)
    elif get_messge_bot == "/stat":
        bot.send_message(message.from_user.id, """Чтобы узнать данные про коронавируса,пше  напишите название страны, например: США, Украина, Россия и так далее""")
    elif get_messge_bot == 'сша':
        location = covid19.getLocationByCountryCode("US")
        k = 1
    elif get_messge_bot == 'россия':
        location = covid19.getLocationByCountryCode("RU")
        k = 1
    elif get_messge_bot == 'украина':
        location = covid19.getLocationByCountryCode("UA")
        k = 1
    elif get_messge_bot == 'беларусь':
        location = covid19.getLocationByCountryCode("BY")
        k = 1
    elif get_messge_bot == "казакхстан":
        location = covid19.getLocationByCountryCode("KZ")
        k = 1
    elif get_messge_bot == "италия":
        location = covid19.getLocationByCountryCode("IT")
        k = 1
    elif get_messge_bot == "франция":
        location = covid19.getLocationByCountryCode("FR")
        k = 1
    elif get_messge_bot == "германия":
        location = covid19.getLocationByCountryCode("DE")
        k = 1
    elif get_messge_bot == "япония":
        location = covid19.getLocationByCountryCode("JP")
        k = 1
    if final_message == "" and k == 1:
        date = location[0]['last_updated'].split("T")
        time = date[1].split(".")
        final_message = f"<u>Данные по стране:</u>\nНаселение: {location[0]['country_population']:,}\n" \
                    f"Последнее обновление: {date[0]} {time[0]}\nПоследние данные:\n<b>" \
                    f"Заболевших: </b>{location[0]['latest']['confirmed']:,}\n<b>Сметрей: </b>" \
                    f"{location[0]['latest']['deaths']:,}"

        bot.send_message(message.chat.id, final_message, parse_mode='html')
    elif get_messge_bot == "информация" or get_messge_bot == "/info" or get_messge_bot == "/start" or get_messge_bot == "/help" or get_messge_bot == "/stat":
        k = 0
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    # Если нажали на одну из 12 кнопок — выводим гороскоп
    if call.data == "covid":
        # Формируем гороскоп
        msg = """Коронавирусы — это большое семейство вирусов, которые приводят к заболеваниям органов дыхания. Чаще всего — без тяжелых симптомов. Всего насчитывается около 40 видов коронавируса.
Пандемию вызвал $АВ$-Со\-2, который впервые был обнаружен в Китае в конце декабря.
Считается, что инкубационный период нового коронавируса — до 14 дней. Все это время человек может быть носителем вируса, но не подозревать об этом. Именно поэтому стоит соблюдать двухнедельный карантин, если вы вернулись из страны, где много случаев заражения, или контактировали с заболевшим."""
        # Отправляем текст в Телеграм
        bot.send_message(call.message.chat.id, msg)
    elif call.data == "sim":
        # Формируем гороскоп
        msg = """Часто наблюдаемые симптомы:
- повышение температуры тела;
- сухой кашель;
- утомляемость.
У некоторых инфицированных могут также наблюдаться:
- различные болевые ощущения;
- боль в горле;
- диарея;
- конъюнктивит;
- головная боль;
- потеря обоняния и вкусовых ощущений;
- сыпь на коже или депигментация ногтей на руках и ногах.
Симптомы тяжелой формы заболевания:
- затрудненное дыхание или одышка;
- ощущение сдавленности или боль в грудной клетке;
- нарушение речи или двигательных функций.
Если у вас наблюдаются симптомы тяжелой формы заболевания, незамедлительно обратитесь за медицинской помощью. Прежде чем посещать клинику или больницу, позвоните и предупредите о своем визите."""
        # Отправляем текст в Телеграм
        bot.send_message(call.message.chat.id, msg)
    elif call.data == "seb":
        # Формируем гороскоп
        msg = """Если вам кажется, что у вас есть симптомы коронавируса или ОРВИ — вызовите врача. Лучше оставаться дома, чтобы не заражать других.
не стоит заниматься самолечением и использовать народные средства — своевременная медицинская помощь может облегчить симптомы и предотвратить развитие заболевания.
Обратиться к врачу можно по телефону, указанному на сайте вашей поликлиники, или по номерам 112 или 103, а также по номеру горячей линии: 8-800-2000-112."""
        # Отправляем текст в Телеграм
        bot.send_message(call.message.chat.id, msg)
    elif call.data == "mif":
        # Формируем гороскоп
        msg = """Вспышки новых инфекции, в том числе вирусных, часто приводят к распространению недостоверной информации об их симптомах, передаче и лечении. Всемирная организация здравоохранения опровергла популярные мифы о новом коронавирусе.
— Почта из Китая не представляет угрозы — новым коронавирусом нельзя заразиться через писЬма и посылки.
— На данный момент нет никаких доказательств, что домашние животные — например, собаки или кошки — могут быть переносчиками нового коронавируса.
— Вакцины против пневмонии не защищают от нового коронавируса.
Для него требуется специальная вакцина, которую прямо сейчас разрабатывают ученые.
— Не существует никаких доказательств, что чеснок, кунжутное масло, жидкость для полоскания рта или солевой раствор для носа помогают в борьбе с вирусом.
— Новый коронавирус не лечится антибиотиками. Их могут назначить, если вирус привёл к развитию бактериальных инфекций — только против них и действуют антибиотики.
— На данный момент специальных лекарств для профилактики или лечения нового коронавируса нет — ученые работают над их созданием. Тем не менее обращаться к врачу необходимо каждому пациенту. Медицинская помощь поможет облегчить симптомы и не допустить дальнейшего развития заболевания."""
        # Отправляем текст в Телеграм
        bot.send_message(call.message.chat.id, msg)


bot.polling(none_stop=True, interval=0)
