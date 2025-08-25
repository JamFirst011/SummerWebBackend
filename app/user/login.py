import json
import os
from flask import jsonify

path = './files/accounts/'

def _login(name,pwd):
    user_path = path + f'{name}.json'
    if os.path.exists(user_path):
        with open(user_path, 'r') as f:
            user_info = json.load(f)
        if user_info['password'] == pwd:
            return jsonify({'status': True, 'msg': 'Login Success', 'extra_info': user_info})
        else: 
            return jsonify({'status': False, 'msg': 'Password Error', 'extra_info': {}})
    else :
        return jsonify({'status': False, 'msg': 'User Not Found','extra_info': {}})

def _register(data):
    name = data.get('username')
    user_path = path + f'{name}.json'
    if not os.path.exists(user_path):
        with open(user_path, 'w') as f:
            init_info = data
            init_info['id'] = _allocate_user_id()
            init_info['inventories'] = []
            init_info['orders'] = []
            json.dump(init_info, f,ensure_ascii=False,indent=4)
        return jsonify({'status': True, 'msg': 'Register Success','id': init_info['id']})
    else : return jsonify({'status': False, 'msg': 'User has Registered, Please Login dirrectly'})

def _add_box(name,boxes,cmd):
    user_path = path + f'{name}.json'
    if not os.path.exists(user_path):
        raise Exception('User File Not Found')
    if cmd not in ['add', 'remove']:
        raise Exception('Invalid Command')

    with open(user_path, 'r') as f:
        json_data = json.load(f)
        if cmd == 'add':
            for box in boxes:
                json_data['inventories'].append(box)
        elif cmd == 'remove': 
            for box in boxes:
                if box in json_data['inventories']:
                    json_data['inventories'].remove(box)
    with open(user_path,'w') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)
    return jsonify({'status': True, 'msg': 'Success'})

def _add_order(name,order_id, order_name, order_num, order_price, order_time, cmd):
    user_path = path + f'{name}.json'
    with open(user_path,'r') as f:
        user_info = json.load(f)
    
    if cmd == 'add': 
        if order_id in [od['order_id'] for od in user_info['orders']]: 
            raise Exception('Order ID has been used')
        
        user_info['orders'].append({
            'order_id': order_id,
            'order_name': order_name,
            'order_num': order_num,
            'order_price': order_price,
            'order_time': order_time,
        })
    else : 
        if order_id not in [od['order_id'] for od in user_info['orders']]:
            raise Exception('Order ID not found')
        user_info['orders'] = [od for od in user_info['orders'] if od['order_id'] != order_id]

    with open(user_path,'w') as f:
        json.dump(user_info, f, ensure_ascii=False, indent=4)
    return jsonify({'status': True, 'msg': 'Success'})

def _allocate_user_id():
    return len(os.listdir(path))