import random
from datetime import timedelta
from human import Human

class Event:
    
    def __init__(self):
        self.start_date = 0
        self.end_date = 0
        self.time = 0
        self.type = None
        self.name = ""
        
    def random_event(self, current_date):
        self.start_date = current_date
        self.type = random.choice([self.war,  self.pandemia, self.hunger, self.disaster, self.new_source, self.med_achieve, self.harvest, self.tech_achieve]) # вызов случайной функции
        if self.type == self.war or self.type == self.new_source:
            self.time = timedelta(days = random.randint(0, 1460))
        elif self.type == self.pandemia or self.type == self.med_achieve:
            self.time = timedelta(days = random.randint(0, 1095))
        elif self.type == self.hunger or self.type == self.harvest:
            self.time = timedelta(days = random.randint(0, 365))
        elif self.type == self.disaster or self.type ==self.tech_achieve:
            self.time = timedelta(days = random.randint(0, 180))
        self.end_date = self.start_date + self.time
            
        self.type()
        # отрицательные факторы
    def war(self):
        self.name = "WAR!"     
        Human.man_job = round(Human.man_job / 2, 2)
        Human.woman_job = round(Human.woman_job * 1.6, 2)
        Human.incident_death = 0.0001
        Human.resourses *= 0.9995
        
    def pandemia(self):
        self.name = "PANDEMIA!"
        Human.death_k = 1.1
        Human.born_k = round(Human.born_k / 1.5, 3)
        Human.man_job = round(Human.man_job * 0.9, 2)
        Human.woman_job = round(Human.woman_job * 0.9, 2)
        
    def hunger(self):
        self.name = "HUNGER!"
        Human.incident_death = 0.00005
        Human.resourses *= 0.998
        Human.man_job = round(Human.man_job * 0.8, 2)
        Human.woman_job = round(Human.woman_job * 0.8, 2)
        
    def disaster(self):
        self.name = "DISASTER"
        Human.incident_death = 0.0002
        Human.resourses *= 0.996
        Human.man_job = round(Human.man_job * 0.9, 2)
        Human.woman_job = round(Human.woman_job * 0.9, 2)
            
          # положительные факторы              
    def new_source(self):
        self.name = "NEW SOURCE!"
        if Human.resourses < 0:
            Human.resourses += random.randint(10000, 100000) 
        Human.resourses *= 1.001
        Human.born_k = round(Human.born_k * 1.2, 3)
        Human.man_job = round(Human.man_job * 1.3, 2)
        Human.woman_job = round(Human.woman_job * 1.2, 2)
        
    def med_achieve(self):
        self.name = "MEDICAL ACHIEVEMENT!"
        Human.death_k = round(Human.death_k * 0.95, 4)
        Human.born_k = round(Human.born_k * 1.3, 3)
        Human.man_job = round(Human.man_job * 1.1, 2)
        Human.woman_job = round(Human.woman_job * 1.1, 2)
            
    def harvest(self):
        self.name = "HARVEST!"
        Human.resourses *= 1.003
        Human.death_k = round(Human.death_k * 0.99, 4)
        Human.man_job = round(Human.man_job * 1.2, 2)
        Human.woman_job = round(Human.woman_job * 1.2, 2)
        
    def tech_achieve(self):
        self.name = "TECHNICAL ACHIEVEMENT!"
        Human.born_k = round(Human.born_k * 1.2, 3)
        Human.resourses *= 1.005
        Human.man_job = round(Human.man_job * 1.1, 2)
        Human.woman_job = round(Human.woman_job * 1.1, 2)