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
    url_list = [] # 크롤링된 url을 저장할 빈 리스트 선언

    for page in range(1, 11): # 링커리어 자소서 페이지는 638페이지 정도 되는데 테스트 하려고 범위를 10까지로 지정
        url = f"https://linkareer.com/cover-letter/search?page={page}&tab=all" # 각 페이지에 대한 url을 생성
        driver.get(url) # url을 driver.get 메서드를 이용해 브라우저에 로

        try:
            # 10초간 대기하면서 페이지의 특정 요소가 로드될 때까지 기다림
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//a[contains(@href, 'cover-letter') and not(contains(@href, 'search'))]")))
            # 'cover-letter'를 포함하고 'search'를 포함하지 않는 링크 요소 찾기
            url_tags = driver.find_elements(By.XPATH, "//a[contains(@href, 'cover-letter') and not(contains(@href, 'search'))]")

            for tag in url_tags:
                url_name = tag.get_attribute('href') # 각 링크 요소에서 'href' 속성을 가져옴
                url_list.append(url_name) # 가져온 url을 url_list에 추가가

        except Exception as e: # 예외처리
            print(f"Error occurred while crawling: {e}") # 예외가 발생하면 콘솔에 출력

    return url_list # 크롤링 완료되면 url_list를 반환


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
def save_to_excel(data, filename='./self_introductions.xlsx'):
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
