//index.js
//获取应用实例
var app = getApp();
var WxParse = require('../../wxParse/wxParse.js');

Page({
    data: {
        autoplay: true,
        interval: 3000,
        duration: 1000,
        swiperCurrent: 0,
        hideShopPopup: true,
        buyNumber: 1,
        buyNumMin: 1,
        buyNumMax: 1,
        canSubmit: false, //  选中时候是否允许加入购物车
        shopCarInfo: {},
        shopType: "addShopCar",//购物类型，加入购物车或立即购买，默认为加入购物车,
        id: 0,
        shopCarNum: 4,
        commentCount: 2
    },
    onLoad: function (e) {
        console.log(e.id);
        var that = this;
        that.setData({
            'id': e.id,
            // "info": {
            //     "id": 1,
            //     "name": "小鸡炖蘑菇",
            //     "summary": '<p>多色可选的马甲</p><p><img src="http://www.timeface.cn/uploads/times/2015/07/071031_f5Viwp.jpg"/></p><p><br/>相当好吃了</p>',
            //     "total_count": 2,
            //     "comment_count": 2,
            //     "stock": 2,
            //     "price": "80.00",
            //     "main_image": "/images/food.jpg",
            //     "pics": [ '/images/food.jpg','/images/food.jpg' ]
            // },
            // buyNumMax: 2,
            commentList: [
                {
                    "score": "好评",
                    "date": "2017-10-11 10:20:00",
                    "content": "非常好吃，一直在他们加购买",
                    "user": {
                        "avatar_url": "/images/more/logo.png",
                        "nick": "angellee 🐰 🐒"
                    }
                },
                {
                    "score": "好评",
                    "date": "2017-10-11 10:20:00",
                    "content": "非常好吃，一直在他们加购买",
                    "user": {
                        "avatar_url": "/images/more/logo.png",
                        "nick": "angellee 🐰 🐒"
                    }
                }

            ]
        });
        this.getInfo()
        // WxParse.wxParse('article', 'html', that.data.info.summary, that, 5);
    },
    goShopCar: function () {
        wx.reLaunch({
            url: "/pages/cart/index"
        });
    },
    toAddShopCar: function () {
        this.setData({
            shopType: "addShopCar"
        });
        this.bindGuiGeTap();
    },
    tobuy: function () {
        this.setData({
            shopType: "tobuy"
        });
        this.bindGuiGeTap();
    },
    addShopCar: function () {
        var that = this
        wx.request({
            // url:'http://127.0.0.1:5000/api/v1/cart/add',
            url: app.buildUrl('/v1/cart/add'),
            method: 'POST',
            data: {
                'id': that.data.id,
                'num': that.data.buyNumber,
                'type':1,
            },
            header: app.getRequestHeader(),
            success(res) {
                console.log(res.data.data.info);
                if (res.data.code == 0) {
                    app.alert({'content': res.data.msg})
                    return
                }
                app.alert({
                    'content':res.data.msg});
                that.closePopupTap()
                // that.setData({
                //
                //     info: res.data.data.info,
                //     buyNumMax: res.data.data.info.stock,
                // })
                // WxParse.wxParse('article', 'html', that.data.info.summary, that, 5);
            }
        })
    },
    buyNow: function () {
        // var that = this;
        // wx.request({
        //     url: app.buildUrl('/v1/order/purchase'),
        //     method: 'GET',
        //     data: {
        //         'id': that.data.id,
        //         'num': that.data.buyNumber,
        //     },
        //     header: app.getRequestHeader(),
        //     success(res) {
        //         if (res.data.code != 1) {
        //             app.alert({'content': res.data.msg});
        //             return
        //         }
                wx.redirectTo({
                    url: "/pages/order/index?id="+this.data.id+"&num="+this.data.buyNumber
                });
                // that.setData({
                //     goods_list: res.data.data.goods_list,
                //     default_address:res.data.data.default_address,
                //     address_id:res.data.data.default_address.id,
                //     yun_price: res.data.data.yun_price,
                //     pay_price:res.data.data.pay_price,
                //     total_price: res.data.data.total_price,
                //     params: null
        //         // });
        //     }
        // });

},

    /**
     * 规格选择弹出框
     */
    bindGuiGeTap: function () {
        this.setData({
            hideShopPopup: false
        })
    },
    /**
     * 规格选择弹出框隐藏
     */
    closePopupTap: function () {
        this.setData({
            hideShopPopup: true
        })
    },
    numJianTap: function () {
        if (this.data.buyNumber <= this.data.buyNumMin) {
            return;
        }
        var currentNum = this.data.buyNumber;
        currentNum--;
        this.setData({
            buyNumber: currentNum
        });
    },
    numJiaTap: function () {
        if (this.data.buyNumber >= this.data.buyNumMax) {
            return;
        }
        var currentNum = this.data.buyNumber;
        currentNum++;
        this.setData({
            buyNumber: currentNum
        });
    },
    //事件处理函数
    swiperchange: function (e) {
        this.setData({
            swiperCurrent: e.detail.current
        })
    },
    getInfo: function () {
        var that = this;
        wx.request({
            // url:'http://127.0.0.1:5000/api/v1/food/info',
            url: app.buildUrl('/v1/food/info'),
            method: 'GET',
            data: {
                'id': that.data.id,
            },
            header: app.getRequestHeader(),

            success(res) {
                console.log(res.data.code)
                if (res.data.code == -1) {
                    app.alert({
                        'content': res.data.msg
                    })
                }
                that.setData({
                    info: res.data.data.info,
                    buyNumMax: res.data.data.info.stock,
                })
                WxParse.wxParse('article', 'html', that.data.info.summary, that, 5);
            }
        })
    }
});
