# 파이썬으로 파일 다운로드 하기

인스타 크롤링을 해서 사진을 다운받아 올 것이기 때문에, 연습용으로 구글 이미지에서 원하는 검색어를 입력했을 때 해당 이미지들을 다운받아오는 코드를 짜보자

우선 이미지 파일들이 있는 url 주소를 찾아내야한다.
```
https://www.google.co.kr/search?q=%EA%B3%A0%EC%96%91%EC%9D%B4&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjkr_jl0NzmAhWOv5QKHTWwB90Q_AUoAXoECA8QAw&biw=944&bih=947#imgrc=_
```
다음과 같이 괴랄한 주소가 나오는데, 이는
```
https://www.google.co.kr/search?q=고양이&tbm=isch
```
와 같은 주소이다 ㅎㅎ;
```
keyword = "고양이"
base_url = "https://www.google.co.kr/search?q="
for_image = "&tbm=isch"
url = base_url + keyword + for_image # 고양이 검색했을 때 페이지
```
기본 코드다.

이제 저 url에서 이미지들이 각각 어떤 값을 가지고 있는지에 대한 규칙을 찾아서 request이용해서 다운받기만 하면 된다.

![](https://i.imgur.com/jTa3fmS.png)
일단 해당 url을 통해서 html코드를 전부 받아왔다. 잘 찾아보면, img 태그에 사진의 제목과 원본 파일의 주소가 들어있는 것을 알 수 있다.

그럼 이제 html 코드에서 img 태그만 뜯어내보자

```
# Download image from google

import requests
from bs4 import BeautifulSoup

keyword = "고양이"
base_url = "https://www.google.co.kr/search?q="
for_image = "&tbm=isch"

url = base_url + keyword + for_image # 고양이 검색했을 때 페이지
source = requests.get(url).text

soup = BeautifulSoup(source, 'html.parser')
img_data = soup.find_all("img")

#f = open('source.txt', 'w')
#f.write(source)
#f.close()

f = open('result.txt', 'w')
f.write(str(img_data))
f.close()
```

![](https://i.imgur.com/hGvS1lA.png)
다음과 같이 img가 들어간 태그들을 그대로 가져왔다. 이제 해당 리스트에 대해서 각 요소마다 src 속성에 대한 값을 다운받게만 하면 된다.

```
# Download image from google

import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen

keyword = "고양이"
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
```

별 다른 설명이 필요없다. url 형식의 값에서 속성이 src인 값들만 뽑아서 따로 저장 한 후, 해당 url 파일을 저장하는 코드다.

일단 20개만 다운로드 되는데, 이후 자동으로 스크롤 내릴때마다 생기는 파일들을 다운받는 것은 다음에 구현하도록 하자