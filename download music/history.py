from flask import Blueprint, request, jsonify

from sql import User, app, History, db, User_history
from user import authorized_user

history = Blueprint('history', __name__)


@history.route('/user/history', methods=['GET'])
def query():
    Authorization = request.headers.get('Authorization')
    page = int(request.args.get('page'))

    if not Authorization:
        return jsonify(code=404, message='您还没有登录，请先登录'), 200
    else:
        token = authorized_user(Authorization)
    if not token:
        return jsonify(code=404, message='登录状态认证失败，请重新登录'), 200

    if token:
        id = token.get("id")  # 同download
        list = []
        try:
            with app.app_context():
                user = User.query.get(id)
                history = user.history  # 获取所有记录
                total = len(history)  # 根据长度决定页数
                if total == 0:
                    return jsonify(code=404, message='没有下载历史'), 200
                if total % 10 == 0:
                    pages = int(total / 10)
                else:
                    pages = int(total / 10) + 1
                history_query = History.query.filter(History.id.in_([history.id for history in history]))
                # 根据id查询记录，chatGPT牛逼，同时也是垃圾，之前给的table类害人不浅，debug很久
                # 分页查询历史记录
                histories = history_query.paginate(page=page, per_page=10).items
                for h in histories:  # 这里h.id之前临时设置为1，导致所有状态都跟第一个一样，debug一天。。。。。
                    f = db.session.query(User_history).filter_by(user_id=id, history_id=h.id).first()  # 获取特定关联记录
                    dict = {'name': h.name, 'artist': h.artist, 'album': h.album, 'duration': h.duration,
                            'fav': f.fav,
                            'rid': h.rid, 'id': h.id}
                    list += [dict]
                data_list = {'list': list, 'count': pages}
            return jsonify(code=200, message='success', data=data_list), 200
        except Exception as e:
            return jsonify(code=404, message=f'查询失败，{e}'), 200


@history.route('/user/history/lc', methods=['PUT'])
def update():
    Authorization = request.headers.get('Authorization')
    update = request.get_json()
    hid = update.get('id')
    fav = update.get('fav')

    if not Authorization:
        return jsonify(code=404, message='您还没有登录，请先登录'), 200
    else:
        token = authorized_user(Authorization)
    if not token:
        return jsonify(code=404, message='登录状态认证失败，请重新登录'), 200

    if token:
        id = token.get("id")
        try:
            with app.app_context():
                f = db.session.query(User_history).filter_by(user_id=id, history_id=hid).first()
                # print(f.fav)
                history = History.query.get(hid)
                if not f:
                    return jsonify(code=404, message='找不到该记录'), 200
                else:
                    f.fav = fav  # table类不能这样用，垃圾chatGPT
                    db.session.commit()
                dict = {'name': history.name, 'artist': history.artist, 'album': history.album,
                        'duration': history.duration, 'rid': history.rid}
            return jsonify(code=200, message='success', data=dict), 200
        except Exception as e:
            return jsonify(code=404, message=f'更改失败，{e}'), 200


@history.route('/user/history', methods=['DELETE'])
def delete():
    Authorization = request.headers.get('Authorization')
    delete = request.get_json()
    type = delete.get('type')
    hid = delete.get('id')
    list = delete.get('list')

    if not Authorization:
        return jsonify(code=404, message='您还没有登录，请先登录'), 200
    else:
        token = authorized_user(Authorization)
    if not token:
        return jsonify(code=404, message='登录状态认证失败，请重新登录'), 200

    if token:
        id = token.get("id")
        try:
            with app.app_context():
                if type == 0:  # 根据给的type决定删除形式
                    d0 = db.session.query(User_history).filter_by(user_id=id, history_id=hid).first()
                    db.session.delete(d0)
                    db.session.commit()
                    return jsonify(code=200, message='success'), 200
                if type == 1:
                    for i in list:
                        d1 = db.session.query(User_history).filter_by(user_id=id, history_id=i).first()
                        db.session.delete(d1)
                        db.session.commit()
                    return jsonify(code=200, message='success'), 200
        except Exception as e:
            return jsonify(code=404, message=f'删除失败，{e}'), 200
