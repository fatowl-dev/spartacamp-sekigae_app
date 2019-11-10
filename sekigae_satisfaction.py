# シャッフルのロジックに満足度を採用したもの
# 特定回数完全ランダムのシャッフルを繰り返し、
# 各シャッフルの満足度を評価、満足度が1番高い
# 席順を採用する
import copy
import random

from sekigae import SekigaeData, PersonalData, SeatData


# 履歴を参照し、隣の席の組み合わせの満足度を計算
def get_buddy_stsf_lv(personal_data: PersonalData, seat_number: int, seat_order: list) -> float:
    return 0.0


# 席の場所の満足度(過去に同じ席になったことが多いと低くなる)
def get_seat_place_stsf_lv(personal_data: PersonalData, seat_number) -> float:
    return 0


# 左利きを考慮した場合の満足度を計算
def get_lefty_stsf_lv(personal_data: PersonalData, seat_data: SeatData) -> float:
    return 0


# 前に行きたい人を考慮した場合の満足度を計算
def get_forward_stsf_lv(personal_data: PersonalData, seat_data: SeatData) -> float:
    return 0


# 席順を解析して満足度お算出する
def analyse_satisfaction_level(data: SekigaeData, seat_order: list):
    stsf_lv = 0.0
    for i in range(len(seat_order)):
        member = data.get_member_by_id(seat_order[i])
        seat = data.get_seat_by_index(i)
        stsf_lv += get_buddy_stsf_lv(member, i, seat_order)
        stsf_lv += get_seat_place_stsf_lv(member, i, seat_order)
        stsf_lv += get_lefty_stsf_lv(member, seat)
        stsf_lv += get_forward_stsf_lv(member, seat)

    return stsf_lv


# 満足度を使って席順を決める
def shuffle_by_satisfaction(data: SekigaeData, trial_num=100) -> SekigaeData:
    # 1.席をシャッフルする
    # 2.シャッフルした席の満足度を算出
    # 3.満足度が一番高いものを保存
    # 4.1から3を繰り返す
    member_num = len(data.member_list)

    max_stsf_lv = -9999999999999
    seat_order = None
    for i in range(trial_num):
        # 席をシャッフル
        seat_list = [n for n in range(member_num)]
        random.shuffle(seat_list)
        # 満足度を算出
        stsf_lv = analyse_satisfaction_level(data, seat_list)
        # 一番高いものを保存
        if max_stsf_lv < stsf_lv:
            seat_order = seat_list

    # 新しい席替えデータを作成
    new_data = copy.deepcopy(data)
    new_data.order_dict = {}
    for i in range(0, len(seat_order)):
        # 席順のリストを新しいデータに反映
        new_data.order_dict[str(i)] = seat_order[i]
        # ペアの履歴をつくる
        if i % 2 == 0 and i < len(seat_order) - 1:
            new_data.get_member_by_id(seat_order[i]).buddy_history_list.append(seat_order[i + 1])
        else:
            new_data.get_member_by_id(seat_order[i]).buddy_history_list.append(seat_order[i - 1])
        # 席の履歴
        new_data.member_list[seat_order[i]].seat_history_list.append(i)
    return new_data
