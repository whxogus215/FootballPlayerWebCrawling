from glob import glob
from tokenize import group
from bs4 import BeautifulSoup
from numpy import sort
import requests
import pandas as pd
import time
from math import ceil

class transferCrawling:

    def __init__(self, list_num, typeList, pos,sort):
        # 포지션 별로 다른 url 크롤링  
        self.pos_dict = {'ALL':"alle",'GK':"Torwart",'DF':"Abwehr",'MF':"Mittelfeld",'FW':"Sturm"}
        # index.html에서 입력받는 값들
        self.list_num = list_num
        self.typeList = typeList
        self.pos = pos
        self.sort = sort

    # 웹 크롤링
    def show_valueList(self):
        self.list_num = int(self.list_num)

        headers = {'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}

        player_list=[]

        # pos_dict value 값 저장
        pos_value = self.pos_dict.get(self.pos)

        for i in range(1, ceil(self.list_num/25)+1):
            url = f'https://www.transfermarkt.com/spieler-statistik/wertvollstespieler/marktwertetop/plus/ajax/yw1/ausrichtung/{pos_value}/spielerposition_id/alle/altersklasse/alle/jahrgang/0/land_id/0/kontinent_id/0/yt0/Show/0//page/{i}'

            r = requests.get(url, headers=headers)
            soup = BeautifulSoup(r.text, 'html.parser')

            # 마지막 페이지에서 limit 설정
            if i == ceil(self.list_num/25):
                limit_count = self.list_num % 25 # 마지막 페이지의 남은 개수
                player_info = soup.find_all('tr', class_ = ['odd','even'], limit = limit_count )
            else :
                player_info = soup.find_all('tr', class_ = ['odd','even'])

            for info in player_info:
                player = info.find_all("td")
                name = player[3].text 
                position = player[4].text
                age = player[5].text 
                nation = player[6].img['alt'] 
                team = player[7].img['alt'] 
                value = player[8].text.strip()
                player_list.append([name, position, age, nation, team, value])

            time.sleep(1) # 페이지 당 1초 씩 sleep (차단 방지)
        
        # 크롤링 끝
        global df
        df = pd.DataFrame(player_list, 
            columns=['Player', 'Position', 'Age', 'Nat.', 'Club', 'Value'])
        df.index+=1

        df['Value'] = df['Value'].str.replace('€','')
        df['Value'] = df['Value'].str.replace('m','').astype('float')

        if not self.typeList:
            df.drop(columns=['Value'], inplace=True)
        else:
            for data in self.typeList:
                self.data_prePro(data) # 데이터 전처리
            df.drop(columns=['Value'], inplace=True)
        self.sort_valueList()

        return df

    # 국가별 인원 수 처리
    def show_nationList(self):
        group_data = df.groupby('Nat.').size().sort_values(ascending=False)
        group_data = group_data.reset_index()

        group_data.rename(columns={0:'Count'}, inplace=True)
        group_data.rename(columns={'Nat.':'Nation'}, inplace=True)

        return group_data

    # dataframe 정렬
    def sort_valueList(self):
        if self.sort == "descending":
            df.sort_values(by='Age', ascending=False, inplace=True)
            df.reset_index(drop=True, inplace=True)
            df.index+=1
        elif self.sort == "ascending":
            df.sort_values(by='Age', ascending=True, inplace=True)
            df.reset_index(drop=True, inplace=True)
            df.index+=1

    # dataframe 열 개수
    def get_size(self):
        # dataframe의 열 개수 정수형으로 추출
        index_num = df.shape[0]
        return index_num

    # dataframe Value Column 전처리
    def data_prePro(self, data):
        if data == "USD":
            df['Value($)'] = df['Value']*1.01
            df['Value($)'] = df['Value($)'].round(3)
            df['Value($)'] = df['Value($)'].astype(str)+'M'
        elif data == "EUR":
            df['Value(€)'] = df['Value']
            df['Value(€)'] = df['Value(€)'].round(3)
            df['Value(€)'] = df['Value(€)'].astype(str)+'M'
        elif data == "KRW":
            df['Value(₩)'] = df['Value']*13
            df['Value(₩)'] = df['Value(₩)'].round(3)
            df['Value(₩)'] = df['Value(₩)'].astype(str)+'억'


    if __name__ == "__main__":
        show_valueList(230, ['USD'], "AL")    

