from scapy.all import *
from .logger import Logger
import copy
import random
from pyshark import *

class TraceManipulator():
	"""
	is reponsible for manipulating the given trace
	"""

	def __init__(self, input, output):
		"""
		:return:
		"""
		self.trace = rdpcap(input)
		self.logger = Logger(output + ".backtrack.txt")
		self.logger.addMessage("============\n!!! NOTE !!!\nModifications listed in this file are always related to the most recent change. First packet index is 1. \n============\n", 'w')
		
	def cloneRandomPackets(self, count):
		for i in range(count):
			src = random.randrange(0, len(self.trace)-1, 1)
			dst = random.randrange(0, len(self.trace)-1, 1)
			packet = copy.copy(self.trace[src])
			self.__clone(dst, packet)
			self.logger.addMessage("Cloned packet: " + str(src+1) + " to " + str(dst+1) + "\n")
	
	def cloneConsecutiveRandomPacket(self, count):
		src = random.randrange(0, len(self.trace)-1, 1)
		packet = copy.copy(self.trace[src])
		dst = random.randrange(0, len(self.trace)-1, 1)
		for i in range(count):
			self.__clone(dst, packet)
		self.logger.addMessage("Cloned packet: " + str(src+1) + " to " + str(dst+1) + " " + str(count) + " times\n")
	
	def removeRandomPackets(self, count):
		for i in range(int(count)):
			j = random.randrange(0, len(self.trace)-1, 1)
			pkt = self.__remove(j)
			self.logger.addMessage("Removed packet: " + str(j+1) + "\n")
	
	def removeConsecutivePackets(self, count):
		j = random.randrange(0, len(self.trace)-1-count, 1)
		for i in range(count):
			pkt = self.__remove(j)
		self.logger.addMessage("Removed packet: " + str(j+1) + "\n")
	
	def swapRandomPackets(self, count):
		for i in range(count):
			a = random.randrange(0, len(self.trace)-1, 1)
			b = random.randrange(0, len(self.trace)-1, 1)
			self.__swap(a, b)
			self.logger.addMessage("Swapped packets: " + str(a+1) + ", " + str(b+1) + "\n")
	
	def executeRulesFromFile(self, filename):
		file = open(filename, "r")
		for row in file:
			if row[0] == '#':
				continue
				
			row = row.strip("\n")
			columns = row.split(' ')
			for index in range(len(columns)):
				columns[index] = columns[index].strip("\"")
				columns[index] = columns[index].strip("\'")
			
			if columns[0] == 'clone':
				self.cloneRandomPackets(columns[1])
				continue
				
			if columns[0] == 'clonec':
				self.cloneConsecutiveRandomPacket(columns[1])
				continue
				
			if columns[0] == 'rm':
				self.removeRandomPackets(columns[1])
				continue
				
			if columns[0] == 'rmc':
				self.removeConsecutivePackets(columns[1])
				continue
				
			if columns[0] == 'swap':
				self.swapRandomPackets(columns[1])
				continue
		
	def write(self, filename):
		wrpcap(filename, self.trace)
	
	def __clone(self, index, packet):
		nextTimeStamp = self.trace[index].time
		if nextTimeStamp <= packet.time:
			packet.time = (self.trace[index].time + self.trace[index+1].time)/2
			print(self.trace[index].time)
		self.trace.insert(index, packet)
		
	def __remove(self, index):
		return self.trace.pop(index)		
		
	def __swap(self, indexA, indexB):
		a = self.trace.pop(indexA)
		b = self.trace.pop(indexB)
		tmpTime = a.time
		a.time = b.time
		b.time = tmpTime
		self.trace.insert(indexA, b)
		self.trace.insert(indexB, a)