import os

import requests
from flask import Blueprint, request, jsonify, send_file

from sql import app, History, db, User
from user import authorized_user


# 因为不知名的原因，直接使用ajax，会有概率出现反爬。所以这边思路：先通过搜索页面的ajax获取rid，然后通过下面的网址，获取具体歌曲信息。
def info(rid):
    detailurl = f'http://m.kuwo.cn/newh5/singles/songinfoandlrc?musicId={rid}&httpsStatus=1'
    detail = requests.get(detailurl).json()['data']['songinfo']
    return detail


search = Blueprint('search', __name__)


@search.route('/search', methods=['GET'])
def Search():
    Authorization = request.headers.get('Authorization')
    text = request.args.get('text')
    page = request.args.get('page')

    if not Authorization:
        return jsonify(code=404, message='您还没有登录，请先登录'), 200
    else:
        token = authorized_user(Authorization)
    if not text:
        return jsonify(code=404, message='请输入要搜索的歌曲和歌手'), 200
    elif token:
        url = 'http://www.kuwo.cn/api/www/search/searchMusicBykeyWord'
        header = {
            'Cookie': 'kw_token=9D4Z9CV6SD5',
            'csrf': '9D4Z9CV6SD5',
            'Referer': 'http://www.kuwo.cn/search/list',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76'
        }
        params = {'key': text,
                  'pn': page,
                  'rn': 10,
                  'httpsStatus': 1
                  }
        response = requests.get(url=url, params=params, headers=header)
        # print(response.json())
        json = response.json()
        total = int(json['data']['total'])  # 获取ajax提供的歌曲总数
        # 这里进行判别和分页
        if total == 0:
            return jsonify(code=404, message=f'抱歉，还没有找到与"{text}"相关的内容'), 200
        if total % 10 == 0:
            pages = int(total / 10)
        else:
            pages = int(total / 10) + 1
        # print(token)
        list = []
        json_list = json['data']['list']
        for data in json_list:  # 根据json_list中的各个歌曲的rid，进行反反爬，代价是时间比较久，异步还不会。。。
            rid = data['rid']
            message = info(rid)
            # print(message)
            dict = {"name": message['songName'],
                    "artist": message['artist'],
                    "album": message['album'],
                    "duration": message['songTimeMinutes'],
                    "rid": message['id']
                    }
            list += [dict]
        data_list = {'list': list, 'count': pages}
        # print(list)
        return jsonify(code=200, message='success', data=data_list), 200
    else:
        return jsonify(code=404, message='登录状态认证失败，请重新登录'), 200


@search.route('/search/download/<rid>', methods=['GET'])
def download(rid):
    try:
        os.makedirs('music')  # 创建music文件夹
    except Exception as e:
        print(e)
    detail = info(rid)
    Authorization = request.headers.get('Authorization')
    if not Authorization:
        return jsonify(code=404, message='您还没有登录，请先登录'), 200
    token = authorized_user(Authorization)
    # print(token)
    id = token.get('id')  # 通过token来获取用户身份
    if not token:
        return jsonify(code=404, message='登录状态认证失败，请重新登录'), 200
    if token:
        try:
            with app.app_context():
                user = User.query.get(id)
                query0 = History.query.filter(History.rid == rid).first()  # 查询是否存在记录
                if not query0:
                    add0 = History(name=detail['songName'], artist=detail['artist'], album=detail['album'],
                                   duration=detail['songTimeMinutes'], rid=detail['id'])
                    db.session.add(add0)
                    user.history.append(add0)  # 增加关联
                    db.session.commit()
                else:
                    user.history.append(query0)
                    db.session.commit()
                title = f'{detail["songName"]}-{detail["artist"]}'  # 设置文件名
                file_path = f'music/{title}.mp3'  # 路径
                if os.path.exists(file_path):  # 是否存在，不会异步删除。。。
                    return send_file(file_path, as_attachment=True)  # 发送文件
                else:
                    infourl = f'http://www.kuwo.cn/api/v1/www/music/playUrl?mid={rid}&type=convert_url3&br=320kmp3'
                    musicurl = requests.get(infourl).json()['data']['url']
                    # 通过上面网址来获取歌曲的真实地址。为什么不用外链转化工具？自己操作感觉更爽嘛。b站搜得到爬酷我的教程
                    musicdata = requests.get(musicurl).content
                    with open(file_path, mode='wb') as f:
                        f.write(musicdata)
                    return send_file(file_path, as_attachment=True)
        except Exception as e:
            return jsonify(code=404, message=f'下载记录导入失败，{e}'), 200
