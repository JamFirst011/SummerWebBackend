from flask import Flask,request,Blueprint
import typing as t
from app.post.post import _send_post,_syn
import time

post_blueprint = Blueprint('post', __name__,url_prefix='/post')

@post_blueprint.route('/send',methods=['POST'])
def send_post():
    '''
    接受参数：{post: {}}
    返回参数：{status: True/False,msg : 'Success/Fail',id : int}
    '''
    data = request.get_json()
    post = data['post']
    return _send_post(post)

@post_blueprint.route('/syn',methods=['POST'])
def syn():
    '''
    接受参数：{keey : True}
    返回参数：{status : True/False,Posts : []}
    '''
    return _syn()