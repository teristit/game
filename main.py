import start_window
import platformer


class Main:
    def __init__(self):
        self.game = 0
        self.run()

    def run(self):
        if self.game == 0:
            self.startwindow()
        elif self.game == 1:
            self.myplatformer()

    def startwindow(self):
        self.game = start_window.run()
        self.run()

    def myplatformer(self):
        self.game = platformer.run()
        self.game = 0
        self.run()


Main()
