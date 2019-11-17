import re
from nltk.corpus import words
import enchant
import sys
def checkforhash(str):                  ##This function checks if any hash tag exists and splits the string sent to it as parameter accordingly
    ret = []
    length = len(str)
    if '#' in str:
        if(str[0] != '#'):
            i = 1
            while(str[i] != '#'):
                i += 1 
            temp = str[:i -1]
            #print(temp)
            ret.append(temp)
            curr = i
            prev = i
        else:
            curr = 0
            prev = 0
        for i in range(curr, length - 1):
            if(str[i] == '#'):
                temp = str[prev:i]
                ret.append(temp)
                prev = i
        temp = str[prev:length]
        ret.append(temp)               
    else:
        ret.append(str) 
    return ret

def checkforuser(str):              ##This function checks for any user references and splits the string sent to it as parameter accordingly
    ret = []
    length = len(str)
    if '@' in str:
        if(str[0] != '@'):
            i = 1
            while(str[i] != '@'):
                i += 1 
            temp = str[:i -1]
            ret.append(temp)
            curr = i
            prev = i
        else:
            curr = 0
            prev = 0
        for i in range(curr, length - 1):
            if(str[i] == '@'):
                temp = str[prev:i]
                ret.append(temp)
                prev = i
        temp = str[prev:length]
        ret.append(temp)               
    else:
        ret.append(str) 
    return ret

