# 인스타 크롤링

이거 참고하세여

https://hackmd.io/@H9a0IrQ5QL6VVWhA0jE8_Q/Sk8AOCpCr

길게 쓸거 없다. 일단 유저피드를 잘 가져와서 내가 원하는 값을 가져올 수 있는지 확인해보자

```
# https://hackmd.io/FXPqj77JR16UpCy0hirm0g

insta = 'https://www.instagram.com/'
user_name = 'fromis9jiheon' # change this
get_feed = '?__a=1'

query_hash = '/graphql/query/?query_hash=e769aa130647d2354c40ea6a439bfc08'
variables = '&variables='
first = '"first":50,' # get 50 posts

url = insta + user_name + get_feed
source = requests.get(url).text # get code

j_source = json.loads(source)
get_graphql = j_source['graphql']
get_user = get_graphql['user']
user_id = str(get_user['id']) # this is user id
down = get_user['display_url']

print(down)
```

중간중간 필요없는 것들이 껴 있긴 하지만, 위 코드로 실행하면 원하는 값을 가져올 수 있다.
그러면 json을 올바르게 가져왔다는 뜻이니, 페이지를 하나하나 뜯어보면서 어떤 값들을 가져오고, 어떻게 사용해야할 지 알아보자

json parser로 정리한 다음에 보면, 대부분의 사진은

![](https://i.imgur.com/4hchJx4.png)
저런식으로  display_url 값에 해당한다. 그런데 여기에는 첫번째 사진들밖에 없다. 그래서 확인해봤는데, 상단에 있는 shortcode값을 이용해서 해당 페이지에 들어가면 이후의 사진들도 얻을 수 있다.

https://www.instagram.com/p/B68XhLkAFg7/

이 상태에서 뒤에 ?__a=1 을 붙여준다면 해당 json 코드 안에 사진들이 들어있는 것을 볼 수 있다.

일단 알아둬야할 것은 다음과 같다. 동영상과 사진을 구분하는 법은 __typename값으로 구분할 수 있다.
사진의 경우  GraphImage
동영상의 경우 GraphVideo로 나타난다.

GraphSidecar 같은 경우, 여러 사진이 있는 경우로, shortcode를 활용하면 모든 사진을 볼 수 있다.

www.instagram.com/p/shortcode/?__a=1
이렇게

![](https://i.imgur.com/7HiDwLp.png)
위에 첫번째 node에는 첫번째 사진에 대한 정보가 들어있고, 두번째 node에는 두번째 사진에 대한 정보가 들어있다.

이제 대충 구상이 끝났다.

일단 유저 피드에서 필요한 값들을 긁어온 후, 사진들에 대한 정보를 가져온다. 이때 __typename을 활용한다. 이후 display_url 값을 가져와서 type에 맞게 자료를 저장한다.

위 과정대로 구현하면서 생긴 문제로는 최초의 유저 피드 json 코드값이랑, 이후에 end_cursor를 활용했을 때 json 코드 값이랑 일부 코드가 다르다. 그래서 그 점을 예외처리 해야했다.

다른점은 graphql 이 data로 바뀐거랑 그 윗부분이 없다는 점?
![](https://i.imgur.com/IMGDlmr.png)

이사진은 초기 피드



```
# https://hackmd.io/FXPqj77JR16UpCy0hirm0g

import requests, os
import json
from urllib.request import urlopen

def loop_insta_page(input_url):
    num = 0
    end_cursor = ""
    source2 = requests.get(input_url).text # get code
    j_source2 = json.loads(source2)

    try:
        get_first = j_source2['graphql']
    except BaseException:
        get_first = j_source2['data'] 

    get_user = get_first['user']
    get_edge_owner_to_timeline_media = get_user['edge_owner_to_timeline_media']
    get_page_info = get_edge_owner_to_timeline_media['page_info']
    end_cursor = get_page_info['end_cursor']
    has_next_page = get_page_info['has_next_page']

    get_edges = get_edge_owner_to_timeline_media['edges'] # type(get_edges) == list
    
    for nodes in get_edges :
        node = nodes['node'] # disply_url, typename in this key
        shortcode = node['shortcode']
        
        hidden_url = insta + "/p/" + shortcode + get_feed # get hidden pic/vid
        hidden_source = requests.get(hidden_url).text
        j_tmp = json.loads(hidden_source)
        get_graphql2 = j_tmp['graphql']
        get_shortcode_media = get_graphql2['shortcode_media']
    
        if get_shortcode_media['__typename'] == "GraphSidecar" :
            get_edge_sidecar_to_children = get_shortcode_media['edge_sidecar_to_children']
            get_edges2 = get_edge_sidecar_to_children['edges']
        
            for nodes2 in get_edges2 :
                node2 = nodes2['node']
                typename = node2['__typename']
                num += 1
            
                if typename == "GraphVideo" :
                    download_func(str(node2['video_url']), ".mp4", shortcode + str(num))
                else :
                    download_func(str(node2['display_url']), ".jpg", shortcode + str(num))
        
        else :
            if get_shortcode_media['__typename'] == "GraphImage" :
                download_func(str(get_shortcode_media['display_url']), ".jpg", shortcode)
            else :
                download_func(str(get_shortcode_media['video_url']), ".mp4", shortcode)
          
    global url
    url = insta + query_hash + variables + '{"id":"' + user_id + '",' + first + '"after":"' + end_cursor + '"}'
    
def download_func(download_this, type_of_file, short):
    download_url = urlopen(download_this).read()
    with open(directory + '/' + str(short) + type_of_file, 'wb') as f:
            f.write(download_url)
            print(str(short) + type_of_file)

if __name__ == '__main__' :
    
    global insta
    global query_hash
    global variables
    global first
    global user_id
    global has_next_page
    global directory
    
    insta = 'https://www.instagram.com/'
    user_name = '' 
    get_feed = '?__a=1'
    query_hash = 'graphql/query/?query_hash=e769aa130647d2354c40ea6a439bfc08'
    variables = '&variables='
    first = '"first":12,' # get 12 posts
    
    user_id = ""
    url = ""
    has_next_page = True
    
    directory = os.getcwd() + '/download'
    os.makedirs(directory)
    
    user_name = input("Enter the user name : ")
    
    url = insta + user_name + get_feed
    source = requests.get(url).text # get code

    j_source = json.loads(source)

    get_first = j_source['graphql']

    get_user = get_first['user']
    user_id = str(get_user['id']) # this is user id

    get_edge_owner_to_timeline_media = get_user['edge_owner_to_timeline_media']
    count = get_edge_owner_to_timeline_media['count'] # this is count
    
    print("USER ID : %s" %user_id)
    print("POSTS : %s" %count)
    
    print("Downloading..")
    
    while has_next_page == True:
        loop_insta_page(url)
        
    print("Done!")
```

제대로 코드를 다듬은 게 아니라서 효율적으로 굴러가는지는 따져보지 않았다.
굴러가면 그만 ㅎㅎ

+)게시물 수가 적은 계정으로 테스트 해봤는데, 마지막 페이지에서 end_cursor가 값이 들어있지 않은 상태에서 변수를 지정해 오류로 프로그램이 종료되는 현상이 있었다.
이거 예외처리 해줌