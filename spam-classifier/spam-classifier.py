#!/usr/bin/python

import tokenizer
import operator
from collections import Counter
from math import log

def category_probability(vector, training_data):
	#P(c|d) = P(d|c) * P(c) d=w1...wn (feature vector)
	#P(c) = number of documents tagged c / number of documents total
	#P(c|d) = P(w1|c)*...*P(wn|c)
	#P(wi|c) = number of times wi occurs in documents tagged with c / number of words in documents with c
	prob_c = float(len(training_data.messages)) / float(len(training_data.messages) + len(training_data.messages))
	
	prob_cd = 0.0
	for feature in vector.keys():
		if feature in dictionary:
			test_for_zero = float(training_data.unigrams[feature]) / float(sum(training_data.unigrams.values()))
			if test_for_zero > 0:
				this_prob = log(test_for_zero,2)
				this_prob = this_prob ** vector[feature]
				if this_prob > 0:
					this_prob *= -1.0
			else:
				this_prob = 0.0
			prob_cd += this_prob
	
	return log(prob_c, 2) + prob_cd



if __name__ == '__main__':
	global nonspam_training
	global spam_training
	global nonspam_test
	global spam_test
	global dictionary
		
	# STEP 1
	#add each file in each training and test directory to the tokenizer
	nonspam_training = tokenizer.tokenizer("nonspam-train")
	spam_training = tokenizer.tokenizer("spam-train")
	nonspam_test = tokenizer.tokenizer("nonspam-test")
	spam_test = tokenizer.tokenizer("spam-test")
	
	# build the dictionary
	dictionary = nonspam_training.unigrams + spam_training.unigrams + nonspam_test.unigrams + spam_test.unigrams
	sorted_dictionary = sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True)
	dictionary = sorted_dictionary[0:2500]
	dictionary = [i[0] for i in dictionary]

			
	#true positive = said spam was spam
	#false positive = said spam was not spam
	#true negative = said not spam was not spam
	#false negative = said not spam was spam
	true_positives = 0
	false_positives = 0
	true_negatives = 0
	false_negatives = 0
	for message in nonspam_test.messages:
		spam_probability = category_probability(message, spam_training)
		nonspam_probability = category_probability(message, nonspam_training)
		if spam_probability < nonspam_probability:
			true_negatives += 1
		else:
			false_positives += 1
	for message in spam_test.messages:
		spam_probability = category_probability(message, spam_training)
		nonspam_probability = category_probability(message, nonspam_training)
		if spam_probability > nonspam_probability:
			true_positives += 1
		else:
			false_negatives += 1
	print "True positives: " + str(true_positives)
	print "False positives: " + str(false_positives)
	print "True negatives: " + str(true_negatives)
	print "False negatives: " + str(false_negatives)
	precision = float(true_positives) / float(len(spam_test.messages))
	recall = float(true_positives) / float(true_positives + false_positives)
	print "Precision: " + str(precision)
	print "Recall: " + str(recall)
	print "F-score: " + str(float(2.0 * precision * recall ) / float(precision + recall))