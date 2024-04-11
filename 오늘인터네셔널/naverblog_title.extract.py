#!/usr/bin/env python
# coding: utf-8

# In[2]:


import requests
import pandas as pd
from bs4 import BeautifulSoup

# 제목 추출할 네이버 블로그 주소
url = 'https://blog.naver.com/PostView.naver?blogId=on2455&logNo=223402362339&categoryNo=13&parentCategoryNo=13&from=thumbnailList'
response = requests.get(url)
html = response.text

soup = BeautifulSoup(html, 'html.parser')

target_class = 'se-module se-module-text se-title-text'

titles = soup.find_all(class_=target_class)

# 제목을 담을 리스트 초기화
title_list = []

for title in titles:
    title_text = title.get_text(strip=True)  # 텍스트 추출 및 공백 제거
    title_list.append(title_text)

# 데이터프레임 생성
df = pd.DataFrame({'Titles': title_list})

# 엑셀 파일로 저장
df.to_excel('./titles.xlsx', index=False)


# In[ ]:




