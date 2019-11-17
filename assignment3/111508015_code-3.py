import re
import sys
def main():
	try:
		f = open(sys.argv[1], "r")
	except IndexError:
		print("File name not specified in command line argument. Correct usage python3 assignment3.py <FileName>\n")
		exit()
	except FileNotFoundError:
		print("File does not exist. Please enter an existential file name and try again.\n")
		exit()
	text = f.read()
	inputs = re.split(' ', text)
	data = []
	for i in range(len(inputs)):
		if not '\n' in inputs[i]:
			data.append(inputs[i])
	#print(data)
	funigram = open("unigram.txt", "w")
	fbigram = open("bigram.txt", "w")
	ftrigram = open("trigram.txt", "w")
	ffourgram = open("fourgram.txt", "w")
	ffivegram = open("fivegram.txt", "w")
	for i in range(len(data)):
		funigram.write(data[i] + "\n")
		#funigram.write("\n")
	for i in range(len(data) - 1):
		fbigram.write(data[i] + "\t\t\t" + data[i + 1] + "\n")
	for i in range(len(data) - 2):
		ftrigram.write(data[i] + "\t\t\t" + data[i + 1] + "\t\t\t" + data[i + 2] + "\n")
	for i in range(len(data) - 3):
		ffourgram.write(data[i] + "\t\t\t" + data[i + 1] + "\t\t\t" + data[i + 2] + "\t\t\t" + data[i + 3] + "\n")
	for i in range(len(data) - 4):
		ffivegram.write(data[i] + "\t\t\t" + data[i + 1] + "\t\t\t" + data[i + 2] + "\t\t\t" + data[i + 3] + "\t\t\t" + data[i + 4] + "\n")
	ffivegram.close()
	ffourgram.close()
	ftrigram.close()
	fbigram.close()
	funigram.close()
	f.close()

if __name__ == "__main__":
	main()
