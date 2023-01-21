"""
ファイル名 : RunSchedule.py
■概要
処理を定期実行するためのモジュールです
"""
# ライブラリ、モジュールをインポート
import schedule  # スケジュール
import time  # 時刻
import TwitterClient
from CreateSentens import CreateSentens


def day_task():
    """
    処理
        譲渡用猫情報の各ページ(北西部、南東部)の情報をまとめたツイートをする
    """
    area_list = ['nw', 'se']
    for area in area_list:
        TwitterClient.tweet(CreateSentens(area).sentens_2())


def start_schedule(run_time='09:00'):
    schedule.every().day.at(run_time).do(day_task)
    print('')
    # スケジュールスタート
    while True:
        schedule.run_pending()
        print('Schedule in progress...')
        time.sleep(30)


TwitterClient.test_tweet()
input_time = input('Runtime? [hh:mm] : ')
start_schedule(input_time)
