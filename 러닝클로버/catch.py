from bs4 import BeautifulSoup
import requests

url = 'https://www.catch.co.kr/JobN/CoverLetter/PassCoverLetter/GoUBtkDDINum-BIWWmEyoA2'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
print(soup)
soup.find_all('p')
soup.find_all('p', attrs={'class': 'univ'})
soup.find_all('p', attrs={'class': 'spec'})

# p 태그의 class에 해당하는 텍스트 가져오기
p_tags = soup.find_all('p', class_=True)
for p in p_tags:
    print(p.text)

# html_code = """
# <p class="corp"><span class="pic"><img alt="농협은행" src="https://board.jinhak.com/BoardV1/Upload/Job/Company/CI/H80827.jpg"/></span></p>,
# <p class="q">농협은행</p>,
# <p class="ctg mt5"><span>2022 상반기</span> <span class="nobar">일반</span></p>,
# <p class="ctg2">영업/고객상담 (일반영업)</p>,
# <p class="stit">합격스펙</p>,
# <p class="univ">서울과학기술대학교 / 영어영문학과 (3.58/4.5)</p>,
# <p class="spec"><span class="bar"><b>어학</b> <em>없음</em></span> <span class="bar"><b>자격증</b> <em>없음</em></span> <span class="bar"><b>수상내역</b> <em>없음</em></span> <span class="bar"><b>인턴/대외활동</b> <em>없음</em></span> <span class="bar"><b>경력</b> <em>없음</em></span></p>,
# <p class="spec"><span class="bar"><b>지원/합격내역</b> <em><b>1</b>개 기업 지원,<b class="ml5">1</b>개 기업 서류 합격,<b class="ml5">100%</b> 서류합격률<!-- --></em></span></p>
# """
# soup = BeautifulSoup(html_code, 'html.parser')

# # p 태그의 class에 해당하는 텍스트 가져오기
p_tags = soup.find_all('p', class_=True)
for p in p_tags:
    print(p.text)


