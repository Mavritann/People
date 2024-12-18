import os
import random
from datetime import date, timedelta

from event import Event
from human import Human

start_date = date.today() # сегодняшняя стартовая дата
current_date = date.today()  # текущая дата

population = []  # живые люди
dead = []  # умершие люди
men = 0
women = 0
avr_death_age, avr_death_men_age, avr_death_women_age, max_age = 0, 0, 0, 0
new_event = None
event_chance = [False]
event_days = 0
dead_men = 0
dead_women = 0

for item in range(100):  # цикл, создающий людей и добавляющий их в список
    new = Human(current_date)
    population.append(new)
    item += 1
    if new.sex == "man":
        men += 1
    else:
        women += 1

def one_day():  # функция, которая увеличивает время на 1 день
    global current_date, population, dead, men, women, avr_death_age, avr_death_men_age, avr_death_women_age, max_age, new_event, event_chance, event_days, dead_men, dead_women
    current_date += timedelta(days = 1)
    os.system("cls")  # очистка консоли
    print(current_date)
    
    for pers in population:  # цикл, выводящий информацию о людях
        pers.one_day_later()
        pers.ymd_age()
        
        if pers.alive == ["dead"]: # добавляет в dead спис
            dead.append(pers)
            population.remove(pers)
            if pers.sex == "man":
                men -= 1
                dead_men += 1
            else:
                women -= 1
                dead_women += 1

            if len(dead) > 0: # средний возраст смерти
                avr_death_age = sum([pers.age for pers in dead]) / len(dead) / 365  
                if dead_men > 0:
                    avr_death_men_age = sum([pers.age for pers in dead if pers.sex == "man"]) / dead_men / 365
                if dead_women > 0:
                    avr_death_women_age = sum([pers.age for pers in dead if pers.sex == "woman"]) / dead_women / 365

        if pers.ck == ["yes"]: # рождение нового человека
            new_born = Human(current_date)
            population.append(new_born)
            if new_born.sex == "man":
                men += 1
            else:
                women += 1

    if len(population) > 0:
        avr_age = sum([pers.age for pers in population]) / len(population) / 365 # средний возраст
        max_age = round(max([pers.age for pers in population]) / 365, 2)
        Human.avr_resourses = round (Human.resourses / len(population), 2)  
    else:
        avr_age, max_age, Human.avr_resourses = 0, 0, 0

    print(f"{len(population)} alives: {men} men, {women} women")
    print(f"Average age: {round(avr_age, 2)}")
    print(f"Max current age: {max_age}")
    print(f"Total dead: {len(dead)}, men: {dead_men}, women: {dead_women}")
    print(f"Average death age: {round(avr_death_age, 2)}, men: {round(avr_death_men_age, 2)}, women: {round(avr_death_women_age, 2)}")
    print(f"Total resourses: {round(Human.resourses)}, average: {Human.avr_resourses}")
    print(f"The average number of children: {Human.born_k}, death factor: {Human.death_k}")
    print(f"Male mining: {Human.man_job}, female mining: {Human.woman_job}, child spending: {Human.child_spend}, adult spending: {Human.adult_spend}")

    Human.res_correction(Human) # корректировка популяции 
    Human.incident_death = 0
        
    if event_chance == [False]:
        event_chance = random.choices([True, False], weights = [1, 180]) # вызов случайного события
        if event_chance == [True]:
            new_event = Event()
            new_event.random_event(current_date)
            event_days = 0             
    elif event_chance == [True]:
        event_days += 1
        new_event.type()
        print(f"{new_event.name} Days: {event_days}, {new_event.end_date}")
        if event_days == new_event.time.days:
            event_chance = [False]

while len(population) > 0:  # цикл, считает дни
    one_day()
    #time.sleep(0.01) # задержка в секундах

passed_time = (current_date - start_date).days  # вычисляем пройденное время
print()
print(f"{passed_time} days passed.")
print()

sorted_dead = sorted(dead, key=lambda human: human.age)  # сортируем умерших по возрасту
for deads in sorted_dead[-10:]:  # выводим 10 самых старых умерших
    print(deads.birth_date, deads.sex, deads.ymd_age(), deads.dead_date)

print(f"Average age of death: {round(avr_death_age, 2)}, men: {round(avr_death_men_age, 2)}, women: {round(avr_death_women_age, 2)}")