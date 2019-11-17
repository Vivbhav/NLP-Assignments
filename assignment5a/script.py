import nltk
import sys
from nltk.tag.stanford import StanfordNERTagger

def main():
	try:
		filename = sys.argv[1]
		f = open(filename, "r")
	except IndexError:
		print("You probably didn't specify an input file. Correct format python3 ass5.py <InputFileName>")
		exit() 
	except FileNotFoundError:
		print("The file you specified does not exist. Please check and try again.")
		exit()
	inputs = f.readlines() 

	jar = './stanford-ner.jar'
	model = './ner-model-english.ser.gz'
	ner_tagger = StanfordNERTagger(model, jar, encoding='utf8')
	
	file2 = open("NER_labelled_Corpus_111508015.txt", "w")
	
	for sentence in inputs:
		words = nltk.word_tokenize(sentence)

		for x in ner_tagger.tag(words):
			file2.write(x[0] + "_" + x[1] + " ")
		file2.write('\n')

if __name__ == "__main__":
	main()
