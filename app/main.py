import random
from enum import Enum

import pyxel


class Direction(Enum):
    """キャラクターとドーナツの方向を表す列挙型"""

    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


class App:
    """ゲームアプリケーションのメインクラス"""

    def __init__(self):
        """ゲームの初期化を行う"""
        pyxel.init(128, 128, title="ガマグチくんのもぐもぐパニック")
        pyxel.load("assets/assets.pyxres")
        self.reset_game()

    def reset_game(self):
        """ゲームの状態をリセットする"""
        # サウンドの設定
        pyxel.sound(5).set_volumes("4")
        pyxel.sound(6).set_volumes("4")
        pyxel.sound(7).set_volumes("4")
        pyxel.playm(0, loop=True)

        self.game_over = False

        # キャラクターの初期設定
        self.x = pyxel.width // 2  # 画面中央のX座標
        self.y = pyxel.height // 2  # 画面中央のY座標
        self.direction = Direction.LEFT  # 初期の向き
        self.score = 0  # スコアの初期値
        self.life = 3  # ライフの初期値

        # ドーナツ生成に関する変数
        self.spawned_donuts = 0
        self.donut_speed = 0
        self.donut_interval = 30
        self.donuts_for_difficulty_increase = random.randint(2, 4)

        # ドーナツのデータを格納するリスト
        self.donuts = []

    def update(self):
        """ゲームの状態を更新する"""
        if self.game_over:
            if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
                self.reset_game()
            return

        self.update_direction()
        self.spawn_and_update_donuts()
        self.handle_donut_collisions()

    def update_direction(self):
        """キャラクターの向きを更新する"""
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            self.direction = Direction.RIGHT
        elif pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            self.direction = Direction.LEFT
        elif pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
            self.direction = Direction.UP
        elif pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
            self.direction = Direction.DOWN

    def spawn_and_update_donuts(self):
        """ドーナツの生成と更新を行う"""
        if pyxel.frame_count % self.donut_interval == 0:
            self.spawned_donuts += 1
            self.spawn_donut()
            self.update_difficulty()

        # ドーナツの位置を更新
        for donut in self.donuts:
            donut["x"] += donut["dx"]
            donut["y"] += donut["dy"]

    def update_difficulty(self):
        """ゲームの難易度を更新する"""
        if self.spawned_donuts >= self.donuts_for_difficulty_increase:
            self.spawned_donuts = 0
            self.donut_speed = random.choice(range(-30, 31, 10))
            self.donut_interval = max(10, self.donut_interval - 1)
            self.donuts_for_difficulty_increase = random.randint(3, 5)

    def handle_donut_collisions(self):
        """ドーナツとの衝突を処理する"""
        for donut in self.donuts[:]:
            if abs(donut["x"] - pyxel.width // 2) < 2 and abs(donut["y"] - pyxel.height // 2) < 2:
                self.handle_donut_collision(donut)

    def handle_donut_collision(self, donut):
        """個々のドーナツとの衝突を処理する"""
        if self.direction == donut["direction"]:
            self.score += 1
            pyxel.play(1, 0)
        else:
            self.life -= 1
            pyxel.play(2, 1)
            if self.life <= 0:
                self.game_over = True
                pyxel.play(2, 2)
                pyxel.stop(0)
        self.donuts.remove(donut)

    def draw(self):
        """ゲーム画面を描画する"""
        pyxel.cls(0)
        pyxel.bltm(0, 0, 0, 0, 0, 128, 128)

        if not self.game_over:
            self.draw_character()
            self.draw_donuts()

        self.draw_ui()

        if self.game_over:
            self.draw_game_over()

    def draw_character(self):
        """キャラクターを描画する"""
        sprite_x = {Direction.UP: 0, Direction.DOWN: 16, Direction.LEFT: 32, Direction.RIGHT: 48}[self.direction]
        pyxel.blt(self.x - 8, self.y - 8, 0, sprite_x, 0, 16, 16, 6)

    def draw_donuts(self):
        """ドーナツを描画する"""
        for donut in self.donuts:
            pyxel.blt(int(donut["x"] - 5), int(donut["y"] - 5), 0, 0, 16, 10, 10, 6)

    def draw_ui(self):
        """UIを描画する"""
        pyxel.text(5, 10, f"Score: {self.score}", pyxel.COLOR_BLACK)
        for i in range(self.life):
            pyxel.blt(pyxel.width - 15 * (i + 1), 8, 0, 16, 16, 11, 10, 6)

    def draw_game_over(self):
        """ゲームオーバー画面を描画する"""
        pyxel.text(pyxel.width // 2 - 20, pyxel.height // 2 - 10, "GAME OVER", pyxel.COLOR_RED)
        pyxel.text(pyxel.width // 2 - 45, pyxel.height // 2 + 10, "Press Enter to Restart", pyxel.COLOR_BLACK)

    def spawn_donut(self):
        """新しいドーナツを生成する"""
        side = random.choice(list(Direction))
        x, y, dx, dy = self.calculate_donut_position_and_velocity(side)
        self.donuts.append({"x": x, "y": y, "dx": dx, "dy": dy, "direction": side})

    def calculate_donut_position_and_velocity(self, side):
        """ドーナツの初期位置と速度を計算する"""
        if side in (Direction.UP, Direction.DOWN):
            x = pyxel.width // 2
            y = 0 if side == Direction.UP else pyxel.height
            dx = 0
            dy = (pyxel.height // 2 - y) / max(1, 60 - self.donut_speed)
        else:
            x = 0 if side == Direction.LEFT else pyxel.width
            y = pyxel.height // 2
            dx = (pyxel.width // 2 - x) / max(1, 60 - self.donut_speed)
            dy = 0
        return x, y, dx, dy

    def run(self):
        """ゲームを実行する"""
        pyxel.run(self.update, self.draw)


App().run()
