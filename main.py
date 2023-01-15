import csv

import fish_eat_fish
import kybik
import platformer
import start_window


class Main:
    def __init__(self):
        self.game = 0
        self.run()

    def run(self):
        if self.game == 0:
            self.startwindow()
        elif self.game == 1:
            self.myplatformer()
        elif self.game == 2:
            self.mykybik()
        elif self.game == 3:
            self.myfish_eat_fish()

    def startwindow(self):
        self.game = start_window.run()
        self.run()

    def myplatformer(self):
        level = self.levelselection()
        print(level)
        if level != 4:
            with open('levels/level.csv', encoding="utf8") as csvfile:
                reader = csv.reader(csvfile, delimiter=';', quotechar='"')
                for index, row in enumerate(reader):
                    if index > 10:
                        break
                    if level == index + 1:
                        self.game = platformer.run(row[0])
        self.game = 0
        self.run()

    def mykybik(self):
        self.game = kybik.Menu()
        self.game = 0
        self.run()

    def myfish_eat_fish(self):
        self.game = fish_eat_fish.run()
        self.game = 0
        self.run()

    def levelselection(self):
        level = start_window.run(
            names=['выберите уровень', '    1    ', '    2    ', '    3    ', 'выйти'])
        return level
Main()
