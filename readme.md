# 功能介绍

配合云函数或者服务器，实现每天自动打卡及信息上报

**健康码打卡：**

    是否发烧：否
    
    体温：36.5

**信息上报：**

    一切按您上次上报的信息为准，脚本不会修改任何信息
    从服务器拿到上次的上报信息后，就直接上报了


**如果您的健康信息不实，请勿使用此脚本**


# 使用方法

## 使用腾讯云函数

1. 在腾讯云创建一个云函数，并将脚本上传



2. 修改脚本的配置信息
   1. 您需要申请一个server酱key(若已有key填入配置信息即可，跳过此步)

      申请网址：<http://sc.ftqq.com/?c=code>

      使用Github一键登录，获取sckey

      然后将sckey填写到脚本配置区对应位置

   2. 创建一个腾讯云文档保存cookies(公开可访问)

      获取cookies，在浏览器登录<https://www.ioteams.com/ncov/#/index>

      然后按F12，复制cookies

      ![2020/04/08/eb5720408023840.png](http://cdn.z2blog.com/2020/04/08/eb5720408023840.png)

      只复制`cookie`冒号后面的内容

      然后粘贴到新建的腾讯云普通文档中（如果以后cookie失效，就在这个文档更新cookie）

      ![http://cdn.z2blog.com/2020/04/08/522d90408023519.png](http://cdn.z2blog.com/2020/04/08/522d90408023519.png)

      点击右上角的分享，选择`获取链接的人可查看`

      然后复制链接，填写到脚本配置对应位置

      ![2020/04/08/485010408024127.png](http://cdn.z2blog.com/2020/04/08/485010408024127.png)

   3. 配置腾讯云函数api触发

      在我们刚才创建的云函数里面，选择`触发方式`

      触发方式选择`API网关触发器`

      请求方式选择`GET` 保存

      ![2020/04/08/e09040408024346.png](http://cdn.z2blog.com/2020/04/08/e09040408024346.png)

      复制API接口链接，并在此连接后面加上`?update=True`

      例如接口链接为`http://aaaa.com/test`

      则完整链接为`http://aaaa.com/test?update=True`

      然后将完整链接写到配置区对应位置

      ![2020/04/08/10a470408024600.png](http://cdn.z2blog.com/2020/04/08/10a470408024600.png)

   4. 设置cookies文件存储路径(腾讯云函数跳过此步骤)

```python
# server酱
SERVER_CHAN_SCKEY = 'xxxxxxxx'
# 申请地址http://sc.ftqq.com/3.version
# 功能：每次的打卡信息都会推送至你的个人微信
SERVER_CHAN_CONFIG = {
	'status': True,  # 如果关闭server酱功能，请改为False
	'url': 'https://sc.ftqq.com/{}.send'.format(SERVER_CHAN_SCKEY)
}

# 腾讯文档地址
# 功能：用于读取cookies和更新
# 目测cookies有效时长是10天，手动更新
TENCENT_FILE_URL = 'xxxxxx' # 腾讯云文档的公开分享链接

# API
# 功能：用于更新cookies 以及 主动打卡
TENTCENT_CLOUD_FUNC_REMOTE_URL = ""

# cookies缓存文件路径
# 功能：保存cookies文件
# 如果使用腾讯云函数，此路径不可修改
COOKIES_PATH = "/tmp"
```



3. 配置云函数的每日定时运行

   还是在刚才的触发方式

   触发方式，选择`定时触发`

   触发周期，选择`自定义周期`

   Cron表达式，输入`0 5 0 * * * *`  表示每日0点5分0秒执行

   更多Cron表达式参考这篇文章

   <https://cloud.tencent.com/document/product/583/9708#cron-.E8.A1.A8.E8.BE.BE.E5.BC.8F>

   ![2020/04/08/814d50408024928.png](http://cdn.z2blog.com/2020/04/08/814d50408024928.png)



# 其他问题

Q：cookies失效了，如何更新cookies？

> A：1)首先需要打开你的腾讯云文档，删除之前的cookies，然后将新的cookies粘贴上去；2)访问api，手动更新cookies以及打卡





Q：支持手机验证码登录吗？

> A：暂时不支持，后面应该会更新



