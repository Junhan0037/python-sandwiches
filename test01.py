#!/usr/bin/env python3 
#시카고 샌드위치 맛집 분석
from bs4 import BeautifulSoup
from urllib.request import urlopen

url_base = 'https://www.chicagomag.com'
url_sub = '/Chicago-Magazine/November-2012/Best-Sandwiches-Chicago/'
url = url_base + url_sub

#html코드
html = urlopen(url)
soup = BeautifulSoup(html, "html.parser")
print(soup)

#태그 찾기
print('======================================================================')
print(soup.find_all('div', 'sammy'))
print('======================================================================')
print(len(soup.find_all('div', 'sammy')))   #맛집 50개인데 길이가 50 정확!
print('======================================================================')
print(soup.find_all('div', 'sammy')[0])

#원하는 데이터 추출
tmp_one = soup.find_all('div', 'sammy')[0]
#랭킹 추출
print(tmp_one.find(class_='sammyRank').get_text())
#메뉴, 가게 이름 추출
print(tmp_one.find(class_='sammyListing').get_text())
#하이퍼링크 주소 추출
print(tmp_one.find('a')['href'])

#정규식
import re
tmp_string = tmp_one.find(class_='sammyListing').get_text()

#메뉴, 가게 이름 분리 (split에서 OR연산자 사용가능!)
rank = []
main_menu = []
cafe_name = []
url_add = []
#태그 추출
list_soup = soup.find_all('div', 'sammy')
from urllib.parse import urljoin
for item in list_soup:
    #랭킹 추출
    rank.append(item.find(class_='sammyRank').get_text())
    #메뉴, 가게이름 추출하여 분리
    tmp_string = item.find(class_='sammyListing').get_text()
    main_menu.append(re.split('\n|\r\n', tmp_string)[0])
    cafe_name.append(re.split('\n|\r\n', tmp_string)[1])
    #상대경로를 절대경로로 변경 (앞에 url_base를 붙인다)
    url_add.append(urljoin(url_base, item.find('a')['href']))
print(rank[:5])
print(cafe_name[:5])
print(url_add[:5])
print(len(rank), len(main_menu), len(cafe_name), len(url_add))

#pandas로 변경 및 컬럼 순서 수정
import pandas as pd
data = {'Rank':rank, 'Menu':main_menu, 'Cafe':cafe_name, 'URL':url_add}
df = pd.DataFrame(data, columns=['Rank', 'Cafe', 'Menu', 'URL'])
print(df.head(5))
df.to_csv('03. best_sandwiches_list_chicago.csv', sep=',', encoding='utf-8')

df = pd.read_csv('03. best_sandwiches_list_chicago.csv', index_col=0)
print(df.head())

#1등 랭킹의 URL에서 p태그의 addy class 크롤링
html = urlopen(df['URL'][0])
soup_temp = BeautifulSoup(html, "html.parser")
price_tmp = soup_temp.find('p', 'addy').get_text()
print(price_tmp)

#가격 추출
print(price_tmp.split()[0])
#맨 뒤에 점(.)이 항상 붙어서 처리
print(price_tmp.split()[0][:-1])
#두 번째부터 맨 마지막에서 세 번째까지 선택하여 하나의 문장으로 출력 (join)
print(' '.join(price_tmp.split()[1:-2]))

'''
Jupter Notebook에서 상태 진행바를 쉽게 만들어주는 tqdm 모듈
cmd창에서 conda install -c conda-forge tqdm
'''

