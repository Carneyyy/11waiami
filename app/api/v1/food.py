from app.libs.redprint import RedPrint
from flask import request, jsonify
from app.utils.common import buildPicUrl
from app.models.food import Category, Food

api = RedPrint('food', description='食品模块')
"""

"""


@api.route('/search')
def search():
    res = {'code': 1, 'msg': '成功', 'data': {}}
    categories = []
    categorys = Category.query.filter(Category.status == 1).order_by(Category.weight.desc()).all()
    categories.append({
        "id": 0,
        "name": "全部"
    })
    for category in categorys:
        temp_data = {}
        temp_data['id'] = category.id
        temp_data['name'] = category.name
        categories.append(temp_data)
    res['data']['categories'] = categories

    foods = []
    all_foods = Food.query.filter(Food.status == 1).order_by(Food.month_count.desc()).limit(3).all()
    for food in all_foods:
        temp_data = {}
        temp_data['id'] = food.id
        temp_data['pic_url'] = buildPicUrl(food.main_image)
        foods.append(temp_data)
    res['data']['banners'] = foods

    return jsonify(res)


@api.route('/all')
def all():
    res = {'code': 1, 'msg': '成功', 'data': {}}
    try:
        cid = request.values.get('cid')
        page = request.values.get('page')
        if not page:
            page = '1'
        cid = int(cid)
        page = int(page)
        pagesize = 1
        offset = (page - 1) * pagesize
        goods = []
        # if not cid or cid == '0':
        #     all_good = Food.query.offset(offset).limit(pagesize).all()
        #
        # else:
        #     all_good = Food.query.filter_by(cat_id=cid).all()
        query = Food.query.filter_by(status=1)
        if cid == 0:
            all_good = query.all()
        else:
            all_good = query.filter_by(cat_id = cid).all()
        for good in all_good:
            temp_data = {}
            temp_data['id'] = good.id
            temp_data['name'] = good.name
            temp_data['min_price'] = str(good.price)
            temp_data['price'] = str(good.price)
            temp_data['pic_url'] = buildPicUrl(good.main_image)
            goods.append(temp_data)
        res['data']['goods'] = goods
        if len(all_good) < pagesize:
            res['data']['ismore'] = 0
        else:
            res['data']['ismore'] = 1
        return jsonify(res)

    except Exception as e:
        res['code'] = -1
        res['msg'] = '参数错误'
        return jsonify(res)


@api.route('/info')
def info():
    res = {'code': 1, 'msg': '成功', 'data': {}}
    try:
        id = request.args.get('id')
        if not id:
            res['code'] = -1
            res['msg'] = '参数有误222222'
            return jsonify(res)
        id = int(id)
        if id <= 0:
            res['code'] = -1
            res['msg'] = '参数有误11111'
            return jsonify(res)
        food = Food.query.get(id)
        info = {}
        info['id'] = food.id
        info['name'] = food.name
        info['summary'] = food.summary
        info['total_count'] = food.total_count
        info['comment_count'] = food.comment_count
        info['stock'] = food.stock
        info['price'] = str(food.price)
        info['main_image'] = buildPicUrl(food.main_image)
        info['pics'] = [buildPicUrl(food.main_image), buildPicUrl(food.main_image), buildPicUrl(food.main_image)]
        res['data']['info'] = info
        return jsonify(res)
    except Exception as e:
        print('hhahahhahahahhahahaha', e ,'==========================================')
        res['code'] = -1
        res['msg'] = '参数错误======================================'
        return jsonify(res)
