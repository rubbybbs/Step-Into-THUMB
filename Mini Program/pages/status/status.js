// pages/status/status.js
const app = getApp()

Page({

  /**
   * 页面的初始数据
   */
  data: {
    status: '',
    activeNum: 0,
    steps: [{ 'stepName': '报名表填写', 'stepCont': '请填写报名表' }, { 'stepName': '面试中', 'stepCont': '' }, { 'stepName': '面试结束', 'stepCont': '' }, { 'stepName': '面试结果', 'stepCont': ''}]
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
    console.log('navigateto status')
    let _this = this
    let session = wx.getStorageSync('key')
    console.log('session=', session)
    if (session) {
      wx.request({
        url: app.globalData.serveraddr + '/Step-Into-THUMB/candidate/get-status?session=' + session,
        method: "GET",
        header: {
          'content-type': 'application/json'
        },
        success: function (res) {
          console.log(res);
          console.log(res.data.status)
          _this.setData({
            activeNum: res.data.stage
          })
          let newsteps = _this.data.steps;
          for (let i=0; i<=_this.data.activeNum; i++) {
            if (i<=2) {
              newsteps[i].stepCont = res.data.status[i];
            }
            else {
              newsteps[i].stepCont = res.data.content;
            }
          }
          _this.setData({
            steps: newsteps
          })
          _this.setData({
            status: res.data.status
          })
        },
        fail: function (res) {
          console.log('get status fail')
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