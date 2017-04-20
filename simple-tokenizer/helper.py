#!/usr/bin/python

#Amerie Lommen & Dominic Pearson
#CS 404 Group Assignment 1 - Question 1: Tokenization
#Part 2: Write your own tokenize
#Item (a): Class to separate punctuation from words

class hw1_tokenizer:
    #List of individual tokens
    tokens =[]
    
    #List of contraction expansions
    expansions = {"'m":"am",
                                    "'ll":"will",
                                    "'re":"are",
                                    "n't":"not",
                                    "wo":"will",
                                    "'ve":"have",
                                    "'d":"would",
                                    "ca": "can"}

    #Check if character is a punctuation
    def is_punct(self, char):
        return (not char.isalnum()) and (not char.isspace())

    #Add word to list of tokens after performing expansion. Also check if word is the beginning of a sentence and update num_sentences
    def record(self, word):
        if word and not word.isspace():	
            #Check if word is the first word in a sentence
            last_word = self.tokens[len(self.tokens) - 1] if len(self.tokens) > 0 else ""
            last_char = last_word[len(last_word) - 1] if len(last_word) > 0 else ""
            if last_char == "" or (last_char == '!' or last_char == '?' or last_word == "..." or last_char == '.') and word[0].isupper():
                self.num_sentences += 1
            if word in self.expansions:
                self.tokens.append(self.expansions[word])
            else:
                self.tokens.append(word)

    #Takes a string and places individual tokens in the token list
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
            #Record '.' as token if surrounded by characters or at end of token containing other '.'s
            #i.e. if not part of actonym such as U.S.A.
            elif data[c] == '.':
                if (data[c+1].isspace() and not any(char == '.' for char in data[start:c])) or (self.is_punct(data[c+1]) or self.is_punct(data[c-1])):
                    self.record(data[start:c])
                    self.record(data[c])
                    start = c + 1
                #If previous 2 chars are '.', record ('...') as token
                elif c > 1 and data[c-1] == '.' and data[c-2] == '.':
                    self.record(data[start:c-2])
                    self.record(data[c-2:c+1])
                    start = c + 1
            #Record "'" as token if whitespace on either side (i.e. is acting as quote)
            #Otherwise, "'" is start of next token unless previous character was n (which is included in next token) and next is t		
            elif data[c] == "'":
                if data[c+1].isspace() or c < 1 or data[c-1].isspace():
                    self.record(data[start:c])
                    self.record(data[c])
                    start = c + 1
                else:
                    if data[c-1] == 'n' and data[c+1] == 't':
                        self.record(data[start:c-1])
                        start = c-1
                    else:
                        self.record(data[start:c])
                        start = c
            #Record ':' as token if whitespace on either side (i.e. not part of time expression such as 11:00 or a URL)
            elif data[c] == ':':
               if data[c+1].isspace() or c < 1 or data[c-1].isspace():
                    self.record(data[start:c])
                    self.record(data[c])
                    start = c + 1
            #Record '/' as token if part of token containing '.' or ':' (i.e. a URL) or either side is not a number
            #(i.e. is part of a date expression such as 01/16/2016)
            elif data[c] == '/':
                if not any(char == '.' or char == ':' for char in data[start:c]) and (not data[c+1].isdigit() and not data[c+1].isdigit()):
                    self.record(data[start:c])
                    self.record(data[c])
                    start = c + 1
            #Record following punctuation as tokens if either side is space or punctuation (otherwise part of URL or email)
            elif data[c] in ['@','_','?','-','+','=','&']:
                if data[c+1].isspace() or self.is_punct(data[c+1]) or data[c-1].isspace() or self.is_punct(data[c-1]):
                    self.record(data[start:c])
                    self.record(data[c])
                    start = c + 1
            #Record all other punctuation as tokens
            elif not(data[c].isalnum()) and not data[c] == '\\' and not data[c] == '$':
                 self.record(data[start:c])
                 self.record(data[c])
                 start = c + 1
    
    #On instantiation, perform tokenization and count sentences
    def __init__(self, raw_string):
        self.string = raw_string
        self.num_sentences = 0
        self.tokenize()

