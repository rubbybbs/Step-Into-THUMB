// pages/form/form.js
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
    questions: [],
  },

  initForm(form) {
    
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    
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
    console.log('nvigateto form')
    let _this = this
    let session = wx.getStorageSync('key')
    wx.request({
      url: app.globalData.serveraddr + '/Step-Into-THUMB/candidate/get-empty-form?session=' + session,
      header: {
        'content-type': 'application/json'
      },
      success: function (res) {
        console.log(res);
        if (!res.data["form"]) {
          wx.showToast({
            title: res.data.msg
          });
          setTimeout(function () {
            wx.navigateBack({
              url: '../index/index',
            })
          }, 500);
        }
        let Form = JSON.parse(res.data["form"]);
        console.log(Form['question']);
        let gen = [];
        for (let x in Form['question']) {
          console.log(Form['question'][x])
          let ques = Form['question'][x];
          if (ques.type == "Choice") {
            ques["changeFunc"] = "bindChange" + x;
            ques["ChoiceIndex"] = 0;
            ques["ChoicesArray"] = [];
            for (let item in ques.Choices) {
              ques.ChoicesArray.push(ques.Choices[item].Choice);
            }
            console.log(ques.Choices)

            _this[ques["changeFunc"]] = function (e) {

              let tmp = this.data.questions;
              tmp[x]["ChoiceIndex"] = e.detail.value;
              _this.setData({
                questions: tmp
              })

            }

          }
          gen.push(ques)
        }
        console.log("gen", gen)
        _this.setData({
          questions: gen
        })
        //请求允许发送服务通知
        wx.requestSubscribeMessage({
          tmplIds: ['AdymfH-LXIsQlfV8VKJ7fnq5gAJjdayvD4Zo_58PfYw',],
          success: function (res) {
            console.log('success', res['AdymfH-LXIsQlfV8VKJ7fnq5gAJjdayvD4Zo_58PfYw'])
          },
          fail: function (res) {
            console.log('fail', res.errMsg)
          }
        });
      },
      fail: function () {
        console.log("failed get-empty-form")
        wx.showToast({
          icon: "none",
          title: "当前无法报名"
        });
        setTimeout(function () {
          wx.navigateBack({
            url: '../index/index',
          })
        }, 500);
      }
    })
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
    console.log('formId', e.detail.formId);
    let question = []
    for (let x in this.data.questions) {
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
    console.log(question)
    let session = wx.getStorageSync('key')
    wx.request({
      url: app.globalData.serveraddr + '/Step-Into-THUMB/candidate/submit-application?session='+session, 
      method: 'POST',
      data:{
        question
      },
      header: {
        'content-type': 'application/json'
      },
      success: function (res) {
        console.log(res)
        wx.showToast({
          title: "提交成功"
        });
        setTimeout(function () {
          wx.navigateBack({
            url: '../index/index',
          })
        }, 500);
      }
    })
  },
})
