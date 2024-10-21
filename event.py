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
        self.type = random.choice([self.war,  self.pandemia, self.frost, self.harvest, self.baby_boom, self.new_source, self.fire, self.medical_achieve]) # вызов случайной функции
        self.type()
        # отрицательные факторы
    def war(self):
        self.name = "WAR!"
        self.time = timedelta(days = random.randint(0, 3650))
        self.end_date = self.start_date + self.time        
        
    def pandemia(self):
        self.name = "PANDEMIA!"
        self.time = timedelta(days = random.randint(0, 1825))
        self.end_date = self.start_date + self.time
        
    def frost(self):
        self.name = "FROST!"
        self.time = timedelta(days = random.randint(0, 1050))
        self.end_date = self.start_date + self.time
        
    def fire(self):
        self.name = "FIRE!"
        self.time = timedelta(days = random.randint(0, 180))
        self.end_date = self.start_date + self.time
        # положительные факторы    
    def harvest(self):
        self.name = "HARVEST!"
        self.time = timedelta(days = random.randint(0, 1825))
        self.end_date = self.start_date + self.time
        
    def baby_boom(self):
        self.name = "BABY BOOM!"
        self.time = timedelta(days = random.randint(0, 7300))
        self.end_date = self.start_date + self.time
        
    def new_source(self):
        self.name = "NEW SOURCE!"
        self.time = timedelta(days = random.randint(0, 3650))
        self.end_date = self.start_date + self.time
        
    def medical_achieve(self):
        self.name = "MEDICAL ACHIEVEMENT!"
        self.time = timedelta(days = random.randint(0, 180))
        self.end_date = self.start_date + self.time