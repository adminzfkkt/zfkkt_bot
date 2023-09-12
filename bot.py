#!/zfkk_bot python3

import telebot
import requests
import telegram

from telegram import BotCommand


from telebot import types

bot = telebot.TeleBot('6262291120:AAHWI73o1nKuKuqalgF-1x-MIgJ9a8yatto')


# Зберігатимемо інформацію про клієнтів та їхні файли в словнику
subscribed_users = {}
clients = {}

def get_latest_news():
    url = "https://zfkkt.org.ua/news/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all("article")
    
    latest_news = []
    for article in articles:
        title = article.find("h2").text
        link = url + article.find("a")["href"]
        latest_news.append((title, link))
    
    return latest_news


@bot.message_handler(commands=['start'])
def start(message):

    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Абітурієнт🙎‍♂🙎‍♀")
    item2 = types.KeyboardButton("Студент👨‍🎓👩‍🎓")
    item3 = types.KeyboardButton("Викладач👨‍🏫")
    item4 = types.KeyboardButton("Задати питання❓📝")
    item5 = types.KeyboardButton("Новини коледжу")
    back =  types.KeyboardButton("Повернутися↩️")
    markup.add(item1, item2, item3, item4, item5, back)
    bot.send_message(message.chat.id,'🖐 Ласкаво просимо, Я - ЗФККТбот, створенний для допомоги абітурієнтам, студентам та викладачам.', reply_markup=markup)


@bot.message_handler(commands=['reply_to_client'])
def reply_to_client(message):
    # Фахівець надсилає відповідь конкретному клієнту за його ID
    args = message.text.split()
    if len(args) < 3:
        bot.send_message(message.chat.id, "Неправильний формат команди. Введіть /reply_to_client <client_id> <message>")
        return
    client_id = int(args[1])
    if client_id not in clients:
        bot.send_message(message.chat.id, f"Клієнта з ID {client_id} не знайдено.")
        return
    response = " ".join(args[2:])
    bot.send_message(clients[client_id]["chat_id"], f"Фахівець відповів:\n{response}")


