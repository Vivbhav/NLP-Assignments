import sys

def Viterbi_Algorithm(sentence, taglist, lexicalprobab, bigramprobab):
	line = sentence.lower()
	numwords = line.strip().split(" ")
	w = len(numwords)
	t = len(taglist)
	#print(t)
	sequencescore = []
	temp = []
	backtrack = []
	for i in range(t):
		temp.append(lexicalprobab.get((numwords[0], taglist[i]), 0.0001) * bigramprobab.get(('begin', taglist[i]), 0.0001))
	sequencescore.append(temp)
	for w1 in range(1, w):
		temp = []
		temp2 = []
		for i in range(t):
			maxim = [sequencescore[w1 - 1][j] * bigramprobab.get((taglist[j], taglist[i]), 0.0001) for j in range(t)]
			#print(maxim)
			temp2.append(maxim.index(max(maxim)))
			temp.append(max(maxim) * lexicalprobab.get((numwords[w1], taglist[i]), 0.0001))
		sequencescore.append(temp)
		backtrack.append(temp2)
	index = sequencescore[w - 1].index(max(sequencescore[w - 1]))
	sequence = []
	sequence.append(index)
	j = w - 2
	while j > -1:
		index = backtrack[j][index]
		sequence.append(index)
		j -= 1
	result = ""
	numwords = sentence.strip().split(" ")
	for i in range(w):
		result = result + numwords[i] + "_" + taglist[sequence[w -1 - i]] + " "
	return result

def Lexical_Probability(wordlist,taglist):
	#print(taglist)
	wtcount = dict()
	tcount = dict()
	probability = dict()
	for word, tag in zip(wordlist, taglist):
		for w, t in zip(word, tag):
			wtcount[(w, t)] = wtcount.get((w,t), 0) + 1
			tcount[t] = tcount.get(t, 0) + 1
	for word, tag in wtcount:
		probability[(word, tag)] = wtcount[(word, tag)]*1.0/tcount[tag]
	#print(tcount)
	return probability, tcount
	
def Bigram_Probability(tags, tagcount):
	bigramprobability = dict()
	probabtgiventcount = dict()
	for tag in tags:
		for tag1, tag2 in zip(tag[0:], tag[1:]):
			probabtgiventcount[(tag1, tag2)] = probabtgiventcount.get((tag1, tag2), 0) + 1
	for tag1, tag2 in probabtgiventcount:
		bigramprobability[(tag1, tag2)] = probabtgiventcount[(tag1, tag2)]*1.0/tagcount[tag1]
	return bigramprobability

def main():
	try:
		filename = sys.argv[1]
		f = open(filename, "r")
	except IndexError:
		print("You probably didn't specify an input file. Correct format python3 111508015_Assign4_Code.py <TestFileName>")
		exit()
	except FileNotFoundError:
		print("The file you specified does not exist. Please check and try again.")
		exit()
	fread = open('train.txt', 'r')
	dataset = fread.readlines()
	fread.close()
	wordslist = []
	tagslist = []
	for line in dataset:
		tag = ['begin']
		word = ['begin']
		for i in line.strip().split():
			p = i.rsplit('_')
			tag.append(p[-1])
			word.append(p[0].lower())
		tag.append('END')
		word.append('END')
		tagslist.append(tag)
		wordslist.append(word)
	lexicalprobab, tagcount = Lexical_Probability(wordslist, tagslist)
	bigramprobab = Bigram_Probability(tagslist, tagcount)
	taglist = []
	for key in tagcount:
		taglist.append(key)
	fwrite = open("output.txt", "w")
	lines = f.readlines()
	for line in lines:
		result = Viterbi_Algorithm(line, taglist, lexicalprobab, bigramprobab)
		fwrite.write(result)
		fwrite.write("\n")
	fwrite.close()
	f.close()

if __name__ == "__main__":
	main()
