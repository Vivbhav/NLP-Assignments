import re
from nltk.corpus import words
import enchant
import sys
from nltk.stem.porter import *
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter

#opening few lines shall read input from file
def main():
    filename = sys.argv[1]
    try:
        f = open(filename, "r")
    except FileNotFoundError:
        print("The file you specified does not exist. Please check and try again")
        exit()
    
 
    f1 = f.read()
    inputs = []
    inputs = re.split('\n', f1)
    
    removelist = []
    newlist = []
    # removing dots in case of a float 
    # eg. 95.27% then we have three tokens as
    # '95', , '.', and '27'
    # in such a case remove the '.'
     
    for i in range(len(inputs)):
        if inputs[i] == '.' and inputs[i - 1].isdigit() and i < len(inputs) - 1 and inputs[i + 1].isdigit():
            pass
        else:
            newlist.append(inputs[i])

    # removing any integers
    finallist = []
    for i in range(len(newlist)):
        if newlist[i].isdigit() == True:
            pass
        else:   
            finallist.append(newlist[i])
    
    # using porter stemmer for stemming
    stemmer = PorterStemmer()
    stemmed = [stemmer.stem(word) for word in newlist]
        
    # removing stop words
    stop_words = set(stopwords.words('english'))
    filtered = [w for w in stemmed if not w in stop_words]

    # counting the times each words occurs
    wordcount = Counter(filtered)
    
    ## writing output to file
    #fwrite.write("\n")
    #for i in range(len(wordcount)):
    fwrite = open("output.txt", "w+")   
    for item in wordcount.items():
        fwrite.write("{}\t{}".format(*item))
        fwrite.write("\n")
     
main()
