#!/usr/bin/env python
# coding: utf-8

# In[16]:


import requests
from bs4 import BeautifulSoup
from bs4 import Comment
from PIL import Image
import re
import os
import pandas as pd


# 블로그에서 게시물의 내용을 추출하는 함수 
def extract_naverBlog(url):

    response = requests.get(url) # 주어진 url을 이용하여 웹페이지의 내용을 가져옴
    soup = BeautifulSoup(response.text, 'html.parser') # html 코드를 파싱
    ifra = soup.find('iframe', id='mainFrame') # 블로그의 내용이 포함된 iframe을 가리키는 것
    post_url = 'https://blog.naver.com' + ifra['src'] # 실제 게시물의 주소는 iframe의 src 속성에 포함
    #print(post_url)

    res = requests.get(post_url) # 해당 게시물의 내용을 가져옴
    soup2 = BeautifulSoup(res.text, 'html.parser') # html 코드를 파싱

    # 제목 추출
    titles = soup2.find_all('div', {'class': re.compile('^se-module se-module-text se-title-tex.*')})
    post_title = titles[0].text # titles 리스트의 첫 번째 요소에서 텍스트 내용을 추출 후 저장
    post_title = post_title.replace('\n', '') # 게시물 제목 개행 문자 제거

    special_char = '\/:*?"<>|.' 
    for c in special_char:
        if c in post_title:
            post_title = post_title.replace(c, '')  # 특수 문자 제거

    # 저장 폴더 만들기
    dir_names = post_title.replace(' ', '').replace('\n', '') # 제목에서 공백과 개행 문자를 제거하여 폴더 이름을 생성
    if not os.path.exists('./naverBlog'):# 경로에 해당하는 폴더가 없다면
        os.mkdir('./naverBlog') # 폴더 생성
    else:  
        pass
    if not os.path.exists('naverBlog/' + dir_names): # 경로에 있는 폴더 중에서 dir_names와 동일한 이름의 폴더가 있다면
        os.makedirs('./naverBlog/' + dir_names) # dir_names와 같은 이름의 폴더를 생성
    else:
        pass

    post_dir_name = './naverBlog/' + dir_names

    # 본문 내용을 html 타입으로 저장
    # script 등 태그 제거
    [x.extract() for x in soup2.find_all('script')] # HTML에서 모든 'script' 태그를 찾아서 제거
    [x.extract() for x in soup2.find_all('style')] # HTML에서 모든 'style' 태그를 찾아서 제거
    [x.extract() for x in soup2.find_all('meta')] # HTML에서 모든 'meta' 태그를 찾아서 제거
    [x.extract() for x in soup2.find_all('noscript')] # HTML에서 모든 'noscript' 태그를 찾아서 제거
    [x.extract() for x in soup2.find_all(text=lambda text:isinstance(text, Comment))] # HTML에서 주석을 모두 찾아서 제거            

    html = soup2.prettify("utf-8") # prettify() 메서드를 사용하여 HTML을 예쁘게 출력
    html_filename = post_title.replace('\n', '') + '.html' # 게시물의 제목에서 개행 문자(\n)를 제거하고, '.html' 확장자를 붙여서 HTML 파일의 이름을 생성
    with open(post_dir_name + '/' + html_filename, 'wb') as f: # 게시물의 내용을 저장할 HTML 파일 열기
        f.write(html)

    # 페이지 내용(텍스트) 추출
    contents = '' # 추출한 텍스트 내용을 저장할 빈 문자열 생성
    txt_contents = soup2.find_all('div', {'class': re.compile('^se-module se-module-tex.*')}) # 'div' 요소 찾기
    for p_span in txt_contents: # 찾은 모든 요소들에 대해 반복
        for txt in p_span.find_all('span'): # 각 요소 안에서 모든 'span' 요소 찾기
            #print(txt.get_text() + '\n')
            contents += txt.get_text() + '\n' # 'span' 요소에서 텍스트를 추출하여 contents 문자열에 추가

    txt_filename = post_title.replace('\n', '') + '.txt' # 게시물의 제목에서 개행 문자 제거 후, 'txt'확장자 붙여서 텍스트 파일의 이름을 생성
    with open(post_dir_name + '/' + txt_filename, 'w', encoding='utf-8') as f: # 추출한 텍스트 내용을 저장할 텍스트 파일 열기
        f.write(contents)   

    # 이미지 추출
    imgs = soup2.find_all('img', class_='se-image-resource') # se-image-resource인 모든 'img' 태그 찾기
    # print(len(imgs))
    # print(imgs)
    cnt = 1
    for img in imgs: # 찾은 모든 이미지에 대해 반복
        # <img src=  가 아닌  data-lazy-src=  부분을 가져와야 큰 이미지임
        #print(img.get('data-lazy-src'))  # img['data-lazy-src']
        img_url = img.get('data-lazy-src') # 각 이미지의 data-lazy-src 속성을 가져와서 이미지의 url을 추출
        ## pillow.Image로 이미지 format 알아내기
        imageObj = Image.open(requests.get(img_url, stream=True).raw) # PIL의 Image 모듈을 사용하여 이미지의 파일 형식 알아내기
        img_format = imageObj.format # 이미지의 파일 형식을 알아내 img_format 변수에 저장                  
        res_img = requests.get(img_url).content # 이미지의 url을 사용하여 requests 모듈을 이용해 이미지
        if img_format: # 이미지 파일이 존재한다면
            img_name = str(cnt) + '.' + img_format # 이미지 파일의 이름을 순서와 파일 형식을 조합하여 생성
        else:
            img_name = str(cnt) + '.jpg'

        #print(img_name)
        # 블로그에서 이미지를 표시할 때 일부 이미지가 없는 경우가 있어 이를 필터링하기 위한 조건
        if len(res_img) > 100:  # 이미지 용량이 100 bytes 이상인지 확인
            with open(post_dir_name + '/' + img_name, 'wb') as f: # 이미지를 저장할 파일 열기
                f.write(res_img)
            cnt += 1 # 이미지 파일의 이름에 순서를 부여
    
    # 제목과 내용을 데이터프레임으로 저장
    data = {'제목': [post_title], '내용': [contents]} 
    df = pd.DataFrame(data) # 딕셔너리를 데이터 프레임으로 변환
    
    # 엑셀 파일로 저장
    excel_filename = post_title.replace('\n', '') + '.xlsx' # 엑셀 파일의 이름 생성. 개행 문자 제거하고, 확장자로 '.xlsx' 추가하여 생성
    excel_filepath = post_dir_name + '/' + excel_filename # 엑셀 파일의 저장 경로 생성
    df.to_excel(excel_writer=excel_filepath, index=False) # 데이터 프레임을 엑셀 파일로 저장
            
# 추출할 url 주소
url = 'https://blog.naver.com/on2455/223406867437'
extract_naverBlog(url)


# In[ ]:




