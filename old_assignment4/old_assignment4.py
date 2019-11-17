import sys

def viterbialgorithm(line, taglist, lp, bp):
	lin = line.lower()
	lst = lin.strip().split(" ")
	w = len(lst)
	t = len(taglist)
	seqscr = []
	temp = []
	trace = []
	#Initialization
	for i in range(t):
		temp.append(lp.get((lst[0], taglist[i]), 0.0001) * bp.get(('START', taglist[i]), 0.0001))
	seqscr.append(temp)
	#Iteration
	for w1 in range(1, w):
		temp = []
		trtemp = []
		for i in range(t):
			mx = [seqscr[w1-1][j] * bp.get((taglist[j], taglist[i]), 0.0001) for j in range(t)]
			trtemp.append(mx.index(max(mx)))
			temp.append(max(mx)*lp.get((lst[w1], taglist[i]), 0.0001))
		seqscr.append(temp)
		trace.append(trtemp)
	#Backtracking
	index = seqscr[w-1].index(max(seqscr[w-1]))
	final = []
	final.append(index)
	j = w - 2
	while j >= 0:
		index = trace[j][index]
		final.append(index)
		j -= 1
	result = ""
	lst = line.strip().split(" ")
	for i in range(w):
		result = result + lst[i] + "_" + taglist[final[w -1 - i]] + " "
	return result

def lexicalprobability(wordlist,taglist):
	wtcount = {}
	tcount = {}
	probability = {}
	for word, tag in zip(wordlist, taglist):
		for w, t in zip(word, tag):
			wtcount[(w, t)] = wtcount.get((w,t), 0) + 1
			tcount[t] = tcount.get(t, 0) + 1
	for word, tag in wtcount:
		probability[(word, tag)] = wtcount[(word, tag)] * 1.0 / tcount[tag]
	return probability, tcount
	
def bigramprobability(taglist, tcount):
	bigram = {}
	probabtgiventcount = {}
	for tag in taglist:
		for tag1, tag2 in zip(tag[0:], tag[1:]):
			probabtgiventcount[(tag1, tag2)] = probabtgiventcount.get((tag1, tag2), 0) + 1
	for tag1, tag2 in probabtgiventcount:
		bigram[(tag1, tag2)] = probabtgiventcount[(tag1, tag2)] * 1.0 / tcount[tag1]
	return bigram	

def main():
	fread = open('train.txt', 'r')
	dataset = fread.readlines()
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
	lp, tagcount = lexicalprobability(words, tags)
	bp = bigramprobability(tags, tagcount)
	taglist = []
	for key in tagcount:
		taglist.append(key)
	with open(sys.argv[1], 'r') as fread:
		fwrite = open("output.txt", "w")
		lines = fread.readlines()
		for line in lines:
			result = viterbialgorithm(line, taglist, lp, bp)
			fwrite.write(result)
			fwrite.write("\n")
		fwrite.close()
	fread.close()

if __name__ == "__main__":
	main()
