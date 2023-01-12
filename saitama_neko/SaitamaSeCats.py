"""
ファイル名 : SaitamaSeCats.py
■概要
埼玉県のホームページ内の譲渡用猫情報ページ
・https://www.pref.saitama.lg.jp/b0716/joutoseineko-n.html
・https://www.pref.saitama.lg.jp/b0716/joutoseineko-s.html
の内容を取り扱うモジュールです

■注意
本プログラム内に記載されているURL
「https://www.pref.saitama.lg.jp/b0716/joutoseineko-n.html」「https://www.pref.saitama.lg.jp/b0716/joutoseineko-s.html」
は埼玉県のホームページであり、このURL上に公開されている記事、写真、図画、その他データ類の著作権は、埼玉県、またはその情報提供者に帰属します。
"""
# ライブラリをインポート
import requests  # HTML取得
import re  # 正規表現
from bs4 import BeautifulSoup   # HTML解析

class AreaCodeError(Exception):
    """
    [例外クラス]SaitamaCatsの引数が不正な時に呼び出されます
    """
    pass



class SaitamaCats:
    """
    譲渡用猫ページの情報を取り扱うクラス
    """
    def __init__(self,area):
        """
        処理
            "nw"なら「北部・西部」 (https://www.pref.saitama.lg.jp/b0716/joutoseineko-n.html)
            "se"なら「南部・東部」 (https://www.pref.saitama.lg.jp/b0716/joutoseineko-s.html)
            の情報で初期化
        引数
        ・area(string)
            "nw", "se"のいずれかの文字列を指定
        """
        self.area = area
        self.bs4_page = self.import_page()
        self.cats_arr = self.extract_data()
        self.cats_count_all = 0
        self.cats_count_wanted = 0
        self.cats_count_interview = 0
        self.cats_count_decided = 0

    def import_page(self):
        """
        処理
            "self.area"の値に対応するbs4オブジェクトを取得する
        戻り値
            "self.area"の値に対応するbs4オブジェクト
        """
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

    def extract_data(self):
        """
        処理
            "self.bs4_page"(譲渡用猫情報のbs4オブジェクト)に対して以下の処理を行う
            ・猫の情報が記載されている<table>要素と譲渡状況(etc."お見合い中です！")を辞書形式にまとめる {見出し1: 値1, 見出し2: 値2, ...}
            ・辞書形式に変換した<table>要素をリストに格納 [{}, {}, ...]
        戻り値
            (リスト) [{見出し1: 値1, 見出し2: 値2, ...}, {}, ...]
        """
        # テーブルを登録する配列(戻り値) 
        arr = []
        # インポートしたデータからページの主となる部分を抽出
        main_contents = self.bs4_page.find('div',attrs={"id" : "tmp_contents"})
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

    def count_cats(self,filter = 'all'):
        """
        処理
            引数で指定した譲渡状況の猫の数を数える
        引数
            ・filter(string)
                'all', 'wanted', 'interview', 'decided' から指定。
                ・all
                    譲渡状況にかかわらずすべての猫をカウント(デフォルト値)
                ・wanted
                    譲渡状況の記載がない(飼い主募集中)の猫をカウント
                ・interview
                    譲渡状況が「お見合い中です」の猫をカウント
                ・decided
                    譲渡状況が「飼い主さんが決まりました！」の猫をカウント
        """

        def count(value):
            """
            処理
                self.cats_arr内にいくつ引数で指定した譲渡状況の猫がいるか数える
            引数
                ・value(string)
                    譲渡状況を指定
                    etc.('お見合い中です', '飼い主さんが決まりました！')
            戻り値
                引数で指定した譲渡状況の猫の数 (int)
            """
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