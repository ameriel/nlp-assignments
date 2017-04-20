#!/usr/bin/python
from collections import Counter

#Amerie Lommen & Dominic Pearson
#CS 404 Group Assignment 3 - Helper

class tokenizer:

	#Add word to appropriate lists
	def record(self, pairstring):
		if pairstring and not pairstring.isspace():
			pair = pairstring.strip().split('/')
			#Add word and tag to in-order lists
			self.words.append(pair[0])
			self.tags.append(pair[1])

			#Update counts
			self.tag_unigram_counts[pair[1]] += 1
			if len(self.tags) > 1:
				tag = pair[1]
				prev_tag = self.tags[len(self.tags) - 2]
				if prev_tag in self.tag_bigram_counts:
					self.tag_bigram_counts[prev_tag][tag] += 1
				else:
					self.tag_bigram_counts[prev_tag] = Counter({})
					self.tag_bigram_counts[prev_tag][tag] = 1
			self.word_unigram_counts[pair[0]] += 1
			
			#Add tag to tag_dictionary for word
			if pair[0] not in self.tag_dictionary:
				self.tag_dictionary[pair[0]] = {}
				self.tag_dictionary[pair[0]] = Counter(self.tag_dictionary[pair[0]])
			self.tag_dictionary[pair[0]][pair[1]] += 1
				

    #Separate words (on newline) to place in lists
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
	def __init__(self, filename):
		self.words = []
		self.tags = []
		self.tag_unigram_counts = Counter({})
		self.word_unigram_counts = Counter({})
		self.tag_dictionary = Counter({})
		self.tag_bigram_counts = Counter({})
		self.sing_tt = Counter({})
		self.sing_tw = Counter({})

		with open(filename, 'r') as corpusfile:
			self.string=corpusfile.read().replace('\r','')

		self.tokenize()

		#Values for one-count smoothing
		for tag in self.tag_unigram_counts:
			self.sing_tt[tag] = len(['.' for i in self.tag_bigram_counts[tag] if self.tag_bigram_counts[tag][i] == 1])
			self.sing_tw[tag] = len(['.' for i in self.tag_dictionary if self.tag_dictionary[i][tag] == 1])
			
