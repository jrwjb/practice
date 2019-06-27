class User(object):
	__instance=None
	def __init__(self, name):
		self.name=name

	@classmethod
	def get_instance(cls,name):
		if not cls.__instance:     #如果instance为None
			cls.__instance=User(name)
		return cls.__instance

#u1=User('u1')
#u2=User('u2')
u1=User.get_instance('u1')
u2=User.get_instance('u2')

print(u1==u2)
print(u1.name)
print(u2.name)
print(u1.name==u2.name)
