#!/usr/bin/env python3 
#Beautiful Soup 익히기 (시카고 샌드위치 맛집 분석)
from bs4 import BeautifulSoup

#html페이지 읽기
page = open("03. test_first.html", 'r').read()
soup = BeautifulSoup(page, 'html.parser')

#읽은 html페이지의 내용 출력
print(soup.prettify())

#children옵션 soup변수에서 한 단계 아래에서 포함된 태그들 표시
print(list(soup.children))

#html태그에 접속
html = list(soup.children)[2]
print(html)
print(list(html.children))

#body태그에 접속
body = list(html.children)[3]
print(body)

#바로 body태크에 접속
#print('=================================================')
print(soup.body)

#find(하나만 찾을때), find_all(모두 찾을때) 명령으로 특정 태그 접근
print(soup.find_all('p'))
print('=================================================')
print(soup.find('p'))

#p태그의 class가 'outer-text'인 것 찾기
print('=================================================')
print(soup.find_all('p', class_='outer-text'))

#class이름으로 찾기
print('=================================================')
print(soup.find_all(class_='outer-text'))

#id로 찾기
print('=================================================')
print(soup.find_all(id="first"))

#next_sibling를 이용하여 다음 태그만 찾을 수 있다
print('=================================================')
print(soup.head)
print('=================================================')
print(soup.head.next_sibling)
print('=================================================')
print(soup.head.next_sibling.next_sibling)

#body태그의 p태그 접근
print(body.p)
print('=================================================')
print(body.p.next_sibling.next_sibling)

#get_text() 명령으로 태그 안에 있는 텍스트만 추출
for each_tag in soup.find_all('p'):
    print(each_tag.get_text())

#body전체에서 텍스트 추출
print('=================================================')
print(body.get_text())

#하이퍼링크인 a태그 추출
links = soup.find_all('a')
print(links)
#href 속성을 찾아서 링크 주소를 추출
for each in links:
    href = each['href']
    text = each.string
    print(text + ' -> ' + href)

#금융정보 추출
from urllib.request import urlopen
url = "https://finance.naver.com/marketindex/"
page = urlopen(url)

soup = BeautifulSoup(page, "html.parser")
print('=================================================')
print(soup.prettify())
print('=================================================')
print(soup.find_all('span', 'value')[0].string)

