from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
from math import ceil 

def show_valueList(list_num):
    list_num = int(list_num)
    url = "https://www.transfermarkt.com/"

    headers = {'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}
    player_list=[]
    
    # url의 page 부분을 변수로 처리하여 반복문 실행
    for i in range(1, ceil(list_num/25)+1):
        url = f"https://www.transfermarkt.com/spieler-statistik/wertvollstespieler/marktwertetop?ajax=yw1&page={i}"

        r = requests.get(url, headers=headers)

        # BeautifulSoup()으로 웹페이지 분석하기
        soup = BeautifulSoup(r.text, 'html.parser')
        # 선수들의 정보가 담긴 태그와 클래스 찾기
        player_info = soup.find_all('tr', class_ = ['odd','even'])

        # player_info에서 'td' 태그만 모두 찾기
        for info in player_info:
            player = info.find_all("td")
        # 해당 정보를 찾아서 각 리스트에 추가하기
            number = player[0].text 
            name = player[3].text 
            position = player[4].text 
            age = player[5].text 
            nation = player[6].img['alt'] 
            team = player[7].img['alt'] 
            value = player[8].text.strip()
        # 데이터에서 숫자만 가져오기 (인덱싱)
            value = value[1:-1] # ex. €160.00m 에서 €이 [0]이고 m이 [-1] 
        
            player_list.append([number, name, position, age, nation, team, value])
    
        time.sleep(1)  # 1페이지 당 sleep
        
    # pd.DataFrame()으로 저장하기
    df = pd.DataFrame(player_list, 
        columns=['number', 'name', 'position', 'age', 'nation', 'team', 'value'])
    # df.drop(columns=['index'], inplace = True)

    return df[0:list_num] # 입력한 명 수만큼 인덱싱


if __name__ == "__main__":
    show_valueList(10).info()

