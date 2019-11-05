"""
席替えアプリの実装
"""
import json


# 個人のデータを扱うクラス
class PersonalData:
    def __init__(self):
        self.id = 0                     # 一意のID
        self.name = ""                  # 名前
        self.is_lefty = False           # 左利きかどうか
        self.forward_prio = 0           # 前方優先度
        self.buddy_history_list = []    # 過去隣に誰が座っていたかの履歴
        self.seat_history_list = []     # 過去に座ったシートの履歴

    def load_from_dict(self, dic):
        self.buddy_history_list = []
        self.seat_history_list = []
        self.id = dic['id']
        self.name = dic['name']
        self.is_lefty = dic['is_lefty']
        self.forward_prio = dic['forward_prio']
        for buddy in dic['buddy_history_list']:
            self.buddy_history_list.append(buddy)
        for seat in dic['seat_history_list']:
            self.seat_history_list.append(seat)

    def convert_to_dict(self):
        dic = dict()
        dic['id'] = self.id
        dic['name'] = self.name
        dic['is_lefty'] = self.is_lefty
        dic['forward_prio'] = self.forward_prio
        dic['buddy_history_list'] = self.buddy_history_list
        dic['seat_history_list'] = self.seat_history_list
        return dic


# 席のデータを扱うクラス
class SeatData:
    def __init__(self):
        self.index = 0   # 席の番号
        self.table_number = 0   # テーブル番号
        self.lefty_flag = False     # 左利きが座れるかどうか
        self.forward_flag = False   # 前方の席かどうか

    def load_from_dict(self, dic):
        self.index = dic['index']
        self.table_number = dic['table_number']
        self.lefty_flag = dic['lefty_flag']
        self.forward_flag = dic['forward_flag']

    def convert_to_dict(self):
        dic = dict()
        dic['index'] = self.index
        dic['table_number'] = self.table_number
        dic['lefty_flag'] = self.lefty_flag
        dic['forward_flag'] = self.forward_flag
        return dic


# 席替えのデータを扱うクラス
class SekigaeData:
    def __init__(self, file_path=None):
        self.member_list = None  # PersonalDataを格納
        self.seat_list = None    # SeatDataを格納
        self.order_dict = None   # 個人IDを席順に格納する配列

        if not file_path:
            self.member_list = []
            self.seat_list = []
            self.order_dict = dict()
        else:
            self.load_from_file(file_path)

    def load_from_dict(self, dic):
        self.member_list = []
        self.seat_list = []
        self.order_dict = dict()
        for member_dic in dic['member_list']:
            member = PersonalData()
            member.load_from_dict(member_dic)
            self.member_list.append(member)
        for seat_dic in dic['seat_list']:
            seat = SeatData()
            seat.load_from_dict(seat_dic)
            self.seat_list.append(seat)

        self.order_dict = dic['order_dict']

    def load_from_file(self, file_path):
        file = open(file_path, 'r')
        dic = json.load(file)
        file.close()
        self.load_from_dict(dic)

    def convert_to_dict(self):
        dic = dict()

        member_list = []
        for member in self.member_list:
            member_list.append(member.convert_to_dict())
        dic['member_list'] = member_list

        seat_list = []
        for seat in self.seat_list:
            seat_list.append(seat.convert_to_dict())
        dic['seat_list'] = seat_list

        dic['order_dict'] = self.order_dict

        return dic


# filename...前回の席替え結果ファイル
def run(filename):
    pass


# デフォルトの席替えデータを作成する
def create_default_sekigae_data():
    data = SekigaeData()

    # メンバーリスト
    for i in range(0, 14):
        personal_data = PersonalData()
        personal_data.id = i
        personal_data.name = f'member{i:02}'
        personal_data.is_lefty = False
        personal_data.forward_prio = 0
        data.member_list.append(personal_data)

    # 席データ
    for i in range(0, 14):
        seat_data = SeatData()
        seat_data.index = i
        if i == 0 or i == 3 or i == 4 or i == 7 or i == 8 or i == 13:
            seat_data.lefty_flag = True
        else:
            seat_data.lefty_flag = False

        if i <= 3:
            seat_data.table_number = 0
            seat_data.forward_flag = True
        elif 3 < i <= 7:
            seat_data.table_number = 1
            seat_data.forward_flag = True
        else:
            seat_data.table_number = 2
            seat_data.forward_flag = False
        data.seat_list.append(seat_data)

    # 席順データ
    for member in data.member_list:
        data.order_dict[member.id] = member.id

    return data


data = create_default_sekigae_data()
data_dic = data.convert_to_dict()
file = open('json/test.json', 'w')
json.dump(data_dic, fp=file, ensure_ascii=False, indent=2, separators=(',', ': '))
file.close()
data2 = SekigaeData('json/test.json')
print(json.dumps(data2.convert_to_dict(), ensure_ascii=False, indent=2, separators=(',', ': ')))
