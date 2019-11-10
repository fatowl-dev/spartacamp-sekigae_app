"""
席替えアプリの実装
"""
import copy
import json
import random


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

    def buddy_in_history(self, buddy_id):
        for hist in self.buddy_history_list:
            if buddy_id == hist:
                return True

        return False


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
        self.class_name = ""     # 教室の名前
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
        self.class_name = dic['class_name']
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

        dic['class_name'] = self.class_name

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

    def get_member_by_id(self, member_id:int):
        for member in self.member_list:
            if member.id == member_id:
                return member
        return None

    def get_seat_by_index(self, index):
        for seat in self.seat_list:
            if seat.index == index:
                return seat
        return None

    def clear_buddy_history(self):
        for member in self.member_list:
            member.buddy_history_list = []

    def get_lefty_seat_list(self):
        seat_list = [seat for seat in self.seat_list if seat.lefty_flag]
        return seat_list

    def get_lefty_member_list(self):
        member_list = [member for member in self.member_list if member.is_lefty]
        return member_list


def create_pair_list(data: SekigaeData):
    id_list = [member.id for member in data.member_list]

    pair_list = []
    while len(id_list) > 1:
        random.shuffle(id_list)
        first = id_list[0]
        id_list.remove(first)
        second = -1
        for member_id in id_list:
            if not data.get_member_by_id(first).buddy_in_history(member_id):
                second = member_id
                id_list.remove(second)
                break
        if second == -1:
            # 相手が見つからなかったときは履歴をクリアしてやり直し
            data.clear_buddy_history()
            return create_pair_list(data)

        pair_list.append((first, second))

    if len(id_list) == 1:
        pair_list.append((id_list[0], -1))

    return pair_list


# 最初のシャッフル
def first_seat_shuffle(data: SekigaeData):
    # 先に左利きの人の席を決める
    lefty_seat_list = data.get_lefty_seat_list()
    lefty_member_list = data.get_lefty_member_list()
    member_list = copy.copy(data.member_list)   # 未決定メンバーリスト
    seat_list = copy.copy(data.seat_list)       # 未決定席リスト
    random.shuffle(lefty_seat_list)
    random.shuffle(lefty_member_list)
    order = dict()                      # 席替え結果の辞書
    for member in lefty_member_list:
        if len(lefty_seat_list) == 0:
            break
        order[str(lefty_seat_list[0].index)] = member.id
        seat_list.remove(lefty_seat_list[0])    # 決定した席を削除
        lefty_seat_list.pop(0)                  # 決定した席を左可リストから削除
        member_list.remove(member)  # 決定したメンバーを削除

    # 残ったメンバーと席をランダム配置
    random.shuffle(member_list)
    for i in range(len(member_list)):
        order[str(seat_list[i].index)] = member_list[i].id

    # 辞書をリストに変換
    id_list = []
    for i in range(len(order)):
        id_list.append(order[str(i)])

    return id_list


# 二回目以降のシャッフル
def seat_shuffle(data: SekigaeData):
    order = dict()
    # 履歴に被らないようにペアを作成
    pair_list = create_pair_list(data)
    # 左利きがいるペアを抜き出す
    lefty_list = [p for p in pair_list if data.get_member_by_id(p[0]).is_lefty \
                  or (p[1] != -1 and data.get_member_by_id(p[1]).is_lefty)]
    # 未決定リスト
    seat_list = copy.copy(data.seat_list)
    # 左利き対応席リスト
    lefty_seat_list = data.get_lefty_seat_list()
    # 左利きがいるペアを配置
    random.shuffle(lefty_seat_list)
    for pair in lefty_list:
        if len(lefty_seat_list) == 0:
            break
        seat = lefty_seat_list.pop(0)
        seat_list.remove(seat)
        mem = data.get_member_by_id(pair[0])
        seat1_index = None
        if mem.is_lefty:
            order[str(seat.index)] = mem.id
            if seat.index % 2 == 0:
                seat1_index = seat.index + 1
            else:
                seat1_index = seat.index - 1

            mem1 = data.get_member_by_id(pair[1])
            seat1 = data.get_seat_by_index(seat1_index)
            order[str(seat1_index)] = mem1.id
            seat_list.remove(seat1)
            pair_list.remove(pair)
        else:
            mem1 = data.get_member_by_id(pair[1])
            order[str(seat.index)] = mem1.id
            if seat.index % 2 == 0:
                seat1_index = seat.index + 1
            else:
                seat1_index = seat.index - 1
            seat1 = data.get_seat_by_index(seat1_index)
            order[str(seat1_index)] = mem.id
            seat_list.remove(seat1)
            pair_list.remove(pair)

    # 残ったペアを残った席に配置
    random.shuffle(pair_list)
    for pair in pair_list:
        seat0 = seat_list.pop(0)
        seat1_index = None
        if seat0.index % 2 == 0:
            seat1_index = seat0.index + 1
        else:
            seat1_index = seat0.index - 1
        seat1 = data.get_seat_by_index(seat1_index)
        seat_list.remove(seat1)
        order[str(seat0.index)] = pair[0]
        order[str(seat1.index)] = pair[1]

    # 辞書をリストに変換
    id_list = []
    for i in range(len(order)):
        id_list.append(order[str(i)])

    # # ペアをシャッフル
    # random.shuffle(pair_list)
    # # リストに入れる
    # for pair in pair_list:
    #     id_list.append(pair[0])
    #     if pair[1] != -1:
    #         id_list.append(pair[1])
    #
    return id_list


# prev_data...前の席替えデータ
# return: 席替え後のSekigaeData
def execute(prev_data: SekigaeData):
    # 席順の辞書がカラならランダムに並び替える
    id_list = None
    if len(prev_data.order_dict) == 0:
        id_list = first_seat_shuffle(prev_data)
    else:
        id_list = seat_shuffle(prev_data)

    # 新しい席替えデータを作成
    new_data = copy.deepcopy(prev_data)
    new_data.order_dict = dict()
    for i in range(0, len(id_list)):
        # 席順のリストを新しいデータに反映
        new_data.order_dict[str(i)] = id_list[i]
        # ペアの履歴をつくる
        if i % 2 == 0 and i < len(id_list) - 1:
            new_data.get_member_by_id(id_list[i]).buddy_history_list.append(id_list[i+1])
        else:
            new_data.get_member_by_id(id_list[i]).buddy_history_list.append(id_list[i-1])
        # 席の履歴
        new_data.member_list[id_list[i]].seat_history_list.append(i)

    # 表示
    for i in range(0, len(new_data.order_dict)):
        name = new_data.get_member_by_id(new_data.order_dict[str(i)]).name
        print(f'{i+1:02d}: {name}')

    return new_data


# デフォルトの席替えデータを作成する
def create_default_sekigae_data():
    data = SekigaeData()

    data.class_name = "sparta"

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
    # for member in data.member_list:
    #    data.order_dict[member.id] = member.id
    # 席順データは最初は空

    return data


def __main():
    # data = create_default_sekigae_data()
    # data_dic = data.convert_to_dict()
    # file = open('json/test.json', 'w')
    # json.dump(data_dic, fp=file, ensure_ascii=False, indent=2, separators=(',', ': '))
    # file.close()
    # data2 = SekigaeData('json/test.json')
    # print(json.dumps(data2.convert_to_dict(), ensure_ascii=False, indent=2, separators=(',', ': ')))
    data = create_default_sekigae_data()
    lefty_seat_list = data.get_lefty_seat_list()
    for seat in lefty_seat_list:
        print(seat.index)


if __name__ == '__main__':
    __main()
