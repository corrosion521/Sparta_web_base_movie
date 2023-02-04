import requests
from bs4 import BeautifulSoup
# 프로젝트에 필요한 기술들 구현 중요 => 조각 기능 . 이를 먼저 개발
# 이후에 API개발.

# 크롤링 기본 코드들 - bs4, requests이용해서 soup에 담아옴.
url = 'https://movie.naver.com/movie/bi/mi/basic.naver?code=191597'

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get(url,headers=headers)

# print(data.text) 여기서도 html형식이긴 하겠지만..
# BeautifulSoup : html을 수프객체로 만들어서 추출하기 쉽게 만들어줘요.
soup = BeautifulSoup(data.text, 'html.parser')

# 여기에 코딩을 해서 meta tag를 먼저 가져와보겠습니다.
#print(soup)

#참고로 head부분에 meta데이터들이 들어있다. ( 내용적인 부분들)
#meta태그중 og:title 속성을 가진 태그 선택. 그중에서 content속성의 값을 가져와라
title = soup.select_one('meta[property="og:title"]')['content']
image = soup.select_one('meta[property="og:image"]')['content']
desc = soup.select_one('meta[property="og:description"]')['content']

print(title, image, desc)

