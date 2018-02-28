class singleton(object):
	def __new__(cls):
		if not hasattr(cls, '_instance'):
			cls._instance = super(singleton, cls).__new__(cls, *arg, **kwarg)
		return cls._instance


class singleton(object):
	instance = {}
	def getinstance():
		if cls not in instance:
			instance[cls] = cls(*arg, **kwarg)
		retrun instance[cls]
	return getinstance