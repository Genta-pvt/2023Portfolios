import smtplib
from email.mime.text import MIMEText  # メール作成

# 変数初期化
SERVER ='smtp.gmail.com'
FROM = 'zopopop0140@gmail.com'
TO = 'zopopop0140@gmail.com'
PASS = 'odfivqnnquytcxlr'

# メール作成
mail = MIMEText('test')
mail['Subject'] = '本日の埼玉県南部・東部地区における猫の里親募集状況です'
mail['From'] = FROM
mail['To'] = TO

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()