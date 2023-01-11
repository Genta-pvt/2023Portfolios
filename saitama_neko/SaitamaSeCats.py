# ファイル名 : SaitamaSeCats.py
# 機能概要 : 埼玉県の猫里親募集情報を取得して、内容をメール通知する。SeCatsSchedule.py.pyから実行される。

# 本プログラム内に記載されているURL
# 「https://www.pref.saitama.lg.jp/b0716/joutoseineko-n.html」「https://www.pref.saitama.lg.jp/b0716/joutoseineko-s.html」
# は埼玉県のホームページであり、このURL上に公開されている記事、写真、図画、その他データ類の著作権は、埼玉県、またはその情報提供者に帰属します。

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



# 例外クラス AreaCodeError SaitamaCatsの引数が不正な時に呼び出す
class AreaCodeError(Exception):
    pass



# SaitamaCats クラス 埼玉県の猫譲渡情報ページの情報をまとめる・分析するみたいな役割
class SaitamaCats:
    def __init__(self,area):
        self.area = area
        self.bs4_page = self.import_page()
        self.cats_arr = self.extract_data()
        self.cats_count_all = 0
        self.cats_count_wanted = 0
        self.cats_count_interview = 0
        self.cats_count_decided = 0

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
                self.area = 'nw'
                # url設定
                self.url = URL_NW
                # repupests実行
                r = requests.get(self.url)
            # 指定エリア(self.area)が南部・東部のとき
            elif self.area in SOUTHEAST_SET:
                # 値を丸める
                self.area = 'se'
                # url設定
                self.url = URL_SE
                # repupests実行
                r = requests.get(self.url)
            # 指定エリアが(self.area)が不正な値のとき(例外)
            else:
                raise AreaCodeError('Please enter a valid value. Example : nw, se.')
        # 例外処理
        except AreaCodeError as e :
            print(e)
        # 例外発生しないとき requestsで取得したデータをbs4オブジェクトに変換
        else:
            soup = BeautifulSoup(r.content,'html.parser')
            print(self.area) # テスト用出力
            return soup


    # メソッド "extract_data" データ属性"bs4_page"を解析して各猫の情報をまとめた配列を作る(今はnw限定)
    # 戻り値 : [{見出し1: 値1, 見出し2: 値2, ...}, {}, ...]
    def extract_data(self):
        # テーブルを登録する配列(戻り値) 
        arr = []
        # インポートしたデータからページの主となる部分を抽出
        main_contents = self.bs4_page.find('div',attrs={"id" : "tmp_contents" })
        # 各テーブルの情報を登録。(すべてのテーブルで繰り返し)
        for table in main_contents.find_all('table'):
            # テーブルの内容を登録する辞書を定義
            table_dict = {}
            # 譲渡状況を登録(nw限定) 
            if self.area == 'nw':
                table_dict['譲渡状況'] = table.previous_sibling.previous_sibling.get_text(strip = True)
            # 各行の見出しと値をそれぞれ登録（すべての行で繰り返し)
            for tr in table.find_all('tr'):
                # 見出しのテキスト(行内1列目セルのテキスト)
                key = tr.contents[1].get_text(strip = True)
                # 値のテキスト(行内2列目セルのテキスト)
                # (se限定)"管理番号"行の時(セル内に"管理番号", "譲渡状況"が含まれている)
                if self.area == 'se' and key == '管理番号':
                    # セル内の文字列全体
                    whole_td = tr.contents[3].get_text(strip = True)
                    # "管理番号"のみ抽出し値とする
                    value = re.search(r'(.\d+-.\d+)',whole_td).group(1)
                    # "譲渡状況"を抽出、登録
                    table_dict['譲渡状況'] = whole_td.replace(value,'')
                # 値のテキスト(行内2列目セルのテキスト)
                else:
                    value = tr.contents[3].get_text(strip = True)
                # 見出し: 値で登録
                table_dict[key] = value                
            # テーブル → 辞書としたものを配列に登録
            arr.append(table_dict)
        # 戻り値
        return arr


    # 猫数え
    def count_cats(self,filter = 'all'):


        def count(value):
            i = 0
            for elem in self.cats_arr:
                if elem.get('譲渡状況') == value:
                    i += 1
            return i


        if filter == 'all':
            self.cats_count_all = len(self.cats_arr)
            return self.cats_count_all
        elif filter == 'wanted':
            self.cats_count_wanted = count('')
            return self.cats_count_wanted
        elif filter == 'interview':
            self.cats_count_interview = count('お見合い中です')
            return self.cats_count_interview
        elif filter == 'decided':
            self.cats_count_decided = count('飼い主さんが決まりました！')
            return self.cats_count_decided






# 単体で実行したときの処理
if __name__ == '__main__':
    # print(CreateSentens('n').sentens_1())
    # print(SaitamaCats('n').url)
    # print (CreateSentens('n').sentens_2())
    pass