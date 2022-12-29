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
                # repupests実行
                r = requests.get(URL_NW)
            # 指定エリア(self.area)が南部・東部のとき
            elif self.area in SOUTHEAST_SET:
                # 値を丸める
                self.area = 'se'
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
        i = 0
        if filter == 'all':
            self.cats_count_all = len(self.cats_arr)
            return self.cats_count_all
        elif filter == 'wanted':
            for elem in self.cats_arr:
                if elem.get('譲渡状況') == '':
                    i += 1
            self.cats_count_wanted = i
            return self.cats_count_wanted
        elif filter == 'interview':
            for elem in self.cats_arr:
                if elem.get('譲渡状況') == 'お見合い中です':
                    i += 1
            return i
        elif filter == 'decided':
            for elem in self.cats_arr:
                if elem.get('譲渡状況') == '飼い主さんが決まりました！':
                    i += 1
            return i



# 文章作成クラス
class CreateSentens(SaitamaCats):
    def __init__(self,area):
        super().__init__(area)
        self.SENT_1 = '現在、埼玉県の{.area_jp}地区では{.}匹の猫が飼い主を募集しています'
        self.SENT_2 = '【今日の埼玉県<1>の譲渡用猫情報】\n募集中          : <2> 匹\nお見合い中      : <3> 匹\n飼い主さん決定  : <4> 匹\n<5>'
        self.area_jp = self.transrate()
    
    
    def transrate(self):
        if SaitamaCats.area == 'nw':
            jp = '北部・西部'
        elif SaitamaCats.area == 'se':
            jp = '南部・東部'
        return jp

    
    # 文章作成1
    def create_1(self):
        # print(super().count_cats())
        sent = self.SENT_1.replace('<1>',self.area_jp).replace('<2>',str(super().count_cats()))
        return sent


    # 文章作成2
    def create_2(self):
        sent = self.SENT_2.replace('<1>',self.area_jp)
        return sent


# 単体で実行したときの処理
if __name__ == '__main__':
    # print(CreateSentens('n').create_1())
    print (SaitamaCats('s').count_cats('interview'))
    pass