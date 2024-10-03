import random
from datetime import date, timedelta

class Human:
    
    resourses = 0.0

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
        self.born_k = 2.4 # вероятность родить
        self.man_k = 0.00036 # мужской коэффициент смертности
        self.woman_k = 0.00025 # женский коэффициент смертности
        self.age_k = 1.075 # увеличение шанса умереть за год

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
            
    def is_alive(self):
        if self.sex == "man":
            death_factor = (self.man_k*self.age_k**self.years) / 365
        elif self.sex == "woman":
            death_factor = (self.woman_k*self.age_k**self.years) / 365 # вероятность умереть в этот день
        self.alive = random.choices(["alive", "dead"], weights = [1 - death_factor, death_factor])
        self.dead_date = self.birth_date + timedelta(days = self.age)	

    def is_mother(self): # функция рождения детей
        if self.sex == "woman" and self.years >= 15 and self.years < 50:
            self.ck = random.choices(["no", "yes"], weights = [12783, self.born_k]) # вероятность родить    
            if self.ck == ["yes"]:
                self.mother = True
                self.children += 1
               
    def mine_resourses(self):
        if self.sex == "man" and self.years >= 18 and self.years < 65:
            Human.resourses +=6
        if self.sex == "woman" and self.years >= 18 and self.years < 60:
            Human.resourses += 3.6
            
    def spend_resourses(self):
        if self.years < 15:
            Human.resourses -= 2
        else:
            Human.resourses -= 3