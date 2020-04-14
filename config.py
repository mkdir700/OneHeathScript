# ===== 配置区 =====

# server酱
SERVER_CHAN_SCKEY = 'xxxxxxxx'
# 申请地址http://sc.ftqq.com/3.version
SERVER_CHAN_CONFIG = {
    'status': True,  # 如果关闭server酱功能，请改为False
    'url': 'https://sc.ftqq.com/{}.send'.format(SERVER_CHAN_SCKEY)
}

# 腾讯文档地址（用于读取cookies和更新）
TENCENT_FILE_URL = 'xxxxxx'  # 腾讯云文档的公开分享链接

# API 用于更新cookies 以及 手动打卡
TENTCENT_CLOUD_FUNC_REMOTE_URL = ""

# cookies缓存文件路径
COOKIES_PATH = "/tmp"

# ===== 配置区 =====