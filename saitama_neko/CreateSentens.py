import SaitamaSeCats
from datetime import datetime

# 文章作成クラス
class CreateSentens(SaitamaSeCats.SaitamaCats):
    def __init__(self,area):
        super().__init__(area)
        self.SENT_1 = '現在、埼玉県の{}地区では{}匹の猫が飼い主を募集しています'
        self.SENT_2 = '【{}】\n今日の埼玉県{}地区の譲渡用猫情報\n募集中          : {} 匹\nお見合い中      : {} 匹\n飼い主さん決定  : {} 匹\n{}'
        self.area_jp = self.transrate()
    
    
    def transrate(self):
        if self.area == 'nw':
            jp = '北部・西部'
        elif self.area == 'se':
            jp = '南部・東部'
        return jp

    def gen_date(self):
        now = datetime.now()
        date = now.strftime("%Y/%m/%d")
        return date

    
    # 文章作成1
    def sentens_1(self):
        super().count_cats()
        sent = self.SENT_1.format(self.area_jp,self.cats_count_all)
        return sent


    # 文章作成2
    def sentens_2(self):
        for filter in ['wanted', 'interview', 'decided']:
            super().count_cats(filter)
        sent = self.SENT_2.format(self.gen_date(),self.area_jp,self.cats_count_wanted,self.cats_count_interview,self.cats_count_decided,self.url)
        return sent

# 単体で実行したときの処理
if __name__ == '__main__':
    # print(CreateSentens('n').sentens_1())
    # print(SaitamaCats('n').url)
    print (CreateSentens('n').sentens_2())
    pass