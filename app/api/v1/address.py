from app.libs.redprint import RedPrint
from flask import request, jsonify, g
from app.models.address import MemberAddress
from app.models.member import Member
from app import db
import json
api = RedPrint(name='address', description='订单视图')


@api.route('/add',methods=['POST'])
def add():
   resp = {'code': 1, 'msg': '成功', 'data': {}}
   member = g.member
   if not member:
      resp['code'] = -1
      resp['msg'] = '验证失败'
      return jsonify(resp)
   nickame = request.form.get('nickname')
   mobile = request.form.get('mobile')
   province_id = request.form.get('province_id')
   province_str = request.form.get('province_str')
   city_id = request.form.get('city_id')
   city_str = request.form.get('city_str')
   area_id = request.form.get('area_id')
   area_str = request.form.get('area_str')
   address = request.form.get('address')
   if not all([nickame,mobile,province_str,city_id]):
      resp['code'] = -1
      resp['msg'] = '参数不全'
      return jsonify(resp)
   memberaddress = MemberAddress()
   memberaddress.nickname = nickame
   memberaddress.mobile = mobile
   memberaddress.province_id = province_id
   memberaddress.province_str = province_str
   memberaddress.city_id = city_id
   memberaddress.city_str = city_str
   memberaddress.area_id = area_id
   memberaddress.area_str = area_str
   memberaddress.address = address
   memberaddress.member_id = member.id
   count = MemberAddress.query.filter_by(member_id=member.id,is_default=1).count()
   if count == 0:
      memberaddress.is_default = 1
   else:
      memberaddress.is_default = 0
   db.session.add(memberaddress)
   db.session.commit()
   return jsonify(resp)
@api.route('/list',methods=['GET','POST'])
def list():
    res = {'code': 1, 'msg': '成功', 'data': {}}
    token = request.headers.get('token')
    toke = token.split('#')
    if len(toke) != 2:
        res['code'] = -1
        res['msg'] = 'token错误'
        return jsonify(res)
    member = Member.query.get(toke[1])
    print(member,'========================',toke[1])
    if not member:
        res['code'] = -1
        res['msg'] = '用户未找到'
        return jsonify(res)
    addressList=[]
    memberaddress = MemberAddress.query.filter_by(member_id=member.id).all()
    for membe in memberaddress:
        temp_data={}
        temp_data['id'] = membe.id
        temp_data['name'] = membe.nickname
        temp_data['mobile'] = membe.mobile
        temp_data['detail'] = str(membe.province_str+membe.city_str+membe.area_str)
        addressList.append(temp_data)
        print(addressList)
    res['data']['addressList'] = addressList
    return jsonify(res)