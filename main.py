import start_window
import platformer
import kybik
import fish_eat_fish


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
        self.game = platformer.run()
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

Main()
