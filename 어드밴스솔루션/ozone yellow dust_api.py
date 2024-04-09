import requests

# 오존황사 발생정보 조회
url_base = 'http://apis.data.go.kr/B552584/OzYlwsndOccrrncInforInqireSvc/getOzAdvsryOccrrncInfo'
url = url_base 
api_key_utf8 = '%2FjEMJvdXRrLVtFtwr%2BU8UCwlaDibJ70XI3tSO1WAiv2aNo%2BJgK7wpWlQOc7J4zh70e41x%2FQREMkSqHIJDzq9nw%3D%3D'
api_key_decode = requests.utils.unquote(api_key_utf8, encoding='utf-8')

# 연도로 검색
params = {
    'serviceKey' : api_key_decode,
    'returnType' : 'xml',
    'numOfRows' : 100,
    'pangeNo' : 1,
    'year' : 2023
}
response = requests.get(url, params=params)
print(response)
print(response.text)
print(response.content.decode(encoding='utf-8')) # response의 내용을 디코딩하여 문자열로 변환하고 출력하는 작업을 수행


# beautifulsoup을 통해 xml 형식의 문자열을 파싱 (파서는 lxml 사용)
from bs4 import BeautifulSoup

xml = BeautifulSoup(response.text, 'lxml')
type(xml)
xml.find('header')


# 필요한 라이브러리 선언
import pandas as pd

# 문자열을 처리하는 함수
def convert_string(item_, key_):
    try:
        return item.find(key_.lower()).text.strip() # _key를 소문자로 변환하여 검색하고 찾은 값에 양쪽의 공백을 제거한 후 반환
    except AttributeError: # item에서 key_를 찾을 수 없는 경우 AttributeError 발생
        return None
    
items = xml.findAll('item') # xml 문서에서 모든 item 요소 찾기
item_list = [] #item 요소들을 저장할 목적의 빈 리스트 생성

for item in items:
    # item 요소에서 필요한 정보를 추출해 해당 정보의 키와 값을 가진 딕셔너리 item_dict를 만듦
    # convert_string() 함수를 호출하여 각 요소에서 필요한 정보를 추출하고, 해당 키에 맞게 딕셔너리에 저장
    item_dict = {
        '발령일': convert_string(item, 'dataDate'),
        '지역명' : convert_string(item, 'districtName'),
        '권역명' : convert_string(item, 'moveName'),
        '발령시간' : convert_string(item, 'issueTime'),
        '발령농도' : convert_string(item, 'issueVal'),
        '해제시간' : convert_string(item, 'clearTime'),
        '해제농도' : convert_string(item, 'clearVal'),
        '최고농도' : convert_string(item, 'maxVal'),
        '발령단계' : convert_string(item, 'issueLvl')
    }
    item_list.append(item_dict) # 만들어진 item_dict를 item_list에 추가
df = pd.DataFrame(item_list) # item_list에 저장된 dict을 이용하여 데이터 프레임 생성

df.to_excel(excel_writer="./ozone yellow dust.xlsx") # 데이터 프레임을 엑셀 파일로 저장
