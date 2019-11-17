from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
from collections import Counter
import sys
import nltk

def Stats(tagCounter, tagsData):
    	tagslist = ["PERSON", "LOCATION", "ORGANIZATION", "DATE", "TIME", "MONEY", "PERCENT"]
    
	total = 0
    	for tag in tagCounter:
        	total += tagCounter[tag]
    
    	for tag in tagslist:
        	tagCounter[tag] = tagCounter.get(tag, 0) / total

    	fwrite = open("Stat_NER_111508015.txt", "w")
    	fwrite.write("TAG\tPROBABILITY\n")

    	linesformat = "{0}\t{1}\n"
    	for tag in tagslist:
        	fwrite.write(linesformat.format(str(tag), str(tagCounter.get(tag, 0))))

    	fwrite.close()

	linesformat = "{0}\t\t{1}\t\t{2}\t\t{3}\t\t{4}\t\t{5}\t\t{6}\t\t{7}\n"
    	for tag in tagslist:
        	fwrite = open("Pattern_{0}_111508015.txt".format(tag), "w")
        	fwrite.write(linesformat.format("W(i - 2)", "T(i - 2)", "W(i - 1)", "T(i - 1)", "W(i + 1)", "T(i + 1)", "W(i + 2)", "T(i + 2)"))
        
        if tag in tagsData:
            	for l in tagsData[tag]:
                	fwrite.write(linesformat.format(l[0], l[1], l[2], l[3], l[4], l[5], l[6],l[7]))
	        fwrite.close()


def process(filename):
    	fread = open(filename, "r")
 	fwrite = open("NER_labelled_Corpus_111508015.txt", "w")
    
	tagCount = Counter()
	tagContext = dict()
	for line in fread:
        	tags = getNERTags(line)
        for (index,  (word, tag)) in enumerate(tags):
                fwrite.write(word)
                size = len(tags)
            
                if tag != "O":
                    	fwrite.write("_" + tag)
                
                    	tagCount[tag] += 1

                    	if tag not in tagContext:
                        	tagContext[tag] = list()

                    		tagContext[tag].append([getWord(tags, index-2, size), TagFinder(tags, index-2, size), getWord(tags, index-1, size), TagFinder(tags, index-1, size), getWord(tags, index+1, size), TagFinder(tags, index+1, size), getWord(tags, index+2, size), TagFinder(tags, index+2, size)])
                
                	if (word, tag) != tags[-1]:
                    		fwrite.write(" ")
                	else:
                    		fwrite.write("\n")
    
    	fwrite.close()
    	fread.close()
	Stats(tagCount, tagContext)

def getNERTags(sentence):
    	tagger = StanfordNERTagger("ner-model-english.ser.gz", "stanford-ner.jar", encoding = "utf-8")
    	words = word_tokenize(sentence)
    	taggedTokens = tagger.tag(words)
    	return taggedTokens

def getWord(data, index, size):
    	if (index < 0 or index >= size):
        	return "*"
    	return data[index][0]

def TagFinder(data, index, size):
    	if (index < -1 or index > size):
        	return "*"
	if (index == -1):
        	return "START"
	if (index == size):
        	return "END"
	return nltk.pos_tag([data[index][0]])[0][1]

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
    	process(filename)

if __name__ == '__main__':
	main()
