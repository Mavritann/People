import random
from datetime import date, timedelta
from event import Event
from human import Human

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.clock import Clock

Window.size = (650, 900)

Builder.load_file("main_gui.kv")

class MyLayout(Widget):
                 
    def __init__(self):
        super().__init__()
        
        self.start_date = date.today() # сегодняшняя стартовая дата
        self.current_date = date.today()  # текущая дата
        self.population = []  # живые люди
        self.dead = []  # умершие люди
        self.men = 0
        self.women = 0
        self.avr_death_age, self.avr_death_men_age, self.avr_death_women_age, self.max_age = 0, 0, 0, 0
        self.avr_age = 0
        self.new_event = None
        self.event_chance = [False]
        self.event_days = 0
        self.dead_men = 0
        self.dead_women = 0
        
    def start(self):
               
        for item in range(int(self.ids.population_input.text)):  # цикл, создающий людей и добавляющий их в список
            new = Human(self.current_date)
            self.population.append(new)
            item += 1
            if new.sex == "man":
                self.men += 1
            else:
                self.women += 1
                
        Clock.schedule_interval(self.update_label, 0.01) # запуск метода с определённой частотой
        
    def new_buttons(self, old, young):
        anim = Animation(background_color = (0.25, 0.25, 0.25, 1), duration = 5)
        anim &= Animation(color = (1, 1, 1, 1))
        anim.start(old)
        anim.start(young)
     
    def update_label(self, *interval):
        
        if len(self.population) > 0:
            self.ids.date_label.text = str(self.current_date) # вывод текущей даты
            self.current_date += timedelta(days = 1)
            
            for pers in self.population:  # цикл, выводящий информацию о людях
                pers.one_day_later()
                pers.ymd_age()
            
                if pers.alive == ["dead"]: # добавляет в dead спис
                    self.dead.append(pers)
                    self.population.remove(pers)
                    if pers.sex == "man":
                        self.men -= 1
                        self.dead_men += 1
                    else:
                        self.women -= 1
                        self.dead_women += 1

                    if len(self.dead) > 0: # средний возраст смерти
                        self.avr_death_age = sum([pers.age for pers in self.dead]) / len(self.dead) / 365  
                        if self.dead_men > 0:
                            self.avr_death_men_age = sum([pers.age for pers in self.dead if pers.sex == "man"]) / self.dead_men / 365
                        if self.dead_women > 0:
                            self.avr_death_women_age = sum([pers.age for pers in self.dead if pers.sex == "woman"]) / self.dead_women / 365

                if pers.ck == ["yes"]: # рождение нового человека
                    new_born = Human(self.current_date)
                    self.population.append(new_born)
                    if new_born.sex == "man":
                        self.men += 1
                    else:
                        self.women += 1

            if len(self.population) > 0:
                self.avr_age = sum([pers.age for pers in self.population]) / len(self.population) / 365 # средний возраст
                self.max_age = round(max([pers.age for pers in self.population]) / 365, 2)
                Human.avr_resourses = round (Human.resourses / len(self.population), 2)  
            else:
                self.avr_age, self.max_age, Human.avr_resourses = 0, 0, 0
                
            self.ids.alives_label.text = f"{len(self.population)} alives: {self.men} men, {self.women} women"
            self.ids.age_label.text = f"Average age: {round(self.avr_age, 2)}, max current age: {self.max_age}"
            self.ids.dead_label.text = f"Total dead: {len(self.dead)}, men: {self.dead_men}, women: {self.dead_women}"
            self.ids.death_age_label.text = f"Average death age: {round(self.avr_death_age, 2)}, men: {round(self.avr_death_men_age, 2)}, women: {round(self.avr_death_women_age, 2)}"
            self.ids.resourses_label.text = f"Total resourses: {round(Human.resourses)}, average: {Human.avr_resourses}"
            self.ids.factors_label.text = f"The average number of children: {Human.born_k}, death factor: {Human.death_k}"
            self.ids.job_label.text = f"Mining: male - {Human.man_job}, female - {Human.woman_job}, spending: child - {Human.child_spend}, adult - {Human.adult_spend}"
        
            Human.res_correction(Human) # корректировка популяции 
            Human.incident_death = 0
                
            if self.event_chance == [False]: 
                self.event_chance = random.choices([True, False], weights = [1, 180]) # вызов случайного события
                if self.event_chance == [True]:
                    self.new_event = Event()
                    self.new_event.random_event(self.current_date)
                    self.event_days = 0             
            elif self.event_chance == [True]:
                self.event_days += 1
                self.new_event.type()
                self.ids.event_label.text = f"{self.new_event.name} Days: {self.event_days}"
                if self.event_days == self.new_event.time.days:
                    self.event_chance = [False]  
                    self.ids.event_label.text = ""                
            
        else: # если все умерли
            passed_time = (self.current_date - self.start_date).days  # вычисляем пройденное время
            self.ids.date_label.text = f"{str(self.current_date)}, {passed_time} days passed."
            
            Clock.unschedule(self.update_label)            
            self.new_buttons(self.ids.old_button, self.ids.young_button)  
            
    def old(self):                
        sorted_dead = sorted(self.dead, key = lambda human: human.age)  # сортируем умерших по возрасту
        self.ids.date_label.text = "List of the most old humans"       
        self.ids.alives_label.text = f"{sorted_dead[-1].birth_date}, {sorted_dead[-1].sex}, {sorted_dead[-1].ymd_age()}, {sorted_dead[-1].dead_date}"
        self.ids.age_label.text = f"{sorted_dead[-2].birth_date}, {sorted_dead[-2].sex}, {sorted_dead[-2].ymd_age()}, {sorted_dead[-2].dead_date}"
        self.ids.dead_label.text = f"{sorted_dead[-3].birth_date}, {sorted_dead[-3].sex}, {sorted_dead[-3].ymd_age()}, {sorted_dead[-3].dead_date}"
        self.ids.death_age_label.text = f"{sorted_dead[-4].birth_date}, {sorted_dead[-4].sex}, {sorted_dead[-4].ymd_age()}, {sorted_dead[-4].dead_date}"
        self.ids.resourses_label.text = f"{sorted_dead[-5].birth_date}, {sorted_dead[-5].sex}, {sorted_dead[-5].ymd_age()}, {sorted_dead[-5].dead_date}"
        self.ids.factors_label.text = f"{sorted_dead[-6].birth_date}, {sorted_dead[-6].sex}, {sorted_dead[-6].ymd_age()}, {sorted_dead[-6].dead_date}"
        self.ids.job_label.text = f"{sorted_dead[-7].birth_date}, {sorted_dead[-7].sex}, {sorted_dead[-7].ymd_age()}, {sorted_dead[-7].dead_date}"
        self.ids.event_label.text = f"{sorted_dead[-8].birth_date}, {sorted_dead[-8].sex}, {sorted_dead[-8].ymd_age()}, {sorted_dead[-8].dead_date}"
        
    def young(self):                
        sorted_dead = sorted(self.dead, key = lambda human: human.age)  # сортируем умерших по возрасту
        # labels_list = [self.ids.alives_label.text, self.ids.age_label.text, 
        #                self.ids.death_age_label.text, self.ids.death_age_label.text, self.ids.resourses_label.text,
        #                self.ids.factors_label.text, self.ids.job_label.text, self.ids.event_label.text]
        self.ids.date_label.text = "List of the most young humans"

        # for dead in sorted_dead[0:7]:
        #     labels_list[sorted_dead.index(dead)] = f"{dead.birth_date}, {dead.sex}, {dead.ymd_age()}, {dead.dead_date}"
        #     print(labels_list[sorted_dead.index(dead)])
                    
        self.ids.alives_label.text = f"{sorted_dead[0].birth_date}, {sorted_dead[0].sex}, {sorted_dead[0].ymd_age()}, {sorted_dead[0].dead_date}"
        self.ids.age_label.text = f"{sorted_dead[1].birth_date}, {sorted_dead[1].sex}, {sorted_dead[1].ymd_age()}, {sorted_dead[1].dead_date}"
        self.ids.dead_label.text = f"{sorted_dead[2].birth_date}, {sorted_dead[2].sex}, {sorted_dead[2].ymd_age()}, {sorted_dead[2].dead_date}"
        self.ids.death_age_label.text = f"{sorted_dead[3].birth_date}, {sorted_dead[3].sex}, {sorted_dead[3].ymd_age()}, {sorted_dead[3].dead_date}"
        self.ids.resourses_label.text = f"{sorted_dead[4].birth_date}, {sorted_dead[4].sex}, {sorted_dead[4].ymd_age()}, {sorted_dead[4].dead_date}"
        self.ids.factors_label.text = f"{sorted_dead[5].birth_date}, {sorted_dead[5].sex}, {sorted_dead[5].ymd_age()}, {sorted_dead[5].dead_date}"
        self.ids.job_label.text = f"{sorted_dead[6].birth_date}, {sorted_dead[6].sex}, {sorted_dead[6].ymd_age()}, {sorted_dead[6].dead_date}"
        self.ids.event_label.text = f"{sorted_dead[7].birth_date}, {sorted_dead[7].sex}, {sorted_dead[7].ymd_age()}, {sorted_dead[7].dead_date}"

class AwesomeApp(App):
    def build(self):
        Window.clearcolor = (0.33, 0.33, 0.33, 1) # цвет
        return MyLayout()

if __name__ == "__main__":
    AwesomeApp().run()
