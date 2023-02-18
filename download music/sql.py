from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/music'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 跟踪修改，暂不需要
# app.config['SECRECT_KEY'] = 'dfhvgehi'  # 设置密钥，随便打，目前不设置没报错
db = SQLAlchemy(app)


# 多对多关系的代码来自于chatGPT，这里十分感谢，虽然大部分给的代码不好用。思路：user和history分别与关联表进行一对多关系，同时fav存在关联表里。这样才能实现不同用户对记录的状态，同时减少history的冗余
# User_history = db.Table('user_history',
#                         db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
#                         db.Column('history_id', db.Integer, db.ForeignKey('history.id'), primary_key=True),
#                         db.Column('fav', db.Integer, nullable=False, default=0)
#                         )

# table不能用model的flask语句，不好用。（设置两个主键可以避免重复关联--chatGPT）
class User_history(db.Model):
    __tablename__ = 'user_history'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    history_id = db.Column(db.Integer, db.ForeignKey('history.id'), primary_key=True)
    fav = db.Column(db.Integer, nullable=False, default=0)


class User(db.Model):  # 设置表格
    __tablename__ = 'user'  # 设置表格名
    id = db.Column(db.Integer, primary_key=True)  # 设置id为int和主键
    username = db.Column(db.String(255), nullable=False)  # 设置username为str（上限255）
    password_hash = db.Column(db.String(255), nullable=False)  # 设置password为str（上限255）
    history = db.relationship('History', secondary='user_history', lazy='subquery',
                              backref=db.backref('user', lazy=True))  # 这里设置反向引用后，history那边就不用设置了

    # 设置访问密码的方法
    @property
    def password(self):
        return self.password_hash

    # 密码加密
    @password.setter
    def password(self, pwd):
        self.password_hash = generate_password_hash(pwd)

    # 验证密码
    def check_password(self, ckpwd):
        return check_password_hash(self.password_hash, ckpwd)


class History(db.Model):  # 设置表格
    __tablename__ = 'history'  # 设置表格名
    name = db.Column(db.String(255), nullable=False)  # 设置username为str（上限255）
    artist = db.Column(db.String(255), nullable=False)  # 设置password为str（上限255）
    album = db.Column(db.String(255), nullable=False)  # 设置album为str（上限255）
    duration = db.Column(db.String(255), nullable=False)  # 设置duration为str（上限255）
    rid = db.Column(db.Integer, nullable=False)  # 设置rid为int
    id = db.Column(db.Integer, primary_key=True)  # 设置id为int和主键


with app.app_context():  # 注意：新版flask操作数据库必须带这个,否则必报错,网上找半天才知道........#
    db.drop_all()  # 初始化表格，需要时再用
    db.create_all()
    name = User.query.filter(User.username == 'admin').first()  # 和db.drop_all()配套使用，设置admin，便于‘admin一键登录’的使用
    # print(name)
    if not name:
        admin = User(username='admin', password='123456')
        db.session.add(admin)
        db.session.commit()
