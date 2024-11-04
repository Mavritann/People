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
    child_spend = 2 # трата ресурсов ребенком за 1 день
    adult_spend = 3 # трата ресурсов взрослым за 1 день
    incident_death = 0 # вероятность смерти от внешнего воздействия

    def __init__(self, current_date, start, end):  
        
        if current_date <= date.today():
            self.birth_date = start + timedelta(days = random.randint(0, (end - start).days)) 
        else:
            self.birth_date = current_date

        self.sex = random.choice(["man", "woman"])
        self.age = (current_date - self.birth_date).days
        self.years = self.age // 365
        self.dead_date = None
        self.alive = "alive"
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
            
    def is_alive(self): # функция жизни, проверяет жив ли человек
        if self.sex == "man":
            self.death_factor = (self.man_k*self.death_k**self.years) / 365
        elif self.sex == "woman":
            self.death_factor = (self.woman_k*self.death_k**self.years) / 365 # вероятность умереть в этот день
        natural = random.choices(["alive", "dead"], weights = [0.97, self.death_factor])
        incident = random.choices(["alive", "dead"], weights = [1, Human.incident_death])
        if natural == ["alive"] and incident == ["alive"]:
            self.alive = ["alive"]
        else:
            self.alive = ["dead"]
        self.dead_date = self.birth_date + timedelta(days = self.age)	

    def is_mother(self): # функция рождения детей
        if self.sex == "woman" and self.years >= 15 and self.years < 50:
            self.ck = random.choices(["no", "yes"], weights = [12783, self.born_k]) # вероятность родить    
               
    def mine_resourses(self): # функция зарабатывания ресурсов
        if self.sex == "man" and self.years >= 18 and self.years < 65:
            Human.resourses += Human.man_job
        if self.sex == "woman" and self.years >= 18 and self.years < 60:
            Human.resourses += Human.woman_job
            
    def spend_resourses(self): # функция траты ресурсов
        if self.years < 15:
            Human.resourses -= Human.child_spend
        else:
            Human.resourses -= Human.adult_spend

    def res_correction(self): # функция коррекции в зависимости от ресурсов
        Human.born_k = round(Human.avr_resourses * 0.0012, 3)
        if Human.born_k > 7:
            Human.born_k = 7
            
        if Human.avr_resourses <= 0:
            Human.born_k, Human.man_job, Human.woman_job = 0, 0, 0
        elif Human.avr_resourses >= 10000:
            Human.man_job, Human.woman_job = 30, 18
        else:       
            Human.man_job = round(Human.avr_resourses * 0.003, 2)
            Human.woman_job = round(Human.avr_resourses * 0.00175, 2)
           
        if Human.avr_resourses <= 500:
            Human.child_spend, Human.adult_spend = 0.5, 0.75
        elif Human.avr_resourses >= 15000:
            Human.child_spend, Human.adult_spend = 15, 23
        else:
            Human.child_spend = round(Human.avr_resourses * 0.001, 2)
            Human.adult_spend = round(Human.avr_resourses * 0.0015, 2)
  
        if Human.avr_resourses >= 2000:
            Human.death_k = round(40 / Human.avr_resourses + 1.055, 4)
        elif Human.avr_resourses >= 0:
            Human.death_k = round(-0.000011 * Human.avr_resourses + 1.097, 4)
        else:
            Human.incident_death = 0.008