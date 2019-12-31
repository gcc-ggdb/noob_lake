# Download image from google
# https://hackmd.io/FigSIXSZSSOj70Z_s-w5sA?both

import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen

keyword = "백지헌" # 검색할 거 넣으면 됨. 귀여운 백지헌 한 번씩 보고 가세요
base_url = "https://www.google.co.kr/search?q="
for_image = "&tbm=isch"

url = base_url + keyword + for_image # 고양이 검색했을 때 페이지
source = requests.get(url).text

soup = BeautifulSoup(source, 'html.parser')
img_data = soup.find_all("img") #img 태그를 가진 것들 다 가져오기

#html 코드 저장용
#f = open('source.txt', 'w')
#f.write(source)
#f.close()

#img 태그 값 저장용
#f = open('result.txt', 'w')
#f.write(str(img_data))
#f.close()

for i in enumerate(img_data):
    download_this = i[1].attrs['src'] # i는 딕셔너리, 속성이 src인 값만 뽑아올거임
    if download_this[0] != "/" : # 뽑아온 url 값에 대해서 필터링
        img_url = urlopen(download_this).read() # 이미지 url
        with open(str(i[0])+'.jpg', 'wb') as f:
            f.write(img_url)