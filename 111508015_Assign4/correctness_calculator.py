from __future__ import division
from nltk.data import load
import numpy as np
import nltk

def main():
	posTaggedList = []
	final_posTaggedList = []
	taggedList = []
	final_taggedList = []
	final_posTaggedList2 = []
	final_taggedList2 = []
	tags = []
	true_pos = {}
	false_neg = {}
	false_pos = {}
	
	tagdict = load('help/tagsets/upenn_tagset.pickle')
	#print(tagdict)	
	fr_pos = open("t2.txt", "r")
	fr_mypos = open("t1.txt", "r")
	fw = open("correctness.txt", "w")
	
	lines_mypos = fr_mypos.readlines()
	tags = tagdict.keys()
	tags = list(tags)	
	for i in lines_mypos:
		i = i.strip().split()
		for j in i:
			taggedList.append(j)	
	for i in range(len(tags)):
		x = []
		for j in range(len(taggedList)):
			#temp = taggedList[j]
			#temp2 = temp.split("_")	
			#print(temp2)
			if tags[i] == taggedList[j].split("_")[1]:
			#if tags[i] == temp2:
				x.append(taggedList[j])
		if len(x) != 0:
			final_taggedList.append(x) 
	lines_pos = fr_pos.readlines()
	
	for i in lines_pos:
		i = i.strip().split()
		for j in i:
			posTaggedList.append(j)
	
	for i in range(len(tags)):
		x = []
		for j in range(len(posTaggedList)):
			if tags[i] == posTaggedList[j].split("_")[1]:
				x.append(posTaggedList[j])
		if len(x) != 0:
			final_posTaggedList.append(x)
	for i in final_taggedList:
		x = []
		y = []
		z = []
		for j in i:
			for k in final_posTaggedList:
				for l in k:
					if j.split("_")[1] == l.split("_")[1]:
						x = np.setdiff1d(k, i)
						y = np.setdiff1d(i, k)
						z = [value for value in i if value in k]
						
		false_neg[j.split("_")[1]] = len(x)
		false_pos[j.split("_")[1]] = len(y)
		true_pos[j.split("_")[1]] = len(z)
	print(false_neg,false_pos,true_pos)	
	for key in false_neg.keys():
		if true_pos[key] + false_pos[key] != 0:
			x = (true_pos[key]/(true_pos[key] + false_pos[key]))
			precision = "Precision of " + key + " = " + str(x)
			fw.write(precision)
			fw.write("\n")
		if true_pos[key] + false_neg[key] != 0:
			y = (true_pos[key]/(true_pos[key] + false_neg[key]))
			recall = "Recall of " + key + " = " + str(y)
			fw.write(recall)
			fw.write("\n")
		if x + y != 0:
			z = (2 * x * y)
			z = z/(x+y)
			f_measure = "F-Measure of " + key + " = " + str(z)
			fw.write(f_measure)
			fw.write("\n\n")
		else:
			f_measure = "F-Measure of " + key + " = 0.0/0.0" 
			fw.write(f_measure)
			fw.write("\n\n")
	fw.close()

main()

