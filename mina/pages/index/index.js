//login.js
//获取应用实例
var app = getApp();
Page({
  data: {
    remind: '加载中',
    angle: 0,
    userInfo: {},
    islogin: false
  },
  goToIndex: function () {
    wx.switchTab({
      url: '/pages/food/index',
    });
  },
  onLoad: function () {
    wx.setNavigationBarTitle({
      title: app.globalData.shopName
    });
    //检查是否登录
    this.checkLogin()
  },
  onShow: function () {

  },
  onReady: function () {
    var that = this;
    setTimeout(function () {
      that.setData({
        remind: ''
      });
    }, 1000);
    wx.onAccelerometerChange(function (res) {
      var angle = -(res.x * 30).toFixed(1);
      if (angle > 14) {
        angle = 14;
      } else if (angle < -14) {
        angle = -14;
      }
      if (that.data.angle !== angle) {
        that.setData({
          angle: angle
        });
      }
    });
  },
  bindGetUserInfo (e) {
    wx.login({
        success (res) {
            if (res.code) {
                console.log(e.detail.userInfo);
                var nickname = e.detail.userInfo.nickName;
                var avatarurl = e.detail.userInfo.avatarUrl;
                var gender = e.detail.userInfo.gender;
            //发起网络请求
              wx.request({
                url:app.buildUrl("/v1/member/login"),
                data: {
                  nickname: nickname,
                  avatarurl: avatarurl,
                  gender: gender,
                  code: res.code,
            },
            method: 'POST',
            header: app.getRequestHeader(),
            success(res) {
              console.log(res.data);
              if (res.data.code == 1){
                app.setToken('token',res.data.data.token);
                wx.switchTab({
                   url:'/pages/food/index',
                });
              }
            }
          })
        } else {
          console.log('登录失败！' + res.errMsg)
        }
      }
    })
  },
  checkLogin:function () {
    var that = this;
    wx.login({
      success(res){
        if ( res.code){
        wx.request({
          url:app.buildUrl('/v1/member/cklogin'),
          data:{
            code:res.code,
          },
          method:'POST',
          header:app.getRequestHeader(),
          success(res) {
            console.log(res.data);
            if (res.data.code == -1){
                app.alert({
                    'content':res.data.msg
                })
            }
              app.setToken('token',res.data.data.token);
              that.setData({
                islogin:true
              })
            }
        })
      }else{
          console.log('登录失败' + res.errMsg)
        }
      }
    })
  }
});
