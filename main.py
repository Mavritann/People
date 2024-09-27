import datetime
import os
import time

from human import Human

start_date = datetime.date.today() # сегодняшняя стартовая дата
current_date = datetime.date.today() # текущая дата
print(start_date)

population = [] # живые люди
dead = [] # умершие люди
men = 0
women = 0

for item in range(1000): # цикл, создающий людей и добавляющий их в список
    new = Human()
    population.append(new)
    item += 1
    if new.sex == "man":
        men += 1
    else:
        women += 1

def one_day(): # функция, которая увеличивает время на 1 день
    global current_date, population, dead, men, women
    current_date += datetime.timedelta(days = 1)
    os.system('cls||clear') # очистка консоли
    print(current_date) 
    for pers in population: # цикл, выводящий информацию о людях
        pers.one_day_later()
        pers.ymd_age()
        if pers.alive == ["dead"]:
            dead.append(pers)
            population.remove(pers)
            if pers.sex == "man":
                men -= 1
            else:
                women -= 1
        #print(pers.birth_date.date(), pers.sex, pers.ymd_age(), pers.alive[0])
    print(f"{len(population)} alives: {men} men, {women} women")
       
while len(population) > 0: # цикл, считает дни
    one_day()
    time.sleep(0.00001) # задержка в секундах

passed_time = (current_date - start_date).days # вычисляем пройденное время
print()
print(f"{passed_time} days passed.")
print()

sorted_dead = sorted(dead, key=lambda human: human.age) # сортируем умерших по возрасту
for pers in sorted_dead[-10:]: # выводим 10 самых старых умерших
    print(pers.birth_date.date(), pers.sex, pers.ymd_age(), pers.alive[0], pers.dead_date.date())
    
average_age = sum([pers.age / 365 for pers in sorted_dead]) / len(sorted_dead)
        
average_men_age = sum([pers.age / 365 for pers in sorted_dead if pers.sex == "man"]) / len([pers for pers in sorted_dead if pers.sex == "man"])
average_women_age = sum([pers.age / 365 for pers in sorted_dead if pers.sex == "woman"]) / len([pers for pers in sorted_dead if pers.sex == "woman"])

print(f"Average age of death: {round(average_age, 3)}, men: {round(average_men_age, 3)}, women: {round(average_women_age, 3)}")