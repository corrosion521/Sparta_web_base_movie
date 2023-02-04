# bs4, requests = > 크롤링
# pymongo, flask, dnspython => db server

# 서버
# post -> 크롤링해서 요청한 데이터 + a 보내줘야함
# 크롤링 하는거? meta_prac(조각기능 이용)

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 크롤링
import requests
from bs4 import BeautifulSoup

# 이하 3줄 db사용 위해
from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:sparta@cluster0.n0vryb2.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')


@app.route("/movie", methods=["POST"])
def movie_post():
    url_receive = request.form['url_give']
    star_receive = request.form['star_give']
    comment_receive = request.form['comment_give']

    # 크롤링 (조각 기능에서 가져옴)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)




    # print(data.text) 여기서도 html형식이긴 하겠지만..
    # BeautifulSoup : html을 수프객체로 만들어서 추출하기 쉽게 만들어줘요.
    soup = BeautifulSoup(data.text, 'html.parser')

    # 여기에 코딩을 해서 meta tag를 먼저 가져와보겠습니다.
    # print(soup)

    # 참고로 head부분에 meta데이터들이 들어있다. ( 내용적인 부분들)
    # meta태그중 og:title 속성을 가진 태그 선택. 그중에서 content속성의 값을 가져와라
    title = soup.select_one('meta[property="og:title"]')['content']
    image = soup.select_one('meta[property="og:image"]')['content']
    desc = soup.select_one('meta[property="og:description"]')['content']

    #db에 넣기
    doc = {
        'title' : title,
        'image' : image,
        'desc' : desc,
        'star' : star_receive,
        'comment' : comment_receive
    }
    db.movies.insert_one(doc)

    return jsonify({'msg': '저장 완료!'})


@app.route("/movie", methods=["GET"])
def movie_get():
    # 여러개 찾기 - 예시 ( _id 값은 제외하고 출력)
    movie_list = list(db.movies.find({}, {'_id': False}))
    
    # response의 구성물 중 하나가 'movies'
    # dictionary느낌 기억
    return jsonify({'movies': movie_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
