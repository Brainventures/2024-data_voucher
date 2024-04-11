#!/usr/bin/env python
# coding: utf-8

# In[2]:


pip install requests


# In[3]:


pip install pandas


# In[1]:


import requests

# 대기오염정보 조회
url_base = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc'
url_spec = 'getMinuDustFrcstDspth'
url = url_base + '/' + url_spec
api_key_utf8 = 'D5v8NPs87kaeUioo2TfiZzJaPeE4mwxyzbDv9UXl1gRRvudDM2I3%2B1Pj1PV2Luz9ZG5NRlub6UYoN%2F5a%2BCuPLQ%3D%3D'
api_key_decode = requests.utils.unquote(api_key_utf8, encoding='utf-8')

# 오늘 날짜로 검색
search_date = '2024-04-04',
params = {
    'serviceKey' : api_key_decode,
    'returnType' : 'xml',
    'searchDate' : search_date,
    'ver' : '1.1'
}
response = requests.get(url, params=params)


# In[2]:


print(response)


# In[3]:


print(response.text)


# In[4]:


print(response.content.decode(encoding='utf-8')) # response의 내용을 디코딩하여 문자열로 변환하고 출력하는 작업을 수행


# In[5]:


# beautifulsoup을 통해 xml 형식의 문자열을 파싱 (파서는 lxml 사용)
from bs4 import BeautifulSoup

xml = BeautifulSoup(response.text, 'lxml')


# In[6]:


type(xml)


# In[7]:


xml.find('header')


# In[8]:


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
        '통보 시간': convert_string(item, 'dataTime'),
        '통보 코드' : convert_string(item, 'informCode'),
        '예보 개황' : convert_string(item, 'infromOverall'),
        '발생 원인' : convert_string(item, 'informCause'),
        '예보 등급' : convert_string(item, 'informGrade'),
        '행동 요령' : convert_string(item, 'actionKnack'),
        '첨부 파일명1': convert_string(item, 'imageUrl1'),
        '첨부 파일명2': convert_string(item, 'imageUrl2'),
        '첨부 파일명3': convert_string(item, 'imageUrl3'),
        '첨부 파일명4': convert_string(item, 'imageUrl4'),
        '첨부 파일명5': convert_string(item, 'imageUrl5'),
        '첨부 파일명6': convert_string(item, 'imageUrl6'),
        '첨부 파일명7': convert_string(item, 'imageUrl7'),
        '첨부 파일명8': convert_string(item, 'imageUrl8'),
        '첨부 파일명9': convert_string(item, 'imageUrl9'),
        '예측 통보 시간': convert_string(item, 'informData')
    }
    item_list.append(item_dict) # 만들어진 item_dict를 item_list에 추가
df = pd.DataFrame(item_list) # item_list에 저장된 dict을 이용하여 데이터 프레임 생성

df.to_excel(excel_writer="./air_info.xlsx") # 데이터 프레임을 엑셀 파일로 저장


# In[9]:


df.iloc[0]


# In[ ]:




