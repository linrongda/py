from datetime import timedelta, datetime

import jwt
from flask import request, jsonify, Blueprint

from sql import User, db, app

user = Blueprint('user', __name__)
# 这里加密是copy
SECRET_KEY = "sdifhgsiasfjaofhslio"  # JWY签名所使用的密钥，是私密的，只在服务端保存
ALGORITHM = "HS256"  # 加密算法，我这里使用的是HS256


# api
@user.route('/user', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    checkPassword = data.get('checkPassword')
    with app.app_context():  # 任何与数据库有关的操作都要在数据库app的下面
        name = User.query.filter(User.username == username).first()
        # print(name)
        if name:  # 如果用户名不唯一，难以辨别身份
            return jsonify(code=404, message='该用户名已存在'), 200
        else:
            if 6 <= len(password) <= 18:  # 这两个前端限制了，感觉有点废话，但是防sql注入应该可以
                if password == checkPassword:
                    try:
                        with app.app_context():
                            register = User(username=username,
                                            password=password)  # 这里password会先通过hash加密再存入数据库，具体看sql.py
                            db.session.add(register)
                            db.session.flush()  # 在commit前用这个，才能获取新增数据的id
                            db.session.commit()
                            dict = {'id': register.id, 'username': username}
                        return jsonify(code=200, message='success', data=dict), 200
                    except Exception as e:
                        return jsonify(code=404, message=f'导入失败，{e}'), 200
                else:
                    return jsonify(code=404, message='两次输入的密码不一致'), 200
            else:
                return jsonify(code=404, message='密码长度不符'), 200


@user.route('/user/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        with app.app_context():
            name = User.query.filter(User.username == username).first()
            # print(name)
            if name:
                login = name.check_password(password)  # 通过hash校验密码
                if login:
                    access_token_expires = timedelta(minutes=60)  # 这里的混淆直接copy网上jwt的教程
                    expire = datetime.utcnow() + access_token_expires
                    payload = {
                        "id": name.id,
                        "name": username,
                        "exp": expire
                    }
                    # 生成Token,返回给前端
                    access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
                    dict = {'id': name.id, 'username': name.username, 'token': access_token}
                    return jsonify(code=200, message='success', data=dict), 200
                else:
                    return jsonify(code=404, message='密码错误'), 200
            else:
                return jsonify(code=404, message='该用户名不存在'), 200
    except Exception as e:
        return jsonify(code=404, message=f'登录失败，{e}'), 200


def authorized_user(token):  # 校验token的函数
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("name")
        # print(username)
        with app.app_context():
            name = User.query.filter(User.username == username).first()
        if name:
            # print(payload)
            return payload
    except Exception as e:
        return False