@bot.message_handler(content_types=['text', 'document', 'photo', 'video', 'voice', 'video_note'])
def bot_message(message):
        # Отримання повідомлень та медіа в режимі консультації
    client_data = None
    if message.text == "Задати питання❓📝":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 =  types.KeyboardButton("Повернутися↩️")
        markup.add(item1)
        bot.send_message(message.chat.id, 'Зв`язатись з нами можна за наступними телефонами:\n (061) 740-33-36 - приймальна комісія;\n (050) 532-70-10 – відповідальний секретар приймальної комісії;\n (061) 702-33-35 - приймальня директора коледжу;\n (061) 702-33-38 - бухгалтерія;\n (061) 702-33-37 - заступник директора з АГР;')
        # При отриманні відповіді "Консультація", збережемо ID клієнта в словнику
        clients[message.from_user.id] = {"chat_id": message.chat.id, "username": message.from_user.username, "mode": "consultation", "messages": []}
        bot.send_message(message.chat.id, 'Ви увійшли в режим консультації. Всі ваші надіслані повідомлення та медіа будуть переслані у груповий чат. Щоб закінчити консультацію, натисніть кнопку "Повернутися↩️".')        
        
    elif message.text == "Повернутися↩️" and message.from_user.id in clients and clients[message.from_user.id]["mode"] == "consultation":
        del clients[message.from_user.id]
        bot.send_message(message.chat.id, 'Ви вийшли з режиму консультації. Дякуємо!')
    elif message.from_user.id in clients and clients[message.from_user.id]["mode"] == "consultation":
        # Отримані дані від клієнта будуть переслані в груповий чат фахівців
        client_data = clients[message.from_user.id]
        client_data["messages"].append(message)
    if client_data:
        # Ви можете зберегти тут всі надіслані повідомлення та медіа у груповий чат
        for message in client_data["messages"]:
            if message.text:
                text = f'Клієнт @{client_data["username"]} (ID: {message.from_user.id}) надіслав повідомлення: {message.text}'
                bot.send_message(-985054076, text)
            if message.document:
                # Додавання інформації про клієнта для документів
                caption = f'Клієнт @{client_data["username"]} (ID: {message.from_user.id}) надіслав документ: {message.document.file_id}'
                bot.send_document(-985054076, message.document.file_id, caption=caption)
            if message.photo:
                # Додавання інформації про клієнта для фото
                caption = f'Клієнт @{client_data["username"]} (ID: {message.from_user.id}) надіслав фото: {message.photo[-1].file_id}'
                bot.send_photo(-985054076, message.photo[-1].file_id, caption=caption)
            if message.video:
                # Додавання інформації про клієнта для відео
                caption = f'Клієнт @{client_data["username"]} (ID: {message.from_user.id}) надіслав відео: {message.video.file_id}'
                bot.send_video(-985054076, message.video.file_id, caption=caption)
            if message.voice:
                # Додавання інформації про клієнта для голосових повідомлень
                caption = f'Клієнт @{client_data["username"]} (ID: {message.from_user.id}) надіслав голосове повідомлення: {message.voice.file_id}'
                bot.send_voice(-985054076, message.voice.file_id, caption=caption)
            if message.video_note:
                # Відправлення круглого відеоповідомлення
                bot.send_video(-985054076, message.video_note.file_id, caption='Це кругле відео')

        # Очистіть список повідомлень користувача після їх пересилання
        client_data["messages"].clear()

        bot.send_message(message.chat.id, 'Ваше повідомлення було відправлено фахівцям. Вони зв`яжуться з вами найближчим часом.')
    
    elif message.text == "Абітурієнт🙎‍♂🙎‍♀":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Анкета абітурієнта",)
        item2 = types.KeyboardButton("Підготовчі курси")
        item3 = types.KeyboardButton("Profi Forum")
        item4 = types.KeyboardButton("Спеціальності")
        item5 = types.KeyboardButton("Гуртожиток")
        item6 = types.KeyboardButton("Адреса колежду")
        item7 = types.KeyboardButton("Контакти📧☎")
        back =  types.KeyboardButton("Повернутися↩️")
        markup.add(item1, item2, item3, item4, item5, item6, item7, back)
        
        bot.send_message(message.chat.id, 'Вітаю тебе, о майбутній студент/студентка!🖖 Наш коледж приймає на навчанння за рахунок державного бюджету випускників 9-х та 11-х класів. Якщо тебе зацікавило навчання у коледжі або є питання, на які ти не знайшов відповіді, ти можеш заповнити Анкету абітурієнта, і ми зв`яжемося з тобою найближчим часом. ', reply_markup=markup)
    elif message.text == "Студент👨‍🎓👩‍🎓":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Розклад")
        item2 = types.KeyboardButton("Студентське самоврядування")
        item3 = types.KeyboardButton("Бібліотека")
        item4 = types.KeyboardButton("Гуртки, секції, проекти")
        item5 = types.KeyboardButton("Працевлаштування")
        item6 = types.KeyboardButton("Корисна інформація")
        back = types.KeyboardButton("Повернутися↩️")
        markup.add(item1, item2, item3, item4, item5, item6, back)
        bot.send_message(message.chat.id, 'Ця інформація призначена для студентів які вже навчаються в коледжі, тут вони можуть знайти корисну для них інформацію', reply_markup=markup)
    elif message.text == "Викладач👨‍🏫":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Графік освітнього процессу")
        item2 = types.KeyboardButton("Графік зайнятості викладачів")
        item3 = types.KeyboardButton("Графік чергувань")
        item4 = types.KeyboardButton("Навчально-методичний кабінет")
        item5 = types.KeyboardButton("Профспілка")
        item6 = types.KeyboardButton("Діяльність робочих та дорадчих органів")
        back = types.KeyboardButton("Повернутися↩️")
        markup.add(item1, item2, item3, item4, item5, item6, back)
        bot.send_message(message.chat.id, 'Ця інформація призначена для викладачів. Тут викладачі зможуть побачити графік заннять, а також інформацію необхідну для них', reply_markup=markup)
    elif message.text == "Анкета абітурієнта":
        bot.send_message(message.chat.id,'Переходь за покликанням, де ти можеш заповнити Анкету абітурієнта, і ми зв`яжемося з тобою найближчим часом: https://docs.google.com/forms/d/e/1FAIpQLSdRViwG9KnYIk4ETQrJ54gGVseCU_YaJyMnz8Ou2dyrx0JEfA/viewform')
    elif message.text == "Підготовчі курси":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Інтерактивний буклет")
        item2 = types.KeyboardButton("Розклад підготовчих курсів")
        item3 = types.KeyboardButton("Дистанційні курси")
        back = types.KeyboardButton("Повернутися↩️")
        markup.add(item1, item2, item3, back)
        bot.send_message(message.chat.id, 'ВСП “Запорізький фаховий коледж комп’ютерних технологій НУ “Запорізька політехніка” проводить підготовчі курси до вступу. Вартість курсів складає 2000₴ за весь період навчання.\n Період навчання складає 3 місяці.\n За підсумками курсів абітурієнтам нараховуються додаткові бали при вступі. http://zfkkt.org.ua/pidgotovchi-kursi-do-vstupu', reply_markup=markup) 
    elif message.text == "Інтерактивний буклет":
        bot.send_message(message.chat.id,'https://drive.google.com/file/d/1efMaNglUACfmGsJIDuKv8SHgYpCdlh3B/view')
    elif message.text == "Розклад підготовчих курсів":
        bot.send_message(message.chat.id,'Математика: Понеділок, Вівторок \n Українська мова:Середа,Четвер\n Початок занять о 16.00 \n https://zfkkt.org.ua/rozklad-pidgotovchik-kursiv')
    elif message.text == "Дистанційні курси":
        bot.send_message(message.chat.id,'1.Завантажити зразок заяви (https://drive.google.com/file/d/1snI_KSZpjjcrVXqMrc-Ytd5F79w8zFwm/view?usp=sharing) \n 2.Роздрукувати зразок та заповнити його \n 3.Відсканувати заповнений зразок \n 4.Надіслати скановану копію на адресу zfkktnuzp@ukr.net разом зі сканкопією квитанції про оплату курсів \n Довідка за телефоном +380683604017 - відповідальний секретар приймальної комісії \n УВАГА! В разі виконання оплати підготовчих курсів батьками або опікунами в "Призначені платежу" ОБОВ`ЯЗКОВО вказати ПІБ АБІТУРІЄНТА. \n Реквізити для оплати: \n ВСП «ЗФККТ НУ «Запорізька політехніка» \n Код ЄДРПОУ 34910699 \n Розр. рахунок UА598201720313201004201013669 \n Призначення: Оплата за підготовчі курси ПІБ АБІТУРІЄНТА')
    elif message.text == "Profi Forum":
        bot.send_message(message.chat.id, 'Profi Forum - це зустріч абітурієнтів із нашим коледжем та його викладачами, який проходить з 2021 р. На цьому заході абітурієнти можуть власноруч створити 3D модель, роздрукувати її на 3D принтері, опанувати паяльну станцію, особисто можуть задати питання викладачам та керівництву коледжа щодо перспектив їхніх майбутніх спеціальностей, умов вступу тощо. \n  Нижче можете ознайомитися із минулими заходами.')
        bot.send_message(message.chat.id, 'http://zfkkt.org.ua/child/profi-forum')
    elif message.text == "Спеціальності":
        bot.send_message(message.chat.id, 'Коледж здійснює навчання за наступними спеціальностями:\n 113 Прикладна математика\n 174 Автоматизація, комп’ютерно-інтегровані технології та робототехніка\n 123 Комп’ютерна інженерія\n 171 Електроніка\n 172 Електронні комунікації та радіотехніка')
        bot.send_message(message.chat.id, 'http://zfkkt.org.ua/specialnosti')
    elif message.text == "Гуртожиток":
        bot.send_message(message.chat.id, 'ВСП «ЗФККТ НУ «Запорізька політехніка» має в розпорядженні власний гуртожиток, який розташований за адресою м.Запоріжжя, пр. Соборний, 117а. \n Гуртожиток коледжу - це девятиповерхова будівля, яка знаходиться у безпосередній близькості до навчальних корпусів коледжа. \n Гуртожиток забезпечує 100% проживання усіх бажаючих студентів, де створені комфортні умови для їх проживання, самопідготовки та проведення дозвілля. \n Загальна кількість місць для проживання – 256. \n Станом на 01.11.2022 року кількість вільних місць – 0. \n Вартість проживання згідно кошторису (за ліжкомісце): \n - для студентів коледжів – 604 грн за місяць; \n - для студентів університетів – 800 грн за місяць; \n -для сторонніх осіб – не менше 1200 грн за місяць.')
    elif message.text == "Адреса колежду":
        markup = types.InlineKeyboardMarkup(row_width=1)
        item1 = types.InlineKeyboardButton("Прокласти маршрут", url='https://www.google.com/maps/dir//%D0%BF%D1%80%D0%BE%D1%81%D0%BF%D0%B5%D0%BA%D1%82+%D0%A1%D0%BE%D0%B1%D0%BE%D1%80%D0%BD%D0%B8%D0%B9,+117+%D0%97%D0%B0%D0%BF%D0%BE%D1%80%D1%96%D0%B6%D0%B6%D1%8F+%D0%97%D0%B0%D0%BF%D0%BE%D1%80%D1%96%D0%B6%D1%81%D0%BA%D0%B0+%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C+69000/@47.8306092,35.1527953,17z/data=!4m8!4m7!1m0!1m5!1m1!1s0x40dc60acadb87ac7:0x251ccc40267f52f8!2m2!1d35.1527953!2d47.8306092?entry=ttu')
        markup.add(item1)
        bot.send_message(message.chat.id, '📍Адреса: м. Запоріжжя, пр. Соборний, 117, зуп. транспорту "Площа Пушкіна"/"Трампарк"', reply_markup=markup)
        back = types.KeyboardButton("Повернутися↩️")
        markup.add(item1, back)
    elif message.text == "Контакти📧☎":
        bot.send_message(message.chat.id, 'Зв`язатись з нами можна за телефонами:\n (061) 740-33-36 - приймальна комісія;\n (050) 532-70-10 – відповідальний секретар приймальної комісії;\n (061) 702-33-35 - приймальня директора коледжу;\n (061) 702-33-38 - бухгалтерія;\n (061) 702-33-37 - заступник директора з АГР; \n пошта коледжу zfkktnuzp@ukr.net')
        bot.send_message(message.chat.id, 'Або через цей бот, повернувшись в стартове меню і обравши кнопку "Задати питання❓📝"' )
    elif message.text == "Розклад":
        markup = types.InlineKeyboardMarkup(row_width=1)
        item1 = types.InlineKeyboardButton("Переглянути в PDF форматі", url='https://drive.google.com/drive/folders/1422AWz1ISvrXvtXa2gRnu2WcYbyw8cRi')
        markup.add(item1)
        bot.send_message(message.chat.id, 'Подивитись на сайті коледжу https://zfkkt.org.ua/rozklad', reply_markup=markup)
    elif message.text == "Студентське самоврядування":
        bot.send_message(message.chat.id, 'Студентське самоврядування — це право і можливість студентів вирішувати питання навчання і побуту, захисту прав та інтересів студентів, а також брати участь в управлінні вищим навчальним закладом; є формою самоорганізації студентів, самостійною громадською діяльністю, механізмом представництва й відстоювання своїх прав і, найголовніше, можливістю самореалізації студента як відкритої, цілеспрямованої та освіченої особистості.')
        bot.send_message(message.chat.id, 'Студентська рада -  це виконавчий орган студентського самоврядування. Суть його існування полягає у реальній участі студентів в управлінні навчально-виховним процесом. Студентська рада не лише приймає участь у вирішення різноманітних освітніх питань у коледжі, а й самостійно планує, організовує, проводить різноманітні заходи: інтелектуального, розважального, спортивного характеру. Також підтримує студентську молодь, чия життєва позиція спрямована на активну участь у громадському житті, захищаючи права та інтереси студентів. Студентська рада коледжу у своїй структурі має студради відділень відповідних спеціальностей., які формуються за рахунок студентського самоврядування групи.')
        bot.send_message(message.chat.id, 'Студентське самоврядування групи складається зі старости групи, заступника старости та профорга. \n Анкета  "Хто ти?" https://forms.gle/AH2rbDBvMyfzwFh68 Заходь! Відповідай! Чиль! Пропонуй!  \n Приєднуйтесь до соцмереж: \n Instagram: https://www.instagram.com/student_zfkkt/ \n TG-канал студентів ЗФККТ: https://t.me/zfkkt \n Discord канал: https://discord.gg/wktStj6t')
        
    elif message.text == "Бібліотека":
        bot.send_message(message.chat.id, 'Бібліотека являє собою невідємну складову частину сучасного навчального закладу. Навіть в наш час загальної інформатизації книга все ще залишається безцінним носієм інформації. Знання багатьох поколінь вміло зібрані, чудово структуровані та легкодоступні містяться в книжках нашої бібліотеки.')
        bot.send_message(message.chat.id, 'Бібліотека коледжу розпочинає свою історію з 1944 року. На сьогоднішній день книжковий фонд бібліотеки налічує більше 55 тисяч примірників.')
        bot.send_message(message.chat.id,'Наразі в бібліотеці проводиться цикл робіт пов’язаних із впровадженням, спрямованої на задоволення найсучасніших потреб навчального процесу, полегшення пошукової роботи та осучаснення бібліотечної справи. Зараз кількість записів в електронній бібліотеці складає більше 14 тисяч примірників технічної літератури і на цьому робота не завершається.')
        bot.send_message(message.chat.id,'https://zfkkt.org.ua/child/elektronna-biblioteka-ta-jiji-znachimist')
    elif message.text == "Гуртки, секції, проекти":
        bot.send_message(message.chat.id, 'В нашому коледжі є багато багато гуртків, такі як:\n Предметні гуртки \n Гуртки розвитку професійних вмінь та навичок \n Гуртки розвитку "SOFT SKILLS" \n Спортивні секції')
        bot.send_message(message.chat.id, 'Ретельніше дізнатися про гуртки та секції ви зможете за посиланням')
        bot.send_message(message.chat.id, 'http://zfkkt.org.ua/gurtki-sekciji-proekti')
    elif message.text == "Працевлаштування":
        bot.send_message(message.chat.id, 'Сервісний центр "LEIT" запрошує здобувачів освіти 3-4 курсів спеціальностей:\n- 171 Електроніка;\n- 172 Телекомунікації та радіотехніка; \n- 151 Автоматизація та комп’ютерно-інтегровані технології \n- 123 Комп’ютерна інженерія\n Для ознайомлення з напрямком роботи центру (ремонт мобільних телефонів, планшетів, ноутбуків, встановлення додатків, комплексна діагностика техніки, малої та середньої побутової техніки, а також гіробордів, гіроскутерів, моноколеса, електросамокатіві тощо) з метою можливості проходження практичного навчання та подальшим працевлаштування.')
        bot.send_message(message.chat.id, 'Контакти:\n м. Запоріжжя , пр. Соборний , 64\n Tel: +380673257640, +380995200278\n Link:https://leit.in.ua/')
        bot.send_message(message.chat.id, 'ПІДРОЗДІЛ СПРИЯННЯ ПРАЦЕВЛАШТУВАННЮ ВИПУСКНИКІВ \n https://zfkkt.org.ua/vipuskniku')
    elif message.text == "Корисна інформація":
        bot.send_message(message.chat.id, 'Ознайомитись з корисною для студента інформацією ви зможете далі за посиланням')
        bot.send_message(message.chat.id, 'http://zfkkt.org.ua/korisna-informaciya')
    elif message.text == "Графік освітнього процессу":
        markup = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton("Переглянути в PDF форматі", url='https://drive.google.com/file/d/1fBlw27vwRliA12xzLA1zEOTjCJvowmSA/view?usp=sharing')
        item2 = types.InlineKeyboardButton("Графік екзаменів", url='https://drive.google.com/file/d/1fOJ1g9ekhe9WhruU3x_HzeLw6kBs-sD7/view')
        markup.add(item1, item2)
        bot.send_message(message.chat.id, 'Подивитись на сайті коледжу \n https://zfkkt.org.ua/grafik-navchalnogo-procesu', reply_markup=markup)
    elif message.text == "Графік зайнятості викладачів":
        bot.send_message(message.chat.id, 'Графік зайнятості викладачів')
        markup = types.InlineKeyboardMarkup(row_width=1)
        item1 = types.InlineKeyboardButton("Переглянути в PDF форматі", url='https://drive.google.com/file/d/14IlIN5of75aNmbd4MHcDF5EHN69tZw-2/view?usp=sharing')
        markup.add(item1)
        bot.send_message(message.chat.id, 'Подивитись на сайті коледжу \n https://zfkkt.org.ua/grafik-zaynyatosti-vikladachiv', reply_markup=markup)
    elif message.text == "Графік чергувань":
        markup = types.InlineKeyboardMarkup(row_width=1)
        item1 = types.InlineKeyboardButton("Переглянути в PDF форматі", url='https://drive.google.com/file/d/1Qnqfxu-zCt0_-HeOz7C9y2Rwm87Hsl4U/view?usp=sharing')
        markup.add(item1)
        bot.send_message(message.chat.id, 'Графік чергувань у гуртожитку', reply_markup=markup)
    elif message.text == "Навчально-методичний кабінет":
        bot.send_message(message.chat.id, 'Навчально-методичний кабінет призначений для розвитку професіїной компетентності та підвищення кваліфікації викладачів \n https://zfkkt.org.ua/metodkabinet')
        markup = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton("Планування розвитку професійних компетентностей викладачів", url='https://drive.google.com/file/d/1o5I6HGDWPdVZp-ZG4YTerkfA2vViiOTm/view?usp=sharing')
        item2 = types.InlineKeyboardButton("Форма обліку підвищення кваліфікації", url='https://forms.gle/7QDT3bsZQyC91hZq6')
        markup.add(item1, item2)
        bot.send_message(message.chat.id, 'Підвищення кваліфікації викладачів. \n Ви можете внести результати своїх курсів та семінарів натиснувши опцію "Форма обліку підвищення кваліфікації" ', reply_markup=markup)

    elif message.text == "Профспілка":
        markup = types.InlineKeyboardMarkup(row_width=4)
        item1 = types.InlineKeyboardButton("СТАТУТ ПРОФЕСІЙНОЇ СПІЛКИ ПРАЦІВНИКІВ РАДІОЕЛЕКТРОНІКИ ТА МАШИНОБУДУВАННЯ УКРАЇНИ", url='http://zfkkt.org.ua/files/Vukladachu/PROFSPILKA/C%D1%82%D0%B0%D1%82%D1%83%D1%82%20%D0%BF%D1%80%D0%BE%D1%84%D1%81%D0%BF%D1%96%D0%BB%D0%BA%D0%B8%20%D0%A0%20%D1%82%D0%B0%20%D0%9C%20%D0%A3%D0%BA%D1%80%D0%B0%D1%97%D0%BD%D0%B8.pdf')
        item2 = types.InlineKeyboardButton("СКЛАД ТА РОЗПОДІЛ ОБОВ’ЯЗКІВ МІЖ ЧЛЕНІВ ПРОФСПІЛКОВОГО КОМІТЕТУ ППО ЗКР ЗНТУ", url='https://drive.google.com/file/d/1zqu10BlzxqW_d47e52zrC71L8CWrROmi/view?usp=sharing')
        item3 = types.InlineKeyboardButton("СПИСОК ЧЛЕНІВ ПРОФСПІЛКИ ПРАЦІВНИКІВ РАДІОЕЛЕКТРОНІКИ І МАШИНОБУДУВАННЯ ЗКР ЗНТУ", url='http://zfkkt.org.ua/files/Vukladachu/PROFSPILKA/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA%20%D1%87%D0%BB%D0%B5%D0%BD%D1%96%D0%B2%20%D0%BF%D1%80%D0%BE%D1%84%D1%81%D0%BF%D1%96%D0%BB%D0%BA%D0%B8.pdf')
        item4 = types.InlineKeyboardButton("СТАТИСТИЧНИЙ ЗВІТ ПЕРВИННОЇ ПРОФСПІЛКОВОЇ ОРГАНІЗАЦІЇ ЗА 2017 РІК", url='http://zfkkt.org.ua/files/Vukladachu/PROFSPILKA/%D0%A1%D1%82%D0%B0%D1%82%D0%B8%D1%81%D1%82%D0%B8%D1%87%D0%BD%D0%B8%D0%B9%20%D0%B7%D0%B2%D1%96%D1%82%20%D0%BF%D0%BF%D0%BE.pdf')
        markup.add(item1, item2, item3, item4)
        bot.send_message(message.chat.id, 'У цьому розділі знаходиться інформація про профспілку працівників радіоелектроніки та машинобудування України \n https://zfkkt.org.ua/profspilka', reply_markup=markup)
    elif message.text =="Діяльність робочих та дорадчих органів":
        bot.send_message(message.chat.id, 'У цьому розділі показана діяльність таких органів як:\n Педагогічна рада https://zfkkt.org.ua/pedagogichna-rada \n Адміністративна рада https://zfkkt.org.ua/pedagogichna-rada \n Методична рада https://zfkkt.org.ua/metodichna-rada \n Атестаційна комісія http://zfkkt.org.ua/atestaciyna-komisiya')
        bot.send_message(message.chat.id, 'http://zfkkt.org.ua/diyalnist-robochih-ta-doradchih-organiv')
    elif message.text =="Повернутися↩️":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Абітурієнт🙎‍♂🙎‍♀")
        item2 = types.KeyboardButton("Студент👨‍🎓👩‍🎓")
        item3 = types.KeyboardButton("Викладач👨‍🏫")
        item4 = types.KeyboardButton("Задати питання❓📝")
        item5 = types.KeyboardButton("Новини коледжу")
        back =  types.KeyboardButton("Повернутися↩️")
        markup.add(item1, item2, item3, item4, item5, back)
        bot.send_message(message.chat.id, '🖐 Ласкаво просимо, Я - ЗФККТбот, створенний для допомоги абітурієнтам, студентам та викладачам.', reply_markup=markup)

    elif message.text == "Новини коледжу":
        markup = types.ReplyKeyboardMarkup(row_width=3)
        subscribe_btn = types.KeyboardButton('/subscribe')
        unsubscribe_btn = types.KeyboardButton('/unsubscribe')
        back = types.KeyboardButton("Повернутися↩️")
        markup.add(subscribe_btn, unsubscribe_btn, back)
        bot.send_message(message.chat.id, "Вітаю! Ви можете підписатися на новини за допомогою команди /subscribe.", reply_markup=markup)
    
    elif message.text == "/subscribe":
        chat_id = message.chat.id
        if chat_id not in subscribed_users:
            subscribed_users[chat_id] = []

        bot.send_message(chat_id, "Ви успішно підписалися на новини!")

    elif message.text == "/unsubscribe":
        chat_id = message.chat.id
        if chat_id in subscribed_users:
            del subscribed_users[chat_id]
            bot.send_message(chat_id, "Ви відписалися від новин.")

