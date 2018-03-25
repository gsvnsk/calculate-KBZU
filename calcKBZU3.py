# -*- coding: utf-8 -*-

from __future__ import print_function

token = '471830238:AAHEkYhFIkfsd5SvluOOaolMeLMFz9WrVqI'
import telebot
from telebot import types
from datetime import datetime, timedelta

bot = telebot.TeleBot(token)
#global Person

class Person:
    def __init__(self, name):
        self.name = name
        self.weightfakt = 0
        self.weightplan = 0
        self.weightdef = 0
        self.program = 0
        self.idiet = 0
        self.age = 18
        self.sex = 0

person_dict = {}
# Handle '/start' and '/help'
# Программа
# Стройность==0
# Масса==1
# Рельеф==2
# Возраст==3
# Особая==4
# Sex  Жен==0 Муж==1
# weightdef Учёт дефицита веса Нет=0, Да=1

programs = ['Стройность','Масса','Рельеф']

# Функция расчёта количества белков, жиров, углеводов и калорий
# в зависимости от веса, пола, программы и типа дня
def calculCPFC(weightfakt, weightplan, sex, program,iDiet,weightdef):

    global fatlunch, fatdinner, fatsupper,\
            carbohydratelunch, carbohydratedinner,carbohydratesupper,\
            proteinlunch, proteindinner,proteinsupper,\
            calorylunch, calorydinner,calorysupper,\
            fattotal,carbohydratetotal,proteintotal,calorytotal

# Все коэффициенты в массивах зависят от типа дня и от типа программы
# Тип диеты дня        НУг   СрУг ВУг
# Тип программы        Стройность Масса Рельеф

# Коэффициент для расчёта количества белка на день в зависимости от веса и пола
    proteinDietkoeff = [[2.5, 2.3, 2.0],
                        [2.3, 2.3, 2.3],
                        [2.5, 2.3, 2.0]]
# Изменения для 3 сезона 17.03.2018
#    proteinDietkoeff = [[2.3, 2.0, 1.5],
#                        [2.3, 2.3, 2.3],
#                        [2.3, 2.0, 1.5]]
    if sex == 1:
        proteinDietkoeff = [[2.5, 2.5, 2.3],
                            [2.5, 2.5, 2.5],
                            [2.5, 2.3, 2.3]]

# Изменения для 3 сезона 17.03.2018
#    if sex == 1:
#        proteinDietkoeff = [[3.0, 2.5, 2.0],
#                            [2.5, 2.5, 2.5],
#                            [3.0, 2.5, 2.0]]
# Коэффициент для расчёта количества жира на день в зависимости от веса и пола
    fatDietkoeff = [[1.0, 0.8, 0.8],
                    [1.0, 1.0, 1.0],
                    [1.0, 0.8, 0.8]]
# Изменения для 3 сезона 17.03.2018
#    fatDietkoeff = [[0.9, 0.8, 0.8],
#                    [1.0, 1.0, 1.0],
#                    [0.9, 0.8, 0.8]]
    if sex == 1:
        fatDietkoeff = [[0.8, 0.7, 0.7],
                        [1.0, 1.0, 1.0],
                        [0.8, 0.7, 0.7]]
# Изменения для 3 сезона 17.03.2018
#    if sex == 1:
#        fatDietkoeff = [[0.8, 0.7, 0.7],
#                        [1.0, 1.0, 1.0],
#                        [0.8, 0.7, 0.7]]

# Коэффициент для расчёта количества углеводов на день в зависимости от веса и пола
    carbohydrateDietkoeff = [[0.5, 1.3, 2.0],
                             [1.7, 2.1, 3.2],
                             [0.8, 1.5, 2.2]]
# Изменения для 3 сезона 17.03.2018
#    carbohydrateDietkoeff = [[0.8, 1.5, 2.3],
#                             [1.7, 2.1, 3.5],
#                             [1.2, 1.7, 2.5]]
    if sex == 1:
        carbohydrateDietkoeff = [[0.7, 1.7, 2.0],
                                 [2.0, 2.3, 4.0],
                                 [1.2, 1.8, 2.6]]

# Изменения для 3 сезона 17.03.2018
#    if sex == 1:
#        carbohydrateDietkoeff = [[1.0, 2.0, 2.5],
#                                 [2.0, 2.3, 4.0],
#                                 [1.4, 2.2, 2.7]]

    # Названия Программ
#    Programms = [u'Стройность', u'Масса', u'Рельеф']

# Лимиты для расчёта количества белка на день в зависимости от пола
    proteinlimit = [[999.0, 999.0, 999.0],
                    [999.0, 999.0, 999.0],
                    [999.0, 999.0, 999.0]]
    if sex == 1:
        proteinlimit = [[200.0, 200.0, 180.0],
                        [200.0, 200.0, 200.0],
                        [200.0, 200.0, 180.0]]

# Изменения для 3 сезона 17.03.2018
#    if sex == 1:
#        proteinlimit = [[260.0, 999.0, 999.0],
#                        [200.0, 200.0, 200.0],
#                        [260.0, 200.0, 999.0]]

# Лимиты для расчёта количества жира на день в зависимости от пола
    fatlimit = [[80.0, 80.0, 80.0],
                [65.0, 65.0, 65.0],
                [80.0, 80.0, 80.0]]
# Изменения для 3 сезона 17.03.2018
#    fatlimit = [[80.0, 80.0, 80.0],
#                [65.0, 65.0, 65.0],
#                [60.0, 60.0, 60.0]]

    if sex == 1:
        fatlimit = [[80.0, 80.0, 80.0],
                    [80.0, 80.0, 80.0],
                    [80.0, 80.0, 80.0]]
# Изменения для 3 сезона 17.03.2018
#    if sex == 1:
#       fatlimit = [[80.0, 80.0, 80.0],
#                   [80.0, 80.0, 80.0],
#                   [70.0, 70.0, 70.0]]

# Лимиты для расчёта количества углеводов на день в зависимости от пола
    carbohydratelimit = [[60.0, 80.0, 130.0],
                         [120.0, 170.0, 200.0],
                         [60.0, 80.0, 160.0]]

# Изменения для 3 сезона 17.03.2018
#    carbohydratelimit = [[999.0, 80.0, 140.0],
#                         [120.0, 170.0, 200.0],
#                         [999.0, 95.0, 170.0]]

    if sex == 1:
        carbohydratelimit = [[999.0, 140.0, 150.0],
                             [150.0, 200.0, 230.0],
                             [999.0, 150.0, 200.0]]

# Изменения для 3 сезона 17.03.2018
#    if sex == 1:
#        carbohydratelimit = [[999.0, 150.0, 160.0],
#                             [150.0, 200.0, 230.0],
#                             [999.0, 160.0, 180.0]]

# Коэффициент для расчёта количества белка на Завтрак-Обед-Ужин в зависимости от программы
    proteindaykoeff = [[0.30, 0.35, 0.35],
                       [0.30, 0.35, 0.35],
                       [0.30, 0.35, 0.35]]
# Коэффициент для расчёта количества жира на Завтрак-Обед-Ужин в зависимости от программы
    fatdaykoeff = [[0.40, 0.30, 0.30],
                   [0.40, 0.30, 0.30],
                   [0.40, 0.30, 0.30]]
# Коэффициент для расчёта количества углеводов на Завтрак-Обед-Ужин в зависимости от программы
    carbohydratedaykoeff = [[0.60, 0.40, 0.0],
                            [0.40, 0.35, 0.25],
                            [0.60, 0.40, 0.0]]

# Расчёт общего дневного количества белков, жиров, углеводов и калорий
    #Программа Стройность и Программа Рельеф
    if program == 0 or  program ==2 :
        fattotal = weightfakt * fatDietkoeff[program][iDiet]
        if fattotal > fatlimit[program][iDiet]: fattotal = fatlimit[program][iDiet]
        carbohydratetotal = weightplan * carbohydrateDietkoeff[program][iDiet]
        if carbohydratetotal > carbohydratelimit[program][iDiet]: carbohydratetotal = \
        carbohydratelimit[program][iDiet]
        proteintotal = weightplan * proteinDietkoeff[program][iDiet]
        if proteintotal > proteinlimit[program][iDiet]: proteintotal = proteinlimit[program][
            iDiet]
        calorytotal = (carbohydratetotal + proteintotal) * 4. + fattotal * 9.

    #Программа Масса
    if program == 1 :
        fattotal = weightfakt * fatDietkoeff[program][iDiet]
        if fattotal > fatlimit[program][iDiet]: fattotal = fatlimit[program][iDiet]
        carbohydratetotal = weightfakt * carbohydrateDietkoeff[program][iDiet]
        if carbohydratetotal > carbohydratelimit[program][iDiet]: carbohydratetotal = \
        carbohydratelimit[program][iDiet]
        proteintotal = weightfakt * proteinDietkoeff[program][iDiet]
        if proteintotal > proteinlimit[program][iDiet]: proteintotal = proteinlimit[program][
            iDiet]
        calorytotal = (carbohydratetotal + proteintotal) * 4. + fattotal * 9.

# Изменение от 22.02.2018 Учет дефицита массы тела
#Строй Жен Низко Белок 2,5 гр/кг желаемого веса  если желаемый вес менее 50кг, то белков в сутки должно быть минимум 140г
# weightfakt, weightplan, sex, program,iDiet,weightdef
    if program==0 and sex==0 and iDiet==0 and weightplan>0 and (weightplan<50 or weightdef==1 ):
        if proteintotal < 140 : proteintotal = 140

#Масса Жен Низко Белок 2,3 гр/кг фактического веса Если фактический вес менее 55кг, умножаем на 2,5
    if program == 1 and sex == 0 and (weightplan < 55 or weightdef == 1): proteintotal = weightfakt * 2.5
#Масса Жен Средне  Белок 2,3 гр/кг Если фактический вес менее 55кг, умножаем на 2,5.
#    if program == 1 and sex == 0 and iDiet == 1 and (weightplan < 55 or weightdef == 1): proteintotal = weightfakt * 2.5
#Масса Жен Высоко Белок 2,3 гр/кг Если фактический вес менее 55кг, умножаем на 2,5
#    if program == 1 and sex == 0 and iDiet == 2 and (weightplan < 55 or weightdef == 1): proteintotal = weightfakt * 2.5

#Масса Жен Низко Жир 1 гр/кг фактического веса Если фактический вес менее 55кг, умножаем на 1,5
    if program == 1 and sex == 0 and (weightplan < 55 or weightdef == 1): fattotal = weightfakt * 1.5
#Масса Жен Средне  Жир 1 гр/кг Если фактический вес менее 55кг, умножаем на 1,5
#    if program == 1 and sex == 0 and iDiet == 1 and (weightplan < 55 or weightdef == 1): fattotal = weightfakt * 1.5
#Масса Жен Высоко Жир 1 гр/кг Если фактический вес менее 55кг, умножаем на 1,5
#    if program == 1 and sex == 0 and iDiet == 2 and (weightplan < 55 or weightdef == 1): fattotal = weightfakt * 1.5

#Масса Жен Низко Углеводы 1,7 гр/кг фактического веса Если фактический вес менее 55кг, умножаем на 2, не более 150г углеводов в сутки
    if program == 1 and sex == 0 and iDiet == 0 and (weightplan < 55 or weightdef == 1):
        carbohydratetotal = weightfakt * 2
        if carbohydratetotal > 150 : carbohydratetotal=150
#Масса Жен Средне  Углеводы 2,1 гр/кг Если фактический вес менее 55кг, умножаем на 2,3
    if program == 1 and sex == 0 and iDiet == 1 and (weightplan < 55 or weightdef == 1): carbohydratetotal = weightfakt * 2.3
#Масса Жен Высоко Углеводы 2,7-3,5 гр/кг фактического веса  Если фактический вес менее 55кг, умножаем на 3
    if program == 1 and sex == 0 and iDiet == 1 and (weightplan < 55 or weightdef == 1): carbohydratetotal = weightfakt * 3

# Расчёт отдельно количества белков, жиров, углеводов и калорий на Завтрак-Обед-Ужин
    fatlunch = fattotal * fatdaykoeff[program][0]
    fatdinner = fattotal * fatdaykoeff[program][1]
    fatsupper = fattotal * fatdaykoeff[program][2]

    carbohydratelunch = carbohydratetotal * carbohydratedaykoeff[program][0]
    carbohydratedinner = carbohydratetotal * carbohydratedaykoeff[program][1]
    carbohydratesupper = carbohydratetotal * carbohydratedaykoeff[program][2]

    proteinlunch = proteintotal * proteindaykoeff[program][0]
    proteindinner = proteintotal * proteindaykoeff[program][1]
    proteinsupper = proteintotal * proteindaykoeff[program][2]

    calorylunch = (carbohydratelunch + proteinlunch) * 4. + fatlunch * 9.
    calorydinner = (carbohydratedinner + proteindinner) * 4. + fatdinner * 9.
    calorysupper = (carbohydratesupper + proteinsupper) * 4. + fatsupper * 9.

    return  (fatlunch, fatdinner, fatsupper,
            carbohydratelunch, carbohydratedinner,carbohydratesupper,
            proteinlunch, proteindinner,proteinsupper,
            calorylunch, calorydinner,calorysupper,
            fattotal,carbohydratetotal,proteintotal,calorytotal)

#Функция печати на экране личных показателей и резальтатов расчета
def printscreenCPFC(name, fatlunch, fatdinner, fatsupper, \
            carbohydratelunch, carbohydratedinner, carbohydratesupper, \
            proteinlunch, proteindinner, proteinsupper, \
            calorylunch, calorydinner, calorysupper, \
            fattotal, carbohydratetotal, proteintotal, calorytotal):
    person = person_dict[name]
    CPFCstring = format(u'🔥Вес ' + \
                        str(person.weightfakt) + u'-->' + \
                        str(person.weightplan) + u'\nПр-ма ' + \
                        Programms[person.program])
    if (person.sex == 1):
        CPFCstring = CPFCstring + u' для мужчин'
    else:
        CPFCstring = CPFCstring + u' для женщин'
    if (person.weightdef == 1):
        CPFCstring = CPFCstring + u' с дефицитом веса'

    bot.send_message(name, CPFCstring)

    CPFCstring = format(u'🔥        Утро    Обед    Ужин')
    CPFCstring = CPFCstring + '\n' + u'Ж гр.     {0:>2.0f}  {1:>8.0f}   {2:>8.0f}'.format(fatlunch, fatdinner,
                                                                                          fatsupper)
    CPFCstring = CPFCstring + '\n' + u'У гр.      {0:>2.0f}  {1:>8.0f}   {2:>8.0f}'.format(carbohydratelunch,
                                                                                           carbohydratedinner,
                                                                                           carbohydratesupper)
    CPFCstring = CPFCstring + '\n' + u'Б гр.      {0:>2.0f}  {1:>8.0f}   {2:>8.0f}'.format(proteinlunch, proteindinner,
                                                                                           proteinsupper)
    CPFCstring = CPFCstring + '\n' + u'К          {0:>2.0f} {1:>8.0f} {2:>8.0f}'.format(calorylunch, calorydinner,
                                                                                        calorysupper)
    bot.send_message(name, CPFCstring)

    CPFCstring = format(u'Всего на день') + '\n' + u'Жиры гр.          {0:>2.0f}'.format(fattotal)
    CPFCstring = CPFCstring + '\n' + u'Углеводы гр.  {0:>2.0f}'.format(carbohydratetotal)
    CPFCstring = CPFCstring + '\n' + u'Белки гр.        {0:>2.0f}'.format(proteintotal)
    CPFCstring = CPFCstring + '\n' + u'Калории        {0:>2.0f}'.format(calorytotal)
    bot.send_message(name, CPFCstring)

    return

# Названия Программ
Programms = [u'Стройность', u'Масса', u'Рельеф']

# Типы дней и названия типов дней
idietsday = [0, 1, 0, 1, 0, 1, 2, 0, 1]
# Изменения для 3 сезона 17.03.2018
#idietsday = [0, 1, 0, 1, 0, 1, 2, 0, 1]
idietsdayStr = [u'Низкоуглеводный', u'Среднеуглеводный', u'Высокоуглеводный']

# Расчёт и контрольная печать расчёта
#calculCPFC(Person.weightfakt, Person.weightplan, Person.sex, Person.program, Person.idiet, Person.weightdef)

CPFKstring = format(u'Распределение суточного \n КБЖУ по приёмам пищи\n Бот стартовал ')
print(CPFKstring)
# Изменение 22.02.2018 -  убрать контрольную распечатку
#CPFKstring = format(u"КБЖУ       Завтрак      Обед      Ужин    Итого")
#print (CPFKstring)
#CPFKstring = u'Жиры гр.    {0:>6.0f} {1:>8.0f} {2:>8.0f} {3:>8.0f}'.format(fatlunch, fatdinner, fatsupper, fattotal)
#print (CPFKstring)
#CPFKstring = u'Углеводы гр.{0:>6.0f} {1:>8.0f} {2:>8.0f} {3:>8.0f}'.format(carbohydratelunch, carbohydratedinner, carbohydratesupper, carbohydratetotal)
#print (CPFKstring)
#CPFKstring = u'Белки гр.   {0:>6.0f} {1:>8.0f} {2:>8.0f} {3:>8.0f}'.format(proteinlunch, proteindinner, proteinsupper, proteintotal)
#print (CPFKstring)
#CPFKstring = u'Калории     {0:>6.0f} {1:>8.0f} {2:>8.0f} {3:>8.0f}'.format(calorylunch, calorydinner, calorysupper, calorytotal)
#print (CPFKstring)

# Старт диалога для расчёта
@bot.message_handler(commands=['help', 'start'])
# Печать на экране меню для выбора вида расчёта
def process_menu1_step(message):
    try:
        name = message.chat.id
        person = Person(name)
        person_dict[name] = person
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        markup.row(u'🔥Вес ' + \
            str(person.weightfakt) + u'-->' + \
            str(person.weightplan) + u'\nПр-ма ' + \
            Programms[person.program], u'⚙Настройки')
        markup.row(u'КБЖУ-1\n' + datetime.strftime(datetime.today(), '%d-%b'), u' КБЖУ-2\n' \
            + datetime.strftime(datetime.today() + timedelta(1), '%d-%b'), u' КБЖУ-3\n' \
            + datetime.strftime(datetime.today() + timedelta(2), '%d-%b'))
        markup.row(u'КБЖУ день\nнизкоугле', u'КБЖУ день\nсреднеугле', u'КБЖУ день\nвысокоугле')
        msg = bot.reply_to(message, u'Выберите пункт меню', reply_markup=markup)
        bot.register_next_step_handler(msg, process_name_step)
    except Exception as e:
        bot.reply_to(message, 'menu1oooops')

# Расчёт, печать и переход в зависимости от нажатой кнопки меню
def process_name_step(message):
    try:
        name = message.chat.id
        person = person_dict[name]
        txtmsg = message.text
        if   (u'КБЖУ-1' in txtmsg):
            iDiet = idietsday[datetime.weekday(datetime.today())]
            calculCPFC(person.weightfakt, person.weightplan, person.sex, person.program, iDiet, person.weightdef)
            CPFCstring = format(u'КБЖУ на ' + datetime.strftime(datetime.today(), '%d-%b') + '\n' \
                                + u'Автор @SergeyNovosib' + '\n' \
                                + idietsdayStr[iDiet] + u' день')
            bot.send_message(name, CPFCstring)
            printscreenCPFC(name, fatlunch, fatdinner, fatsupper,
                            carbohydratelunch, carbohydratedinner, carbohydratesupper,
                            proteinlunch, proteindinner, proteinsupper,
                            calorylunch, calorydinner, calorysupper,
                            fattotal, carbohydratetotal, proteintotal, calorytotal)

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
            msg = bot.reply_to(message, u'Выберите пункт меню', reply_markup=markup)
            bot.register_next_step_handler(msg, process_name_step)
        elif (u'КБЖУ-2' in txtmsg):
            iDiet = idietsday[datetime.weekday(datetime.today()+ timedelta(1))]
            calculCPFC(person.weightfakt, person.weightplan, person.sex, person.program, iDiet, person.weightdef)
            CPFCstring = format(u'КБЖУ на ' + datetime.strftime(datetime.today()+ timedelta(1), '%d-%b') + '\n' \
                                + u'Автор @SergeyNovosib' + '\n' \
                                + idietsdayStr[iDiet] + u' день')
            bot.send_message(name, CPFCstring)
            printscreenCPFC(name, fatlunch, fatdinner, fatsupper,
                            carbohydratelunch, carbohydratedinner, carbohydratesupper,
                            proteinlunch, proteindinner, proteinsupper,
                            calorylunch, calorydinner, calorysupper,
                            fattotal, carbohydratetotal, proteintotal, calorytotal)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
            msg = bot.reply_to(message, u'Выберите пункт меню', reply_markup=markup)
            bot.register_next_step_handler(msg, process_name_step)
        elif (u'КБЖУ-3' in txtmsg):
            iDiet = idietsday[datetime.weekday(datetime.today()+ timedelta(2))]
            calculCPFC(person.weightfakt, person.weightplan, person.sex, person.program, iDiet, person.weightdef)
            CPFCstring = format(u'КБЖУ на ' + datetime.strftime(datetime.today()+ timedelta(2), '%d-%b') + '\n' \
                                + u'Автор @SergeyNovosib' + '\n' \
                                + idietsdayStr[iDiet] + u' день')
            bot.send_message(name, CPFCstring)

            printscreenCPFC(name, fatlunch, fatdinner, fatsupper,
                            carbohydratelunch, carbohydratedinner, carbohydratesupper,
                            proteinlunch, proteindinner, proteinsupper,
                            calorylunch, calorydinner, calorysupper,
                            fattotal, carbohydratetotal, proteintotal, calorytotal)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
            msg = bot.reply_to(message, u'Выберите пункт меню', reply_markup=markup)
            bot.register_next_step_handler(msg, process_name_step)

        elif (u'низкоугле' in txtmsg):
            iDiet = 0
            calculCPFC(person.weightfakt, person.weightplan, person.sex, person.program, iDiet, person.weightdef)
            CPFCstring = format(u'КБЖУ на ' + idietsdayStr[iDiet] + u' день')
            bot.send_message(name, CPFCstring)
            printscreenCPFC(name, fatlunch, fatdinner, fatsupper,
                            carbohydratelunch, carbohydratedinner, carbohydratesupper,
                            proteinlunch, proteindinner, proteinsupper,
                            calorylunch, calorydinner, calorysupper,
                            fattotal, carbohydratetotal, proteintotal, calorytotal)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
            msg = bot.reply_to(message, u'Выберите пункт меню', reply_markup=markup)
            bot.register_next_step_handler(msg, process_name_step)

        elif (u'среднеугле' in txtmsg):
            iDiet = 1
            calculCPFC(person.weightfakt, person.weightplan, person.sex, person.program, iDiet, person.weightdef)
            CPFCstring = format(u'КБЖУ на ' + idietsdayStr[iDiet] + u' день')
            bot.send_message(name, CPFCstring)
            printscreenCPFC(name, fatlunch, fatdinner, fatsupper,
                            carbohydratelunch, carbohydratedinner, carbohydratesupper,
                            proteinlunch, proteindinner, proteinsupper,
                            calorylunch, calorydinner, calorysupper,
                            fattotal, carbohydratetotal, proteintotal, calorytotal)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
            msg = bot.reply_to(message, u'Выберите пункт меню', reply_markup=markup)
            bot.register_next_step_handler(msg, process_name_step)

        elif (u'высоко' in txtmsg):
            iDiet = 2
            calculCPFC(person.weightfakt, person.weightplan, person.sex, person.program, iDiet, person.weightdef)
            CPFCstring = format(u'КБЖУ на ' + idietsdayStr[iDiet] + u' день')
            bot.send_message(name, CPFCstring)
            printscreenCPFC(name, fatlunch, fatdinner, fatsupper,
                            carbohydratelunch, carbohydratedinner, carbohydratesupper,
                            proteinlunch, proteindinner, proteinsupper,
                            calorylunch, calorydinner, calorysupper,
                            fattotal, carbohydratetotal, proteintotal, calorytotal)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            msg = bot.reply_to(message, u'Выберите пункт меню', reply_markup=markup)
            bot.register_next_step_handler(msg, process_name_step)

        elif   (txtmsg == u'Мужчина'):
            person.sex = 1
            markup2 = types.ReplyKeyboardMarkup(resize_keyboard=False, one_time_keyboard=False)
            msg = bot.reply_to(message, u'⚙Настройки', reply_markup=markup2)
            bot.register_next_step_handler(msg, process_name_step)
        elif (txtmsg == u'Женщина'):
            person.sex = 0
            markup2 = types.ReplyKeyboardMarkup(resize_keyboard=False, one_time_keyboard=False)
            msg = bot.reply_to(message, u'⚙Настройки', reply_markup=markup2)
            bot.register_next_step_handler(msg, process_name_step)
        elif (u'Стройность' in txtmsg):
            person.program = 0
            markup2 = types.ReplyKeyboardMarkup(resize_keyboard=False, one_time_keyboard=False)
            msg = bot.reply_to(message, u'⚙Настройки', reply_markup=markup2)
            bot.register_next_step_handler(msg, process_name_step)
        elif (u'Масса' in txtmsg):
            person.program = 1
            markup2 = types.ReplyKeyboardMarkup(resize_keyboard=False, one_time_keyboard=False)
            msg = bot.reply_to(message, u'⚙Настройки', reply_markup=markup2)
            bot.register_next_step_handler(msg, process_name_step)
        elif (u'Рельеф' in txtmsg):
            person.program = 2
            markup2 = types.ReplyKeyboardMarkup(resize_keyboard=False, one_time_keyboard=False)
            msg = bot.reply_to(message, u'⚙Настройки', reply_markup=markup2)
            bot.register_next_step_handler(msg, process_name_step)
        elif (u'Дефицит' in txtmsg):
            if person.weightdef == 1:
                person.weightdef = 0
            else:
                person.weightdef = 1

            markup2 = types.ReplyKeyboardMarkup(resize_keyboard=False, one_time_keyboard=False)
            msg = bot.reply_to(message, u'⚙Настройки', reply_markup=markup2)
            bot.register_next_step_handler(msg, process_name_step)
        elif (u'план' in txtmsg):
            person.weightplan = 1
            msg = bot.reply_to(message, u'Ваш вес по плану?')
            bot.register_next_step_handler(msg, process_weightplan_step)
        elif (u'факт' in txtmsg):
            person.weightfakt = 1
            msg = bot.reply_to(message, u'Ваш вес факт в начале?')
            bot.register_next_step_handler(msg, process_weightfakt_step)

        elif (u'Настройки' in txtmsg):

