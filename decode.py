#!/usr/bin/python

##############################################
# (c) 2016 Raymond Ng University of Sheffield
##############################################

import os,re,sys
import mesh
import viterbi
from optparse import OptionParser

def main():

	parser = OptionParser()
	parser.usage = "%prog [options] > out"
	parser.add_option("--mesh-file","",dest="mesh_file",
		help = "Mesh file to calculate n-best")
	parser.add_option("--nbest-size",default=100,dest="nbest_size",
		help = "Number of N-best to decode")

	(options, args) = parser.parse_args()
	mesh_file = options.mesh_file
	nbest_size = int(options.nbest_size)
	

        # while read wordlist and scorelist
        cn =  mesh.mesh(mesh_file)
        stclen = len(cn.wordslist)
        vs = viterbi.Viterbi_Solver(stclen,nbest_size)


        # initiate state object
        vsstates = [viterbi.VSState(cn.wordslist[0][0],None,None,cn.mainscoreslist[0][0],None)]
        for i in range(1,stclen):
                vsdaughters = list()
                for vsstate in vsstates:
			vsstate.CreateChildren(cn.wordslist[i],None,cn.mainscoreslist[i])
                        vsdaughters += vsstate.children
                vs.SortStateSiblings(vsdaughters,reverse=True)
                vs.PruneSortedSiblings(vsdaughters)
                vsstates = vsdaughters

	nbestid = 0
	for finalstate in vsstates:
		nbestid += 1
		if nbestid > nbest_size:
			break	
		sys.stdout.write('"*/nbest_'+str(nbestid)+'/'+cn.uid+'.rec"\n')
		sys.stdout.write(finalstate.MLFFullPath()+'\n')
		# sys.stdout.write(finalstate.TXFullPath()+'\n')
			
			
		

		
		
                # debug
                # print len(vsstates)
                # print "===="

                # for k in vsstates:
                #        tmpstate = k
                #        sys.stdout.write(str(tmpstate.overallscore)+' ')
                #        while tmpstate.parent != None:
                #                sys.stdout.write(tmpstate.word+' ('+str(tmpstate.mainscore)+') ')
                #                tmpstate = tmpstate.parent
                #        print '\n'





if __name__ == '__main__':
        main()