def send_news_to_subscribers():
    latest_news = get_latest_news()
    
    for chat_id, subscribed_articles in subscribed_users.items():
        for title, link in latest_news:
            if title not in subscribed_articles:
                bot.send_message(chat_id, f"📰 Новина: {title}\n🔗 Посилання: {link}")
                subscribed_users[chat_id].append(title)

@bot.message_handler(commands=['reply_to_client'])
def reply_to_client(message):
    # Перевірка, чи користувач вводить ідентифікаторx клієнта
    if len(message.text.split()) > 1:
        client_id = message.text.split()[1]  # Отримати id клієнта з команди
        client_id = int(client_id)  # Перевести id в цілочисельне значення
        if client_id in clients:
            # Перевірка, чи клієнт з таким id існує у словнику клієнтів
            bot.send_message(message.chat.id, f"Відповідь на питання клієнта @{clients[client_id]['username']}:")
            # Отримати текст відповіді від фахівця
            reply_text = " ".join(message.text.split()[2:])
            # Відправити відповідь клієнту
            bot.send_message(clients[client_id]['chat_id'], reply_text)
        else:
            bot.send_message(message.chat.id, "Клієнт з таким ID не знайдений.")
    else:
        bot.send_message(message.chat.id, "Будь ласка, введіть ID клієнта та текст відповіді у форматі: /reply_to_client [ID] [текст відповіді]")    

commands = [
    BotCommand("start", "Почати взаємодію з ботом"),
    BotCommand("help", "Допомога"),
    BotCommand("reply_to_client", "Відповісти клієнту")
]
bot.polling(none_stop=True)
