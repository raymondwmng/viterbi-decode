#!/usr/bin/python

##############################################
# (c) 2016 Raymond Ng University of Sheffield
##############################################

import os,re,sys
import gzip

class mesh(object):
        def __init__(self, f_mesh, wordslist=None, scoreslist=None, mainscoreslist=None, uid=None, numAlign=None):
                if wordslist == None or mainscoreslist == None:
                        # load wordslist and mainscoreslist from file
                        if re.match(r'\S+.gz',f_mesh):
				fm = gzip.open(f_mesh,'rb')
			else:
				fm = open(f_mesh,'r')
                        self.wordslist = list()
                        self.mainscoreslist = list()
                        self.scoreslist = list()
                        wordslistid = -1
                        # to do: add mainscoreslist() capabilities in future
                        uid_pattern = re.compile(r'^name\s+(\S+)$')
                        numAlign_pattern = re.compile(r'^numaligns\s+(\d+)$')
                        mainscores_pattern = re.compile(r'^align\s+(\d+)\s+(.*)$')
                        wordscores_pattern = re.compile(r'^info\s+(\d+)\s+(.*)$')
                        while True:
                                line = fm.readline()
                                if line == '':
                                        break
                                line = line.rstrip('\n')
                                m1 = uid_pattern.search(line)
                                if (m1):
                                        self.uid = m1.group(1)
                                m2 = numAlign_pattern.search(line)
                                if (m2):
                                        self.numAlign = m2.group(1)
                                m3 = mainscores_pattern.search(line)
                                if (m3):
                                        wordslistid += 1
                                        words = m3.group(2).split()[0:len(m3.group(2).split()):2]
                                        self.wordslist.append(words)
                                        mainscores = m3.group(2).split()[1:len(m3.group(2).split()):2]
                                        self.mainscoreslist.append(mainscores)
                                m4 = wordscores_pattern.search(line)
                                if (m4):
                                        pass
                        fm.close()
                else:
                        # ignore f_mesh input
                        self.uid = uid
                        self.numAlign = numAlign
                        self.wordslist = wordslist
                        self.scoreslist = scoreslist
                        self.mainscoreslist = mainscoreslist

