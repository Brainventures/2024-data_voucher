#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import pandas as pd
from bs4 import BeautifulSoup

# 제목 추출할 네이버 블로그 주소
url = 'https://blog.naver.com/PostView.naver?blogId=on2455&logNo=223402362339&categoryNo=13&parentCategoryNo=13&from=thumbnailList'
response = requests.get(url)
html = response.text

soup = BeautifulSoup(html, 'html.parser')

target_class = 'se-module se-module-text se-title-text'

titles = soup.find_all(class_= target_class)


# 엑셀 파일로 저장할 데이터를 담을 빈 리스트 선언
title_list = []

for title in titles:
    print(title.text)
    
df = pd.DataFrame(title_list, columns=['Titles'])

# 엑셀 파일로 저장
df.to_excel('./titles.xlsx', index=False)


# In[ ]:




