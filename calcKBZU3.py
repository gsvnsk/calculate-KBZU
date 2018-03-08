# -*- coding: utf- 8 -*-
#token = '471830238:AAHEkYhFIkfsd5SvluOOaolMeLMFz9WrVqI'
import telebot

#bot = telebot.TeleBot(token)
from telebot import types

from datetime import datetime
from datetime import date

class CPFCcalc:
    def __init__(self, name):
        self.name = name
        self.weightfakt = None
        self.weightplan = None
        self.program = None
        self.sex = None		 	# Жен==Female==0 Муж==Male==1
        self.daytype = None
        self.tday = None     	# ttoday==0 ttomorrow==1

user_dict = {}

###Программы###
#Стройность==Снижение веса==Lowerweight==0
#Стройность==Снижение веса==Lowerweight== Вес менее 50кг
#Масса==Mass==1
#Масса==Mass== Вес менее 55кг
#Рельеф==Relief==2
#Возраст-Мы молоды-Стать моложе==Age==3
#Особая==Special==4

#Sex  Жен==Female==0 Муж==Male==1

# На сегодня ttoday==0
# На завтра ttomorrow==1

# Вес сейчас
# Вес нужно
weightfakt=96
weightplan=89

###iDiet Тип диеты дня DietType[жен=0/муж=1]### 
# = 0 Низкоуглеводный    
# = 1 Среднеуглеводный   
# = 2 Высокоуглеводный   
# По графику
proteinDietkoeff=      [[2.5, 2.3, 2.0],\
						[2.5, 2.5, 2.3]]
fatDietkoeff=          [[1.0, 0.8, 0.8],\
						[0.8, 0.7, 0.7]]
carbohydrateDietkoeff= [[0.5, 1.3, 2.0],\
						[0.7, 1.7, 2.0]]


###Ограничение по КБЖУ для разных дней [жен=0/муж=1]### 
# = 0 Низкоуглеводный    день
# = 1 Среднеуглеводный   день
# = 2 Высокоуглеводный   день
proteinlimit=      [[999.0,  999.0,   999.0],\
					[200.0,  200.0,   180.0]]
fatlimit=          [[ 80.0,   80.0,    80.0],\
					[ 80.0,   80.0,   100.0]]
carbohydratelimit= [[ 60.0,   80.0,   130.0],\
					[999.0,  140.0,   150.0]]
# calorylimit=      [9999.  9999.   9999.]

###Распределение по приемам пищи### 
# = 0 программа Стройность
# = 1 программа Масса
# = 2 программа Рельеф
#                      lunch      dinner  supper
#                      Завтрак    Обед    Ужин
fatdaykoeff=         [[0.40,      0.30,   0.30],\
					  [0.30,      0.35,   0.35],\
					  [0.30,      0.35,   0.35]]
carbohydratedaykoeff=[[0.60,      0.40,    0.0],\
					  [0.40,      0.30,   0.30],\
					  [0.40,      0.30,   0.30]]
proteindaykoeff=     [[0.30,      0.35,   0.35,\
					  [0.40,      0.35,   0.25],\
					  [0.60,      0.40,   0.00]]

###iDiet Тип диеты дня DietType###
# = 0 Низкоуглеводный    
# = 1 Среднеуглеводный   
# = 2 Высокоуглеводный   

###Корректировки рациона при низком весе###
#программа Стройность вес < 50 кг
#Низкоуглеводный день белок
#
#программа Масса вес < 55 кг
#Низкоуглеводный день белок
#Среднеуглеводный день белок, углеводы
#Высокоуглеводный день белок, жиры, углеводы
#
#программа Рельеф вес < 50 кг
#Низкоуглеводный день белок
#

###iDietDay Тип диеты по дням недели ( Пн ... Вс,Пн)###
iDietDay = [1, 0, 1, 0, 1, 1, 2, 1, 0]
iDiet=iDietDay[datetime.weekday(date.today())]

# iDiet=0

fattotal=weightfakt*fatDietkoeff[iDiet]
if fattotal > fatlimit[iDiet]: fattotal = fatlimit[iDiet]
carbohydratetotal=weightplan*carbohydrateDietkoeff[iDiet]
if carbohydratetotal > carbohydratelimit[iDiet]: carbohydratetotal = carbohydratelimit[iDiet]
proteintotal=weightplan*proteinDietkoeff[iDiet]
if proteintotal > proteinlimit[iDiet]: proteintotal = proteinlimit[iDiet]
calorytotal=(carbohydratetotal+proteintotal)*4. + fattotal*9.


fateating[0]=fatlunch=fattotal*fatdaykoeff[0]
fateating[1]=fatdinner=fattotal*fatdaykoeff[1]
fateating[2]=fatsupper=fattotal*fatdaykoeff[2]

carboeating[0]=carbohydratelunch=carbohydratetotal*carbohydratedaykoeff[0]
carboeating[1]=carbohydratedinner=carbohydratetotal*carbohydratedaykoeff[1]
carboeating[2]=carbohydratesupper=carbohydratetotal*carbohydratedaykoeff[2]

proteineating[0]=proteinlunch=proteintotal*proteindaykoeff[0]
proteineating[1]=proteindinner=proteintotal*proteindaykoeff[1]
proteineating[2]=proteinsupper=proteintotal*proteindaykoeff[2]

caloryeating[0]=calorylunch=(carbohydratelunch+proteinlunch)*4. + fatlunch*9.
caloryeating[1]=calorydinner=(carbohydratedinner+proteindinner)*4. + fatdinner*9.
caloryeating[2]=calorysupper=(carbohydratesupper+proteinsupper)*4. + fatsupper*9.
CPFCstring = format("Распределение суточного \n КБЖУ по приёмам пищи")
print CPFCstring
CPFCstring = format("КБЖУ       Завтрак      Обед      Ужин    Итого")
print u"КБЖУ       Завтрак     Обед     Ужин    Итого"
CPFCstring = 'Жиры гр.    {0:>6.0f} {1:>8.0f} {2:>8.0f} {3:>8.0f}'.format(fatlunch, fatdinner, fatsupper, fattotal)
print CPFCstring
CPFCstring = 'Углеводы гр.{0:>6.0f} {1:>8.0f} {2:>8.0f} {3:>8.0f}'.format(carbohydratelunch, carbohydratedinner, carbohydratesupper, carbohydratetotal)
print CPFCstring
CPFCstring = 'Белки гр.   {0:>6.0f} {1:>8.0f} {2:>8.0f} {3:>8.0f}'.format(proteinlunch, proteindinner, proteinsupper, proteintotal)
print CPFCstring
CPFCstring = 'Калории     {0:>6.0f} {1:>8.0f} {2:>8.0f} {3:>8.0f}'.format(calorylunch, calorydinner, calorysupper, calorytotal)
print CPFCstring

return
