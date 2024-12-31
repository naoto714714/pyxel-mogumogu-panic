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
        pyxel.init(120, 120, title="玉入れられ")
        pyxel.load("assets/assets.pyxres")

        # キャラクターの初期設定
        self.x = pyxel.width // 2  # 画面中央のX座標
        self.y = pyxel.height // 2  # 画面中央のY座標
        self.direction = Direction.DOWN  # 初期の向き
        self.score = 0  # スコアの初期値

        self.dot_count = 0
        self.dot_speed = 0
        self.dots_until_speed_change = random.randint(2, 4)

        # 各向きに対応するキャラクターのパターン
        self.directions = {
            Direction.UP: [
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [0, 1, 0, 1, 0],
                [0, 1, 0, 1, 0],
                [0, 0, 1, 0, 0],
            ],
            Direction.RIGHT: [
                [0, 0, 0, 1, 1],
                [0, 1, 1, 0, 0],
                [1, 0, 0, 0, 0],
                [0, 1, 1, 0, 0],
                [0, 0, 0, 1, 1],
            ],
            Direction.DOWN: [
                [0, 0, 1, 0, 0],
                [0, 1, 0, 1, 0],
                [0, 1, 0, 1, 0],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
            ],
            Direction.LEFT: [
                [1, 1, 0, 0, 0],
                [0, 0, 1, 1, 0],
                [0, 0, 0, 0, 1],
                [0, 0, 1, 1, 0],
                [1, 1, 0, 0, 0],
            ],
        }

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
        if pyxel.frame_count % 30 == 0:  # 30フレームごと
            self.dot_count += 1
            self.spawn_dot()
            print(f"{self.dot_count} : {self.dots_until_speed_change}")
            if self.dot_count >= self.dots_until_speed_change:
                self.dot_count = 0
                self.dot_speed = random.choice(range(-30, 31, 10))
                self.dots_until_speed_change = random.randint(2, 4)
                print("*" * 10)

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
        pyxel.cls(7)  # 背景を白に設定

        # 向きに応じたキャラクターのドットパターンを描画
        pattern = self.directions[self.direction]
        for i, row in enumerate(pattern):
            for j, col in enumerate(row):
                if col == 1:
                    pyxel.pset(self.x + j - 2, self.y + i - 2, pyxel.COLOR_BLACK)

        # 点を描画
        for dot in self.dots:
            pyxel.pset(int(dot["x"]), int(dot["y"]), 9)  # 点の色を指定して描画

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
