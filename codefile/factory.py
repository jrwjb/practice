class Person(object):
	
	def __init__(self, name):
		self.name=name

	def work(self, axe_type):
		print(f'{self.name}开始砍柴')

		#axe = StoneAxe('石斧')

		#工厂模式
		axe = Factory.create_axe(axe_type)
		axe.cut_tree()

class Axe(object):

	def __init__(self, name):
		self.name=name

	def cut_tree(self):
		print(f'{self.name}')

class StoneAxe(Axe):
	
	def cut_tree(self):
		print('使用石头做的石斧砍树')

class SteelAxe(Axe):
	
	def cut_tree(self):
		print('使用钢斧砍树')


class Factory(object):
	
	@staticmethod
	def create_axe(type):
		if type == 'stone':
			return StoneAxe('石斧')
		elif type == 'steel':
			return SteelAxe('纲斧')
		else:
			print('没有该斧')





p = Person('hh')
p.work('stone')
