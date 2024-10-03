import os
from datetime import date, timedelta
from human import Human

start_date = date.today() # сегодняшняя стартовая дата
current_date = date.today()  # текущая дата
print(start_date)

population = []  # живые люди
dead = []  # умершие люди
men = 0
women = 0
children = 0
avr_death_age, avr_death_men_age, avr_death_women_age, max_age = 0, 0, 0, 0

for item in range(100):  # цикл, создающий людей и добавляющий их в список
    new = Human(current_date)
    population.append(new)
    item += 1
    if new.sex == "man":
        men += 1
    else:
        women += 1

def one_day():  # функция, которая увеличивает время на 1 день
    global current_date, population, dead, men, women, avr_death_age, avr_death_men_age, avr_death_women_age, max_age
    current_date += timedelta(days=1)
    os.system("cls")  # очистка консоли
    print(current_date)
    for pers in population:  # цикл, выводящий информацию о людях
        pers.one_day_later()
        pers.ymd_age()
        if pers.alive == ["dead"]:  # добавляет в dead спис
            dead.append(pers)
            population.remove(pers)
            if pers.sex == "man":
                men -= 1
            else:
                women -= 1
        if pers.ck == ["yes"]:
            new_born = Human(current_date)
            population.append(new_born)

            if new_born.sex == "man":
                men += 1
            else:
                women += 1

        if len(population) > 0:
            avr_age = (sum([pers.age for pers in population]) / len(population) / 365)  # средний возраст
        else:
            avr_age = 0
        max_age = round(max([pers.age for pers in population]) / 365, 2)

        dead_men, dead_women = 0, 0
        for pers in dead:
            if pers.sex == "man":
                dead_men += 1
            else:
                dead_women += 1

        if len(dead) > 0:  # средний возраст смерти
            avr_death_age = sum([pers.age for pers in dead]) / len(dead) / 365
        if dead_men > 0:
            avr_death_men_age = (sum([pers.age for pers in dead if pers.sex == "man"]) / dead_men / 365)
        if dead_women > 0:
            avr_death_women_age = (sum([pers.age for pers in dead if pers.sex == "woman"])/ dead_women / 365)

    print(f"{len(population)} alives: {men} men, {women} women")
    print(f"Average age: {round(avr_age, 2)}")
    print(f"Max current age: {max_age}")
    print(f"Total dead: {len(dead)}, men: {dead_men}, women: {dead_women}")
    print(f"Average death age: {round(avr_death_age, 2)}, men: {round(avr_death_men_age, 2)}, women: {round(avr_death_women_age, 2)}")
    print(f"Total resourses: {round(Human.resourses)}, average: {round(Human.resourses / len(population), 2)}")

while len(population) > 0:  # цикл, считает дни
    one_day()
    #time.sleep(0.0001) # задержка в секундах

passed_time = (current_date - start_date).days  # вычисляем пройденное время
print()
print(f"{passed_time} days passed.")
print()

sorted_dead = sorted(dead, key=lambda human: human.age)  # сортируем умерших по возрасту
for deads in sorted_dead[-10:]:  # выводим 10 самых старых умерших
    print(deads.birth_date, deads.sex, deads.ymd_age(), deads.alive[0], deads.dead_date)

print(f"Average age of death: {round(avr_death_age, 3)}, men: {round(avr_death_men_age, 3)}, women: {round(avr_death_women_age, 3)}")