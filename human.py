import random
from datetime import date, datetime, timedelta

class Human:
    
    birth_age = [] # массив возрастов, в которые рожали

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
        self.months = int((self.age % 365.25) // 30.4166)
        self.days = int((self.age % 365.25) % 30.4166)
        self.str_age = (str(self.years) + " years " + str(self.months) + " months " + str(self.days) + " days")
        return self.str_age
    
    def one_day_later(self):
        self.age += 1 # прибавляет один день
        self.is_alive()
        if self.alive == ["alive"]:
            self.is_mother()
            
    def is_alive(self):
        if self.sex == "man":
            self.dk = (0.00036*1.075**self.years) / 365
        elif self.sex == "woman":
            self.dk = (0.00025*1.075**self.years) / 365 # вероятность умереть в этот день
        self.alive = random.choices(["alive", "dead"], weights = [1 - self.dk, self.dk])
        self.dead_date = self.birth_date + timedelta(days = self.age)	

    def is_mother(self): # функция рождения детей
        if self.sex == "woman" and self.years >= 15 and self.years < 50:
            self.ck = random.choices(["no", "yes"], weights = [12783, 2.4]) # вероятность родить    
            if self.ck == ["yes"]:
                self.mother = True
                self.children += 1
                global birth_age # можно убрать
                self.birth_age.append(self.years)