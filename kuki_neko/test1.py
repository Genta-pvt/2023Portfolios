from bs4 import BeautifulSoup
import requests
import re

def CreateCatlist(url):
    r = requests.get(url)
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
    return(tables)

south_cats = CreateCatlist('https://www.pref.saitama.lg.jp/b0716/joutoseineko-s.html')
print('現在、埼玉県南部・東部地区では',f'{len(south_cats):2}','匹の猫が里親を募集しています')