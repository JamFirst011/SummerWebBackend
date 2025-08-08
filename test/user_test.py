import os
import time
import json

path = './files/accounts/'
payload = {
    "username": "new_user",
    "password": "123456",
    "time": "2025-08-03 23:55:00"
}

def clear_cache():
    if os.path.exists(path + f'{payload["username"]}.json'):
        os.remove(path + f'{payload["username"]}.json')

# test_register.py
def test_register_success(client):
    response = client.post('/user/register', json=payload)
    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data["status"] is True
    clear_cache()

def test_register_existing_user(client):
    response = client.post('/user/register', json=payload)
    response = client.post('/user/register', json=payload)
    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data["status"] is False
    assert json_data["msg"] == 'User has Registered, Please Login dirrectly'
    clear_cache()

def test_login_success_and_pwd_error(client):
    client.post('/user/register', json=payload)
    login_payload = {
        "username": payload["username"],
        "password": payload["password"],
    }
    response = client.post('/user/login', json=login_payload)
    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data["status"] is True
    assert 'inventories' in json_data['extra_info']
    assert 'orders' in json_data['extra_info']

    login_payload["password"] = "wrong_password"
    response = client.post('/user/login', json=login_payload)
    json_data = response.get_json()
    assert json_data["status"] is False
    clear_cache()

def test_add_box_success(client):
    client.post('/user/register', json=payload)

    add_box_payload = {
        "name": payload["username"],
        "boxes": ["box1", "box2"],
        "cmd": "add"
    }
    response = client.post('/user/add-box', json=add_box_payload)
    json_data = response.get_json()

    assert response.status_code == 200
    print(json_data)
    assert json_data["status"] is True

    # Verify the boxes were added
    user_path = os.path.join(path, f'{payload["username"]}.json')
    with open(user_path, 'r') as f:
        user_info = json.load(f)
        assert "box1" in user_info['inventories']
        assert "box2" in user_info['inventories']

    remove_box_payload = {
        'name' : payload['username'],
        'boxes' : ['box1'],
        'cmd' : 'remove'
    }
    response = client.post('/user/add-box',json=remove_box_payload)
    json_data = response.get_json()

    assert json_data['status'] is True
    with open(user_path,'r') as f:
        user_info = json.load(f)
        assert 'box1' not in user_info['inventories']
        assert 'box2' in user_info['inventories']
    clear_cache()

def test_add_order_success(client):
    client.post('/user/register', json=payload)

    add_order_payload = {
        'name' : payload['username'],
        'order_id' : 1,
        'order_name' : 'order1',
        'order_num' : 1,
        'order_price' : 100,
        'order_time' : '2025-08-03 23:55:00',
        'cmd' : 'add'
    }
    response = client.post('/user/add-order',json=add_order_payload)
    json_data = response.get_json()
    assert json_data['status'] is True
    with open(os.path.join(path,f'{payload["username"]}.json'),'r') as f:
        user_info = json.load(f)
        assert 'order1' in [od['order_name'] for od in user_info['orders']]

    redundency_order_payload = {
        'name' : payload['username'],
        'order_id' : 1,
        'cmd' : 'add'
    }
    response = client.post('/user/add-order',json=redundency_order_payload)
    json_data = response.get_json()
    assert json_data['status'] is False

    time.sleep(5)

    remove_order_payload = {
        'name' : payload['username'],
        'order_id' : 1,
        'cmd' : 'remove'
    }
    response = client.post('/user/add-order',json=remove_order_payload)
    json_data = response.get_json()
    assert json_data['status'] is True
    with open(os.path.join(path,f'{payload["username"]}.json'),'r') as f:
        user_info = json.load(f)
        assert 'order1' not in [od['order_name'] for od in user_info['orders']]
    clear_cache()





