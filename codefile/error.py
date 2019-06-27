class PwdEr(Exception):
	
	def __init__(self, pw, min_len):
		self.pw = pw
		self.min_len = min_len

	def __str__(self):
		return f'{self.pw}错误,密码长度最小为{self.min_len}'


def reg(name, pwd):
	if len(pwd) < 6:
		raise PwdEr(pwd, 6)
	else:
		pass

try:
	reg('hh', '123')
except Exception as e:
	print(e)
