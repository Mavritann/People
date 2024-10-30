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
        
        self.start_date = date.today() # текущая стартовая дата
        self.current_date = date.today()  # текущая дата
        self.ids.end_date_input.text = str(date.today()) # вносит текущую дату в поле
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
        # делает поля ввода неактивными пока работает программа
        self.ids.population_input.readonly = True
        self.ids.start_date_input.readonly = True
        self.ids.end_date_input.readonly = True
        self.ids.resourses_input.readonly = True
        
        Human.resourses = int(self.ids.resourses_input.text)
               
        for item in range(int(self.ids.population_input.text)):  # цикл, создающий людей и добавляющий их в список
            new = Human(self.start_date, self.ids.start_date_input.text, self.ids.end_date_input.text)
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
                    new_born = Human(self.current_date, "", "")
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
            self.ids.factors_label.text = f"The numbers of children: {Human.born_k}, death factor: {Human.death_k}"
            self.ids.job_label.text = f"Male mining: {Human.man_job}, female mining: {Human.woman_job}"
            self.ids.spend_label.text = f"Child spending: {Human.child_spend}, adult spending: {Human.adult_spend}"

            Human.incident_death = 0
            Human.res_correction(Human) # корректировка популяции 
                
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
            
            Clock.unschedule(self.update_label)    # окончание цикла   
            # поля ввода опять становятся активными
            self.ids.population_input.readonly = False
            self.ids.start_date_input.readonly = False
            self.ids.end_date_input.readonly = False
            self.ids.resourses_input.readonly = False
     
            self.new_buttons(self.ids.old_button, self.ids.young_button)  
            
    def old(self):    
        sorted_dead = sorted(self.dead, key = lambda human: human.age, reverse = True)  # сортируем умерших по возрасту
        labels_list = [self.ids.alives_label, self.ids.age_label, self.ids.dead_label, 
                       self.ids.death_age_label, self.ids.resourses_label, self.ids.factors_label, 
                       self.ids.job_label, self.ids.spend_label, self.ids.event_label]
        self.ids.date_label.text = "List of the most old humans"

        for dead in sorted_dead[0:9]:
            labels_list[sorted_dead.index(dead)].text = f"{dead.birth_date}, {dead.sex}, {dead.ymd_age()}, {dead.dead_date}"
                    
    def young(self):                
        sorted_dead = sorted(self.dead, key = lambda human: human.age)  # сортируем умерших по возрасту
        labels_list = [self.ids.alives_label, self.ids.age_label, self.ids.dead_label, 
                       self.ids.death_age_label, self.ids.resourses_label, self.ids.factors_label, 
                       self.ids.job_label, self.ids.spend_label, self.ids.event_label]
        self.ids.date_label.text = "List of the most young humans"

        for dead in sorted_dead[0:9]:
            labels_list[sorted_dead.index(dead)].text = f"{dead.birth_date}, {dead.sex}, {dead.ymd_age()}, {dead.dead_date}"
                    
class AwesomeApp(App):
    def build(self):
        Window.clearcolor = (0.33, 0.33, 0.33, 1) # цвет
        return MyLayout()

if __name__ == "__main__":
    AwesomeApp().run()