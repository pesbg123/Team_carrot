import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import certifi
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
ca = certifi.where()

client = MongoClient(
    'mongodb+srv://sparta:test@cluster0.1v14zkv.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta


@app.route('/')
def home():
    return render_template('index.html')

# id 구현함


@app.route("/members", methods=["POST"])
def members_post():
    name_receive = request.form['name_give']
    image_receive = request.form['image_give']
    blog_receive = request.form['blog_give']
    comment_receive = request.form['comment_give']
    hobby_receive = request.form['hobby_give']

    all_members = list(db.members.find({}, {'_id': False}))
    if not all_members:
        id = 1
    else:
        last_member = all_members[-1]
        if 'id' in last_member:
            id = last_member['id'] + 1
        else:
            id = 1

    doc = {
        'id': id,
        'name': name_receive,
        'image': image_receive,
        'blog': blog_receive,
        'comment': comment_receive,
        'hobby': hobby_receive
    }
    db.members.insert_one(doc)
    return jsonify({'msg': '저장 완료!'})


@app.route("/members", methods=["GET"])
def member_get():
    all_members = list(db.members.find({}, {'_id': False}))
    return jsonify({'result': all_members})


@app.route('/members/memberid', methods=['POST'])
def delete_member():
    data = request.json
    name_receive = data['name_give']
    db.members.delete_one({'name': name_receive})
    return jsonify({'msg': '삭제 완료!'})


@app.route('/subpage')
def member():
    return render_template('subpage.html')


@app.route("/subpage/comment", methods=["GET"])
def comments_show():
    all_commnets = list(db.comments.find({}, {'_id': False}).sort('_id', -1))
    return jsonify({'result': all_commnets})

# id구현함


@app.route("/subpage/commentid", methods=["POST"])
def comments_post():
    id_receive = int(request.form.get('id_give'))
    nickname_receive = request.form.get('nickname_give')
    comment_receive = request.form.get('comment_give')

    last_comment = db.comments.find_one({}, sort=[('comment_id', -1)])

    if not last_comment:
        comment_id = 1
    elif 'comment_id' not in last_comment:
        comment_id = 1
    else:
        comment_id = last_comment['comment_id'] + 1

    doc2 = {
        'id': id_receive,
        'comment_id': comment_id,
        'nickname': nickname_receive,
        'comment': comment_receive
    }
    db.comments.insert_one(doc2)
    return jsonify({'msg': '저장 완료!'})


@app.route('/subpage/nicknameid', methods=['POST'])
def delete_comment():
    data = request.json
    comments_receive = data['comment_give']
    db.comments.delete_one({'nickname': comments_receive})
    return jsonify({'msg': '삭제완료!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
