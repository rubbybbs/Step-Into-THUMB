//index.js
//获取应用实例
const app = getApp()

Page({
  data: {
    motto: 'Hello World',
    userInfo: {},
    hasUserInfo: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo')
  },
  //事件处理函数
  bindViewTap: function() {
    wx.navigateTo({
      url: '../logs/logs'
    })
  },
  bindFillForm: function() {
    wx.navigateTo({
      url: '../form/form',
    })
  },
  bindStatus: function() {
    wx.navigateTo({
      url: '../status/status',
    })
  },
  onLoad: function () {
    if (app.globalData.userInfo==null) {
      wx.navigateTo({
        url: '../login/login',
      })
    }
    this.setData({
      userInfo: app.globalData.userInfo,
      hasUserInfo: true
    })
  },
  onShow: function () {
    if (app.globalData.userInfo == null) {
      wx.navigateTo({
        url: '../login/login',
      })
    }
    this.setData({
      userInfo: app.globalData.userInfo,
      hasUserInfo: true
    })
  },
  getUserInfo: function(e) {
    console.log(e)
    app.globalData.userInfo = e.detail.userInfo
    this.setData({
      userInfo: e.detail.userInfo,
      hasUserInfo: true
    })
  }
})
