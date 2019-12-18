//index.js
//获取应用实例
const app = getApp()

// 打开调试
wx.setEnableDebug({
  enableDebug: true
})


Page({
  data: {
    clientHeight: 0,
    userInfo: {},
    hasUserInfo: false,
    attentionAnim: '',
    pageNumber: 0,
    pageNum: 4,
    canIUse: wx.canIUse('button.open-type.getUserInfo'),
    touchS: [0,0],
    touchE: [0,0]
  },
  //事件处理函数
  bindViewTap: function() {
    wx.navigateTo({
      url: '../logs/logs'
    })
  },
  bindFillForm: function() {
    /*wx.requestSubscribeMessage({
      tmplIds: ['AdymfH-LXIsQlfV8VKJ7fnq5gAJjdayvD4Zo_58PfYw',],
      success: function (res) {
        console.log('success', res['AdymfH-LXIsQlfV8VKJ7fnq5gAJjdayvD4Zo_58PfYw'])
      },
      fail: function (res) {
        console.log('fail', res.errMsg)
      }
    });*/
    let code = wx.getStorageSync('code')
    if (!code) {
      console.log("form check session fail")
      app.globalData.flag = false;
      console.log('false', app.globalData.flag)
      wx.navigateTo({
        url: '../login/login?next=' + 'form',
      });
    }
    else {
      wx.checkSession({
        success: function () {
          console.log("form check session success")
          
              app.globalData.flag = true;
              wx.navigateTo({
                url: '../form/form',
              })

        },
        fail: function () {
          console.log("form login fail")
          app.globalData.flag = false;
          console.log('false', app.globalData.flag)
          wx.navigateTo({
            url: '../login/login?next=' + 'form',
          });
        }
      })
    }
  },
  bindStatus: function() {
    let code = wx.getStorageSync('code')
    if (!code) {
      console.log("status check session fail")
      app.globalData.flag = false;
      console.log('false', app.globalData.flag)
      wx.navigateTo({
        url: '../login/login?next=' + 'status',
      });
    }
    else {
      wx.checkSession({
        success: function () {
          console.log("status check session success")
          console.log('session=', code)
          
              app.globalData.flag = true;
              wx.navigateTo({
                url: '../status/status',
              })

        },
        fail: function () {
          console.log("status check session fail")
          app.globalData.flag = false;
          console.log('false', app.globalData.flag)
          wx.navigateTo({
            url: '../login/login?next=' + 'status',
          });
        }
      })
    }
  },
  onReady: function() {
    var attentionAnim = wx.createAnimation({
      duration: 400,
      timingFunction: 'ease',
      delay: 0
    })
    //设置循环动画
    this.attentionAnim = attentionAnim
    var next = true;
    setInterval(function () {
      if (next) {
        //根据需求实现相应的动画
        this.attentionAnim.translate(0,4).step()
        next = !next;
      } else {
        this.attentionAnim.translate(0,-4).step()
        next = !next;
      }
      this.setData({
        //导出动画到指定控件animation属性
        attentionAnim: attentionAnim.export()
      })
    }.bind(this), 400)
  },
  onLoad: function () {
    let _this = this;
    wx.getSystemInfo({
      success: function (res) {
        _this.setData({
          clientHeight: res.windowHeight
        });
      }
    });
    
    /*console.log(app.globalData.flag)
    if (app.globalData.flag==false) {
      wx.navigateTo({
        url: '../login/login',
      })
    }*/
    
    /*console.log("login")
      let value = wx.getStorageSync('key')
      if (value) {
        wx.checkSession({
          success: function () {
            wx.request({
              url: "",
              data: value,
              success: function (res) {
                if (res.hasSession) {
                  if (res.expired) {
                    console.log("session过期，重新登录")
                    app.globalData.flag=false
                    wx.navigateTo({
                      url: '../login/login',
                    })
                  }
                  else {
                    console.log("欢迎回来")
                  }
                }
                else {
                  //开发者服务器上没有我们自定义的session，重新登录
                  console.log("无此session，重新登录")
                  //设置登录标识为false
                  app.globalData.flag = false
                  wx.navigateTo({
                    url: '../login/login',
                  })
                }             
              }
            })
          },
          fail: function() {
            // session_key 已经失效，需要重新执行登录流程
            //设置登录标识为false
            app.globalData.flag = false
            wx.navigateTo({
              url: '../login/login',
            })
          }
        })
      }
      else {
        //本地缓存中没有自定义的session登录态信息,则进行首次登录或者后续处理
        //设置登录标识为false
        
        app.globalData.flag = false
        console.log("login")
        wx.navigateTo({
          url: '../login/login'
        })
        console.log("login")
      }*/
  },
  onShow: function () {
    
  },
  bindArrow: function () {
    let cur = this.data.pageNumber + 1;
    if (cur >= this.data.pageNum) cur = this.data.pageNum - 1;
    this.setData({
      pageNumber: cur
    })
  },
  catchTouchMove: function (res) {
    return false;
  },
  touchStart(e) {
    //console.log(e)
    this.data.touchS = [e.changedTouches[0].pageX, e.changedTouches[0].pageY]
  },
  touchEnd(e) {
    //console.log(e)
    this.data.touchE = [e.changedTouches[0].pageX, e.changedTouches[0].pageY]
    if (this.data.touchE[1]-this.data.touchS[1] < -100) {
      //next page
      let cur = this.data.pageNumber + 1;
      if (cur >= this.data.pageNum) cur = this.data.pageNum - 1;
      this.setData({
        pageNumber: cur
      })
    }
    else if (this.data.touchE[1] - this.data.touchS[1] > 100) {
      //last page
      let cur = this.data.pageNumber - 1;
      if (cur <= 0) cur = 0;
      this.setData({
        pageNumber: cur
      })
    }
  },

})
