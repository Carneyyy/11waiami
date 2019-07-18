from app.libs.redprint import RedPrint
from flask import request, jsonify, g
from app.models.order import PayOrder, PayOrderItem
from app.models.food import Food
from app.utils.common import buildPicUrl
from app.models.address import MemberAddress

api = RedPrint(name='order_list', description='订单列表')
@api.route('/index', methods=['POST','GET'])
def list():
    res = {'code': 1, 'msg': '成功', 'data': {}}

    member = g.member
    if not member:
        res['code'] = -1
        res['msg'] = '该用户不存在'
        return jsonify(res)

    # // ["待付款", "待发货", "待收货", "待评价", "已完成", "已关闭"]
    # // ["-8", "-7", "-6", "-5", "1", "0"]

    status = request.args.get('status')
    print(status, '----------------------------')

    order_list = []
    payorders = PayOrder.query.filter_by(member_id=member.id, status=status).all()
    for payorder in payorders:
        temp_data = {}
        temp_data['status'] = payorder.status
        temp_data['status_desc'] = payorder.status_desc
        temp_data['date'] = payorder.create_time.strftime('%Y-%m-%d %H:%M:%S')
        temp_data['note'] = payorder.note
        temp_data['total_price'] = str(payorder.total_price)
        temp_data['order_number'] = payorder.create_time.strftime('%Y%m%d%H%M%S') + str(payorder.id).zfill(5)
        goods_list = []

        # 查订单商品
        payorderitems = PayOrderItem.query.filter_by(pay_order_id=payorder.id).all()
        for payorderitem in payorderitems:
            food = Food.query.get(payorderitem.food_id)
            temp_food = {}
            temp_food['pic_url'] = buildPicUrl(food.main_image)

            goods_list.append(temp_food)

        temp_data['goods_list'] = goods_list
        order_list.append(temp_data)

    res['data']['order_list'] = order_list
    return jsonify(res)
@api.route('/detail', methods=['POST','GET'])
def detail():
    res = {'code': 1, 'msg': '成功', 'data': {}}
    member = g.member
    if not member:
        res['code'] = -1
        res['msg'] = '该用户不存在'
        return jsonify(res)
    status = request.args.get('status')
    print(status,'====================================================================================')
    ordr_list = []
    payorders = PayOrder.query.filter_by(member_id=member.id, status=status).all()
    for payorder in payorders:
        temp_data = {}
        temp_data['order_sn'] = payorder.order_sn
        temp_data['status'] = payorder.status
        temp_data['status_desc'] = payorder.status_desc
        temp_data['deadline'] = payorder.create_time.strftime('%Y-%m-%d %H:%M:%S')
        temp_data['pay_price'] = str(payorder.pay_price)
        temp_data['yun_price'] = str(payorder.yun_price)
        temp_data['total_price'] = str(payorder.total_price)
        memberaddress=MemberAddress.query.filter_by(id=payorder.express_address_id).first()
        address = {}
        address['name'] = memberaddress.nickname
        address['mobile'] = memberaddress.mobile
        address['address'] = str(memberaddress.province_str+memberaddress.city_str+memberaddress.area_str)
        temp_data['address'] = address
        goods = []
        payorderitems = PayOrderItem.query.filter_by(pay_order_id=payorder.id).all()
        for payorderitem in payorderitems:
            food = Food.query.get(payorderitem.food_id)
            temp_food = {}
            temp_data['name'] = food.name
            temp_data['price'] = str(food.price)
            temp_data['unit'] = payorderitem.quantity
            temp_data['pic_url'] = buildPicUrl(food.main_image)
            goods.append(temp_food)
        temp_data['goods'] = goods
        ordr_list.append(temp_data)
    res['data']['order_list'] = ordr_list
    return jsonify(res)
