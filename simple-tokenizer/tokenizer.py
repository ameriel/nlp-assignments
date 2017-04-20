#!/usr/bin/python

#Amerie Lommen & Dominic Pearson
#CS 404 Group Assignment 1 - Question 1: Tokenization
#Part 2: Write your own tokenizer
#Item (b): Collect information for nc.txt

from operator import itemgetter

#Build list of stopwords from provided file
with open('stopwords.txt', 'r') as swfile:
	stopwords_raw=swfile.read().replace('\r','')
stopwords = stopwords_raw.split('\n')
stopwords.append("'s")

#Function to determine if given word is either a stopword or punctuation
def is_stopword(word):
	global stopwords
	if word in stopwords:
		return True
	elif not any((char.isalpha() or char.isdigit() or char.isspace()) for char in word):
		return True
	else:
		return False

#Include class from part a in order to tokenize the file and count sentences
with open('nc.txt', 'r') as corpusfile:
	data=corpusfile.read()	
print "Analyzing nc.txt..."
import helper
hw1_instance = helper.hw1_tokenizer(data)
tokens = hw1_instance.tokens

print "Number of sentences: " + str(hw1_instance.num_sentences);

#Build a dictionary of types based on list of tokens
#Key: word from token list, value: number of times that token occurs in the list
types = {}
for token in tokens:
	if token in types:
		types[token] += 1
	else:
		types[token] = 1

#Count total number of tokens and types
num_tokens = len(tokens)
num_types = len(types)
print "Number of tokens: " + str(num_tokens)
print "Number of types: " + str(num_types)
print

#Report most common tokens
sorted_types = sorted(types.items(), key=itemgetter(1), reverse=True)
print "Most common tokens:"
print '{0:<15} {1:<10} {2:<15}'.format("VALUE","COUNT","% OF ALL TOKENS")
for word in sorted_types[:100]:
	word_count = word[1]
	word_percent = (float(word_count) / float(num_tokens)) * 100.0
	print '{0:<15} {1:<10} {2:<15}'.format(word[0],word_count,word_percent)
print

print "Most common tokens (excluding stopwords and punctuation): "
print '{0:<15} {1:<10} {2:<15}'.format("VALUE","COUNT","% OF ALL TOKENS")
num_printed = 0
for word in sorted_types:
	if not is_stopword(word[0]):
		word_count = word[1]
		word_percent = (float(word_count) / float(num_tokens)) * 100.0
		print '{0:<15} {1:<10} {2:<15}'.format(word[0],word_count,word_percent)
		num_printed += 1
	if num_printed == 100:
		break
print

#Count singletons, digits/punctuation/alphanumeric, etc.
num_singletons = 0
num_has_digits = 0
num_has_punct = 0
num_has_alphnum = 0
for word in types.keys():
	if types[word] == 1:
		num_singletons = num_singletons + 1
	if any(char.isdigit() for char in word):
		num_has_digits += types[word]
	if any(not char.isdigit() and not char.isalpha() and not char.isspace() for char in word):
		num_has_punct += types[word]
	if any(char.isdigit() for char in word) and any(char.isalpha() for char in word):
		num_has_alphnum += types[word]
print "Number of singletons: " + str(num_singletons) + ' (' + str((float(num_singletons) / float(num_types)) * 100.0) + '% of types)'
print "Number of tokens containing digits: " + str(num_has_digits)
print "Number of tokens containing punctuation: " + str(num_has_punct)
print "Number of tokens containing digits and letters: " + str(num_has_alphnum)
print

#Calculate and report token pairs}
pairs = {}
for i in range(0,len(tokens)-1):
		if not is_stopword(tokens[i]) and not is_stopword(tokens[i+1]):
		    pair = tokens[i] + ' ' + tokens[i+1]
		    if pair in pairs:
		        pairs[pair] += 1
		    else:
		        pairs[pair] = 1
num_pairs = len(tokens) - 1
sorted_pairs = sorted(pairs.items(), key=itemgetter(1), reverse=True)

print "Most common token pairs (excluding stopwords and punctuation):"
print '{0:<15} {1:<10} {2:<15}'.format("VALUE","COUNT","% OF ALL PAIRS")
for pair in sorted_pairs[:100]:
	pair_percent = (float(pair[1]) / float(num_pairs)) * 100
	print '{0:<25} {1:<10} {2:<15}'.format(pair[0],pair[1],pair_percent)
