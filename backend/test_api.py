import requests
import json

BASE_URL = 'http://localhost:5000/api/v1'

def test_register():
    url = f'{BASE_URL}/auth/register'
    data = {
        'username': 'admin',
        'password': '123456',
        'email': 'admin@example.com'
    }
    response = requests.post(url, json=data)
    print('注册响应:', response.json())
    return response.json()

def test_login():
    url = f'{BASE_URL}/auth/login'
    data = {
        'username': 'admin',
        'password': '123456'
    }
    response = requests.post(url, json=data)
    print('登录响应:', response.json())
    return response.json()

if __name__ == '__main__':
    # 测试注册
    test_register()
    # 测试登录
    test_login() 