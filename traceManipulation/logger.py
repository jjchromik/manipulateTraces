class Logger():
	"""
		reponsible for logging the changes
	"""

	def __init__(self, filename):
		self.backtrackFile = filename
		self.addMessage("============\n!!! NOTE !!!\nModifications listed in this file are always related to the most recent change. First packet index is 1. \n============\n", 'w')
		
	def addMessage(self, msg, mode='a'):
		fp = open(self.backtrackFile, mode)
		fp.write(msg)
		fp.close()
	