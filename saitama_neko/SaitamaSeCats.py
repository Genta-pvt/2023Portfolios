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


def create_catlist():
    # 変数定義
    # labels = {'num':'','att':'','date':'','kind':'','sex':'','color':'','age':'','other':'','contact':''}
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


def send_mail():
    # 定数初期化
    SERVER ='smtp.gmail.com'
    FROM = 'zopopop0140@gmail.com'
    TO = 'zopopop0140@gmail.com'
    PASS = 'odfivqnnquytcxlr'

    # メール作成
    mail = MIMEText(create_catlist())
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
    print(create_catlist())
    # send_mail()