# Печать меню для выбора настроек расчёта
            markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
            if person.weightdef == 1:
                CPFCstring = u'Дефицит\nвеса❓НЕТ'
            else:
                CPFCstring = u'Дефицит\nвеса❓ДА'
#            markup2.row(u'Вес факт\n' + str(Person.weightfakt) + u'❓', u'Вес план\n' + str(Person.weightplan) + u'❓',
#            Изменение 22.02.2018 - в Настройках убрать из кнопки цифры веса
            markup2.row(u'Вес факт❓', u'Вес план❓',
                        CPFCstring)
            markup2.row(u'Мужчина', u'Женщина')
            markup2.row(u'Программа\nРельеф', u'Программа\nМасса')
            markup2.row(u'Программа\nСтройность', u'⬅Назад')
            msg = bot.reply_to(message, u'⚙Настройки', reply_markup=markup2)
            bot.register_next_step_handler(msg, process_name_step)
# Изменение 08.03.2018 Добавлено u'start' in txtmsg для корректного рестарта при зависании канала
        elif (u'Назад' in txtmsg or u'start' in txtmsg):

# Печать меню при возврате из настроек расчёта
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)

            markup.row(u'🔥Вес ' + \
                       str(person.weightfakt) + u'-->' + \
                       str(person.weightplan) + u'\nПр-ма ' + \
                       Programms[person.program], u'⚙Настройки')
            markup.row(u'КБЖУ-1\n' + datetime.strftime(datetime.today(), '%d-%b'), u' КБЖУ-2\n' \
                       + datetime.strftime(datetime.today() + timedelta(1), '%d-%b'), u' КБЖУ-3\n' \
                       + datetime.strftime(datetime.today() + timedelta(2), '%d-%b'))
            markup.row(u'КБЖУ день\nнизкоугле', u'КБЖУ день\nсреднеугле', u'КБЖУ день\nвысокоугле')

            msg = bot.reply_to(message, u'Выберите пункт меню', reply_markup=markup)

            bot.register_next_step_handler(msg, process_name_step)


        else:
            msg = bot.reply_to(message, u'Выберите пункт меню')
            bot.register_next_step_handler(msg, process_name_step)

    except Exception as e:
        msg = bot.reply_to(message, u'Выберите пункт меню')
        bot.register_next_step_handler(msg, process_name_step)

