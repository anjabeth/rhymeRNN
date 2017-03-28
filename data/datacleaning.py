import re

def main():
	text = open("theiliad.txt")

	#clear the output file so this script can be run multiple times
	with open("theiliad_cleaned.txt", "w") as iliad:
		iliad.write("")

	output = open("theiliad_cleaned.txt", "a")
	for line in text:
		#get rid of parenthetical numbers
		newline = re.sub(r'\(\d*\)', "", line)
		#get rid of illustrations in brackets
		newline = re.sub(r'\[.*\]', "", newline)
		#get rid of all-caps text
		newline = re.sub(r'\b[A-Z]+\b',"", newline)
		output.write(newline)

	text.close()
	output.close()


if __name__ == '__main__':
	main()