'''
from tqdm import tqdm_notebook

price = []
address = []
#가격, 주소 추출
#spyder에서는 지원이 안됨. for n in tqdm_notebook(df.index):
for n in df.index:
    html = urlopen(df['URL'][n])
    soup_temp = BeautifulSoup(html, 'lxml')
    gettings = soup_temp.find('p', 'addy').get_text()
    price.append(gettings.split()[0][:-1])
    address.append(' '.join(gettings.split()[1:-2]))
print(price)
print(address)
'''
#위의 과정이 오래걸리므로 강제로 적음
price = ['$10', '$9', '$9.50', '$9.40', '$10', '$7.25', '$16', '$10', '$9', '$17', '$11', '$5.49', '$14', '$10', '$13', '$4.50', '$11.95', '$11.50', '$6.25', '$15', '$5', '$6', '$8', '$5.99', '$7.52', '$11.95', '$7.50', '$12.95', '$7', '$21', '$9.79', '$9.75', '$13', '$7.95', '$9', '$9', '$8', '$8', '$7', '$6', '$7.25', '$11', '$6', '$9', '$5.49', '$8', '$6.50', '$7.50', '$8.75', '$6.85']
address = ['2109 W. Chicago Ave.,', '800 W. Randolph St.,', '445 N. Clark St.,', '914 Noyes St., Evanston,', '825 W. Fulton Mkt.,', '100 E. Walton', '1639 S. Wabash Ave.,', '2211 W. North Ave.,', '3619 W. North Ave.,', '3267 S. Halsted St.,', '2537 N. Kedzie Blvd.,', 'Multiple', '3124 N. Broadway,', '3455 N. Southport Ave.,', '2657 N. Kedzie Ave.,', '1120 W. Grand Ave.,', '1141 S. Jefferson St.,', '333 E. Benton Pl.,', '1411 N. Wells St.,', '1747 N. Damen Ave.,', '3209 W. Irving Park', 'Multiple', '5347 N. Clark St.,', '2954 W. Irving Park Rd.,', 'Multiple', '191 Skokie Valley Rd., Highland Park,', 'Multiple', '1818 W. Wilson Ave.,', '2517 W. Division St.,', '218 W. Kinzie', 'Multiple', '1547 N. Wells St.,', '415 N. Milwaukee Ave.,', '1840 N. Damen Ave.,', '1220 W. Webster Ave.,', '5357 N. Ashland Ave.,', '1834 W. Montrose Ave.,', '615 N. State St.,', 'Multiple', '241 N. York Rd., Elmhurst,', '1323 E. 57th St.,', '655 Forest Ave., Lake Forest,', 'Hotel Lincoln, 1816 N. Clark St.,', '100 S. Marion St., Oak Park,', '26 E. Congress Pkwy.,', '2018 W. Chicago Ave.,', '25 E. Delaware Pl.,', '416 N. York St., Elmhurst,', '65 E. Washington St.,', '3351 N. Broadway,']
#50위가 맞는지 길이로 확인
print(len(price))
print(len(address))
print(len(df))

#데이터프레임에 가격, 주소 항목추가
df['Price'] = price
df['Address'] = address
#필요한 항목추출, 인덱스를 순위로 설정
df = df.loc[:, ['Rank', 'Cafe', 'Menu', 'Price', 'Address']]
df.set_index('Rank', inplace=True)
print(df.head())

df.to_csv('03. best_sandwiches_list_chicago2.csv', sep=',', encoding='utf-8')

#맛집 위치를 지도에 표시
import folium
import googlemaps
import numpy as np

df = pd.read_csv('03. best_sandwiches_list_chicago2.csv', index_col=0)

#구글지도API
gmaps_key = "AIzaSyDMgtEhS_gxWY2RETnV-wdUFa3UoH2xOPM"
gmaps = googlemaps.Client(key=gmaps_key)

#위도, 경도
lat = []
lng = []
for n in df.index:
    #Multiple은 제외
    if df['Address'][n] != 'Multiple':
        target_name = df['Address'][n] + 'Cicago'
        gmaps_output = gmaps.geocode(target_name)
        location_output = gmaps_output[0].get('geometry')
        lat.append(location_output['location']['lat'])
        lng.append(location_output['location']['lng'])
    else:
        lat.append(np.nan)
        lng.append(np.nan)
df['lat'] = lat
df['lng'] = lng

#50개의 맛집의 위도, 경도의 평균값을 중앙에 마크
mapping = folium.Map(location=[df['lat'].mean(), df['lng'].mean()], zoom_start=11)
folium.Marker([df['lat'].mean(), df['lng'].mean()], popup='center').add_to(mapping)
mapping.save('map1.html')

#50개의 맛집의 위도, 경도 표시 및 가게이름 표시
mapping = folium.Map(location=[df['lat'].mean(), df['lng'].mean()], zoom_start=11)
for n in df.index:
    if df['Address'][n] != 'Multiple':
        folium.Marker([df['lat'][n], df['lng'][n]], popup=df['Cafe'][n]).add_to(mapping)
mapping.save('map2.html')

