// pages/login/login.js
const app = getApp()

// 打开调试
wx.setEnableDebug({
  enableDebug: true
})


Page({

  /**
   * 页面的初始数据
   */
  data: {
    next: 'index'
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    console.log(options)
    this.data.next = options.next
    console.log('login next', this.data.next)
    if (!this.data.next) {
      this.data.next = 'index';
    }
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
    console.log("navigateto login")
    app.globalData.flag = false;
    /*wx.checkSession({
      success: function () {
        console.log("login success")
        wx.request({
          url: app.globalData.serveraddr + '/Step-Into-THUMB/candidate/register',
          method: 'POST',
          data: {
            code: res.code
          },
          success: function (res) {
            wx.setStorageSync('key', res.data.session)
            app.globalData.flag = true;
          }
        })
        app.globalData.flag = true;
      },
      fail: function () {
        console.log("login fail")
        app.globalData.flag = false;
      }
    })*/
    console.log('../' + this.data.next + '/' + this.data.next)
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  },

  getUserInfo: function (e) {
    
    /*app.globalData.userInfo = e.detail.userInfo
    if (app.globalData.userInfo) {
      wx.navigateBack({
        url: '../index/index',
      })
    }*/
    let _this = this;
    wx.login({
      success: function(res) {
        if (res.code) {
          wx.setStorageSync('code', res.code)
          wx.request({
            url: app.globalData.serveraddr + '/Step-Into-THUMB/candidate/register',
            method: 'POST',
            data: {
              code: res.code
            },
            success: function (res) {
              console.log(res)
              if (res.data.session) {
                console.log("登录成功")
                wx.showToast({
                  title: '登录成功',
                  icon: 'success',
                  duration: 500
                });
                wx.setStorageSync('key', res.data.session)
                console.log("set true", '../' + _this.data.next + '/' + _this.data.next)
                app.globalData.flag = true;
                setTimeout(function () {
                  wx.redirectTo({
                    url: '../' + _this.data.next + '/' + _this.data.next
                  })
                }, 500)
              }
              else {
                console.log("登陆失败")
              }
            },
            fail: function () {
              console.log("登陆失败")
            }
          })
        }
        else {
          console.log("no respones")
        }
      },
      fail: function(res){
        console.log(res)
      }
    })
  }
})