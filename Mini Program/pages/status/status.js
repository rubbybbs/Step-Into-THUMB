// pages/status/status.js
const app = getApp()

Page({

  /**
   * 页面的初始数据
   */
  data: {
    status: ''
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    /*let _this = this
    let session = wx.getStorageSync('key')
    if (session) {
      wx.request({
        url: app.globalData.serveraddr + '/Step-Into-THUMB/candidate/get-status?session=' + session,
        method: "GET",
        header: {
          'content-type': 'application/json'
        },
        success: function (res) {
          console.log(res);
        }
      })
    }
    else {
      app.globalData.flag = false;
      wx.navigateTo({
        url: '../login/login',
      })
    }*/
    
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
    let _this = this
    wx.checkSession({
      success: function () {
        console.log("success")
        app.globalData.flag = true;
      },
      fail: function () {
        app.globalData.flag = false;
      }
    })
    if (!app.globalData.flag) {
      wx.navigateTo({
        url: '../login/login',
      })
    }
    let session = wx.getStorageSync('key')
    if (session) {
      wx.request({
        url: app.globalData.serveraddr + '/Step-Into-THUMB/candidate/get-status?session=' + session,
        method: "GET",
        header: {
          'content-type': 'application/json'
        },
        success: function (res) {
          console.log(res);
          _this.setData({
            status: res.data.status
          })
        }
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

  }
})