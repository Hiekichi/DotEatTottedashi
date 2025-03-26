import pyxel
import random

class DotEat:
    def __init__(self):
        # ゲーム画面の初期化 (128x128ピクセル)
        pyxel.init(128, 128, title="PacMad")
        
        # ゲームの状態を初期化
        self.init_game()
        
        # ゲームループの開始
        pyxel.run(self.update, self.draw)
    
    def init_game(self):
        # スコアと残機
        self.score = 0
        self.lives = 3
        self.game_over = False
        
        # 迷路のマップ (0=道, 1=壁)
        self.maze = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1],
            [1,0,1,1,0,1,0,0,0,0,1,0,1,1,0,1],
            [1,0,0,0,0,1,1,1,1,1,1,0,0,0,0,1],
            [1,0,1,1,0,0,0,1,1,0,0,0,1,1,0,1],
            [1,0,1,1,0,1,0,0,0,0,1,0,1,1,0,1],
            [1,0,0,0,0,1,0,1,1,0,1,0,0,0,0,1],
            [1,1,1,1,0,1,0,1,1,0,1,0,1,1,1,1],
            [1,1,1,1,0,1,0,0,0,0,1,0,1,1,1,1],
            [1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1],
            [1,0,1,1,0,1,0,0,0,0,1,0,1,1,0,1],
            [1,0,0,1,0,1,1,1,1,1,1,0,1,0,0,1],
            [1,1,0,1,0,0,0,0,0,0,0,0,1,0,1,1],
            [1,0,0,0,0,1,1,1,1,1,1,0,0,0,0,1],
            [1,0,1,1,1,1,0,0,0,0,1,1,1,1,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ]
        
        # ドットの位置 (初期は全ての道にドットを配置)
        self.dots = []
        for y in range(len(self.maze)):
            for x in range(len(self.maze[0])):
                if self.maze[y][x] == 0:  # 道の場合
                    self.dots.append((x, y))
        
        # プレイヤーの初期位置
        self.player_x = 1
        self.player_y = 1
        self.player_dir = 0  # 0=右, 1=下, 2=左, 3=上
        
        # 敵の初期設定 (position, direction, color)
        self.enemies = [
            {"x": 14, "y": 14, "dir": random.randint(0, 3), "color": 8},
            {"x": 14, "y": 1, "dir": random.randint(0, 3), "color": 11},
            {"x": 1, "y": 14, "dir": random.randint(0, 3), "color": 10}
        ]
        
        # アニメーション用タイマー
        self.anim_time = 0
        self.move_timer = 0
    
    def update(self):
        # ゲームオーバー時の処理
        if self.game_over:
            if pyxel.btnp(pyxel.KEY_R):
                self.init_game()
            return
        
        self.anim_time = (self.anim_time + 1) % 30
        
        # プレイヤーの入力による方向変更
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player_dir = 0
        elif pyxel.btn(pyxel.KEY_DOWN):
            self.player_dir = 1
        elif pyxel.btn(pyxel.KEY_LEFT):
            self.player_dir = 2
        elif pyxel.btn(pyxel.KEY_UP):
            self.player_dir = 3
        
        # 移動タイマー更新
        self.move_timer += 1
        if self.move_timer >= 6:  # 6フレームごとに移動
            self.move_timer = 0
            
            # プレイヤーの移動
            next_x, next_y = self.player_x, self.player_y
            if self.player_dir == 0:
                next_x += 1
            elif self.player_dir == 1:
                next_y += 1
            elif self.player_dir == 2:
                next_x -= 1
            elif self.player_dir == 3:
                next_y -= 1
            
            # 壁でなければ移動
            if 0 <= next_x < len(self.maze[0]) and 0 <= next_y < len(self.maze) and self.maze[next_y][next_x] == 0:
                self.player_x, self.player_y = next_x, next_y
            
            # 敵の移動
            for enemy in self.enemies:
                # ランダムに方向を変える (20%の確率)
                if random.random() < 0.2:
                    enemy["dir"] = random.randint(0, 3)
                
                # 次の位置を計算
                next_x, next_y = enemy["x"], enemy["y"]
                if enemy["dir"] == 0:
                    next_x += 1
                elif enemy["dir"] == 1:
                    next_y += 1
                elif enemy["dir"] == 2:
                    next_x -= 1
                elif enemy["dir"] == 3:
                    next_y -= 1
                
                # 壁でなければ移動、壁なら方向転換
                if 0 <= next_x < len(self.maze[0]) and 0 <= next_y < len(self.maze) and self.maze[next_y][next_x] == 0:
                    enemy["x"], enemy["y"] = next_x, next_y
                else:
                    enemy["dir"] = random.randint(0, 3)
        
        # ドットの収集
        if (self.player_x, self.player_y) in self.dots:
            self.dots.remove((self.player_x, self.player_y))
            self.score += 10
            
            # 全てのドットを集めたらクリア
            if not self.dots:
                # ドットが0になったらクリア (次のレベルや勝利画面への遷移)
                self.game_over = True
        
        # 敵との衝突判定
        for enemy in self.enemies:
            if self.player_x == enemy["x"] and self.player_y == enemy["y"]:
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over = True
                else:
                    # プレイヤーを初期位置に戻す
                    self.player_x = 1
                    self.player_y = 1
    
    def draw(self):
        # 背景を黒で塗りつぶす
        pyxel.cls(0)
        
        # 迷路の描画
        for y in range(len(self.maze)):
            for x in range(len(self.maze[0])):
                if self.maze[y][x] == 1:  # 壁
                    pyxel.rect(x * 8, y * 8, 8, 8, 5)
        
        # ドットの描画
        for x, y in self.dots:
            pyxel.rect(x * 8 + 3, y * 8 + 3, 2, 2, 7)
        
        # プレイヤーの描画 (パックマンの口パクアニメーション)
        mouth_angle = abs((self.anim_time % 20) - 10) / 10
        if self.player_dir == 0:  # 右
            pyxel.circ(self.player_x * 8 + 4, self.player_y * 8 + 4, 3, 10)
            if mouth_angle > 0.2:
                pyxel.tri(
                    self.player_x * 8 + 4, self.player_y * 8 + 4,
                    self.player_x * 8 + 7, self.player_y * 8 + 4 - 3 * mouth_angle,
                    self.player_x * 8 + 7, self.player_y * 8 + 4 + 3 * mouth_angle,
                    0
                )
        elif self.player_dir == 1:  # 下
            pyxel.circ(self.player_x * 8 + 4, self.player_y * 8 + 4, 3, 10)
            if mouth_angle > 0.2:
                pyxel.tri(
                    self.player_x * 8 + 4, self.player_y * 8 + 4,
                    self.player_x * 8 + 4 - 3 * mouth_angle, self.player_y * 8 + 7,
                    self.player_x * 8 + 4 + 3 * mouth_angle, self.player_y * 8 + 7,
                    0
                )
        elif self.player_dir == 2:  # 左
            pyxel.circ(self.player_x * 8 + 4, self.player_y * 8 + 4, 3, 10)
            if mouth_angle > 0.2:
                pyxel.tri(
                    self.player_x * 8 + 4, self.player_y * 8 + 4,
                    self.player_x * 8 + 1, self.player_y * 8 + 4 - 3 * mouth_angle,
                    self.player_x * 8 + 1, self.player_y * 8 + 4 + 3 * mouth_angle,
                    0
                )
        elif self.player_dir == 3:  # 上
            pyxel.circ(self.player_x * 8 + 4, self.player_y * 8 + 4, 3, 10)
            if mouth_angle > 0.2:
                pyxel.tri(
                    self.player_x * 8 + 4, self.player_y * 8 + 4,
                    self.player_x * 8 + 4 - 3 * mouth_angle, self.player_y * 8 + 1,
                    self.player_x * 8 + 4 + 3 * mouth_angle, self.player_y * 8 + 1,
                    0
                )
        
        # 敵の描画
        for enemy in self.enemies:
            pyxel.circ(enemy["x"] * 8 + 4, enemy["y"] * 8 + 4, 3, enemy["color"])
        
        # スコアとライフの表示
        pyxel.text(5, 2, f"SCORE:{self.score}", 7)
        pyxel.text(80, 2, f"LIVES:{self.lives}", 7)
        
        # ゲームオーバー表示
        if self.game_over:
            if self.lives <= 0:
                pyxel.text(40, 60, "GAME OVER!", 8)
            else:
                pyxel.text(45, 60, "YOU WIN!", 11)
            pyxel.text(30, 70, "PRESS R TO RESTART", 7)

# ゲームの開始
DotEat()