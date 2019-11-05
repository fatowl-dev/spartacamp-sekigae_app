"""
席替えアプリ

使い方:
 Pythonのバージョン: 3.7

 コマンドラインから以下のように実行
 $ python3 app <file>
 - <file>に前回の席替え結果ファイル(JSON)を指定
"""
import sys
import os


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

    # 第一引数のファイルが存在しているか確認
    if not os.path.isfile(file_name):
        print('エラー: 指定されたファイルがありません。')
        print_usage()
        exit(1)

    # sekigae.run(file_name)


