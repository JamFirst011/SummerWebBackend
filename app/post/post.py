import json
import os
from flask import jsonify

path = './files/post.json'

def _send_post(post):
    with open(path,'r') as f:
        public_data = json.load(f)

    id = public_data['num']
    post['id'] = id
    post['summary'] = ' '.join(block['text'] for block in post['content'] if block['text']!='')[:100] + '......'
    public_data['Posts'].append(post)
    public_data['num'] = id+1
    with open(path,'w') as f:
        json.dump(public_data,f,ensure_ascii=True,indent=4)
    return jsonify({
        'status' : True,
        'msg' : 'Send Success',
        'id' : id,
        'summary' : post['summary']
    })

def _syn():
    with open(path,'r') as f:
        data = json.load(f)
    for i in range(len(data['Posts'])):
        data['Posts'][i]['content'] = []
    return jsonify({
        'status' : True,
        'msg' : 'Synchronize Success',
        'Posts' : data['Posts']
    })

def _post_detail(id):
    with open(path,'r') as f:
        data = json.load(f)
    for post in data['Posts']:
        if post['id'] == id:
            return jsonify({
                'status' : True,
                'msg' : 'Get Post Success',
                'post' : post
            })
    return jsonify({
        'status' : False,
        'msg' : 'Post is Not Found',
        'post' : {}
    })