#!/usr/bin/python

import sys, re, os
import numpy as np
# from Queue import PriorityQueue

class State(object):
	# attribute 
	# +-- word: word
	# +-- score: score vector
	# +-- mainscore: deterministic score for overallscore calculation
	# +-- w: weight vector
	# +-- overallscore: overall score
	# +-- parent
	def __init__(self, word, score, w=None, mainscore=None, parent=None):
		self.children = []
		self.parent = parent 
		self.word = word				# from external input
		self.score = np.array(score).astype(float)	# from external input
		# assign w and mainscore
		if (w != None and mainscore == None):
			if parent != None:
				self.w = parent.w
			else:
				self.w = np.array(w).astype(float)
			self.mainscore = np.dot(self.w, self.score)
		elif (w == None and mainscore != None):
			self.w = None
			self.mainscore = np.array(mainscore).astype(float)
		else:
			sys.stderr.write('Use either w or mainscore, but not both!\n')
		# assign overallscore
		if parent != None:
			self.overallscore = parent.overallscore + self.mainscore
		else:		
			self.overallscore = self.mainscore	
	def GetKBest(self,K):
		pass
	def CreateChildren(self,words,scores,mainscores):
		pass

class VSState(State):
	def __init__(self, word, score, w, mainscore, parent):
		super(VSState, self).__init__(word, score, w, mainscore, parent)
	# problem: GetKBest is function run in the parent level, not in the self level!!
	# def GetKbest(self,K):
	# 	if self.value == self.goal:
	# --------------------------------------
	# Upon every align, 
	# -- read all the words in the align,
	# -- stores all the scores in score,
	# -- put the normalised score to mainscore
	# -- calculate the culminative score (overallscore) 
	# -- return as a child
	def CreateChildren(self,words,scores,mainscores=None):	
		if not self.children:	# just to make sure children do not created repeatedly
			for i in range(0,len(words)):
				word = words[i]
				if (scores != None):
					score = scores[i]
				else:
					score = None
				if (mainscores != None):
					mainscore = mainscores[i]
				else:
					mainscore = None
				dummyw = None
				child = VSState(word,score,dummyw,mainscore,self)
				self.children.append(child)
		else:
			sys.stderr.write("children for this node has been created!\n")
			sys.exit(-1)
	def GetSiblings(self):
		if self.parent == None:		# top-level
			return [self]
		else:
			return self.parent.children
	def MLFFullPath(self):
		tmpstate = self
		mlfstring = list()
		while True:
			# np.set_printoptions(precision=8)
			if tmpstate.word != '*DELETE*':
				mlfstring.append(tmpstate.word+' '+str(tmpstate.mainscore))
			if tmpstate.parent == None:
				break
			tmpstate = tmpstate.parent
		# reverse the whole list (FILO) and print
		mlfstring.reverse()	
		return ('\n'.join(mlfstring)+'\n.')
	def TXFullPath(self):
		tmpstate = self
		txstring = list()
		while True:
			if tmpstate.word != '*DELETE*':
				txstring.append(tmpstate.word)
			if tmpstate.parent == None:
				break
			tmpstate = tmpstate.parent
		txstring.reverse()
		return (' '.join(txstring))
			

			
		

class Viterbi_Solver:
	def __init__(self, numalign, prunef):
		self.path = []
		self.visitedQueue = []
		self.prunef = prunef
		# self.priorityQueue = PriorityQueue()
	def SortStateSiblings(self, siblings, reverse=False):
		siblings[:] = [(x.overallscore, x) for x in siblings]
		siblings.sort(reverse=reverse)
		siblings[:] = [val for (key,val) in siblings]
		return			# sort in place, just return
	def PruneSortedSiblings(self, siblings):
		###############################
		checkDuplicate = True
		if checkDuplicate:
			stclist = list()
			removelist = list()
			# fill in removelist
			for i in range(0,len(siblings)):
				thisstc = siblings[i].TXFullPath()
				if thisstc in stclist:
					removelist.append(i)
				stclist.append(thisstc)		
			# remove from back
			for j in range(len(removelist)-1,-1,-1):
				siblings.pop(removelist[j])
		################################
		while len(siblings) > self.prunef:
			siblings.pop()	
		return
	

	# def Solve(self):
	#	startState = VSState(self, value, score, mainscore, ...)
			
	#	count = 0
	#	self.priorityQueue.put((0, count, startState))
	#
	#	while (not self.path and self.priorityQueue.qsize());
	#		closesChild = self.priorityQueue.get()([2])



