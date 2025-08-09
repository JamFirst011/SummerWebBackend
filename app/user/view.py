from flask import Flask,request,Blueprint
from app.user.login import _register, _login, _add_box, _add_order
import typing as t
import time

user_blueprint = Blueprint('user', __name__,url_prefix='/user')

'''
User_File 格式为：
{
    "username": "new_user",
    "password": "123456",
    "time": "2025-08-03 23:55:00",
    "inventories": [],
    "orders": []
}
'''

@user_blueprint.route('/login',methods=['POST'])
def login():
    '''
    接受参数：  {username,password}
    返回值： {status:True/False, msg:'success/fail',extra_info:{}}
    '''
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    return _login(username, password)

@user_blueprint.route('/register',methods=['POST'])
def register():
    '''
    接受参数：  {username,password,time}
    返回值： {status:True/False, msg:'Success/Fail'}
    '''
    data = request.get_json()
    return _register(data)

@user_blueprint.route('/add-box',methods=['POST'])
def add_box():
    '''
    用于添加和删除物品
    接受参数：  {name,boxes,cmd}
    返回值： {status:True/False, msg:'Success/Fail'}
    '''
    try:
        data = request.get_json()
        name = data.get('name')
        boxes = data.get('boxes')
        cmd = data.get('cmd')
        return _add_box(name,boxes,cmd)
    except Exception as e:
        return {'status': False, 'msg': str(e)}

@user_blueprint.route('/add-order',methods=['POST'])
def add_order():
    '''
    用于添加和删除订单
    接受参数：  {name,order_id, order_name,order_num,order_price,order_time,cmd}
    返回值： {status:True/False, msg:'Success/Fail'}
    '''
    try:
        data = request.get_json()
        order_id = data.get('order_id')
        order_name = data.get('order_name')
        order_num = data.get('order_num')
        order_price = data.get('order_price')
        order_time = data.get('order_time')
        name = data.get('name')
        cmd = data.get('cmd')
        return _add_order(name,order_id,order_name, order_num, order_price, order_time,cmd) 
    except Exception as e:
        return {'status': False, 'msg': str(e)}
