"""
席替えアプリの実装
"""

# 個人のデータを扱うクラス
class PersonalData:
    def __init__(self):
        self.id = 0                     # 一意のID
        self.name = ""                  # 名前
        self.is_lefty = False           # 左利きかどうか
        self.forward_prio = 0           # 前方優先度
        self.buddy_history_list = []    # 過去隣に誰が座っていたかの履歴
        self.seat_history_list = []     # 過去に座ったシートの履歴


# 席のデータを扱うクラス
class SeatData:
    def __init__(self):
        self.global_index = 0   # 席全体の番号
        self.local_index = 0    # テーブル内での番号
        self.table_number = 0   # テーブル番号
        self.lefty_flag = False # 左利きが座れるかどうか
        self.forward_flag = False   # 前方優先の席かどうか


# 席替えのデータを扱うクラス
class SekigaeData:
    def __init__(self):
        self.member_list = []   # PersonalDataを格納
        self.seat_list = []     # SeatDataを格納
        self.order_list = []    # 個人IDを席順に格納する配列


# filename...前回の席替え結果ファイル
def run(filename):
    pass