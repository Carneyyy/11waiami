from app.libs.redprint import RedPrint
from flask import request, jsonify, json, g
from app.models.cart import MemberCart
from app.models.food import Food
from app.utils.common import buildPicUrl
from app.models.address import MemberAddress
from app import db
from app.models.order import PayOrder, PayOrderItem
import hashlib, time, random

api = RedPrint(name='order', description='订单模块')

@api.route('/index', methods=['POST'])
def index():
    res = {'code': 1, 'msg': '成功', 'data': {}}
    ids = request.form.get('ids')
    note = request.form.get('note')
    member = g.member
    if not member:
        res['code'] = -1
        res['msg'] = '该用户不存在'
        return jsonify(res)
    ids = json.loads(ids)
    goods_list = []
    yun_price = 0
    pay_price = 0
    for id in ids:
        temp_data = {}
        membercart = MemberCart.query.filter_by(food_id=id, member_id=member.id).first()
        food = Food.query.get(id)
        temp_data['id'] = id
        temp_data['name'] = food.name
        temp_data['price'] = str(food.price)
        temp_data['pic_url'] = buildPicUrl(food.main_image)
        temp_data['number'] = membercart.quantity
        goods_list.append(temp_data)

        pay_price += membercart.quantity * food.price

    address = MemberAddress.query.filter_by(member_id=member.id, is_default=1).first()
    default_address = {}
    default_address['id'] = address.id
    default_address['name'] = address.nickname
    default_address['mobile'] = address.mobile
    default_address['detail'] = str(address.province_str + address.city_str + address.area_str)
    total_price = yun_price + pay_price
    res['data']['goods_list'] = goods_list
    res['data']['default_address'] = default_address
    res['data']['total_price'] = str(total_price)
    res['data']['yun_price'] = str(yun_price)
    res['data']['pay_price'] = str(pay_price)
    return jsonify(res)


@api.route('/create', methods=['POST'])
def create():
    res = {'code': 1, 'msg': '成功', 'data': {}}
    # try:
    member = g.member
    if not member:
        res['code'] = -1
        res['msg'] = '该用户不存在'
        return jsonify(res)
    ids = request.form.get('ids')
    address_id = request.form.get('address_id')
    note = request.form.get('note')
    ids = json.loads(ids)
    pay_price = 0
    yun_price = 0
    for id in ids:
        membercart = MemberCart.query.filter_by(food_id=id, member_id=member.id).first()
        if not membercart:
            continue
        food = Food.query.get(id)

        if not food or food.status != 1:
            continue

        pay_price += food.price * membercart.quantity
    memberaddress = MemberAddress.query.get(address_id)
    if not memberaddress:
        res['code'] = -1
        res['msg'] = '该地址不存在'
        return jsonify(res)
    payorder = PayOrder()
    payorder.order_sn = geneOrderSn()
    payorder.total_price = yun_price + pay_price
    payorder.yun_price = yun_price
    payorder.pay_price = pay_price
    payorder.note = note
    payorder.status = -8
    payorder.express_status = -1
    payorder.express_address_id = address_id
    payorder.express_info = memberaddress.showAddress()
    payorder.comment_status = -1
    payorder.member_id = member.id

    db.session.add(payorder)

    foods = db.session.query(Food).filter(Food.id.in_(ids)).with_for_update().all()
    temp_stock = {}
    for food in foods:
        temp_stock[food.id] = food.stock
    # time.sleep(50)
    for id in ids:
        membercart = MemberCart.query.filter_by(food_id=id, member_id=member.id).first()
        if membercart.quantity > temp_stock[id]:
            res['code'] = -1
            res['msg'] = '库存不足'
            return jsonify(res)
        food = db.session.query(Food).filter(Food.id == id).update({
            'stock': temp_stock[id] - membercart.quantity
        })
        if not food:
            raise Exception('更新失败')
        food = Food.query.get(id)

        payorderitem = PayOrderItem()
        payorderitem.quantity = membercart.quantity
        payorderitem.price = food.price
        payorderitem.note = note
        payorderitem.status = 1
        payorderitem.pay_order_id = payorder.id
        payorderitem.member_id = member.id
        payorderitem.food_id = id
        db.session.add(payorderitem)
        db.session.delete(membercart)
    db.session.commit()
    return jsonify(res)
    # except Exception as e:
    #     print(e,'-----------')
    #     db.session.rollback()
    #     res['code'] = -1
    #     res ['msg'] = '出现异常'
    #     return jsonify(res)


import hashlib
import random


def geneOrderSn():
    m = hashlib.md5()
    sn = None
    while True:
        str = "%s-%s" % (int(round(time.time() * 1000)), random.randint(0, 9999999))
        m.update(str.encode("utf-8"))
        sn = m.hexdigest()
        if not PayOrder.query.filter_by(order_sn=sn).first():
            break
    return sn

@api.route('/purchase',methods=['POST','GET'])
def purchase():
    res = {'code': 1, 'msg': '成功', 'data': {}}
    ids = request.args.get('id')
    print('======================================================',ids)
    num = request.args.get('num')
    print('=======================================================',type(num))
    num = int(num)
    member = g.member
    if not member:
        res['code'] = -1
        res['msg'] = '该用户不存在'
        return jsonify(res)
    goods_list = []
    yun_price = 0
    pay_price = 0
    temp_data = {}
    # membercart = MemberCart.query.filter_by(food_id=id,member_id=member.id).first()
    food = Food.query.get(ids)
    temp_data['id'] = ids
    temp_data['name'] = food.name
    temp_data['price'] = str(food.price)
    temp_data['pic_url'] = buildPicUrl(food.main_image)
    temp_data['number'] = num
    goods_list.append(temp_data)
    pay_price += num * food.price
    address = MemberAddress.query.filter_by(member_id=member.id, is_default=1).first()
    default_address = {}
    default_address['id'] = address.id
    default_address['name'] = address.nickname
    default_address['mobile'] = address.mobile
    default_address['detail'] = address.showAddress()
    total_price = yun_price + pay_price
    res['data']['goods_list'] = goods_list
    res['data']['default_address'] = default_address
    res['data']['total_price'] = str(total_price)
    res['data']['yun_price'] = str(yun_price)
    res['data']['pay_price'] = str(pay_price)
    return jsonify(res)

