#!/usr/bin/env python
# coding: utf-8

# In[22]:


import requests

# 제주 대기 환경 정보 
url_base = 'http://air.jeju.go.kr/rest/JejuAirService/getJejuAirList/?date=20240417'
url = url_base 

params = {
    'authApiKey' : '100',
    'startPage' : '10',
    'date' : '8',
    'ver' : '1.1'
}
response = requests.get(url, params=params)


# In[23]:


print(response)


# In[24]:


print(response.text)


# In[25]:


print(response.content.decode(encoding='utf-8')) 


# In[26]:


from bs4 import BeautifulSoup

xml = BeautifulSoup(response.text, 'lxml')


# In[27]:


type(xml)


# In[28]:


xml.find('header')


# In[29]:


# 필요한 라이브러리 선언
import pandas as pd


# 문자열을 처리하는 함수
def convert_string(item_, key_):
    try:
        return item.find(key_.lower()).text.strip() # _key를 소문자로 변환하여 검색하고 찾은 값에 양쪽의 공백을 제거한 후 반환
    except AttributeError: # item에서 key_를 찾을 수 없는 경우 AttributeError 발생
        return None
    
items = xml.findAll('list') # xml 문서에서 모든 item 요소 찾기
item_list = [] #item 요소들을 저장할 목적의 빈 리스트 생성

for item in items:
    # item 요소에서 필요한 정보를 추출해 해당 정보의 키와 값을 가진 딕셔너리 item_dict를 만듦
    # convert_string() 함수를 호출하여 각 요소에서 필요한 정보를 추출하고, 해당 키에 맞게 딕셔너리에 저장
    item_dict = {
        '측정소': convert_string(list, 'SITE'),
        '측정시간' : convert_string(list, 'DT10'),
        'PM10' : convert_string(list, 'PM10'),
        'PM10 지수' : convert_string(list, 'PM10_CAI'),
        'PM25' : convert_string(list,'PM25'),
        'PM25 지수': convert_string(list, 'PM25_CAI'),
        '풍향 상태값' : convert_string(list, 'SWD'),
        '풍향' : convert_string(list, 'WD'),
        '풍속 상태' : convert_string(list, 'SWS'),
        '풍속' : convert_string(list, 'WS')
    }
    item_list.append(item_dict) # 만들어진 item_dict를 item_list에 추가
df = pd.DataFrame(item_list) # item_list에 저장된 dict을 이용하여 데이터 프레임 생성

df.to_excel(excel_writer="./jeju_info.xlsx") # 데이터 프레임을 엑셀 파일로 저장


# In[ ]:




