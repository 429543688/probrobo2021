import random

class Robot(object):

    def __init__(self, maze, alpha=0.5, gamma=0.9, epsilon0=0.5):

        self.maze = maze
        self.valid_actions = self.maze.valid_actions
        self.state = None
        self.action = None

        # 学習ロボットのパラメータを設定する
        self.alpha = alpha
        self.gamma = gamma

        self.epsilon0 = epsilon0
        self.epsilon = epsilon0
        self.t = 0

        self.Qtable = {}
        self.reset()

    def reset(self):
        """
        ロボットをリセットする
        """
        self.state = self.sense_state()
        self.create_Qtable_line(self.state)

    def set_status(self, learning=False, testing=False):
        """
         ロボットがqテーブルを学習しているかどうかを判断する、または テスト手順を終了する
        """
        self.learning = learning
        self.testing = testing

    def update_parameter(self):
        """
        q学習ロボットのパラメータを更新する
        """
        if self.testing:
            # TODO 1. テスト時にランダムな選択をしない
            self.epsilon = 0.0
        else:
            # TODO 2.学習時にパラメータを更新する
            self.t += 1
            self.epsilon = self.epsilon0 / self.t
        return self.epsilon

    def sense_state(self):
        """
        ロボットの現在の状態を取得する
        """
        # TODO 3. ロボットの現在の状態を返す
        return self.maze.sense_robot()

    def create_Qtable_line(self, state):
        """
        現在の状態からqtableを作成する
        """
        # TODO 4. 現在の状態から qtable を作成する
        # qtableは2レベルのdictでなければならない。
        # Qtable[state] ={'u':xx, 'd':xx, ...} とする。
        # もしQtable[state]がすでに終了していたら、次のようにする。
        # 変更しない
        self.Qtable.setdefault(state, {a: 0.0 for a in self.valid_actions})
        
    def choose_action(self):
        """
        与えられたルールに従ったアクションを返す
        """
        def is_random_exploration():

            # TODO 5. ランダムな選択を行うかどうかを返す
            # ヒント：乱数を生成し、比較する
            return random.random() < self.epsilon

        if self.learning:
            if is_random_exploration():
                # TODO 6. ランダムな選択肢を返す
                return random.choice(self.valid_actions)
            else:
                # TODO 7. q値が最も高いアクションを返す
                return max(self.Qtable[self.state], key=self.Qtable[self.state].get)
        elif self.testing:
            # TODO 7. q値が最も高いアクションを選択する
            return max(self.Qtable[self.state], key=self.Qtable[self.state].get)
        else:
            # TODO 6. ランダムな選択肢を返す
            return random.choice(self.valid_actions)
    
    def update_Qtable(self, r, action, next_state):
        """
        与えられたルールに従ってqtableを更新する
        """
        if self.learning:
            # TODO 8. 学習時、qテーブルを更新する。
            self.Qtable[self.state][action] += self.alpha * (r + self.gamma * float(max(self.Qtable[next_state].values())) - self.Qtable[self.state][action])

    def update(self):
        """
        ロボットを更新するときに何をすべきかを説明する手続き
        学習時、テスト時ともに各エポック毎に呼び出される
        現在の行動と報酬を返す
        """
        self.state = self.sense_state() # 現在の状態を取得する
        self.create_Qtable_line(self.state) # 状態について、q taple行を作成する

        action = self.choose_action() # 今の状態を選んで行動する
        reward = self.maze.move_robot(action) # 動作指定ロボットを動かす

        next_state = self.sense_state() # 次の状態になる
        self.create_Qtable_line(next_state) # 次の状態のためのQテーブル行を作成する

        if self.learning and not self.testing:
            self.update_Qtable(reward, action, next_state) # 更新Qテーブル
            self.update_parameter() # 更新パラメータ

        return action, reward
