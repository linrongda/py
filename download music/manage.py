from flask import Flask
from flask_cors import CORS

from history import history
from search import search
from user import user

app = Flask(__name__)
CORS(app)  # 实现跨域
app.register_blueprint(user)  # 注册蓝图
app.register_blueprint(search)
app.register_blueprint(history)

app.run(host='0.0.0.0')  # 内网可用
# 思路：按照作业要求，分为user/search/history三部分，但是由于在其中一部分定义表格会导致循环import，所以将sql单独分出。
