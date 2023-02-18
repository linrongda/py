from flask import Flask, request, jsonify
from sql_api import add0, query0, update0, delete0  # 从sql端api导入add0, query0, update0, delete0四个函数

app = Flask(__name__)


# 应题目要求，状态码一律200，jsonify中code、msg、data等根据结果变化，本项目基本符合RESTful API规范
# 吐槽：我这个应该是最为严谨的代码了，写的时候想出了很多可能会报错的地方，后续都一一返回到前端，返回“未知错误”都是暂时没发现的，希望不会有人在这个酒吧里点炒饭吧（dddd）
@app.route('/')  # 创建开始界面，返回相应输入提示
def hello():
    return jsonify(code=200,
                   msg='hello'
                       '提示：id仅限integer整数，'
                       'title、context、keyword均为string文本（title限255个字符，context限65535个字符，keyword长度限制未知），'
                       'status仅可在“待办”和"已完成"中选择，'
                       'addtime和deadline输入格式为：xxxx-xx-xx xx:xx:xx，'
                       'all值根据需要填写，需要时填写任意True值均可。'
                       '查询时，如果不通过id方法，则需要在路径后加上?page=数字&per_page=数字，更改其中“数字”为你需要的数字，page为第几页，per_page为每页显示多少条数据'), 200


@app.route('/todo', methods=['POST'])  # 路径todo，请求方法'POST'
def add():
    try:
        add = request.get_json()  # 获取输入的json数据
        title = add.get('title')  # 获取输入的title
        context = add.get('context')  # 获取输入的context
        status = add.get('status')  # 获取输入的status
        addtime = add.get('addtime')  # 获取输入的addtime
        deadline = add.get('deadline')  # 获取输入的deadline

        if not all([title, context, status, addtime, deadline]):  # 判断是否输入完整
            return jsonify(code=404, msg='请输入完整'), 200  # 返回提示
        if all([title, context, status, addtime, deadline]):  # 完整，继续
            try:
                p = add0(title, context, status, addtime, deadline)  # 获取add0函数的返回值
                if p:  # 判断是否为True
                    return jsonify(code=200, msg='添加成功',
                                   data=f'title={title}, context={context}, status={status}, addtime={addtime},deadline={deadline}'), 200  # 是，返回数据
                else:
                    return jsonify(code=404, msg='添加失败，原因：数据格式错误'), 200  # 否，返回提示
            except Exception as e:
                return jsonify(code=404, msg='添加失败，原因：' + str(e)), 200  # 其他情况，返回原因
        else:
            return jsonify(code=404, msg='填写错误'), 200  # 可能有用
    except Exception as e:
        return jsonify(code=404, msg=str(e)), 200  # 可能有用


@app.route('/todo', methods=['GET'])  # 路径todo，请求方法'GET'
def query():
    try:
        query = request.get_json()  # 与之前同理，获取数据
        status = query.get('status')
        keyword = query.get('keyword')
        id = query.get('id')
        all = query.get('all')
        list_q = list(filter(None, [status, keyword, id, all]))  # 通过长度判断是否满足查询的要求

        if not list_q:  # 没有数据
            return jsonify(code=404, msg='未设定查询方式或输入错误'), 200
        if list_q:  # 有值
            if len(list_q) == 1:  # 有一个值
                try:
                    result = query0(status, keyword, id, all)  # 获取query0返回值
                    if result:  # 返回值为True
                        if result == 'id':  # 返回值为'id'
                            return jsonify(code=404, msg='查询失败，原因：该id不存在'), 200
                        if result == 'all':  # 返回值为'all'
                            return jsonify(code=404, msg='查询失败，原因：不存在任何事项'), 200
                        if result == 'keyword':  # 返回值为'keyword'
                            return jsonify(code=404, msg='查询失败，原因：不存在包含该关键字的事项'), 200
                        if result == '待办':  # 返回值为'待办'
                            return jsonify(code=404, msg='查询失败，原因：不存在待办事项'), 200
                        if result == '已完成':  # 返回值为'已完成'
                            return jsonify(code=404, msg='查询失败，原因：不存在已完成事项'), 200
                        if id:  # 通过id查询，返回结果
                            Result0 = {'id': result.id, 'title': result.title, 'context': result.context,
                                       'status': result.status,
                                       'addtime': result.addtime, 'deadline': result.deadline}
                            return jsonify(code=200, msg='查询成功', data=f'{Result0}'), 200
                        else:  # 剩下其他情况，进行分页
                            page = int(request.args.get('page'))
                            per_page = int(request.args.get('per_page'))
                            if all(page, per_page):
                                # 别问为什么不用paginate或offset，问就是我这种思路用不了（其实可以，但是要重构代码），只能曲线救国
                                if page * per_page <= len(
                                        result) - 1:  # 判断最后一条不超出列表（注意要减1，长度和列表中的位置不同），即这页完整显示per_page条数据
                                    Result1 = result[(page - 1) * per_page:page * per_page]  # 列表切片
                                elif page * per_page > len(result) - 1 >= (
                                        page - 1) * per_page:  # 判断长度在查询范围中间，即这页不能完整显示per_page条数据，因为数据已经显示完了
                                    Result1 = result[(page - 1) * per_page:len(result)]  # 列表切片
                                else:
                                    Result1 = None  # 其他情况，返回None值
                                if Result1:  # 列表存在
                                    r1 = []  # 设定空列表，用来加数据
                                    for r in Result1:  # 遍历列表
                                        r0 = {'id': r.id, 'title': r.title, 'context': r.context, 'status': r.status,
                                              'addtime': r.addtime, 'deadline': r.deadline}  # 导入数据到字典
                                        r1 += [r0]  # 将字典添加进列表
                                    return jsonify(code=200, msg='查询成功', data=f'{r1}'), 200  # 返回数据
                                else:
                                    return jsonify(code=404, msg='查询失败，原因：当前页面无数据'), 200  # 列表不存在，返回提示
                            else:
                                return jsonify(code=404, msg='请输入当前页数和每页显示的数量'), 200  # 确认输入了query参数
                    else:
                        return jsonify(code=404, msg=f'查询失败，原因：未知错误:{result}'), 200  # 返回值不为True，返回错误
                except Exception as e:
                    return jsonify(code=404, msg='查询失败，原因：' + str(e)), 200  # 可能有用
            if len(list_q) > 1:
                return jsonify(code=404, msg='请设定单一查询方式'), 200  # 长度大于1，返回提示
    except Exception as e:
        return jsonify(code=404, msg=str(e)), 200  # 可能有用


