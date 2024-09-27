import random
from datetime import datetime, timedelta


class Human:
    def __init__(self): 
        start = datetime(1950, 1, 1)
        end = datetime.today()
        self.birth_date = start + timedelta(days = random.randint(0, (end-start).days))
        self.sex = random.choice(["man", "woman"])
        self.age = (datetime.today() - self.birth_date).days
        self.years = self.age // 365
        self.dead_date = None
        self.alive = "alive"

    def ymd_age(self): # функция, которая возвращает возраст в формате Y-M-D
        self.years = int(self.age // 365.25)
        self.months = int((self.age % 365.25) // 30.4166)
        self.days = int((self.age % 365.25) % 30.4166)
        self.str_age = (str(self.years) + " years " + str(self.months) + " months " + str(self.days) + " days")
        return self.str_age

    def one_day_later(self):
        self.age += 1
        self.is_alive()

    def is_alive(self): # функция, которая проверяет, жив ли человек
        if self.sex == "man":
            self.dk = (0.00035*1.075**self.years) / 365
        elif self.sex == "woman":
            self.dk = (0.00025*1.075**self.years) / 365
        self.alive = random.choices(["alive", "dead"], weights = [1 - self.dk, self.dk])
        self.dead_date = self.birth_date + timedelta(days = self.age)