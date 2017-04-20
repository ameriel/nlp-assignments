#!/usr/bin/python

#Amerie Lommen & Dominic Pearson
#CS 404 Group Assignment 1 - Question 2: Minimum Edit Distance
#January 16, 2016

import sys

#Get argument values
args = sys.argv
if len(args) < 3:
	print "Usage: python distance.py source target [n=1]"
	exit()
else:
	source = args[1]
	target = args[2]

if len(args) > 3:
	num_to_show = int(args[3])
else:
	num_to_show = 1

A = []
num_gathered = 0

#Function to trace back through distance array in order to find alignments.
#Returns a list of lists of tuples: each sub-list represents an alignment,
#and each tuple represents a column in the alignment's representation.
def get_ops(i, j, op_list = []):
	global A
	global source
	global dest
	global num_gathered
	source_ix = max(j - 1, 0)
	target_ix = max(i - 1, 0)
	alignments = []
	if i == 0 and j == 0 and num_gathered < num_to_show:
		alignments.append(list(op_list)[::-1]) #columns are built in reverse order, so reverse
		num_gathered += 1
	elif num_gathered < num_to_show:
		#Current cell could have come from substitution or no operation
		if A[i][j] == A[i-1][j-1] + 2 or (A[i][j] == A[i-1][j-1] and source[source_ix] == target[target_ix]):
			op_list.append((source[source_ix],target[target_ix]))
			alignments += get_ops(i-1, j-1, op_list)
			op_list.pop()
		#Current cell could have come from insertion
		if A[i][j] == A[i-1][j] + 1:
			op_list.append(('_',target[target_ix]))
			alignments += get_ops(i-1, j, op_list)
			op_list.pop()
		#Current cell could have come from deletion
		if A[i][j] == A[i][j-1] + 1:
			op_list.append((source[source_ix], '_'))
			alignments += get_ops(i, j-1, op_list)
			op_list.pop()
	return alignments

#Calculate the minimum edit distance and populate array
n = len(target) + 1
m = len(source) + 1
insertcost = 1
deletecost = 1
replacecost = 2
# set up distance array A and initialize values
A = [ [0 for j in range (m)] for i in range(n) ]
for i in range(1,n):
	A[i][0] = A[i-1][0] + insertcost
for j in range(1,m):
	A[0][j] = A[0][j-1] + deletecost
# align source and target strings
for j in range(1,m):
	for i in range(1,n):
		inscost = insertcost + A[i-1][j]
		delcost = deletecost + A[i][j-1]
		if (source[j-1] == target[i-1]): add = 0
		else: add = replacecost
		substcost = add + A[i-1][j-1]
		A[i][j] = min(inscost,delcost,substcost)
#return min edit distance
min_dist = A[n-1][m-1]
print "Levenshtein distance = " + str(min_dist)

#Call function to backtrack through array, then loop through result to print alignments
alignments = get_ops(n-1, m-1)

for alignment in alignments:
	sourcestring = ""
	middlerow = ""
	targetstring = ""
	for column in alignment:
		sourcestring += column[0] + ' '
		targetstring += column[1] + ' '
		if column[0] == column[1]:
			middlerow += "| "
		else:
			middlerow += "  "
	print sourcestring
	print middlerow
	print targetstring
	print
	
