import sys

def lexicalprob(words,tags):
	wordtagcount = {}
	tagcount = {}
	prob = {}
	for word, tag in zip(words, tags):
		for w, t in zip(word, tag):
			wordtagcount[(w, t)] = wordtagcount.get((w,t), 0) + 1
			tagcount[t] = tagcount.get(t, 0) + 1
	for word, tag in wordtagcount:
		prob[(word, tag)] = wordtagcount[(word, tag)]*1.0/tagcount[tag]
	return prob, tagcount
	
def bigramprob(tags, tagcount):
	bprob = {}
	tagtagcount = {}
	for tag in tags:
		for tag1, tag2 in zip(tag[0:], tag[1:]):
			tagtagcount[(tag1, tag2)] = tagtagcount.get((tag1, tag2), 0) + 1
	for tag1, tag2 in tagtagcount:
		bprob[(tag1, tag2)] = tagtagcount[(tag1, tag2)]*1.0/tagcount[tag1]
	return bprob
	
def viterbi(line, taglist, lp, bp):
	lin = line.lower()
	lst = lin.strip().split(" ")
	w = len(lst)
	t = len(taglist)
	seqscr = []
	temp = []
	trace = []
	#Initialization
	for i in range(t):
		temp.append(lp.get((lst[0], taglist[i]), 0.0001)*bp.get(('START', taglist[i]), 0.0001))
	seqscr.append(temp)
	#Iteration
	for w1 in range(1, w):
		temp = []
		trtemp = []
		for i in range(t):
			mx = [seqscr[w1-1][j]*bp.get((taglist[j], taglist[i]), 0.0001) for j in range(t)]
			trtemp.append(mx.index(max(mx)))
			temp.append(max(mx)*lp.get((lst[w1], taglist[i]), 0.0001))
		seqscr.append(temp)
		trace.append(trtemp)
	#Backtracking
	index = seqscr[w-1].index(max(seqscr[w-1]))
	final = []
	final.append(index)
	j = w-2
	while j > -1:
		index = trace[j][index]
		final.append(index)
		j -= 1
	result = ""
	lst = line.strip().split(" ")
	for i in range(w):
		result = result + lst[i] + "_" + taglist[final[w -1 - i]] + " "
	return result

def main():
	fr = open('train.txt', 'r')
	dataset = fr.readlines()
	fr.close()
	words = []
	tags = []
	for line in dataset:
		tag = ['START']
		word = ['START']
		for i in line.strip().split():
			k = i.rsplit('_')
			tag.append(k[-1])
			word.append(k[0].lower())
		tag.append('END')
		word.append('END')
		tags.append(tag)
		words.append(word)
	lp, tagcount = lexicalprob(words, tags)
	bp = bigramprob(tags, tagcount)
	taglist = []
	for key in tagcount:
		taglist.append(key)
	with open(sys.argv[1], 'r') as fr:
		fw = open("output.txt", "w")
		lines = fr.readlines()
		for line in lines:
			result = viterbi(line, taglist, lp, bp)
			fw.write(result)
			fw.write("\n")
		fw.close()
	fr.close()
main()
