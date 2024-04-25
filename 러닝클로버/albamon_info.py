import requests
from bs4 import BeautifulSoup

# 인재정보가 게시된 페이지의 URL
url = 'https://www.albamon.com/human-resources/detail/21064286'

# 페이지에 접속하여 HTML 가져오기
response = requests.get(url)
html = response.text

# BeautifulSoup을 사용하여 HTML 파싱
soup = BeautifulSoup(html, 'html.parser')

# 인재정보를 담을 변수
introduction_text = ''

# 필요한 태그가 들어있는 변수 선언
introduction_div = soup.find('div', class_= 'resume-info__part')
if introduction_div:
    # 자기소개서 내용을 가져옵니다.
    introduction_text = introduction_div.get_text(strip=True)

# 가져온 자기소개서 출력
print("학력:")
print(introduction_text)



## 로그인 자동화 ##
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import pyperclip
from selenium.webdriver.chrome.options import Options


# 최신 셀레니움에서는 더 이상 크롬 드라이버가 필요치 않게되어 경로를 지정할 필요 없어짐
driver = webdriver.Chrome()
time.sleep(10)
driver.get('https://www.albamon.com/user-account/login?redirect_url=&memberType=PERSONAL')
# 'https://www.albamon.com/user-account/login?redirect_url=&memberType=PERSONAL'

# 로그인 자동화
while(True):

    try: 
        driver.find_element(By.CSS_SELECTOR,'#memberId') # 예외처리에 필요 이 구문이 없으면 아이디가 클립보드에 계속 복사됨
        time.sleep(3)  
        nid='wqe3' # 아이디 입력부분
        pyperclip.copy(nid)
        driver.find_element(By.CSS_SELECTOR,'#memberId').send_keys(Keys.CONTROL+'v')
        time.sleep(1)
        npw='angellim215@' # 비밀번호 입력 부분
        pyperclip.copy(npw)
        secure='blank'
        driver.find_element(By.CSS_SELECTOR,'#memberPassword').send_keys(Keys.CONTROL + 'v')
#         pyperclip.copy(secure) # 비밀번호 보안을위해 클립보드에 blank저장
        driver.find_element(By.XPATH,'//*[@id="__next"]').click()
        driver.get('https://www.albamon.com/user-account/login?redirect_url=&memberType=PERSONAL') # 알바몬 사이트로 이동
    
    except: 
        print("no such element") # 예외처리
