from tokenize import group
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
from math import ceil

def show_valueList(list_num, typeList):

    list_num = int(list_num)
    url = "https://www.transfermarkt.com/"

    headers = {'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}
    player_list=[]
    
    for i in range(1, ceil(list_num/25)+1):
        url = f"https://www.transfermarkt.com/spieler-statistik/wertvollstespieler/marktwertetop?ajax=yw1&page={i}"

        r = requests.get(url, headers=headers)

        soup = BeautifulSoup(r.text, 'html.parser')
        player_info = soup.find_all('tr', class_ = ['odd','even'])

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
    
    df = pd.DataFrame(player_list, 
        columns=['#', 'Player', 'Position', 'Age', 'Nat.', 'Club', 'Value'])
    # value 값 전처리
    df['Value'] = df['Value'].str.replace('€','')
    df['Value'] = df['Value'].str.replace('m','').astype('float')

    # 입력 조건에 따라 값 표시
    if not typeList:
    # checkbox 선택 하나도 없을 땐 값 표시 X
        df.drop(columns=['Value'], inplace=True)
    # index의 checkbox 데이터가 배열로 넘어옴
    else:
        for data in typeList:
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

    df = df[0:list_num]
    # 데이터프레임 변환
    group_data = df.groupby('Nat.').size().sort_values(ascending=False)
    group_data = group_data.reset_index()
    group_data.rename(columns={0:'Count'}, inplace=True)
    group_data.rename(columns={'Nat.':'Nation'}, inplace=True)

    # 데이터프레임 합치기
    result = pd.concat([df,group_data], axis=1)
    result.fillna(0, inplace=True)
    result = result.astype({'Count':'int'})
    # Nan -> 0 제거
    result.loc[result['Count'] == 0, 'Count'] = ''
    result.loc[result['Nation'] == 0, 'Nation'] = ''

    return result



if __name__ == "__main__":
    show_valueList(10, typeList=[])
    

