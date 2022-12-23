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


# SaitamaCats クラス 埼玉県の猫譲渡情報ページの情報をまとめる・分析するみたいな役割
class SaitamaCats:
    def __init__(self,area):
        self.area = area
        self.bs4_page = self.import_page()


    # メソッド "import_page" 指定した区域(「北部・西部」or「南部・東部」)のbs4オブジェクトを作る
    # 戻り値：引数に対応するWebページのbs4オブジェクト
    def import_page(self):
        # 定数
        NORTHEAST_SET = {'northeast','NorthEast','Northeast','ne','NE','north','North','n','N'}
        SOUTHWEST_SET = {'southwest','SouthWest','Southwest','sw','SW','south','South','s','S'}
        URL_NE = 'https://www.pref.saitama.lg.jp/b0716/joutoseineko-n.html'
        URL_SW = 'https://www.pref.saitama.lg.jp/b0716/joutoseineko-s.html'

        # URLからbs4オブジェクトを作成(SaitamaCats.areaも設定)
        try:
            # 指定エリア(self.area)が北部・西部のとき
            if self.area in NORTHEAST_SET:
                # 値を丸める
                SaitamaCats.area ='ne'
                # repupests実行
                r = requests.get(URL_NE)
            # 指定エリア(self.area)が南部・東部のとき
            elif self.area in SOUTHWEST_SET:
                # 値を丸める
                SaitamaCats.area ='sw'
                # repupests実行
                r = requests.get(URL_SW)
            # 指定エリアが(self.area)が不正な値のとき(例外)
            else:
                raise Exception('invaild par')
        # 例外処理
        except Exception:
            print('plz input "ne" or "sw".')
        # 例外発生しないとき requestsで取得したデータをbs4オブジェクトに変換
        else:
            soup = BeautifulSoup(r.content,'html.parser')
            print(SaitamaCats.area) # テスト用出力
            return soup


    # 作成中メソッド レビュー不要です
    def extract_data(self):
        pass
        # main_contents : 
        main_contents = self.bs4_page.find('div',attrs={"id" : "tmp_contents" })
        # for table in main_contents

        table_pointer = main_contents.find('table')
        table_desc1 = table_pointer.previous_sibling.previous_sibling
        table1 = table_pointer

        table_pointer = table_pointer.find_next_sibling('table')
        table_desc2 = table_pointer.previous_sibling.previous_sibling
        table2 = table_pointer

        print(table1)
        print(table2)
        # tables = main_contents.find_all('tbody')
        # neko_ippikime = self.bs4_page.




# 未使用クラス レビュー不要
class ImportCatData:
    def create_catlist():
        # 変数定義
        cats_data = []  # すべての猫(<table>)のデータ
        each_table = []  # <table>タグ内のデータを一時的に格納
        # HTMLデータの取得
        r = requests.get('https://www.pref.saitama.lg.jp/b0716/joutoseineko-s.html')
        soup = BeautifulSoup(r.content,'html.parser')

        # 猫のデータを配列に格納
        # すべての<table>(猫情報)で繰り返し
        for t in soup.find_all('table'):
            # すべての<tr>(列)で繰り返し
            for tr in t.find_all('tr'):
                # データ行(2行目)の<td>(セル)のデータをeach_valueに代入
                each_value = tr.find_all('td')[1]
                # each_valueに<p>タグがある時(セル内改行があるとき)
                if x := each_value.find_all('p'):
                    # セル内行をそれぞれstrにしてパッキング。それをeach_tableに追記(空白のセル内行を除く)
                    each_table.append([y.text for y in x if not re.fullmatch(r'[\s]+',y.text)])
                # セル内改行がないとき
                else:
                    # テキストをeach_tableに追記
                    each_table.append(each_value.text.replace('\n',''))
            # cats_dataにeach_tableの内容を追記
            cats_data.append(each_table[:])
            # each_tableを初期化
            each_table.clear()
        # 実行時の日付 + 実行時に何匹里親募集状態の猫がいるかのstrを戻り値に
        message = datetime.date.today().strftime('%Y年%m月%d日') + ' 現在、埼玉県南部・東部地区では' + f'{len(cats_data):2}' + '匹の猫が里親を募集しています'
        return message

# 未使用関数 レビュー不要
def send_mail():
    # 定数初期化
    SERVER ='smtp.gmail.com'
    FROM = 'zopopop0140@gmail.com'
    TO = 'zopopop0140@gmail.com'
    PASS = 'odfivqnnquytcxlr'

    # メール作成
    mail = MIMEText('hoge')
    mail['Subject'] = '本日の埼玉県南部・東部地区における猫の里親募集状況です'
    mail['From'] = FROM
    mail['To'] = TO

    # メール送信
    with smtplib.SMTP(SERVER,587) as smtp:
        smtp.ehlo()
        try:
            smtp.starttls()
            smtp.ehlo
        except smtplib.SMTPNotSupportedError:
            pass
        smtp.login('zopopop0140','mblqqixlbsfgveid')
        smtp.sendmail(FROM, TO, mail.as_string)

# 単体で実行したときの処理
if __name__ == '__main__':
    pass
    hoku_tou = SaitamaCats('ne').extract_data()
    # nan_sei = SaitamaCats('sw')
    # urawa = SaitamaCats('urawa')
    # hoku_tou.extract_data()