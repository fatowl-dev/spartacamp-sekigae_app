import datetime
import json
from glob import glob

from kivy.app import App
from kivy.config import Config
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.properties import ListProperty
from kivy.properties import StringProperty
from kivy.resources import resource_add_path
from kivy.uix.floatlayout import FloatLayout

import sekigae


# メインの処理をするクラス(ウィジェット)
class SekigaeWidget(FloatLayout):
    file_path = StringProperty('None')
    names = ListProperty(['mem' + str(f'{i:02d}') for i in range(14)])  # ここを書き換えると席の名前が変わる
    file_list = ListProperty()

    def __init__(self, **kwargs):
        super(SekigaeWidget, self).__init__(**kwargs)
        self.update_file_list()

    def update_seat_order(self, data: sekigae.SekigaeData):
        for i in range(len(self.names)):
            key = str(i)
            if key in data.order_dict:
                self.names[i] = data.get_member_by_id(data.order_dict[str(i)]).name
            else:
                self.names[i] = 'NO DATA'

    def update_file_list(self):
        self.file_list = glob('json//*.json')

    # ドロップダウンリストからファイルを選択したときの処理
    def on_select_file(self, text):
        self.file_path = text
        data = sekigae.SekigaeData(self.file_path)
        self.update_seat_order(data)

    # シャッフルボタンを押したときの処理
    def on_shuffle_btn_clicked(self):
        if self.file_path == 'None':
            return

        data = sekigae.SekigaeData(self.file_path)
        new_data = sekigae.execute(data)
        self.update_seat_order(new_data)
        # ファイルに保存
        new_data_dict = new_data.convert_to_dict()
        new_file_path = datetime.datetime.now().strftime('json/' + new_data.class_name + '_%Y%m%d%H%M%S.json')
        file = open(new_file_path, 'w')
        json.dump(new_data_dict, fp=file, ensure_ascii=False, indent=2, separators=(',', ': '))
        file.close()
        # ファイルリスト更新
        self.file_path = new_file_path
        self.update_file_list()


# アプリケーションクラス
class SekigaeApp(App):
    def __init__(self, **kwargs):
        super(SekigaeApp, self).__init__(**kwargs)
        self.title = '席替えアプリ'    # ウィンドウの名前を変更

    def build(self):
        return SekigaeWidget()


if __name__ == '__main__':
    # デフォルトに使用するフォントを変更する
    resource_add_path('./fonts')
    LabelBase.register(DEFAULT_FONT, 'ume-ugo5.ttf')  # 日本語が使用できるように日本語フォントを指定する

    Config.set('graphics', 'width', '800')
    Config.set('graphics', 'height', '800')
    app = SekigaeApp()
    app.run()
