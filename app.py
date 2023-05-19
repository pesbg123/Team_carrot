import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import certifi
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
ca = certifi.where()

client = MongoClient(
    'mongodb+srv://sparta:test@cluster0.j8qe8ie.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)

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
    self_introduction_receive = request.form['selfintroduction_give']
    comment_receive = request.form['comment_give']
    hobby_receive = request.form['hobby_give']

    all_members = list(db.members.find({}, {'_id': False}))
    if not all_members:
        id = 1
    else:
        last_member = all_members[-1]
        if 'member_id' in last_member:
            id = last_member['member_id'] + 1
        else:
            id = 1

    doc = {
        'member_id': id,
        'name': name_receive,
        'image': image_receive,
        'selfintroduction': self_introduction_receive,
        'blog': blog_receive,
        'tmi': comment_receive,
        'hobby': hobby_receive
    }
    db.members.insert_one(doc)
    return jsonify({'msg': '저장 완료!'})


@app.route("/members", methods=["GET"])
def member_get():
    all_members = list(db.members.find({}, {'_id': False}))
    return jsonify({'result': all_members})


@app.route('/members/memberid', methods=['DELETE'])
def delete_member():
    data = request.json
    id_receive = data['id_give']
    db.members.delete_one({'member_id': id_receive})
    return jsonify({'msg': '삭제 완료!'})


@app.route("/members/<id>/comments", methods=["GET"])
def comments_show(id):
    all_commnets = list(db.comments.find(
        {'memberid': id}, {'_id': False}).sort('_id', -1))
    return jsonify({'result': all_commnets})

# id구현함


@app.route("/members/<id>/comments", methods=["POST"])
def comments_post(id):
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
        'memberid': id,
        'comment_id': comment_id,
        'nickname': nickname_receive,
        'comment': comment_receive
    }
    db.comments.insert_one(doc2)
    return jsonify({'msg': '저장 완료!'})


@app.route('/members/<id>/comments/delete', methods=['DELETE'])
def delete_comment(id):
    data = request.json
    comments_receive = data['memberid_give']
    db.comments.delete_one({'memberid': id})
    return jsonify({'msg': '삭제완료!'})


@app.route('/members/<id>')
def render_teammember(id):
    _id = int(id)
    print(_id)
    member = db.members.find_one({'member_id': _id})
    print(member)
    return render_template('member.html', member=member)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5002, debug=True)
