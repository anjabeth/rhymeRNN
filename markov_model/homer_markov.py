#!python2

#python 3 does NOT play nice with bsddb, which is necessary for gutenberg, so using python 2 for this
import sys
import io
import textwrap
import markovify
from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers

NUM_SENTENCES =5 
NUM_STANZAS = 5

OUTPUT_LOC_2 = "generated_homer_2gram.txt"
OUTPUT_LOC_3 = "generated_homer_3gram.txt"
OUTPUT_LOC_4 = "generated_homer_4gram.txt"

def main():
	"""Generates text based on The Iliad from 2-gram, 3-gram, and 4-gram models. Text written to OUTPUT_LOCs 2, 3, and 4"""
	the_iliad = strip_headers(load_etext(6130).strip()) #The Iliad (translated by Alexander Pope), with headers and whitespace stripped
	generate_stanzas(the_iliad, 2, OUTPUT_LOC_2)
	generate_stanzas(the_iliad, 3, OUTPUT_LOC_3)
	generate_stanzas(the_iliad, 4, OUTPUT_LOC_4)


def generate_stanzas(text, n, output_loc):
	"""Generates NUM_STANZAS stanzas of NUM_SENTENCES sentences from text using an ngram Markov model with n=n. Writes these to output_loc"""
	the_iliad_model = markovify.Text(text, state_size = n) #N = 3

	stanzas = create_all_stanzas(the_iliad_model)

	clearfile(output_loc) #clear old file to allow running script multiple times to same output location
	f = open(output_loc, "a")
	write_stanzas(f, stanzas)
	f.close()
	
	print "Text written to " + str(output_loc)

def create_all_stanzas(model):
	"""Creates all stanzas and returns them in list form"""
	all_stanzas = list() 
	for i in range(NUM_STANZAS):
		new_stanza = create_one_stanza(model) 
		all_stanzas.append(new_stanza)
	return all_stanzas

def create_one_stanza(model):
	"""Creates and returns one stanza as a string"""
	initial_text = ""
	for i in range(NUM_SENTENCES):
		try:
			initial_text += str(model.make_sentence(tries=50)).encode('utf-8') + " " #increase tries to 50 from default 10 because the Homer text is a pretty short corpus
		except UnicodeEncodeError:
			i -= 1
	return initial_text


def write_stanzas(file, stanzas):
	"""Write stanzas to file using textwrap to make lines of readable length"""
	for i in range(NUM_STANZAS):
		file.write("*************** Stanza" + str(i + 1) + "*************** \n")
		lines = textwrap.wrap(stanzas[i])
		for line in lines:
			file.write((line).encode("utf-8") + "\n")
		file. write("\n\n\n\n")



def clearfile(output_loc):
	"""Clear input file - utility for when running script multiple times"""
	f = open(output_loc, "w")
	f.write("Procedurally Generated Homer by Anja Beth\n\n")
	f.close()

if __name__ == '__main__':
	main()