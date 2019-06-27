class User(object):
	__instance=None
	def __init__(self, name):
		self.name=name

	def __new__(cls, name):
		if not cls.__instance:   # 保证object.__new__()方法只会调用一次
			cls.__instance=object.__new__(cls)
		return cls.__instance

u1=User('u1')
u2=User('u2')

print(u1==u2)
print(u1.name)
print(u2.name)
print(u1.name==u2.name)
