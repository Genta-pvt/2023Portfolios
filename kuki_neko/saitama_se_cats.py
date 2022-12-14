from bs4 import BeautifulSoup
import requests
import re
import datetime
from email.mime.text import MIMEText
import smtplib

def CreateCatlist():
    r = requests.get('https://www.pref.saitama.lg.jp/b0716/joutoseineko-s.html')
    tables = []
    cat_data =[]
    labels = {'num':'','att':'','date':'','kind':'','sex':'','color':'','age':'','other':'','contact':''}
    soup = BeautifulSoup(r.content,'html.parser')

    for t in soup.find_all('table'):
        for tr in t.find_all('tr'):
            td1 = tr.find_all('td')[1]
            if x:=td1.find_all('p'):
                cat_data.append([y.text for y in x if not re.fullmatch(r'[\s]+',y.text)])
            else:
                cat_data.append(td1.text.replace('\n',''))
        tables.append(cat_data[:])
        cat_data.clear()
    message = datetime.date.today().strftime('%Y年%m月%d日') + ' 現在、埼玉県南部・東部地区では' + f'{len(tables):2}' + '匹の猫が里親を募集しています'
    # print(message)
    return(message)

def send_mail():
    SERVER ='smtp.gmail.com'
    FROM = 'zopopop0140@gmail.com'
    TO = 'zopopop0140@gmail.com'
    PASS = 'utptcjkhdaucrgtk'

    mail = MIMEText(CreateCatlist())
    mail['Subject'] = '本日の埼玉県南部・東部地区における猫の里親募集状況です'
    mail['From'] = FROM
    mail['To'] = TO

    with smtplib.SMTP(SERVER,587) as smtp:
        smtp.ehlo()
        try:
            smtp.starttls()
            smtp.ehlo
        except smtplib.SMTPNotSupportedError:
            pass
        smtp.login('zopopop0140@gmail.com','mblqqixlbsfgveid')
        smtp.sendmail(FROM, TO, mail.as_string)

if __name__ == '__main__':
    # print(CreateCatlist())
    send_mail()