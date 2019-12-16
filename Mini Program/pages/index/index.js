//index.js
//获取应用实例
const app = getApp()

// 打开调试
wx.setEnableDebug({
  enableDebug: true
})


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
    console.log(app.globalData.flag)
    if (app.globalData.flag==false) {
      wx.navigateTo({
        url: '../login/login',
      })
    }
    
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
    console.log(app.globalData.flag)
    if (app.globalData.flag == false) {
      wx.navigateTo({
        url: '../login/login',
      })
    }
  },
 
})
