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
        self.time = timedelta(days = random.randint(0, 730))
        self.end_date = self.start_date + self.time        
        self.type = random.choice([self.war,  self.pandemia])#, self.frost, self.harvest, self.baby_boom, self.new_source, self.fire, self.medical_achieve]) # вызов случайной функции
        self.type()
    # отрицательные факторы
    def war(self):
        self.name = "WAR!"
        Human.incident_death = 0.1
        
    def pandemia(self):
        self.name = "PANDEMIA!"
        
    def frost(self):
        self.name = "FROST!"
        
    def fire(self):
        self.name = "FIRE!"
    # положительные факторы    
    def harvest(self):
        self.name = "HARVEST!"
        
    def baby_boom(self):
        self.name = "BABY BOOM!"
        
    def new_source(self):
        self.name = "NEW SOURCE!"
        
    def medical_achieve(self):
        self.name = "MEDICAL ACHIEVEMENT!"