# Печать результатов расчёта
def process_print_screen_step(message):
    try:
        name = message.chat.id
        person = person_dict[name]
        txtmsg = message.text

        CPFCstring = format(u'🔥Вес ' + \
                       str(person.weightfakt) + u'-->' + \
                       str(person.weightplan) + u'\nПр-ма ' + \
                       Programms[person.program])
        if   (person.sex == 1):
            CPFCstring = CPFCstring + u' для мужчин'
        else: CPFCstring = CPFCstring + u' для женщин'
        if   (person.weightdef == 1):
            CPFCstring = CPFCstring + u' с дефицитом веса'

        bot.send_message(name, CPFCstring)

        iDiet = idietsday[datetime.weekday(datetime.today() + timedelta(2))]
        CPFCstring = format(u'КБЖУ ' + u'на '+ datetime.strftime(datetime.today(),'%d-%b')+ '\n' \
                            + idietsdayStr[iDiet] + u' день')
        bot.send_message(name, CPFCstring)
        CPFCstring = format(u'🔥        Утро    Обед    Ужин')
        CPFCstring = CPFCstring + '\n' + u'Ж гр.     {0:>2.0f}  {1:>8.0f}   {2:>8.0f}'.format(fatlunch, fatdinner, fatsupper)
        CPFCstring = CPFCstring + '\n' + u'У гр.      {0:>2.0f}  {1:>8.0f}   {2:>8.0f}'.format(carbohydratelunch, carbohydratedinner,carbohydratesupper)
        CPFCstring = CPFCstring + '\n' + u'Б гр.      {0:>2.0f}  {1:>8.0f}   {2:>8.0f}'.format(proteinlunch, proteindinner, proteinsupper)
        CPFCstring = CPFCstring + '\n' + u'К          {0:>2.0f} {1:>8.0f} {2:>8.0f}'.format(calorylunch, calorydinner, calorysupper)
        bot.send_message(name, CPFCstring)

        CPFCstring = format(u'Всего на день') + '\n' + u'Жиры гр.          {0:>2.0f}'.format(fattotal)
        CPFCstring = CPFCstring + '\n' +u'Углеводы гр.  {0:>2.0f}'.format(carbohydratetotal)
        CPFCstring = CPFCstring + '\n' + u'Белки гр.        {0:>2.0f}'.format(proteintotal)
        CPFCstring = CPFCstring + '\n' + u'Калории        {0:>2.0f}'.format(calorytotal)
        bot.send_message(message.chat.id, CPFCstring)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)

        markup.row(u'🔥Вес ' + \
                   str(person.weightfakt) + u'-->' + \
                   str(person.weightplan) + u'\nПр-ма ' + \
                   Programms[person.program], u'⚙Настройки')
        markup.row(u'КБЖУ-1\n' + datetime.strftime(datetime.today(), '%d-%b'), u' КБЖУ-2\n' \
                   + datetime.strftime(datetime.today() + timedelta(1), '%d-%b'), u' КБЖУ-3\n' \
                   + datetime.strftime(datetime.today() + timedelta(2), '%d-%b'))
        markup.row(u'КБЖУ день\nнизкоугле', u'КБЖУ день\nсреднеугле', u'КБЖУ день\nвысокоугле')

        msg = bot.reply_to(message, u'Выберите пункт меню', reply_markup=markup)

        bot.register_next_step_handler(msg, process_name_step)

    except Exception as e:
        bot.reply_to(message, '3oooops')

