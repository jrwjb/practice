class User(object):
	
	def __init__(self,name,pwd):
		self.name=name
		self.pwd=pwd
		print('对象已构建好，由解释器自动回调，对象初始化')

	# new 方法是当对象构建的时候自动调用的， 该方法必须返回当前类的对象
	def __new__(cls,name,pwd):
		print('User类的对象开始构建')
		return object.__new__(cls)

	def __str__(self):
		return f'{self.name},{self.pwd}'
		

u = User('hh', '123')
print(u)
