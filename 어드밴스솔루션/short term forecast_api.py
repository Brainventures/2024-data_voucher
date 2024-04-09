#!/usr/bin/env python
# coding: utf-8

# In[3]:


import requests

# 기상청_단기예보 조회
url_base = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'
url = url_base 
api_key_utf8 = 'D5v8NPs87kaeUioo2TfiZzJaPeE4mwxyzbDv9UXl1gRRvudDM2I3%2B1Pj1PV2Luz9ZG5NRlub6UYoN%2F5a%2BCuPLQ%3D%3D'
api_key_decode = requests.utils.unquote(api_key_utf8, encoding='utf-8')

# 오늘 날짜로 검색
search_date = '2024-04-04',
params = {
    'serviceKey' : api_key_decode,
    'pageNo' : 1,
    'numOfRows': 1000,
    'dateType' : 'xml',
    'base_date' : 20240404,
    'base_time' : '0600',
    'nx' : 55,
    'ny' : 127
}
response = requests.get(url, params=params)


# In[4]:


print(response)


# In[5]:


print(response.text)


# In[6]:


print(response.content.decode(encoding='utf-8')) # response의 내용을 디코딩하여 문자열로 변환하고 출력하는 작업을 수행


# In[7]:


# beautifulsoup을 통해 xml 형식의 문자열을 파싱 (파서는 lxml 사용)
from bs4 import BeautifulSoup

xml = BeautifulSoup(response.text, 'lxml')


# In[8]:


type(xml)


# In[9]:


xml.find('header')


# In[10]:


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
        '발표일자': convert_string(item, 'baseDate'),
        '발표시각' : convert_string(item, 'baseTime'),
        '예보지점 X좌표' : convert_string(item, 'nx'),
        '예보지점 Y좌표' : convert_string(item, 'ny'),
        '자료구분코드' : convert_string(item, 'category'),
        '실황 값': convert_string(item, 'obsrValue')
    }
    item_list.append(item_dict) # 만들어진 item_dict를 item_list에 추가
df = pd.DataFrame(item_list) # item_list에 저장된 dict을 이용하여 데이터 프레임 생성

df.to_excel(excel_writer="./short term forecast.xlsx") # 데이터 프레임을 엑셀 파일로 저장


# In[ ]:




