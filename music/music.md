### 네이버뮤직차트 크롤링하기

호수의 과제인 인스타 크롤링에 앞서 크롤링에 주로 사용되는 bs4에 대한 감은 가지고 있어야 해서 과제 이전에 연습용으로 진행하게 된 내용

https://rednooby.tistory.com/106
위 사이트를 통해서 연습을 진행하였으며, 완전히 똑같이 하는 것은 별로 도움이 될 것 같지 않아 네이버뮤직차트로 주제를 정하고 진행

```
# check this! https://hackmd.io/tK7FClDLQISwugAt_eXWqQ
# python web scrapping prac1 : Get Naver Music Chart (Top100)
# reference : https://rednooby.tistory.com/106

import requests
from bs4 import BeautifulSoup

url = 'https://music.naver.com/listen/top100.nhn?domain=TOTAL&duration=1d'
source = requests.get(url).text
#print(source)
f = open('source.txt', 'w')
f.write(source)
f.close()
```

다음과 같이 코드를 짜면 네이버 뮤직차트의 html 코드가 얻어질 것이다. 크롬에서 페이지 소스 보기를 했다고 생각하면 된다.

우리는 이런식의 코드는 필요 없다. 저 중에서 차트에 해당되는 값만 빼 와서 출력할 수 있게하면 된다.![](https://i.imgur.com/ZTw0xgk.png)


그렇다면 소스코드 중에서 규칙성을 찾아 노래 제목만 파싱해오면 된다.

![](https://i.imgur.com/pBWmsQo.png)
다 필요없고 아이유의 Blueming을 검색해보자

![](https://i.imgur.com/3CumAWk.png)
우리가 활용할 값은 다음과 같다. 곡 제목 이 들어있는
```
<a href="#30813511" class="_title title NPI=a:track,r:2,i:30813511"  title="Blueming" ><span class="ellipsis">Blueming</span></a>
```
이 부분을 활용한다.

```
<a href="#30790789" class="_title title NPI=a:track,r:3,i:30790789"  title="Into the Unknown" ><span class="ellipsis">Into the Unknown</span></a>
```
3위 곡인 겨울왕국 OST이다. 위 두 값을 비교하면, 어떤 값이 공통적으로 발견되고, 어떤 값이 차이를 보이는지 알 수 있다.

1. 제목
2. r: 순위
3. #, i: 곡 고유번호

위 3개 항목은 곡마다 다른 값을 나타내게될 것이며, 저 값들 외의 것은 동일하단 점을 이용하면 파싱이 쉬울 것이다.

그 외에도 소스코드를 잘 봐보면, 순위, 변동사항, 곡 제목, 아티스트, 앨범 명 등을 볼 수 있다.

순위변동은 필요 없고, 순위/곡 제목/아티스트 이 순으로 크롤링을 해보자.

![](https://i.imgur.com/2niKsVd.png)

일단 우리가 뽑을 값이 어디에 존재하는지 알아야한다. Blueming 노래를 검색해보면 
table 중에서 "name"이라는 클래스 명을 가진 클래스에 우리가 찾고자 하는 문자열이 들어있다. 

```
soup = BeautifulSoup(source, 'html.parser') # 인스턴스 생성
title = soup.select('.name') # name 클래스 내용 다 긁어오기
```
맨 윗 코드에 해당 라인들을 추가하면 된다. 이 코드들은 html코드에서 name 명을 가진 클래스 값들을 다 긁어오게 된다.

![](https://i.imgur.com/reaadZj.png)

저런 느낌으로 진짜 name 클래스 것들은 다 가져와버린다. 맨 위 내용은 우리가 원하던게 아니지만...

이제 저 result 값 중에서도 우리가 원하는 값을 다시 뽑아내보자

- tag[attr]: attr속성이 정의된 모든 Tag
- tag[attr="bar"]: attr속성이 "bar"문자열과 일치하는 모든 Tag
- tag[attr*="bar"]: attr속성이 "bar"문자열과 부분 매칭되는 모든 Tag
- tag[attr^="bar"]: attr속성이 "bar"문자열로 시작되는 모든 Tag
- tag[attr$="bar"]: attr속성이 "bar"문자열로 끝나는 모든 Tag

- tag#tag_id: id가 tag_id인 모든 Tag
- tag.tag_class: 클래스명 중에 tag_class가 포함된 모든 Tag
- tag#tag_id.tag_cls1.tag_cls2
id가 tag_id이고, 클래스명중에 tag_cls1과 tag_cls2가 모두 포함된 Tag
-tag.tag_cls1.tag_cls2
클래스명 중에 tag_cls1과 tag_cls2가 포함된 모든 Tag
-tag.tag_cls1 .tag_cls2
클래스명 중에 tag_cls1이 포함된 Tag의 자식중(직계아니여도됨) 클래스 명에 tag_cls2가 포함된 모든 Tag

이 css selector를 사용해서 해보자

```
title = soup.select('.name a[class^=_title]')
```
코드를 다음과 같이 수정하면 우리가 찾고 있었던 문자열들을 찾을 수 있다.

![](https://i.imgur.com/FYW9ckU.png)
기모링~

저기서 알 수 있는건 랭킹과 곡명뿐이다.
일단 저걸 이쁘게 정리해보고, 그 다음에 앨범명과 아티스트 명을 추가해보자

```
# check this! https://hackmd.io/tK7FClDLQISwugAt_eXWqQ
# python web scrapping prac1 : Get Naver Music Chart (Top100)
# reference : https://rednooby.tistory.com/106

import requests
from bs4 import BeautifulSoup

url = 'https://music.naver.com/listen/top100.nhn?domain=TOTAL&duration=1d' # 네이버 뮤직 TOP 100 주소
source = requests.get(url).text # html 코드 text 형식으로 가져오기
#print(source)

soup = BeautifulSoup(source, 'html.parser') # 인스턴스 생성
title_list = soup.select('.name span[class*=ellipsis]') # name 태그 중 ellipsis로 시작하는 태그 내용 찾아오기

for title in title_list:
    print(title.text)
```

생각이 좀 바뀌었다.
```
<a href="#30790789" class="_title title NPI=a:track,r:3,i:30790789"  title="Into the Unknown" ><span class="ellipsis">Into the Unknown</span></a>
```
저기서 잘 보면 곡 제목은 span class=ellipsis에 들어있는 걸 알 수 있다. 랭킹과 아티스트도 다른 태그에 잘 들어 있다. 그러면 여기서는 제목만 쉽게 가져오고 다른 정보들도 다른 태그에서 잘 가져오는게 더 편하고 깔끔할 것 같다.

생각보다 변수가 많았다.
![](https://i.imgur.com/dEfiX6I.png)
저런식으로 여러 아티스트가 한 앨범에 참여한 경우, span 태그에 들어있는게 아니라 아예 따로 빠져있어서 연관시켜서 가져오는데에 어려움이 있었다. 또한 앨범도, 따로 차트에 앨범명이 명시되어 있는게 아니라, 앨범 사진에 주석마냥 달려있어서 가져오기가 어려웠다. 그래서 그냥 순위랑  곡명만 가져옴.... ㅈㅅ

```
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

f = open('result3.txt', 'w')

for i in range(0, len(title_list)):
    f.write("%d위\t" %(i + 1))
    f.write(title_list[i].text.strip())
    #f.write('\t')
    #f.write(artist_list[i].text.strip())
    f.write('\n')
f.close()
```

아 그리고 top100이긴한데 50위 까지만 가져왔음 ㅎㅎ