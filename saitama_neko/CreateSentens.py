"""
ファイル名 : CreateSentens.py
■概要
埼玉県の譲渡用猫状況ページの情報を説明する短文(Tweet用)を生成するためのモジュールです。
"""
import SaitamaSeCats
from datetime import datetime

# 文章作成クラス
class CreateSentens(SaitamaSeCats.SaitamaCats):
    """
    埼玉県の譲渡用猫状況ページの情報を説明する短文(Tweet用)を生成するクラス
    """
    def __init__(self, area):
        """
        処理
            "nw"なら「北部・西部」 (https://www.pref.saitama.lg.jp/b0716/joutoseineko-n.html)
            "se"なら「南部・東部」 (https://www.pref.saitama.lg.jp/b0716/joutoseineko-s.html)
            の情報で初期化
        引数
        ・area(string)
            "nw", "se"のいずれかの文字列を指定
        """
        super().__init__(area)
        self.SENT_1 = '現在、埼玉県の{}地区では{}匹の猫が飼い主を募集しています'
        self.SENT_2 = '【{}】\n今日の埼玉県{}地区の譲渡用猫情報\n募集中          : {} 匹\nお見合い中      : {} 匹\n飼い主さん決定  : {} 匹\n{}'
        self.area_jp = self.transrate()
    
    def transrate(self):
        """
        処理
            "self.area"の値を日本語に翻訳
        戻り値
            '北部・西部' or '南部・東部' (string)
        """
        if self.area == 'nw':
            jp = '北部・西部'
        elif self.area == 'se':
            jp = '南部・東部'
        return jp

    def gen_date(self):
        """
        処理
            "Y/M/D"の形式で日付の文字列を生成
        戻り値
            "202x/xx/xx" (string)
        """
        now = datetime.now()
        date = now.strftime("%Y/%m/%d")
        return date

    # 文章作成1
    def sentens_1(self):
        """
        処理
            "self.SENT_1"を"SaitamaCats"クラスのデータ属性を利用してフォーマット
        戻り値
            現在、埼玉県のxxx地区では... (string)
        """
        super().count_cats()
        sent = self.SENT_1.format(self.area_jp, self.cats_count_all)
        return sent

    # 文章作成2
    def sentens_2(self):
        """
        処理
            "self.SENT_2"を"SaitamaCats"クラスのデータ属性を利用してフォーマット
        戻り値
            '''
            【20xx/xx/xx】
            今日の埼玉県xxxx地区の譲渡用猫情報
            募集中 ....
            お見合い中 ...
            飼い主さん決定 ...
            '''(string)
        """
        for filter in ['wanted', 'interview', 'decided']:
            super().count_cats(filter)
        sent = self.SENT_2.format(self.gen_date(), self.area_jp, self.cats_count_wanted, self.cats_count_interview, self.cats_count_decided, self.url)
        return sent



# 単体で実行したときの処理
if __name__ == '__main__':
    # print(CreateSentens('n').sentens_1())
    # print(SaitamaCats('n').url)
    print (CreateSentens('n').sentens_2())
    pass