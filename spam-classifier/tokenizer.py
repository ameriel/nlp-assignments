#!/usr/bin/python

#Amerie Lommen & Dominic Pearson
#CS 404 Group Assignment 2 - Helper for Question 1
from os import listdir
from os.path import isfile, join
from collections import Counter

class tokenizer:

	#Add word to appropriate lists
	def record(self, word):
		if word and not word.isspace() and len(word) > 1:
			if not word == '<s>':
				#Add to list of tokens
				self.tokens.append(word)
				#Update count in list of unigrams
				if word in self.unigrams:
					self.unigrams[word] += 1
				else:
					self.unigrams[word] = 1
				if word in self.messages[len(self.messages) - 1]:
					self.messages[len(self.messages) - 1][word] += 1
				else:
					self.messages[len(self.messages) - 1][word] = 1
			else:
				self.messages.append({})
				
				
    #Separate words (on whitespace) to place in lists
	def tokenize(self):
		start =0;
		data = self.string
		for c in range(0, len(data)):
			#Record last token when you hit end of string
			if c == len(data) - 1:
				self.record(data[start:c+1])
			#Whitespace signals end of token
			elif data[c].isspace():
				self.record(data[start:c])
				start = c + 1
    
	#On instantiation, read file, determine sentence boundaries, and perform tokenization
	#Assumes that input files contain a single sentence on each line and no punctuation
	def __init__(self, directory):
		self.tokens = []
		self.unigrams = {}
		self.messages = []	# feature vectors for every message
		self.messages.append({})
                
		# get list of files in directory
		files = [f for f in listdir(directory) if isfile(join(directory, f))]
		# build a big list of all the contents of the files in directory
		self.string = ''
		for filename in files:
			with open(directory + '/' + filename, 'r') as corpusfile:
					self.string += corpusfile.read().replace('\r','').replace('\n','')
			self.string += ' <s> '
		self.tokenize()
		self.unigrams = Counter(self.unigrams)