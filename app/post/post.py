import json
import os
from flask import jsonify

path = './files/post.json'

def _send_post(post):
    with open(path,'r') as f:
        public_data = json.load(f)
    
    id = public_data['num']
    post['id'] = id
    public_data['Posts'].append(post)
    public_data['num'] = id+1
    with open(path,'w') as f:
        json.dump(public_data,f,ensure_ascii=True,indent=4)
    return jsonify({
        'status' : True,
        'msg' : 'Send Success',
        'id' : id
    })

def _syn():
    with open(path,'r') as f:
        data = json.load(f)
    return jsonify({
        'status' : True,
        'msg' : 'Synchronize Success',
        'Posts' : data['Posts']
    })