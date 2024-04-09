#!/usr/bin/env python
# coding: utf-8

# In[37]:


import requests

# # 미세먼지 경보 발령 현황 
url_base = 'http://apis.data.go.kr/B552584/UlfptcaAlarmInqireSvc/getUlfptcaAlarmInfo'
url = url_base 
api_key_utf8 = '%2FjEMJvdXRrLVtFtwr%2BU8UCwlaDibJ70XI3tSO1WAiv2aNo%2BJgK7wpWlQOc7J4zh70e41x%2FQREMkSqHIJDzq9nw%3D%3D'
api_key_decode = requests.utils.unquote(api_key_utf8, encoding='utf-8')

# 2023년도로 검색
# search_date = '2024-04-04',
params = {
    'serviceKey' : api_key_decode,
    'returnType' : 'xml',
    'numOfRows' : 100,
    'pageNo' : 1,
    'year' : 2023,
    'itemCode' : 'PM10',
#     'ver' : '1.1'
}
response = requests.get(url, params=params)


# In[38]:


print(response)


# In[39]:


print(response.text)


# In[40]:


print(response.content.decode(encoding='utf-8')) 


# In[41]:


# beautifulsoup을 통해 xml 형식의 문자열을 파싱 (파서는 lxml 사용)
from bs4 import BeautifulSoup

xml = BeautifulSoup(response.text, 'lxml')


# In[42]:


type(xml)


# In[43]:


xml.find('header')


# In[45]:


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
        '일련번호': convert_string(item, 'sn'),
        '발령일' : convert_string(item, 'dateDate'),
        '지역명' : convert_string(item, 'districtName'),
        '권역명' : convert_string(item, 'moveName'),
        '항목명' : convert_string(item, 'itemCode'),
        '경보단계': convert_string(item, 'issueGbn'),
        '발령일' : convert_string(item, 'issueDate'),
        '발령시간' : convert_string(item, 'issueTime'),
        '발령농도' : convert_string(item, 'issueVal'),
        '해제일' : convert_string(item, 'clearDate'),
        '해제시간' : convert_string(item, 'clearTime'),
        '해제농도' : convert_string(item, 'clearVal')
    }
    item_list.append(item_dict) # 만들어진 item_dict를 item_list에 추가
df = pd.DataFrame(item_list) # item_list에 저장된 dict을 이용하여 데이터 프레임 생성

df.to_excel(excel_writer="./fine dust.xlsx") # 데이터 프레임을 엑셀 파일로 저장


# In[ ]:




