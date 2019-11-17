f = open("Pattern_DATE_111508015.txt")
out = f.readlines()
fw = open("Pattern_DATE.txt", "w")
for i in range(len(out)):
	words = out[i].split("\t")
	for j in range(len(words)):
		fw.write(words[j] + "\t\t")
		print(words[j])
	#fw.write("\n")
#for i in range(len(out)):
#	print(out[i])
#for i in range(0, temp, 8):
#	print(out[i] + "\t\t" + out[i + 1] + "\t\t" + out[i + 2] + "\t\t" + out[i + 3] + "\t\t" + out[i + 4] + "\t\t" + out[i + 5] + "\t\t" + out[i + 6] + "\t\t" + out[i + 7] + "\n")
