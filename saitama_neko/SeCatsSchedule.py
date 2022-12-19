# ファイル名 : se_cats_schedule.py
# 機能概要 : 定期的にSaitamaSeCats.py.pyを実行する

# ライブラリ、モジュールをインポート
import schedule  # スケジュール
import time  # 時刻
import SaitamaSeCats  # SaitamaSeCats.py

# 実行時刻
run_time = '12:00'
# スケジュール設定 毎日run_timeになったら
schedule.every().day.at(run_time).do(SaitamaSeCats.py.create_catlist)
# スケジュールスタート
while True:
    schedule.run_pending()
    time.sleep(30)