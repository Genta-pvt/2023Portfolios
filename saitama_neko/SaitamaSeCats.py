# ファイル名 : SaitamaSeCats.py
# 機能概要 : 埼玉県の猫里親募集情報を取得して、内容をメール通知する。SeCatsSchedule.py.pyから実行される。

# 関数の説明
# 1. create_catlist()
#   ・引数無し
#   ・戻り値
#       (str)message : 実行時の日付 + 実行時に何匹里親募集状態の猫がいるか
#   ・処理概要
#       埼玉県南部・東部地区の里親募集情報ページを解析し配列に格納。何匹の猫が里親募集しているかを数える
# 2. def send_mail()
#   ・引数無し
#   ・戻り値無し
#   ・処理概要
#       create_catlist()を実行し、戻り値をメールで送信する

# ライブラリをインポート
from bs4 import BeautifulSoup   # HTML解析
import requests  # HTML取得
import re  # 正規表現
import datetime  # 時刻
from email.mime.text import MIMEText  # メール作成
import smtplib  # メール送信



# 例外クラス AreaCodeError SaitamaCatsの引数が不正な時に呼び出す
class AreaCodeError(Exception):
    pass



# SaitamaCats クラス 埼玉県の猫譲渡情報ページの情報をまとめる・分析するみたいな役割
class SaitamaCats:
    def __init__(self,area):
        self.area = area
        self.bs4_page = self.import_page()
        # self.cats_arr = self.extract_data_nw()
        self.cat_dict_tmp = \
            {'譲渡状況': '', '管理番号': '', '掲載開始日': '', '種類': '', \
            '性別': '', '毛色': '', '推定年齢': '', 'その他の情報': '', \
            '問合せ先': '', '画像': ''}


    # メソッド "import_page" 指定した区域(「北部・西部」or「南部・東部」)のbs4オブジェクトを作る
    # 戻り値：引数に対応するWebページのbs4オブジェクト
    def import_page(self):
        # 定数
        NORTHWEST_SET = {'northwest', 'NorthWest', 'Northwest', 'nw', 'NW', 'north', 'North', 'n', 'N'}
        SOUTHEAST_SET = {'southeast', 'SouthEast', 'Southeast', 'se', 'SE', 'south', 'South', 's', 'S'}
        URL_NW = 'https://www.pref.saitama.lg.jp/b0716/joutoseineko-n.html'
        URL_SE= 'https://www.pref.saitama.lg.jp/b0716/joutoseineko-s.html'

        # URLからbs4オブジェクトを作成(SaitamaCats.areaも設定)
        try:
            # 指定エリア(self.area)が北部・西部のとき
            if self.area in NORTHWEST_SET:
                # 値を丸める
                SaitamaCats.area = 'nw'
                # repupests実行
                r = requests.get(URL_NW)
            # 指定エリア(self.area)が南部・東部のとき
            elif self.area in SOUTHEAST_SET:
                # 値を丸める
                SaitamaCats.area = 'se'
                # repupests実行
                r = requests.get(URL_SE)
            # 指定エリアが(self.area)が不正な値のとき(例外)
            else:
                raise AreaCodeError('Please enter a valid value. Example : nw, se.')
        # 例外処理
        except AreaCodeError as e :
            print(e)
        # 例外発生しないとき requestsで取得したデータをbs4オブジェクトに変換
        else:
            soup = BeautifulSoup(r.content,'html.parser')
            print(SaitamaCats.area) # テスト用出力
            return soup


    # メソッド "extract_data" データ属性"bs4_page"を解析して各猫の情報をまとめた配列を作る(今はnw限定)
    # 戻り値 : [{見出し1: 値1, 見出し2: 値2, ...}, {}, ...]
    def extract_data_nw(self):
        # テーブルを登録する配列(戻り値) 
        arr = []
        # インポートしたデータからページの主となる部分を抽出
        main_contents = self.bs4_page.find('div',attrs={"id" : "tmp_contents" })
        # 各テーブルの情報を登録。(すべてのテーブルで繰り返し)
        for table in main_contents.find_all('table'):
            # テーブルの内容を登録する辞書を定義
            table_dict = {}
            # 譲渡状況を登録
            table_dict['譲渡状況'] = table.previous_sibling.previous_sibling.string
            # 各行の見出しと値をそれぞれ登録（すべての行で繰り返し)
            for tr in table.find_all('tr'):
                # 見出しのテキスト
                key = tr.contents[1].get_text(strip = True)
                # 値のテキスト
                value = tr.contents[3].contents[1].get_text(strip = True)
                # 見出し: 値で登録
                table_dict[key] = value
            # テーブル → 辞書としたものを配列に登録
            arr.append(table_dict)
        # 戻り値
        return arr



# 単体で実行したときの処理
if __name__ == '__main__':
    pass
    hoku_sei = SaitamaCats('nw').extract_data_nw()
    print(hoku_sei)