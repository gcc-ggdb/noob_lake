# check this! https://hackmd.io/tK7FClDLQISwugAt_eXWqQ
# python web scrapping prac1 : Get Naver Music Chart (Top100)
# reference : https://rednooby.tistory.com/106

import requests
from bs4 import BeautifulSoup

url = 'https://music.naver.com/listen/top100.nhn?domain=TOTAL&duration=1d' # 네이버 뮤직 TOP 100 주소
source = requests.get(url).text # html 코드 text 형식으로 가져오기
#print(source)

soup = BeautifulSoup(source, 'html.parser') # 인스턴스 생성
#ranking_list = soup.select('.ranking span[class^=num]') # ranking 가져오기. 사실상 의미 없으니까 지우자
title_list = soup.select('.name span[class*=ellipsis]') # name 태그 중 ellipsis로 시작하는 태그 내용 찾아오기
#artist_list = soup.select('._artist span[class*=ellipsis]') # 아티스트 명 가져오기

f = open('result.txt', 'w')

for i in range(0, len(title_list)):
    f.write("%d위\t" %(i + 1))
    f.write(title_list[i].text.strip())
    #f.write('\t')
    #f.write(artist_list[i].text.strip())
    f.write('\n')
f.close()