from nltk.corpus import wordnet
from nltk import word_tokenize

def Overlap(sense1, sense2):
	def1 = set(word_tokenize(sense1.definition()))
	def2 = set(word_tokenize(sense2.definition()))
	intersect = len(def1.intersection(def2))
	total = len(def1) + len(def2) - intersect
	return float(intersect) / total

def Overlap_Based_Similarity(word1, word2):
	sense1 = wordnet.synsets(word1)
	sense2 = wordnet.synsets(word2)
	overlap = 0.0
	max_overlap= 0.0
	for i in sense1:
		for j in sense2:
			overlap = Overlap(i, j)
			if overlap > max_overlap:
				max_overlap = overlap
	return max_overlap

def main():
	word1 = input("Enter first word to check its similarity\t")
	word2 = input("Enter second word\t\t\t\t")
    
	sim = Overlap_Based_Similarity(word1.lower(), word2.lower())
	print("Overlap Based Similarity of " + word1 + " and "+ word2 + " is " + str(sim))

if __name__ == "__main__":
	main()
