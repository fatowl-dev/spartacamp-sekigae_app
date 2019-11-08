from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from kivy.properties import ListProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.config import Config
import os

Config.set('graphics', 'width', '640')
Config.set('graphics', 'height', '640')


class SekigaeWidget(FloatLayout):
    file_path = StringProperty('File:')
    names = ListProperty(['mem' + str(f'{i:02d}') for i in range(14)])

    def __init__(self, **kwargs):
        super(SekigaeWidget, self).__init__(**kwargs)

    def select_btn_clicked(self):
        self.file_path = 'File: AAAAAAAAAAAAA'


class SekigaeApp(App):
    def __init__(self, **kwargs):
        super(SekigaeApp, self).__init__(**kwargs)
        self.title = '席替えアプリ'    # ウィンドウの名前を変更

    def build(self):
        return SekigaeWidget()


if __name__ == '__main__':
    app = SekigaeApp()
    app.run()
