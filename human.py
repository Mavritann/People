import random
from datetime import date, timedelta

class Human:
    
    resourses = 200000
    avr_resourses = 0
    born_k = 2.4 # вероятность родить
    man_k = 0.00036 # мужской коэффициент смертности
    woman_k = 0.00025 # женский коэффициент смертности
    death_k = 1.075 # увеличение шанса умереть за год
    man_job = 6 # добыча ресурсов мужичной за 1 день
    woman_job = 3.5 # добыча ресурсов женщиной за 1 день

    def __init__(self, current_date): 
        start = date(1950, 1, 1)
        end = current_date
        if current_date == date.today():
            self.birth_date = start + timedelta(days = random.randint(0, (end - start).days)) 
        else:
            self.birth_date = current_date

        self.sex = random.choice(["man", "woman"])
        self.age = (current_date - self.birth_date).days
        self.years = self.age // 365
        self.dead_date = None
        self.alive = "alive"
        self.mother = False
        self.children = 0
        self.ck = ["no"]

    def ymd_age(self): # функция, которая возвращает возраст в формате Y-M-D
        self.years = int(self.age // 365.25)
        months = int((self.age % 365.25) // 30.4166)
        days = int((self.age % 365.25) % 30.4166)
        str_age = (str(self.years) + " years " + str(months) + " months " + str(days) + " days")
        return str_age
    
    def one_day_later(self):
        self.age += 1 # прибавляет один день
        self.is_alive()
        if self.alive == ["alive"]:
            self.is_mother()
            self.mine_resourses()
            self.spend_resourses()
            self.res_correction()
            
    def is_alive(self): # функция жизни, проверяет жив ли человек
        if self.sex == "man":
            death_factor = (self.man_k*self.death_k**self.years) / 365
        elif self.sex == "woman":
            death_factor = (self.woman_k*self.death_k**self.years) / 365 # вероятность умереть в этот день
        self.alive = random.choices(["alive", "dead"], weights = [0.97, death_factor])
        self.dead_date = self.birth_date + timedelta(days = self.age)	

    def is_mother(self): # функция рождения детей
        if self.sex == "woman" and self.years >= 15 and self.years < 50:
            self.ck = random.choices(["no", "yes"], weights = [12783, self.born_k]) # вероятность родить    
            if self.ck == ["yes"]:
                self.mother = True
                self.children += 1
               
    def mine_resourses(self): # функция зарабатывания ресурсов
        if self.sex == "man" and self.years >= 18 and self.years < 65:
            Human.resourses += Human.man_job
        if self.sex == "woman" and self.years >= 18 and self.years < 60:
            Human.resourses += Human.woman_job
            
    def spend_resourses(self): # функция траты ресурсов
        if self.years < 15:
            Human.resourses -= 2
        else:
            Human.resourses -= 3

    def res_correction(self):
        Human.born_k = round(Human.avr_resourses * 0.0012, 3)
        if Human.born_k > 7:
            Human.born_k = 7
        if Human.resourses < 0:
            Human.born_k = 0
        
        if Human.avr_resourses >= 2000:
            Human.death_k = round(40 / Human.avr_resourses + 1.055, 4)
        elif Human.avr_resourses >= 0:
            Human.death_k = round(-0.000011 * Human.avr_resourses + 1.097, 4)
        else:
            Human.death_k = 1.12