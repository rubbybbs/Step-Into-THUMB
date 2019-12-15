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

  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    console.log("login")
    if (app.globalData.flag==true) {
      wx.reLaunch({
        url: '../index/index',
      })
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
    console.log("login")
    if (app.globalData.flag == true) {
      wx.reLaunch({
        url: '../index/index',
      })
    }
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
    wx.login({
      success: function(res) {
        if (res.code) {
          wx.request({
            url: 'http://127.0.0.1:8000/Step-Into-THUMB/candidate/register',
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
                console.log("set true")
                app.globalData.flag = true;
                setTimeout(function () {
                  wx.navigateBack({
                    url: '../index/index',
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