// pages/form/form.js


Page({

  /**
   * 页面的初始数据
   */
  data: {
    ques: [],
  },
  initForm(form) {
    
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    let _this = this
    wx.request({
      url: 'http://127.0.0.1:8000/Step-Into-THUMB/candidate/get-empty-form', //仅为示例，并非真实的接口地址
      header: {
        'content-type': 'application/json'
      },
      success: function (res) {
        //console.log(res.data["form"])]
        let Form = JSON.parse(res.data["form"])
        console.log(Form)
        let gen = []
        for (let x in Form['question']) {
          console.log(Form['question'][x])
          let ques = Form['question'][x]
          gen.push(ques)
        }
        console.log(gen)
        _this.setData({
          ques: gen
        })
      }
    })
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

  formSubmit: function (e) {
    console.log(e)
  }
})