@app.route('/todo', methods=['PUT'])  # 路径todo，请求方法'PUT'
def update():  # 大部分与query差不多
    try:
        update = request.get_json()  # 同上
        id = update.get('id')
        status = update.get('status')
        all = update.get('all')
        list_u = list(filter(None, [id, status, all]))

        if not list_u:
            return jsonify(code=404, msg='输入两项参数才能更新事项哦'), 200
        if list_u:
            if len(list_u) == 3:
                return jsonify(code=404, msg='当前输入三项，注意只能输入两项'), 200  # 长度3，返回提示
            if len(list_u) == 2:
                if id and all:
                    return jsonify(code=404, msg='不能同时输入id和all'), 200  # 查询方法中id和all不能共用
                try:
                    result = update0(id, status, all)
                    if result:
                        if result == 'id':
                            return jsonify(code=404, msg='更新失败，原因：该id不存在'), 200
                        if result == 'id已完成':
                            return jsonify(code=404, msg='更新失败，原因：该id已经是已完成事项'), 200
                        if result == 'all已完成':
                            return jsonify(code=404, msg='更新失败，原因：所有事项均已完成'), 200
                        if result == 'id待办':
                            return jsonify(code=404, msg='更新失败，原因：该id已经是待办事项'), 200
                        if result == 'all待办':
                            return jsonify(code=404, msg='更新失败，原因：所有事项均为待办'), 200
                        else:
                            return jsonify(code=200, msg='更新成功', data=result), 200
                    else:
                        return jsonify(code=404, msg=f'更新失败，原因：未知错误:{result}'), 200  # 返回值不为True，返回错误
                except Exception as e:
                    return jsonify(code=404, msg='更新失败，原因：' + str(e)), 200  # 可能有用
            if len(list_u) == 1:
                return jsonify(code=404, msg='还需要一项参数才能完成更新'), 200  # 长度不够
    except Exception as e:
        return jsonify(code=404, msg=str(e)), 200  # 可能有用


@app.route('/todo', methods=['DELETE'])
def delete():  # 基本与update一致
    try:
        delete = request.get_json()
        id = delete.get('id')
        status = delete.get('status')
        all = delete.get('all')
        list_d = list(filter(None, [id, status, all]))

        if not list_d:
            return jsonify(code=404, msg='请输入一项参数以删除事项'), 200
        if list_d:
            if len(list_d) == 1:
                try:
                    result = delete0(id, status, all)
                    if result:
                        if result == 'id':
                            return jsonify(code=404, msg='删除失败，原因：该id不存在'), 200
                        if result == 'all':
                            return jsonify(code=404, msg='删除失败，原因：不存在任何事项'), 200
                        if result == '待办':
                            return jsonify(code=404, msg='删除失败，原因：不存在待办事项'), 200
                        if result == '已完成':
                            return jsonify(code=404, msg='删除失败，原因：不存在已完成事项'), 20
                        else:
                            return jsonify(code=200, msg='删除成功', data=result), 200
                    else:
                        return jsonify(code=404, msg=f'删除失败，原因：未知错误:{result}'), 200
                except Exception as e:
                    return jsonify(code=404, msg='删除失败，原因：' + str(e)), 200
            if len(list_d) > 1:
                return jsonify(code=404, msg='参数不得大于一项'), 200
    except Exception as e:
        return jsonify(code=404, msg=str(e)), 200


app.run()
