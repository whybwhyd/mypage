from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import certifi
from bson.objectid import ObjectId

app = Flask(__name__)

ca = certifi.where()
client = MongoClient('mongodb+srv://sparta:test@cluster0.8bt9azj.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

@app.route('/')
def home():
	return render_template('index.html')

@app.route("/food", methods=["POST"])
def food_post():
    title_receive = request.form['title_give']
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']
    star_receive = request.form['star_give']

    doc = {
        'title':title_receive,
		'url':url_receive,
        'comment':comment_receive,
		'star':star_receive
    }

    db.foods.insert_one(doc)

    return jsonify({'msg':'저장완료!'})


@app.route("/food", methods=["GET"])
def food_get():
	all_stores = list(db.foods.find({},{'_id':False}))
	return jsonify({'result':all_stores})
# 삭제 부분
@app.route("/food/delete", methods=["POST"])
def food_delete():
    title_receive = request.form['title_give']
    
    db.foods.delete_one({'title': title_receive})

    return jsonify({'msg':'삭제완료!'})

#수정 부분 title 이 수정이 안돼요
@app.route("/food/edit_post", methods=["POST"])
def food_edit_post():
    title_receive = request.form['title_give']
    edit_title_receive = request.form['edit_title_give']
    edit_url_receive = request.form['edit_url_give']
    edit_comment_receive = request.form['edit_comment_give']
    edit_star_receive = request.form['edit_star_give']

    result = db.foods.update_one({'title': title_receive}, {'$set': {
        'title': edit_title_receive,
        'url': edit_url_receive,
        'comment': edit_comment_receive,
        'star': edit_star_receive
    }})

    if result.modified_count > 0:
        return jsonify({'msg': '수정완료!'})
    else:
        return jsonify({'msg': '수정 실패!'})

#댓글 작성 부분 DB 저장까지는 되는데 값이 undefined로 제대로 저장이 안돼요 
@app.route("/food/add_comment", methods=["POST"])
def add_comment():
    title_receive = request.form['title_give']
    comment_receive = request.form['comment_give']

    db.foods.update_one({'title': title_receive}, {'$push': {'comments': comment_receive}})

    return jsonify({'msg': '작성 완료.', 'result': 'success'})

@app.route("/food/comments", methods=["POST"])
def get_comments():
     data = request.get_json()
     title_receive = data['title_give']

     food = db.foods.find_one({'title': title_receive})
     if food:
         comments = food.get('comments', [])
     else:
         comments = []

     return jsonify({'result': comments})

#좋아요 버튼 기억용 미완성
@app.route('/food/like', methods=['POST'])
def food_like():
    data = request.json
    title = data['title']
    clicked = data['clicked']

    db.foods.update_one({'title': title}, {'$set': {'clicked': clicked}})

    return jsonify({'msg': '버튼 클릭 상태가 업데이트되었습니다.'})


if __name__ == '__main__':
	app.run('0.0.0.0', port=5001, debug=True)