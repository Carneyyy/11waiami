//获取应用实例
var app = getApp();

Page({
    data: {
        buyNumber:1,
        buyNumMin:1,
        buyNumMax:1,
        ids:[],
        id:1,
        address_id:0,
        not:'',
        goods_list: [
            // {
            //     id:22,
            //     name: "小鸡炖蘑菇",
            //     price: "85.00",
            //     pic_url: "/images/food.jpg",
            //     number: 1,
            // },
            // {
            //     id:22,]]/     price: "85.00",
            //     pic_url: "/images/food.jpg",
            //     number: 1,
            // }
        ],
        // default_address: {
        //     name: "编程浪子",
        //     mobile: "12345678901",
        //     detail: "上海市浦东新区XX",
        // },
        // yun_price: "1.00",
        // pay_price: "85.00",
        // total_price: "86.00",
        // params: null
    },
    onShow: function () {
        this.getOrder()


    },

    onLoad: function (options) {
        var ids = JSON.parse(options.ids);
        // console.log(ids);
        var that = this;
        that.setData({
            ids:ids,
        });
        this.getorderindex();
        // console.log(e);


    },
    getInput:function(e){
        this.setData({
            note:e.detail.value,
        })
    },
    createOrder: function (e) {
        var that = this;
        wx.request({
            url: app.buildUrl('/v1/order/create'),
            method: 'POST',
            data: {
                'ids': JSON.stringify(that.data.ids),
                'address_id':that.data.address_id,
                'note':that.data.note
            },
            header: app.getRequestHeader(),
            success(res) {
                if (res.data.code != 1) {
                    app.alert({'content': res.data.msg});
                    return
                }
                wx.redirectTo({
                    url: "/pages/my/order_list"
                });

            }
    })
},



    addressSet: function () {
        wx.navigateTo({
            url: "/pages/my/addressSet"
        });
    },
    selectAddress: function () {
        wx.navigateTo({
            url: "/pages/my/addressList"
        });
    },
    getOrderInfo:function(){
       var that = this;
       wx.request({
           url:app.buildUrl('v1/order/delete'),
           method:'POST',
           data:{
               ids:JSON.stringify(ids)
           },
           header:app.getRequestHeader(),
           success(res) {
               if(res.data.code =1){

               }
           }
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
    getorderindex:function () {
        var that = this;
        wx.request({
            url: app.buildUrl('/v1/order/index'),
            method: 'POST',
            data: {
                'ids': JSON.stringify(that.data.ids),
                // 'address_id':that.data.address_id,
                // 'note':that.data.note
            },
            header: app.getRequestHeader(),
            success(res) {
                if (res.data.code != 1) {
                    app.alert({'content': res.data.msg});
                    return
                }
                that.setData({
                    goods_list: res.data.data.goods_list,
                    default_address:res.data.data.default_address,
                    address_id:res.data.data.default_address.id,
                    yun_price: res.data.data.yun_price,
                    pay_price:res.data.data.pay_price,
                    total_price: res.data.data.total_price,
                    params: null
                });
            }
        })

    },
    getOrder: function () {
        var that = this;
        wx.request({
            url: app.buildUrl('/v1/order/purchase'),
            method: 'GET',
            data: {
                'id': that.data.id,
                'num': that.data.buyNumber,
            },
            header: app.getRequestHeader(),
            success(res) {
                if (res.data.code != 1) {
                    app.alert({'content': res.data.msg});
                    return
                }
                that.setData({
                    goods_list: res.data.data.goods_list,
                    default_address: res.data.data.default_address,
                    address_id: res.data.data.default_address.id,
                    yun_price: res.data.data.yun_price,
                    pay_price: res.data.data.pay_price,
                    total_price: res.data.data.total_price,
                    params: null
                });
            }
        });
    }

});