def process_weightfakt_step(message):
    try:
        name = message.chat.id
        person = person_dict[name]
        weightfakt = float(message.text.replace(",", "."))
#        weightfakt = message.text
        person.weightfakt = weightfakt
        if not weightfakt > 0:
            msg = bot.reply_to(message, u'Вес должен быть > 0. Ваш вес в начале?')
            bot.register_next_step_handler(msg, process_weightfakt_step)
            return
        markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        msg = bot.reply_to(message, u'Вес факт '+ str(person.weightfakt) , reply_markup=markup2)
        bot.register_next_step_handler(msg, process_name_step)

    except Exception as e:
        msg = bot.reply_to(message, u'Вес должен быть числом. Ваш вес в начале?')
        bot.register_next_step_handler(msg, process_weightfakt_step)


def process_weightplan_step(message):
    try:
        name = message.chat.id
        person = person_dict[name]
        weightplan = float(message.text.replace(",", "."))
        person.weightplan = weightplan
        if not weightplan > 0:
            msg = bot.reply_to(message, u'Вес должен быть > 0. Ваш вес по плану?')
            bot.register_next_step_handler(msg, process_weightplan_step)
            return
        markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        msg = bot.reply_to(message, u'Вес по плану '+ str(person.weightplan) , reply_markup=markup2)
        bot.register_next_step_handler(msg, process_name_step)

    except Exception as e:
        msg = bot.reply_to(message, u'Вес должен быть числом. Ваш вес по плану?')
        bot.register_next_step_handler(msg, process_weightplan_step)


# Изменение от 25.02.2018 ошибка по timeout. Увеличен timeout = 40 секунд
if __name__ == "__main__":
    bot.polling(none_stop=True,timeout=60)