def ifurl(str):                     ##This function checks if a string is a valid URL or not
    regex = re.compile(
        r'^(?:http|ftp)s?://' 
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|' 
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' 
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return re.match(regex, str) is not None  


"""This function takes care of three conditions - 
    1. Apostrophe - Splits the string till the end when detects an apostrophe
    2. Checks for any smilies ( ':)' ) and if found tokenizes them
    3. Tokenizes any other single character punctuation marks

"""
def punctuation(str):              
    ret = []
    length = len(str)
    curr = 0
    prev = 0
    for i in range(curr, length):
        if(str[i] == '\''):
            temp = str[prev:]
            ret.append(temp)
            return ret
        if((str[i] == ':') and (str[i + 1] == ')')):
            temp = str[prev:i]
            temp2 = ":)"
            ret.append(temp)
            ret.append(temp2)
            i += 1
            prev = i + 1
        if (str[i] == '.') or (str[i] == ',') or (str[i] == '?') or (str[i] == '!') or (str[i] == '\"') or (str[i] == ':') or (str[i] == ';') or str[i] == '/' or (str[i] == '-'):         ##regex could not be used as I dont want to split on any character but only the selective ones 
            temp = str[prev:i]
            temp2 = str[i]
            ret.append(temp)
            ret.append(temp2)
            prev = i + 1
    temp = str[prev:length]
    ret.append(temp)
    return ret
   
def identifymonth(str):                         ## This function figures out if a string has a month written in it, uses regex to ensure that any form of the month name give a positive output
    temp = re.search(r'[jJ][aA][nN]([uU][aA][rR][yY])?', str)
    if temp:
        return 1
    temp = re.search(r'[fF][eE][bB]([rR][uU][aA][rR][yY])?', str)
    if temp:
        return 2
    temp = re.search(r'[mM][aA][rR]([cC][hH])?', str)
    if temp:
        return 3
    temp = re.search(r'[aA][pP][rR]([iI][lL])?', str)
    if temp:
        return 4
    temp = re.search(r'[mM][aA][yY]', str)
    if temp:
        return 5
    temp = re.search(r'[jJ][uU][nN]([eE])?', str)
    if temp:
        return 6
    temp = re.search(r'[jJ][uU][lL]([yY])?', str)
    if temp:
        return 7
    temp = re.search(r'[aA][uU][gG]([uU][sS][tT])?', str)
    if temp:
        return 8
    temp = re.search(r'[sS][eE][pP]([tT][eE][mM][bB][eE][rR])?', str)
    if temp:
        return 9
    temp = re.search(r'[oO][cC][tT]([oO][bB][eE][rR])?', str)
    if temp:
        return 10
    temp = re.search(r'[nN][oO][vV]([eE][mM][bB][eE][rR])?', str)
    if temp:
        return 11
    temp = re.search(r'[dD][eE][cC]([eE][mM][bB][eE][rR])?', str)
    if temp:
        return 12
    return 0

##This function checks if a given string has multiple legal words inside of it,
##done using enchant library as dictionary
def checkmultiple(str):                 
    d = enchant.Dict("en_US")
    length = len(str)
    ret = []
    end = length - 1
    for i in range(length - 1, -1, -1):
        temp = str[i:end + 1]
        if(d.check(temp) and len(temp) > 1):
            ret.insert(0, temp)
            end = i - 1 
    return ret

tempvar = checkmultiple("iguess")
print(tempvar)
tempvar = checkmultiple("rainwater")
print(tempvar)
tempvar = checkmultiple("walkinthepark")
print(tempvar)
tempvar = checkmultiple("workwell")
print(tempvar)
tempvar = checkmultiple("starstep")
print(tempvar)

##This function identifies any date if it can be obtained through a suitable regular expression 
def identifydateregex(string):
    date = -1
    month = -1
    year = -1
    strdash = "-"
    ret = re.match(r'[0-9]+/[0-9]+/[0-9]+', string)
    ret2 = re.match(r'[0-9]+-[0-9]+-[0-9]+', string)
    
    if not ret and not ret2:
        return ""
    
    if ret:
        sep = re.split('/', string)
        num1 = int(sep[0])
        num2 = int(sep[1])
        num3 = int(sep[2])
        if num1 > num2 and num1 > num3:
            year = num1
            month = num2
            date = num3
        else:
            date = num1
            month = num2
            year = num3
    if ret2:
        sep = re.split('-', string)
        num1 = int(sep[0])
        num2 = int(sep[1])
        num3 = int(sep[2])
        if num1 > num2 and num1 > num3:
            year = num1
            month = num2
            date = num3
        else:
            date = num1
            month = num2
            year = num3
    toret = "CF:D:"
    toret += str(year)
    toret += strdash
    toret += str(month)
    toret += strdash
    toret += str(date)
    return toret

#opening few lines shall read input from file
def main():
    filename = sys.argv[1]
    try:
        f = open(filename, "r")
    except FileNotFoundError:
        print("The file you specified does not exist. Please check and try again")
        exit()
    
    fwrite = open("output.txt", "w+")   
 
    f1 = f.read()
    inputs = []
    inputs = re.split('\n', f1)
    inputs = list(filter(lambda x: x != '', inputs))
    d = enchant.Dict("en_US")

    for tweet in inputs:
        sep = re.split(' ', tweet)       

        length = len(sep)

        for i in range(length):
            dateregex = identifydateregex(sep[i])
            if dateregex != "":
                sep.pop(i)
                sep.insert(i, dateregex)    

        ## below loop shall use the above written individual functions to tokenize the tweet
        final = []
        for i in range(length): 
            if (sep[i][0] == 'C') and (sep[i][1] == 'F') and (sep[i][2] == ':') and (sep[i][3] == 'D') and (sep[i][4] == ':'):
                final.append(sep[i])
                continue
            hashadded = checkforhash(sep[i])
            if(hashadded[0] != sep[i]):
                final.extend(hashadded)
                continue
            useradded = checkforuser(sep[i])
            if(useradded[0] != sep[i]):
                final.extend(useradded) 
                continue
            """hyphencheck = ifhyphen(sep[i])
            if hyphencheck:
                final.extend(hyphencheck)
                continue
            """
            urlcheck = ifurl(sep[i])
            if urlcheck:
                final.append(sep[i])
                continue
            punctuationadded = punctuation(sep[i])
            final.extend(punctuationadded)
        final = list(filter(lambda x: x != '', final))

        ##checking if date, had some problems writing this in a separate function
        newlist = []
        for i in range(len(final)):
            ifmonth = identifymonth(final[i]) 
            if ifmonth > 1 and ifmonth < 12:
                strdash = "-"
                month = ifmonth
                year = -1
                date = -1
                num1 = -1
                num2 = -1
                if(sep[i - 1][:len(final[i - 1]) - 2].isdigit()):
                    num1 = int(final[i - 1][:len(final[i - 1]) - 2])
                if(sep[i - 1].isdigit()):
                    num1 = int(sep[i - 1])
                if (i + 1) < len(final):
                    if(sep[i + 1][:len(final[i + 1]) - 2].isdigit()):
                        num2 = int(final[i + 1][:len(final[i + 1]) - 2])
                    if(sep[i + 1].isdigit()):
                        num2 = int(final[i + 1])
                if num1 != -1 and num2 != -1:
                    if num1 < num2:
                        num1, num2 = num2, num1
                    year = num1
                    date = num2
              
                    toret = "CF:D:"
                    toret += str(year)
                    toret += strdash
                    toret += str(month)
                    toret += strdash
                    toret += str(date)
                    del newlist[-1]
                    newlist.append(toret)
                else:
                    if num1 != 1:
                        if num1 > 30:
                            year = num1   
                            toret = "CF:D:"
                            toret += str(year)
                            toret += strdash
                            toret += str(month)
                            newlist.append(toret)
                        else:
                            date = num1
                            toret = "CF:D:????"
                            toret += strdash
                            toret += str(month)
                            toret += strdash
                            toret += str(date)
                            newlist.append(toret)
                    else:
                        if num2 != 1:
                            if num2 > 30:
                                year = num1   
                                toret = "CF:D:"
                                toret += str(year)
                                toret += strdash
                                toret += str(month)
                                newlist.append(toret)
                            else:
                                date = num1
                                toret = "CF:D:????"
                                toret += strash
                                toret += str(month)
                                toret += strdash
                                toret += str(date)
                                newlist.append(toret)
                        else:   
                            toret = "CF:D:????"
                            toret += strdash
                            toret += str(month)
                            newlist.append(toret)                        
            else:
                    newlist.append(final[i])
            i += 1
        length = len(newlist)

        ##checking for time, could not write a separate function
        i = 0
        while i < length:
            if newlist[i] == ":":
                num1 = -1
                num2 = -1
                if(newlist[i - 1].isdigit()):       
                    num1 = int(newlist[i - 1])
                if i + 1 < length and newlist[i + 1].isdigit():
                    num2 = int(newlist[i + 1])
                if i + 2 < length and newlist[i + 2] == "PM":   
                    num1 += 12
                if num1 != -1 and num2 != -1:
                    string = "CF:T:"
                    string += str(num1)
                    string += str(num2)
                    del newlist[i]
                    newlist.insert(i, string)
                    del newlist[i - 1]
                    del newlist[i]
                    length -= 2
            i += 1
        
        ## checking for apostrophes
        apfile = open("apostrophe.txt", "r")
        apread = apfile.read()
        apostrophes = re.split('\n', apread)
        
        length = len(newlist)
        for i in range(length):
            if '\'' in newlist[i]:
                j = 0
                while j  < (len(apostrophes)):
                    if newlist[i] == apostrophes[j]:
                        temp = apostrophes[j + 1]
                        temp2 = re.split(' ', temp)
                        del newlist[i]
                        newlist.insert(i, temp2[0])
                        newlist.insert(i + 1, temp2[1])
                    j += 2    
         
        print(newlist)
        #the code below can be added for checking multiple legal words inside a token, however the output of such an algorithm largely depends on the words contained in the dictionary used to validate the english words. As a suitable and accurate english dictionary in python is unavailable I have used the best dictionary I found and wrote code for the same.
        """finallist = []
        for i in range(length):
            ret = checkmultiple(newlist[i])
            if d.check(newlist[i]) != True and len(ret) > 1:
                finallist.extend(ret)
            else:
                finallist.append(final[i])
        #print(newlist)
        """
    
        ## writing output to file
        fwrite.write(str(len(newlist)))
        fwrite.write("\n")
        for i in range(len(newlist)):
            fwrite.write(newlist[i])
            fwrite.write("\n")

#main()
