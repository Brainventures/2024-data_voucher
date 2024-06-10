한국환경공단 에어코리아 OpenAPI
기상청 단기예보 OpenAPI





import requests

# 대기오염통계 현황
url_base = 'http://apis.data.go.kr/B552584/ArpltnStatsSvc/getMsrstnAcctoRDyrg'
url = url_base 
api_key_utf8 = '%2FjEMJvdXRrLVtFtwr%2BU8UCwlaDibJ70XI3tSO1WAiv2aNo%2BJgK7wpWlQOc7J4zh70e41x%2FQREMkSqHIJDzq9nw%3D%3D'
api_key_decode = requests.utils.unquote(api_key_utf8, encoding='utf-8')

# 3월로 검색
params = {
    'serviceKey' : api_key_decode,
    'returnType' : 'xml',
    'numOfRows' : 100,
    'pageNo' : 1,
    'inqBginDt' : 20240301,
    'inqEndDt' : 20240331,
    'msrstnName' : '강남구'
#     'ver' : '1.1'
}
response = requests.get(url, params=params)
print(response)
print(response.text)


# beautifulsoup을 통해 xml 형식의 문자열을 파싱 (파서는 lxml 사용)
from bs4 import BeautifulSoup

xml = BeautifulSoup(response.text, 'lxml')
type(xml)
xml.find('header')


# 필요한 라이브러리 선언
import pandas as pd
from bs4 import BeautifulSoup
from xml.dom.minidom import Document


# 문자열을 처리하는 함수
def convert_string(item_, key_):
    try:
        return item.find(key_.lower()).text.strip() # _key를 소문자로 변환하여 검색하고 찾은 값에 양쪽의 공백을 제거한 후 반환
    except AttributeError: # item에서 key_를 찾을 수 없는 경우 AttributeError 발생
        return None
    
xml_content = response.content
soup = BeautifulSoup(xml_content, 'xml')
items = xml.findAll('item') # xml 문서에서 모든 item 요소 찾기
item_list = [] #item 요소들을 저장할 목적의 빈 리스트 생성

for item in items:
    # item 요소에서 필요한 정보를 추출해 해당 정보의 키와 값을 가진 딕셔너리 item_dict를 만듦
    # convert_string() 함수를 호출하여 각 요소에서 필요한 정보를 추출하고, 해당 키에 맞게 딕셔너리에 저장
    item_dict = {
        '측정일': convert_string(item, 'msurDt'),
        '측정소명' : convert_string(item, 'msrstnName'),
        '아황산가스 평균농도' : convert_string(item, 'so2Value'),
        '일산화탄소 평균농도' : convert_string(item, 'co2Value'),
        '오존 평균농도' : convert_string(item, 'o3Value'),
        '이산화질소 평균농도' : convert_string(item, 'no2Value'),
        '미세먼지 평균농도' : convert_string(item, 'pm10Value'),
        '초미세먼지 평균농도' : convert_string(item, 'pm25Value')
    }
    item_list.append(item_dict) # 만들어진 item_dict를 item_list에 추가
df = pd.DataFrame(item_list) # item_list에 저장된 dict을 이용하여 데이터 프레임 생성

df.to_excel(excel_writer="./air pollution statistics.xlsx") # 데이터 프레임을 엑셀 파일로 저장
