from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
from collections import Counter
import sys
import nltk
import csv

mis = "141608006";

feature_list_filename = 'features.csv'
feature_list = []


def intialize_feature_list():
    with open(feature_list_filename, 'r') as feature_list_file:
        csv_reader = csv.reader(feature_list_file, delimiter = ',')
        for row in csv_reader:
            #print(row)
            feature_list.append(row)

# tm2, wm2, tm1, wm1, tp1, wp1, tp2, wp2
def predict_tag(context):
    for feature in feature_list:
        #print(feature)
        # match feature
        match = True
        for i in range(8):
            if (feature[i].lower() != context[i].lower() and feature[i] != ''):
                #print("No match: " + str(i) + " " + feature[i] + " " + context[i])
                match = False
                break
        if (match):
            print("Found: " + str(feature))
            return feature[8] # tag
    return "O"


def getNERTags(line):
    tokens = word_tokenize(line)
    size = len(tokens)
    taggedTokens = []
    for index, token in enumerate(tokens):
        tmp = predict_tag([getWord(tokens, index-2, size), getPOS(tokens, index-2, size), getWord(tokens, index-1, size), getPOS(tokens, index-1, size), getWord(tokens, index+1, size), getPOS(tokens, index+1, size), getWord(tokens, index+2, size), getPOS(tokens, index+2, size)])
        tkn = (token, tmp)
        taggedTokens.append(tkn)
    return taggedTokens


def process(filename):
    file_read = open(filename, "r")
    file_write = open("MY_NER_labelled_Corpus_{0}.txt".format(mis), "w")
    
    intialize_feature_list()

    tagCount = Counter()
    tagContext = dict()
    for line in file_read:
        tags = getNERTags(line)
        for (index,  (word, tag)) in enumerate(tags):
                file_write.write(word)
                size = len(tags)
            
                if tag != "O":
                    file_write.write("_" + tag)
                
                    tagCount[tag] += 1

                    if tag not in tagContext:
                        tagContext[tag] = list()

                    # tagContext[tag].append([getWord(tags, index-2, size), getPOS(tags, index-2, size), getWord(tags, index-1, size), getPOS(tags, index-1, size), getWord(tags, index+1, size), getPOS(tags, index+1, size), getWord(tags, index+2, size), getPOS(tags, index+2, size)])
                
                if (word, tag) != tags[-1]:
                    file_write.write(" ")
                else:
                    file_write.write("\n")
    
    file_write.close()
    file_read.close()

def getWord(data, index, size):
    if (index < 0 or index >= size):
        return ''
    return data[index][0]

def getPOS(data, index, size):
    if (index < -1 or index > size):
        return ''
    if (index == -1):
        return "START"
    if (index == size):
        return "END"
    return nltk.pos_tag([data[index]])[0][1]


def calculate_accuracy():
    output_file = "MY_NER_labelled_Corpus_{0}.txt".format(mis);
    test_file = "NER_labelled_Corpus_{0}.txt".format(mis)

    correct = 0.0
    total = 0

    with open(output_file) as f1:
        with open(test_file) as f2:
            l1 = f1.readlines()
            l2 = f2.readlines()
            for i in range(len(l1)):
                tkn1 = word_tokenize(l1[i])
                tkn2 = word_tokenize(l2[i])
                # print(str(len(tkn1)) + " " + str(len(tkn2)))
                mini = min(len(tkn1), len(tkn2))
                for j in range(mini):
                    if ('_' not in tkn1[j]):
                        continue
                    if (tkn1[j] != tkn2[j] and '_' in tkn1[j]):
                        print("wrong: " + tkn1[j] + ' ' + tkn2[j])
                    else:
                        correct += 1
                    total += 1
    return correct / total * 100

if __name__ == '__main__':
    #if len(sys.argv) != 2:
    #    sys.exit(1)
    #filename = sys.argv[1]
    #print("Processing....")
    #process(filename)
    # process('train.txt')
    print(calculate_accuracy())
