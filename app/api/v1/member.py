from app.libs.redprint import RedPrint
from flask import request, jsonify, current_app
from app import db
from app.service.memberService import memberService
from app.models.member import Member, OauthMemberBind

api = RedPrint('member', description='会员模块')


@api.route('/login', methods=['POST'])
def login():
    res = {'code': 1, 'msg': '成功', 'data': {}}
    nickname = request.form.get('nickname')
    avatarurl = request.form.get('avatarurl')
    gender = request.form.get('gender')
    code = request.form.get('code')
    print(nickname, avatarurl, gender, code)
    if len(code) < 1:
        res['code'] = -1
        res['msg'] = 'code错误'
        return jsonify(res)

    if not all([nickname, avatarurl, gender, code]):
        res['code'] = -1
        res['msg'] = '参数错误'
        return jsonify(res)

    open_id = memberService.getOpenid(code)
    if not open_id:
        res['code'] = -1
        res['msg'] = '获取openid出错'
        return jsonify(res)
    oauthmemberbind = OauthMemberBind.query.filter_by(openid=open_id).first()
    if not oauthmemberbind:
        member = Member()
        member.nickname = nickname
        member.avatar = avatarurl
        member.gender = gender
        member.salt = memberService.getSalt()
        db.session.add(member)
        db.session.commit()

        oauthmemberbind = OauthMemberBind()
        oauthmemberbind.openid = open_id
        oauthmemberbind.client_type = 'wx'
        oauthmemberbind.type = 1
        oauthmemberbind.member_id = member.id

        db.session.add(oauthmemberbind)
        db.session.commit()

    member = Member.query.get(oauthmemberbind.member_id)
    token = "%s#%s" % (memberService.geneAuthCode(member), member.id)
    res['data']['token'] = token
    return jsonify(res)


@api.route('/cklogin', methods=['POST'])
def cklogin():
    res = {'code': 1, 'msg': '成功', 'data': {}}
    code = request.form.get('code')
    if len(code) < 1:
        res['code'] = -1
        res['msg'] = 'code错误'
        return jsonify(res)

    open_id = memberService.getOpenid(code)
    print('====================', open_id)
    if not open_id:
        res['code'] = -1
        res['msg'] = '获取openid出错'
        return jsonify(res)
    oauthmemberbind = OauthMemberBind.query.filter_by(openid=open_id).first()

    if not oauthmemberbind:
        res['code'] = -1
        res['msg'] = '用户不存在'
        return jsonify(res)

    member = Member.query.get(oauthmemberbind.member_id)
    token = "%s#%s" % (memberService.geneAuthCode(member), member.id)
    res['data']['token'] = token
    return jsonify(res)
