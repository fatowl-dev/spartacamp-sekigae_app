"""
席替えアプリ

使い方:
 Pythonのバージョン: 3.7

 コマンドラインから以下のように実行
 $ python3 sekigae_app.py <file>
 - <file>に前回の席替え結果ファイル(JSON)を指定
"""
import datetime
import json
import os
import sys

import sekigae


# 使い方を表示する
def print_usage():
    print("使い方: python3 sekigae_app.py <file>")
    print("       - <file> ... 前回の席替え結果ファイルを指定。")


if __name__ == '__main__':
    args = sys.argv

    # 引数の数を確認
    if len(args) <= 1:
        print("エラー: コマンドライン引数が足りません。")
        print_usage()
        exit(1)

    file_name = sys.argv[1]

    # 第一引数のファイルが存在￿しているか確認
    if not os.path.isfile(file_name):
        print('エラー: 指定されたファイルがありません。')
        print_usage()
        exit(1)

    # データ読み込み
    prev_data = sekigae.SekigaeData(file_name)

    # 席替え実行
    new_data = sekigae.execute(file_name)

    # ファイルに保存
    new_data_dict = new_data.convert_to_dict()
    new_file_path = datetime.datetime.now().strftime('json/' + new_data.class_name + '_%Y%m%d%H%M%S.json')
    file = open(new_file_path, 'w')
    json.dump(new_data_dict, fp=file, ensure_ascii=False, indent=2, separators=(',', ': '))
    file.close()
