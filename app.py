import os
import json
import requests


# 配置区

# server酱
SERVER_CHAN_SCKEY = 'xxxxxxxx'
# 申请地址http://sc.ftqq.com/3.version
SERVER_CHAN_CONFIG = {
	'status': True,  # 如果关闭server酱功能，请改为False
	'url': 'https://sc.ftqq.com/{}.send'.format(SERVER_CHAN_SCKEY)
}

# 腾讯文档地址（用于读取cookies和更新）
TENCENT_FILE_URL = 'xxxxxx' # 腾讯云文档的公开分享链接

# API 用于更新cookies 以及 手动打卡
TENTCENT_CLOUD_FUNC_REMOTE_URL = ""
# https://xxxxxxx.com/test/health?update=True

# cookies缓存文件路径
COOKIES_PATH = "/tmp"

# 配置区


class HeathSign(object):

	def __init__(self):
		self.headers = {
			'Accept': 'Mozilla/5.0 (Linux; Android 10; GM1910 Build/QKQ1.190716.003; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 XWEB/1179 MMWEBSDK/191201 Mobile Safari/537.36 MMWEBID/9776 MicroMessenger/7.0.10.1580(0x27000A5E) Process/appbrand2 NetType/WIFI Language/zh_CN ABI/arm64 miniProgram',
			'Content-Type': 'application/json;charset=UTF-8',
			'Host': 'www.ioteams.com',
			'Referer': 'https://www.ioteams.com/ncov/'
		}
		self.session = requests.session()

	def set_cookies(self):
		"""设置cookies"""
		# cookies有效期10天
		with open(COOKIES_PATH + "/cookies.txt", "r") as f:
			cookies = f.read()
		cookies_dict = {}
		for c in cookies.split(";"):
			c = c.strip()
			key, value = c.split("=")
			cookies_dict[key] = value
			if key == "ncov-access-token-h5":
				self.headers["ncov-access-token"] = value
				cookies_dict["ncov-access-token-health-user"] = value
		self.session.cookies = requests.utils.cookiejar_from_dict(cookies_dict)

	def check_cookies(self):
		"""检测cookies是否存在且是否有效"""

		# 获取cookies
		if "cookies.txt" not in os.listdir(COOKIES_PATH):
			with open(COOKIES_PATH+"/cookies.txt", "w+") as f:
				id = TENCENT_FILE_URL.split('/')[-1]
				r = requests.get('https://docs.qq.com/dop-api/opendoc?normal=1&id={}'.format(id))
				f.write(r.text.split("\n")[3])

		# 验证cookies
		self.set_cookies()
		r = self.session.get('https://www.ioteams.com/ncov/api/sys/user/info', headers=self.headers)
		if r.status_code == 200:
			# 失效cookies
			return True
		else:
			return False

	def server_send(self, dict):
		"""server酱将消息推送至微信"""
		params = {
			'text': '健康码每日自动打卡消息！',
			'desp': dict['detail']
		}

		requests.get(SERVER_CHAN_CONFIG['url'], params=params)

	def get_user_info(self):
		"""获取个人信息"""
		url = 'https://www.ioteams.com/ncov/api/users/healthDetail'
		r = self.session.get(url, headers=self.headers)
		data = json.loads(r.text)
		# 获取上次上报信息以及用户唯一标识符
		self.user_id = data["data"]["data"]["_id"]
		self.latestReport = data["data"]["data"]["latestReport"]
		address = data["data"]["data"]["address"]
		lastHealthReport = data["data"]["data"]["lastHealthReport"]
		address.pop("detail")
		address.pop("_id")
		fields = ["isInitCreate", "remoteHealthLevel", "_id", "temperature", "company", "user", "created_at",
		          "updated_at", "__v", "current_fever"]
		for field in fields:
			lastHealthReport.pop(field)
		lastHealthReport["description"] = ""
		lastHealthReport["at_home"] = True
		# 数据整理
		self.last_report_msg = {"address": address}
		self.last_report_msg.update(lastHealthReport)

	def daily_reports(self):
		"""每日信息上报"""
		# print(self.latestReport)
		# x = self.session.get('https://www.ioteams.com/ncov/api/users/last-report', headers = self.headers)
		url = 'https://www.ioteams.com/ncov/api/users/dailyReport'
		r = self.session.post(url, headers=self.headers, data=json.dumps(self.last_report_msg))
		r = json.loads(r.text)
		if r['msg'] == 'success':
			print('上报信息成功!')
			return {'msg': True, 'detail': '今日信息上报成功'}
		else:
			print(r['msg'])
			return {'msg': False, 'detail': r['msg']}

	def health_report(self):
		"""健康码打卡"""
		data = {
			'current_fever': False,
			'temperature': 36.5
		}
		url = 'https://www.ioteams.com/ncov/api/users/{}/health-report'.format(self.user_id)
		r = requests.patch(url, headers=self.headers, data=json.dumps(data))
		if r.status_code == 204:
			print("打卡成功")
			return {'msg': True, 'detail': '健康码打卡成功'}
		else:
			print("打卡失败")
			return {'msg': False, 'detail': '健康码打卡失败'}

	def run(self):

		if not self.check_cookies():
			msg = {'msg': False, 'detail': '打卡失败，原因：cookies已失效，请及时更新！\r\r<{}>\r\rcookies更新好后，访问上方链接，即可继续打卡'.format(TENTCENT_CLOUD_FUNC_REMOTE_URL)}
			self.server_send(msg)
			return msg

		self.get_user_info()

		h1 = self.daily_reports()
		h2 = self.health_report()

		msg = {'msg': True, 'detail': h1['detail'] + '\r\r' + h2['detail']}
		self.server_send(msg)
		return msg


def main_handler(event=None, context=None):
	# print(event)
	try:
		t = event['queryString']['update']
	except:
		t = False
	if t:
		# 删除旧的cookies文件
		os.remove(COOKIES_PATH+"/cookies.txt")
		print("更新cookies缓存")
	s = HeathSign()
	return s.run()


if __name__ == '__main__':
	main_handler()
