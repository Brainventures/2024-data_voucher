#!/usr/bin/env python
# coding: utf-8

# In[6]:


import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# 브라우저를 초기화하고 반환하는 함수
def initialize_browser():
    return webdriver.Chrome()


# 자기소개서 URL을 크롤링하여 반환하는 함수
def url_crawl(driver):
    url_list = []

    for page in range(1, 11):
        url = f"https://linkareer.com/cover-letter/search?page={page}&tab=all"
        driver.get(url)

        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//a[contains(@href, 'cover-letter') and not(contains(@href, 'search'))]")))
            url_tags = driver.find_elements(By.XPATH, "//a[contains(@href, 'cover-letter') and not(contains(@href, 'search'))]")

            for tag in url_tags:
                url_name = tag.get_attribute('href')
                url_list.append(url_name)

        except Exception as e:
            print(f"Error occurred while crawling: {e}")

    return url_list


# 개별 자기소개서의 정보를 추출하여 반환하는 함수
def extract_self_introduction(driver, url):
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//h1[contains(@class, 'ui') and contains(@class, 'header')]")))
        
        info = driver.find_element(By.XPATH, "//h1[contains(@class, 'ui') and contains(@class, 'header')]")
        specification = driver.find_element(By.XPATH, "//div[@class='ui basic segment']//h3")
        content = driver.find_element(By.ID, "coverLetterContent")
        
        info_list = info.text.split(' / ')
        
        person = {
            'company': info_list[0],
            'job': info_list[1],
            'year': info_list[2],
            'specification': specification.text,
            'self_intro': content.text
        }
        return person
    
    except Exception as e:
        print(f"Error occurred while extracting self introduction: {e}")
        return None
    
    
# 자기소개서 정보를 엑셀 파일로 저장하는 함수
def save_to_excel(data, filename='self_introductions.xlsx'):
    try:
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)
        print(f"Data saved to {filename} successfully.")
    except Exception as e:
        print(f"Error occurred while saving data to Excel: {e}")
    

# 메인 함수
def main():
    try:
        # 브라우저 초기화
        driver = initialize_browser()
        
        # URL 크롤링
        urls = url_crawl(driver)
        
        # 자기소개서 추출
        self_introductions = []
        for url in urls:
            intro = extract_self_introduction(driver, url)
            if intro:
                self_introductions.append(intro)
        
        # 추출된 자기소개서를 엑셀로 저장
        save_to_excel(self_introductions, filename='./self_introductions.xlsx')
        
    finally:
        # 브라우저 닫기
        driver.quit()

        
# 메인 함수 호출
if __name__ == "__main__":
    main()


# In[ ]:




