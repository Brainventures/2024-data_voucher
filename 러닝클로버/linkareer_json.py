#!/usr/bin/env python
# coding: utf-8

# In[4]:


import requests

req = requests.get('https://linkareer.com/cover-letter/32840?page=1&sort=PASSED_AT&tab=all')
req.text


# In[5]:


from bs4 import BeautifulSoup

soup = BeautifulSoup(req.content, 'html.parser')
print(soup)


# In[6]:


import json
import pandas as pd


# 주어진 JSON 데이터
json_data = """
{"scrapCount":4,"university":"인가경","major":"산업경영공학","grades":"3.64/4.5","languageScore":"토익: 805","career":"사회생활 경험: 중소기업유통센터","activity":null,"license":"한국사검 정시험: 고급, 컴퓨터활용능력: 1급, 기타: 정보처리기사,정보보안기사,CPPG,SQLD"}
"""

# JSON 데이터 파싱
data = json.loads(json_data)


# 필요한 정보 추출
organization_name = "NH농협은행"
role = "IT"
university = data.get("university", "")
major = data.get("major", "")
grades = data.get("grades", "")
language_score = data.get("languageScore", "")
career = data.get("career", "")
license = data.get("license", "")


# 추출한 정보를 DataFrame으로 변환
df = pd.DataFrame({
    "기업명": [organization_name],
    "직무": [role],
    "대학/학교": [university],
    "전공": [major],
    "학점": [grades],
    "어학 점수": [language_score],
    "사회생활 경험": [career],
    "자격증": [license]
})


# DataFrame을 엑셀 파일로 저장
filename = './self_introduction.xlsx'
try:
    df.to_excel(filename, index=False)
    print(f"Data saved to {filename} successfully.")
except Exception as e:
    print(f"Error occurred while saving data to Excel: {e}")


# In[ ]:




