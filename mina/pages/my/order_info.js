var app = getApp();
Page({
    data: {},
    onLoad: function (e) {
        var that = this;
        that.getOrderDetail()
    },
    onShow: function () {

        // var that = this;
        // that.setData({
        //     info: {
        //         order_sn:"123123",
        //         status: -8,
        //         status_desc: "待支付",
        //         deadline:"2018-07-31 12:00",
        //         pay_price: "85.00",
        //         yun_price: 0.00,
        //         total_price: "85.00",
        //         address: {
        //             name: "编程浪子",
        //             mobile: "12345678901",
        //             address: "上海市浦东新区XX"
        //         },
        //         goods: [
        //             {
        //                 name: "小鸡炖蘑菇",
        //                 price: "85.00",
        //                 unit: 1,
        //                 pic_url: "/images/food.jpg"
        //             },
        //             {
        //                 name: "小鸡炖蘑菇",
        //                 price: "85.00",
        //                 unit: 1,
        //                 pic_url: "/images/food.jpg"
        //             }
        //         ]
        //     }
        // });
    },
    getOrderDetail:function () {
        var that = this;
        wx.request({
          url:app.buildUrl('/v1/order_list/detail'),
          method:'GET',
          header:app.getRequestHeader(),
          success(res) {
            console.log(res.data);
            if (res.data.code == -1){
                app.alert({
                    'content':res.data.msg
                })
            }
              that.setData({
                 info:res.data.data.order_list
              })
            }
        })
    }
});