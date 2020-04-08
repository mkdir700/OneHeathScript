# 文档暂时没写完

# 功能介绍

配合云函数或者服务器，实现每天自动打卡及信息上报

健康码打卡：

​	是否发烧：否

​	体温：36.5

信息上报：

​	一切按您上次上报的信息为准，脚本不会修改任何信息，从服务器拿到上次的上报信息后，就直接上报了

**如果您的身体健康信息不实，请勿使用此脚本**



# 使用方法

## 配合云函数

1. 在腾讯云创建一个云函数，并将脚本上传



2. 修改脚本的配置信息
   1. 您需要申请一个server酱key(若已有key填入配置信息即可，跳过此步)
   2. 创建一个腾讯云文档(公开可访问)
   3. 配置腾讯云函数api触发
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
# https://xxxxxxx.com/test/health?update=True
TENTCENT_CLOUD_FUNC_REMOTE_URL = ""

# cookies缓存文件路径
# 功能：保存cookies文件
# 如果使用腾讯云函数，此路径不可修改
COOKIES_PATH = "/tmp"
```



3. 配置云函数的触发条件



# 其他问题

Q：cookies失效了，如何更新cookies？

A：1)首先需要打开你的腾讯云文档，删除之前的cookies，然后将新的cookies粘贴上去；2)访问api，手动更新cookies以及打卡



Q：支持手机验证码登录吗？

A：暂时不支持，后面应该会更新



