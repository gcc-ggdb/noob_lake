import requests
import json

url = '''https://www.instagram.com/graphql/query/?query_hash=e769aa130647d2354c40ea6a439bfc08&variables={%22id%22:%225760757115%22,%22first%22:12,%22after%22:%22QVFBdmR1c2FxajdPZDE2YXpqR1pxaHQ4WS1HcXZyWjc3Q2EwaTV3amp0enZWa2tXTHR2VHBZTm9Vc3RtcTdmOUJPejlVekJ6TEVHdTBVOER5bWVvREQ1WQ==%22}'''
source = requests.get(url).text

j_source = json.loads(source)

try:
    print(j_source['graphql'])
except BaseException:
    print(j_source['data'])