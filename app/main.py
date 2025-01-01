import random
from enum import Enum

import pyxel


class Direction(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


class App:
    def __init__(self):
        pyxel.init(128, 128, title="玉入れられ")
        pyxel.load("assets/assets.pyxres")

        # キャラクターの初期設定
        self.x = pyxel.width // 2  # 画面中央のX座標
        self.y = pyxel.height // 2  # 画面中央のY座標
        self.direction = Direction.DOWN  # 初期の向き
        self.score = 0  # スコアの初期値

        self.dot_count = 0
        self.dot_speed = 0
        self.dot_interval = 30
        self.dots_until_speed_change = random.randint(2, 4)

        # 点のデータを格納するリスト
        self.dots = []
        pyxel.run(self.update, self.draw)

    def update(self):
        # 十字キーでキャラクターの向きを変更
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.direction = Direction.RIGHT
        elif pyxel.btn(pyxel.KEY_LEFT):
            self.direction = Direction.LEFT
        elif pyxel.btn(pyxel.KEY_UP):
            self.direction = Direction.UP
        elif pyxel.btn(pyxel.KEY_DOWN):
            self.direction = Direction.DOWN

        # 一定時間ごとに点を生成
        if pyxel.frame_count % self.dot_interval == 0:
            self.dot_count += 1
            self.spawn_dot()
            if self.dot_count >= self.dots_until_speed_change:
                self.dot_count = 0
                self.dot_speed = random.choice(range(-30, 31, 10))
                self.dot_interval = max(10, self.dot_interval - 1)
                self.dots_until_speed_change = random.randint(3, 5)

        # 点の位置を更新
        for dot in self.dots:
            dot["x"] += dot["dx"]
            dot["y"] += dot["dy"]

        # 中央に到達した点を削除し、スコア加算を行う
        for dot in self.dots[:]:
            if abs(dot["x"] - pyxel.width // 2) < 2 and abs(dot["y"] - pyxel.height // 2) < 2:
                # 弾の方向と自分の向きが一致していたらスコア+1
                if self.direction == dot["direction"]:
                    self.score += 1
                    pyxel.play(0, 0)
                self.dots.remove(dot)

    def draw(self):
        # 背景を描画
        pyxel.cls(0)

        # タイルを描画
        pyxel.bltm(0, 0, 0, 0, 0, 128, 128)

        # 向きに応じたキャラクターのドットパターンを描画
        if self.direction == Direction.UP:
            pyxel.blt(self.x - 8, self.y - 8, 0, 0, 0, 16, 16, 6)
        elif self.direction == Direction.DOWN:
            pyxel.blt(self.x - 8, self.y - 8, 0, 16, 0, 16, 16, 6)
        elif self.direction == Direction.LEFT:
            pyxel.blt(self.x - 8, self.y - 8, 0, 32, 0, 16, 16, 6)
        elif self.direction == Direction.RIGHT:
            pyxel.blt(self.x - 8, self.y - 8, 0, 48, 0, 16, 16, 6)

        # 飛んでくるドーナツを描画
        for dot in self.dots:
            pyxel.blt(int(dot["x"] - 5), int(dot["y"] - 5), 0, 0, 16, 10, 10, 6)

        # スコアを右上に表示
        pyxel.text(10, 10, f"Score: {self.score}", pyxel.COLOR_BLACK)

    def spawn_dot(self):
        side = random.choice([Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT])

        if side == Direction.UP:
            x = pyxel.width // 2
            y = 0
            dx = 0
            dy = (pyxel.height // 2 - y) / (60 - self.dot_speed)
            direction = Direction.UP
        elif side == Direction.DOWN:
            x = pyxel.width // 2
            y = pyxel.height
            dx = 0
            dy = (pyxel.height // 2 - y) / (60 - self.dot_speed)
            direction = Direction.DOWN
        elif side == Direction.LEFT:
            x = 0
            y = pyxel.height // 2
            dx = (pyxel.width // 2 - x) / (60 - self.dot_speed)
            dy = 0
            direction = Direction.LEFT
        elif side == Direction.RIGHT:
            x = pyxel.width
            y = pyxel.height // 2
            dx = (pyxel.width // 2 - x) / (60 - self.dot_speed)
            dy = 0
            direction = Direction.RIGHT

        self.dots.append({"x": x, "y": y, "dx": dx, "dy": dy, "direction": direction})


App()
