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
    user_name = 'fromis9jiheon' # change this
    get_feed = '?__a=1'
    query_hash = 'graphql/query/?query_hash=e769aa130647d2354c40ea6a439bfc08'
    variables = '&variables='
    first = '"first":12,' # get 12 posts
    
    user_id = ""
    url = ""
    has_next_page = True
    
    directory = os.getcwd() + '/download'
    os.makedirs(directory)
    
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