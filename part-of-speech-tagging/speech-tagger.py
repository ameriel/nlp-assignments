#!/usr/bin/python
from collections import Counter
import tokenizer
from math import log

#Amerie Lommen & Dominic Pearson
#CS 404 Group Assignment 3

#transition_probability: add-one smoothed probability that t2 follows t1
def transition_probability(t2, t1): #P(t2|t1)
	#prob = float("-inf")
	prob = log(float(1) / float(training_data.tag_unigram_counts[t1] + len(training_data.tag_unigram_counts))) 
	if t1 in training_data.tag_bigram_counts and t2 in training_data.tag_bigram_counts[t1]:
		#prob = log(float(training_data.bigram_counts[t1][t2]) / float(training_data.tag_unigram_counts[t1]))
		prob = log(float(training_data.tag_bigram_counts[t1][t2] + 1) / float(training_data.tag_unigram_counts[t1] + len(training_data.tag_unigram_counts)))
	return prob

#emission_probability: add-one smoothed probability that w is tagged with t
def emission_probability(w, t): #P(w|t)
	if w == '###' and t == '###':
		prob = log(1.0)
	else:
		#prob = float("-inf")
		prob = log(float(1) / float(training_data.tag_unigram_counts[t] + len(training_data.word_unigram_counts) -1))
		if w in training_data.tag_dictionary and t in training_data.tag_dictionary[w]:
			#prob = log(float(training_data.tag_dictionary[w][t]) / float(training_data.tag_unigram_counts[t]))
			prob = log(float(training_data.tag_dictionary[w][t] + 1) / float(training_data.tag_unigram_counts[t] + len(training_data.word_unigram_counts) - 1))
	return prob

#smoothed_transition_probability: one-count smoothed probability that t2 follows t1
def smoothed_transition_probability(t2, t1):
	ptt_backoff = float(training_data.tag_unigram_counts[t2]) / float(len(training_data.tags))
	l = 1 + training_data.sing_tt[t1]
	prob = log(float(training_data.tag_bigram_counts[t1][t2] + l * ptt_backoff) / float(training_data.tag_unigram_counts[t1] + l))
	return prob

#smoothed_emission_probability: one-count smoothed probability that w is tagged with t
def smoothed_emission_probability(w, t):
	ptw_backoff = float(training_data.word_unigram_counts[w] + 1) / float(len(training_data.words) + v)
	l = 1 + training_data.sing_tw[t]
	c_pair = training_data.tag_dictionary[w][t] if w in training_data.tag_dictionary else 0
	c_tag = training_data.tag_unigram_counts[t]
	prob = log(float(c_pair + l * ptw_backoff) / float(c_tag + l))
	return prob

#tag_dictionary: given a word, returns the list of tags that occur with that word in the training data
def tag_dictionary(w):
	if w in training_data.tag_dictionary:
		dictionary = training_data.tag_dictionary[w].keys()
	else:
		dictionary = training_data.tag_unigram_counts.keys()
		dictionary.remove('###')
	return dictionary

#vtag: given a sequence of words, returns the most likely tag sequence using the algorithm discussed in class
def vtag(sequence, smoothing):
	n = len(sequence)
	#Initiate trellis, etc.
	vseq = ["" for i in range(n)] #same length as sequence
	trellis = {}
	backpointer = {}
	for t in training_data.tag_unigram_counts:
		trellis[t] = [float("-inf") for i in range(n)]
		backpointer[t] = ["" for i in range(n)]
	trellis['###'][0] = log(1.0)
	#Fill in trellis with real values
	for i in range(1, n):
		word = sequence[i]
		for ti in tag_dictionary(word): #All possible tags for this word
			for tj in tag_dictionary(sequence[i-1]): #All possible tags for previous word, find pair with max probability
				#j = i-1
				if smoothing:
					prob = smoothed_transition_probability(ti, tj) + smoothed_emission_probability(word, ti) #Switch to addition for log space
					v = trellis[tj][i-1] + prob #Switch to addition for log space
					if v >= trellis[ti][i]:
						trellis[ti][i] = v
						backpointer[ti][i] = tj
				else:
					prob = transition_probability(ti, tj) + emission_probability(word, ti) #Switch to addition for log space
					v = trellis[tj][i-1] + prob #Switch to addition for log space
					if v >= trellis[ti][i]:
						trellis[ti][i] = v
						backpointer[ti][i] = tj
	vseq[n - 1] = '###'
	for i in range(n - 1, 0, -1):
		vseq[i-1] = backpointer[vseq[i]][i]
	return vseq

#calculate_tag_sequence: given a boolean (add one smoothing or no one-count smoothing) prints out the tagging accuracy of Viterbi decoding
def calculate_tag_sequence(smoothing):
	vseq = vtag(test_data.words, smoothing)
	num_total = 0
	num_correct = 0
	num_known = 0
	num_known_correct = 0
	for i in range(len(vseq)):
		if vseq[i] != '###':
			num_total += 1
			if vseq[i] == test_data.tags[i] and vseq[i]:
				num_correct += 1
			if test_data.words[i] in training_data.word_unigram_counts:
				num_known += 1
				if vseq[i] == test_data.tags[i] and vseq[i]:
					num_known_correct += 1
	total_percent = float(num_correct) / float(num_total)
	known_percent = float(num_known_correct) / float(num_known)
	novel_percent = float(num_correct - num_known_correct) / float(num_total - num_known) if num_known < num_total else 0.0
	print "Tagging accuracy (Viterbi decoding): " + str(total_percent * 100.0) + "% (known: " + str(known_percent * 100.0) + "% novel: " + str(novel_percent * 100.0) + "%)\n"

#main method, handles file io, sets globals, and calls calculate_tag_sequence for one count and add one smoothing
if __name__ == '__main__':
	train_file = 'data/en/entrain.txt'
	test_file = 'data/en/entest.txt'
	raw_file = 'data/en/enraw.txt'

	global raw_dictionary
	global training_data
	global test_data
	global v

	print "Tokenizing data...\n"

	#Tokenize training and test data and build counts
	with open(raw_file, 'r') as corpusfile:
		raw_dictionary = set(corpusfile.read().split())
	training_data = tokenizer.tokenizer(train_file)
	test_data = tokenizer.tokenizer(test_file)
	v = len(set(list(raw_dictionary)+list(training_data.word_unigram_counts.keys())))

	print "Calculating add-one smoothing tag sequence..."
	calculate_tag_sequence(False)

	print "Calculating one-count smoothing tag sequence..."
	calculate_tag_sequence(True)




