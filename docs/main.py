import math
import os

import pyxel

# この行を追加して、ファイルの存在を確認します
os.path.isfile("./main.py")


class App:
    def __init__(self):
        pyxel.init(160, 120, title="円運動")
        self.angle = 0
        self.center_x = 80
        self.center_y = 60
        self.radius = 40
        pyxel.run(self.update, self.draw)

    def update(self):
        self.angle += 0.05
        if self.angle > 2 * math.pi:
            self.angle -= 2 * math.pi

    def draw(self):
        pyxel.cls(0)
        x = self.center_x + self.radius * math.cos(self.angle)
        y = self.center_y + self.radius * math.sin(self.angle)
        pyxel.pset(x, y, 11)


App()
