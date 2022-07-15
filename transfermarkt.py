from tokenize import group
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
from math import ceil

# 포지션 별로 다른 url 크롤링   
pos_dict = {'AL':"alle",'GK':"Torwart",'DF':"Abwehr",'MF':"Mittelfeld",'FW':"Sturm"}

def show_valueList(list_num, typeList, position):
    list_num = int(list_num)
    url = "https://www.transfermarkt.com/"

    headers = {'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}
    player_list=[]
    # pos_dict value 값 저장
    pos_value = pos_dict.get(position)

    for i in range(1, ceil(list_num/25)+1):
        url = f'https://www.transfermarkt.com/spieler-statistik/wertvollstespieler/marktwertetop/plus/ajax/yw1/ausrichtung/{pos_value}/spielerposition_id/alle/altersklasse/alle/jahrgang/0/land_id/0/kontinent_id/0/yt0/Show/0//page/{i}'

        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')

        # 마지막 페이지에서 limit 설정
        if i == ceil(list_num/25):
            limit_count = list_num % 25 # 마지막 페이지의 남은 개수
            player_info = soup.find_all('tr', class_ = ['odd','even'], limit = limit_count )
        else :
            player_info = soup.find_all('tr', class_ = ['odd','even'])

        # 함수 만들기
        for info in player_info:
            player = info.find_all("td")
            number = player[0].text 
            name = player[3].text 
            position = player[4].text
            age = player[5].text 
            nation = player[6].img['alt'] 
            team = player[7].img['alt'] 
            value = player[8].text.strip()
            player_list.append([number, name, position, age, nation, team, value])

        time.sleep(1)
    
    # 크롤링 끝
    df = pd.DataFrame(player_list, 
        columns=['', 'Player', 'Position', 'Age', 'Nat.', 'Club', 'Value'])


    df['Value'] = df['Value'].str.replace('€','')
    df['Value'] = df['Value'].str.replace('m','').astype('float')

    if not typeList:
        df.drop(columns=['Value'], inplace=True)
    else:
        for data in typeList:
            # 함수 만들기
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
        df.drop(columns=['Value'], inplace=True)

    
    # 데이터프레임 내용 수정
    # 함수 만들기
    group_data = df.groupby('Nat.').size().sort_values(ascending=False)
    group_data = group_data.reset_index()

    group_data.rename(columns={0:'Count'}, inplace=True)
    group_data.rename(columns={'Nat.':'Nation'}, inplace=True)

    result = pd.concat([df,group_data], axis=1)
    result.fillna(0, inplace=True)
    result = result.astype({'Count':'int'})

    result.loc[result['Count'] == 0, 'Count'] = ''
    result.loc[result['Nation'] == 0, 'Nation'] = ''

    return result

if __name__ == "__main__":
    show_valueList(230, ['USD'], "AL")    

