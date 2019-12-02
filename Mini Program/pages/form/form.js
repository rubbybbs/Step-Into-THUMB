// pages/form/form.js


Page({

  /**
   * 页面的初始数据
   */
  data: {
    questions: [],
  },

  initForm(form) {
    
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    let _this = this
    wx.request({
      url: 'http://127.0.0.1:8000/Step-Into-THUMB/candidate/get-empty-form', 
      header: {
        'content-type': 'application/json'
      },
      success: function (res) {
        //console.log(res.data["form"])]
        let Form = JSON.parse(res.data["form"]);
        console.log(Form);
        let gen = [];
        for (let x in Form['question']) {
          console.log(Form['question'][x])
          let ques = Form['question'][x];
          if (ques.type=="Choice") {
            ques["changeFunc"] = "bindChange" + x;
            ques["ChoiceIndex"] = 1;
            ques["ChoicesArray"] = [];
            for (let item in ques.Choices) {
              console.log("!", ques.Choices[item]);
              ques.ChoicesArray.push(ques.Choices[item].Choice);
            }
            console.log(ques.Choices)
            
            _this[ques["changeFunc"]] = function(e) {
              console.log(e)
              console.log(ques.name, '发生选择改变，携带值为', e.detail.value);
              let tmp = this.data.questions;
              tmp[x]["ChoiceIndex"] = e.detail.value;
              _this.setData({
                questions: tmp
              })
              // console.log(_this.data.questions[x].ChoicesArray)
              /*
              let tmp = "bindChange" + x
              _this.setData({
                [tmp]: e.detail.value
              });*/
            }
            console.log("changeFunc", "bindChange" + x)
          }
          

          gen.push(ques)
        }
        console.log("gen",gen)
        _this.setData({
          questions: gen
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

  bindChange0: function (e) {
    console.log(e)
    console.log('picker country 发生选择改变，携带值为', e.detail.value);
    
    
  },

  formSubmit: function (e) {
    let question = []
    for (let x in this.data.questions) {
      console.log(this.data.questions[x])
      let q = this.data.questions[x]
      if(q.type == "Blank"){
        q.answer = e.detail.value[q.name]
        question.push(q)
      }
      else if (q.type == "Choice") {
        question.push(
          {
            name: q.name,
            type: q.type,
            answer: q.ChoicesArray[q.ChoiceIndex]
          }
        )
      }
      
    }
    
    let session = wx.getStorageSync('key')
    wx.request({
      url: 'http://127.0.0.1:8000/Step-Into-THUMB/candidate/submit-application?session='+session, 
      method: 'POST',
      data:{
        question
      },
      header: {
        'content-type': 'application/json'
      },
      success: function (res) {
        console.log(res)
      }
    })
  },


})
