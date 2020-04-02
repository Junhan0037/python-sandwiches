#!/usr/bin/env python3 
#네이버 영화 평점 기준 영화의 평점 변화 확인하기
from bs4 import BeautifulSoup
import pandas as pd
from urllib.request import urlopen

url_base = "https://movie.naver.com/"
url_syb = "movie/sdb/rank/rmovie.nhn?sel=cur&date=20190221"
url = url_base + url_syb

#html코드
html = urlopen(url)
soup = BeautifulSoup(html, "html.parser")
print(soup)
print(soup.find_all('div', 'tit5'))
print('===============================================')
#1등 영화 제목
print(soup.find_all('div', 'tit5')[0].a.string)
#평점
print(soup.find_all('td', 'point')[0].string)

#1월달 날짜 생성
date = pd.date_range('2019-1-1', periods=31, freq='D')
print(date)

import urllib
movie_date = []
movie_name = []
movie_point = []
for today in date:
    html = "https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=cur&date={date}"
    response = urlopen(html.format(date = urllib.parse.quote(today.strftime('%Y%m%d'))))
    soup = BeautifulSoup(response, "html.parser")
    end = len(soup.find_all('td', 'point'))
    movie_date.extend([today for n in range(0, end)])
    movie_name.extend([soup.find_all('div', 'tit5')[n].a.string for n in range(0, end)])
    movie_point.extend([soup.find_all('td', 'point')[n].string for n in range(0, end)])

movie = pd.DataFrame({'date':movie_date, 'name':movie_name, 'point':movie_point})
print(movie.head())

#날짜가 아닌 영화별로 점수의 합산
import numpy as np
movie_unique = pd.pivot_table(movie, index=['name'], aggfunc=np.sum)
#점수별로 정리
movie_best = movie_unique.sort_values(by='point', ascending=False)
print(movie_best.head())

#특정 영화를 추려서 확인 (날짜별 평점의 변화)
tmp = movie.query('name == ["극한직업"]')
print(tmp)

#'극한직업' 평점 그래프
import matplotlib.pyplot as plt
plt.figure(figsize=(12,8))
plt.plot(tmp['date'], tmp['point'])
plt.legend(loc='best')
plt.grid()
plt.show()

'''
#영화별 날짜 변화에 따른 평점 변화 (오류발생!!)
movie_pivot = pd.pivot_table(movie, index=['date'], columns=['name'], values=['point'])
print(movie_pivot.head())

#인덱스를 낮춤 (맨윗줄 삭제하면서 전체 1칸 올림)
movie_pivot.columns = movie_pivot.columns.droplevel()
print(movie_pivot.head())

#matplotlib 폰트 변경 (한글지원 X 때문)
import platform
from matplotlib import font_manager, rc
plt.rcParams['axes.unicode_minus'] = False
if platform.system() == 'Darwin':
    rc('font', family='AppleGothic')
elif platform.system() == 'Windows':
    path = "c:\Windows\Fonts\malgun.ttf"
    font_name = font_manager.FontProperties(fname=path).get_name()
    rc('font', family=font_name)
else:
    print('Unknown system... sorry~~~~')

#영화 몇 개를 지정해서 날짜별 변화 확인
movie_pivot.plot(y=['보베미안 랩소디', '헌터 킬러', '폴란드로 간 아이들', '트루먼 쇼', '레토'])
plt.legend(loc='best')
plt.grid()
plt.show()
'''

