import nltk
import sys
 
def main():
	with open(sys.argv[1], 'r') as fr:
		fw = open(sys.argv[2], "w")
		lines = fr.readlines()
		for line in lines:
			temp = nltk.word_tokenize(line)
			t = nltk.pos_tag(temp)
			for i in t:
				fw.write(str(i[0] + "_" + i[1] + " "))
			fw.write("\n")
		fw.close()
	fr.close()
main()
