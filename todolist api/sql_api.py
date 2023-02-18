from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# 思路：将api分为sql端api和html端api，通过from import 进行调用，通过严格的html端api的输入限制，来减少报错
# 注，新sqlalchemy库（1.4版本及以后）进行许多修改，query、delete、update等方法变为遗留的方法，运行query时会提醒使用新方法（delete不提醒），但是仍能够使用并返回值，而update直接报错，详情见https://docs.sqlalchemy.org/en/20/changelog/migration_20.html
app = Flask(__name__)  # 实例化app

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/text'  # 连接mysql
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 跟踪修改，暂不需要
# app.config['SECRECT_KEY'] = 'dfhvgehi'  # 设置密钥，随便打，目前不设置没报错

db = SQLAlchemy(app)  # 实例化数据库


class todolist(db.Model):  # 设置表格
    __tablename__ = 'todolist'  # 设置表格名
    id = db.Column(db.Integer, primary_key=True)  # 设置id为int和主键
    title = db.Column(db.String(255), nullable=False)  # 设置title为str（上限255）
    context = db.Column(db.Text, nullable=False)  # 设置context为text（上限65535）
    status = db.Column(db.Enum('已完成', '待办'), nullable=False)  # 设置status为'已完成', '待办'二选一（枚举型）
    addtime = db.Column(db.DateTime, nullable=False)  # 设置addtime为datetime（格式：xxxx-xx-xx xx:xx:xx）
    deadline = db.Column(db.DateTime, nullable=False)  # 设置deadline为datetime（格式：xxxx-xx-xx xx:xx:xx）


with app.app_context():  # 注意：新版flask操作数据库必须带这个,否则必报错,网上找半天才知道........#
    # db.drop_all()  # 初始化表格，需要时再用
    db.create_all()  # 创建表格


def add0(title=None, context=None, status=None, addtime=None, deadline=None):  # 设置add0函数
    try:
        with app.app_context():  # 同上
            add = todolist(title=title, context=context, status=status, addtime=addtime, deadline=deadline)  # 导入输入的数据
            db.session.add(add)  # 导入数据库
            db.session.commit()  # 提交
        return True  # 返回True值，交由html端api继续
    except Exception as e:
        return False  # 其他情况返回False值，交由html端api继续


def query0(status=None, keyword=None, id=None, all=None):  # 设置query0函数，依题，通过id/keyword/all/status进行查询
    try:
        with app.app_context():  # 同
            if status:  # 如果输入的有status，下面进行判断
                if status == '已完成':
                    query_filter1 = todolist.query.filter(todolist.status == '已完成').all()  # 查询是否存在
                    if query_filter1:
                        return query_filter1  # 是，返回查询值
                    else:
                        return '已完成'  # 否，返回'已完成'，交由html端api继续
                if status == '待办':  # 接下去的查、改、删都有查询
                    query_filter2 = todolist.query.filter(todolist.status == '待办').all()
                    if query_filter2:
                        return query_filter2
                    else:
                        return '待办'
            if all:  # 如果all有True值，接下去的if all同理
                query_all = todolist.query.all()
                if query_all:
                    return query_all
                else:
                    return 'all'
            if keyword:  # keyword，由于题目没讲清楚关键字范围，只好全部包括了
                query_keyword1 = todolist.query.filter(todolist.title.contains(keyword)).all()
                query_keyword2 = todolist.query.filter(todolist.context.contains(keyword)).all()
                query_keyword3 = todolist.query.filter(todolist.id.contains(keyword)).all()
                query_keyword4 = todolist.query.filter(todolist.status.contains(keyword)).all()
                query_keyword5 = todolist.query.filter(todolist.addtime.contains(keyword)).all()
                query_keyword6 = todolist.query.filter(todolist.deadline.contains(keyword)).all()
                query_keyword = query_keyword1 + query_keyword2 + query_keyword3 + query_keyword4 + query_keyword5 + query_keyword6
                query_keyword0 = list(set(filter(None, query_keyword)))  # list(set(filter(None, list)))可以除去list中重复和空元素
                query_keyword_ = sorted(query_keyword0, key=lambda x: x.id)  # 将列表中的元素按id排序
                if query_keyword_:
                    return query_keyword_
                else:
                    return 'keyword'
            if id:
                query_get = todolist.query.get(id)
                if query_get:
                    return query_get
                else:
                    return 'id'
    except Exception as e:
        return False


def update0(id=None, status=None, all=None):  # 设置update0函数，根据题目意思，我觉得要先判断status，然后判断用id还是all
    try:
        with app.app_context():  #
            if status == '待办':  # 先status
                if id:  # 然后id
                    update1_no = todolist.query.get(id)  # 查询是否存在
                    if update1_no == None:
                        return 'id'  # 否，返回'id'，交由html端api继续
                    if update1_no.status == '待办':
                        update1_no.status = '已完成'
                        db.session.commit()  # 存在且状态为待办，进行修改，提交，返回str
                        return f'成功将id={id}的待办事项修改为已完成状态'
                    if update1_no.status == '已完成':
                        return 'id已完成'  # 存在但是状态为已完成，返回'id已完成'，交由html端api继续
                if all:  # 以下同理
                    update2_no = todolist.query.filter(todolist.status == '待办').all()
                    if update2_no:
                        for u2n in update2_no:
                            u2n.status = '已完成'
                            db.session.commit()
                        return f'成功将所有的待办事项修改为已完成状态'
                    else:
                        return 'all已完成'
            if status == '已完成':
                if id:
                    update1_yes = todolist.query.get(id)
                    if update1_yes.status == '已完成':
                        update1_yes.status = '待办'
                        db.session.commit()
                        return f'成功将id={id}的已完成事项修改为待办状态'
                    if update1_yes == None:
                        return 'id'
                    if update1_yes.status == '待办':
                        return 'id待办'
                if all:
                    update2_yes = todolist.query.filter(todolist.status == '已完成').all()
                    if update2_yes:
                        for u2y in update2_yes:
                            u2y.status = '待办'
                            db.session.commit()
                        return f'成功将所有已完成的事项修改为待办状态'
                    else:
                        return 'all待办'
    except Exception as e:
        return False


def delete0(id=None, status=None, all=None):  # 设置delete0函数，题目有歧义，我认为是通过id/status/all来删除
    try:
        with app.app_context():  #
            if id:
                delete_get = todolist.query.get(id)
                if delete_get:
                    db.session.delete(delete_get)  # delete已经不能直接接在query的后面，必须用db.session.delete()
                    db.session.commit()
                    return f'成功将id={id}的事项删除'
                else:
                    return 'id'
            if status == '已完成':
                delete_filter1 = todolist.query.filter(todolist.status == '已完成').all()
                if delete_filter1:
                    for df1 in delete_filter1:
                        db.session.delete(df1)
                        db.session.commit()
                    return f'成功将所有已完成的事项删除'
                else:
                    return '已完成'
            if status == '待办':
                delete_filter2 = todolist.query.filter(todolist.status == '待办').all()
                if delete_filter2:
                    for df2 in delete_filter2:
                        db.session.delete(df2)
                        db.session.commit()
                    return f'成功将所有待办的事项删除'
                else:
                    return '待办'
            if all:
                delete_all = todolist.query.all()
                if delete_all:
                    for da in delete_all:
                        db.session.delete(da)
                        db.session.commit()
                    return f'成功将所有的事项删除'
                else:
                    return 'all'
    except Exception as e:
        return False
