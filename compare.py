#!/usr/bin/python
# -*- coding: UTF8 -*-

import sys
import codecs
import re
import glob
import csv
import unicodecsv

score = 0
numberOfLists = 0
numberIncluded = 0
numberNotIncluded = 0
wordsIncluded = {}
wordsNotIncluded = {}
scoreForEach = {}

listsWords = {}

input = {}

with codecs.open("input.csv", "r") as file:
	reader = unicodecsv.reader(file, delimiter=',', encoding='utf-8')
	for row in reader:
		word = re.sub(u'[^ء-يa-zA-Z\p{P} ]', '', row[0]) #Remove all dacritics from word
		input[word] = float(row[1])
		
for fileName in glob.glob("lists/*.csv"):
	numberOfLists += 1
	listsWords[fileName] = {}
	
	with codecs.open(fileName, "r") as file:
		reader = unicodecsv.reader(file, delimiter=',', encoding='utf-8')

		length = 0
		
		curListScore = 0
		for row in reader:
			length += 1
			#print str(row) + " " + str(length) + " " + fileName
			word = re.sub(u'[^ء-يa-zA-Z\.,،?؟! ]', '', row[0]) #Remove all dacritics from word
			frequency = float(row[1])
			
			listsWords[fileName][word] = frequency

			if(word == ""):
				print fileName + " " + str(length)
			if(word in input):
				curListScore += input[word] / frequency
				if(word in wordsIncluded):
					wordsIncluded[word] += frequency
				else:
					numberIncluded += 1
					wordsIncluded[word] = frequency
			else:
				if(word in wordsNotIncluded):
					wordsNotIncluded[word] += frequency
				else:
					numberNotIncluded += 1
					wordsNotIncluded[word] = frequency

		curListScore = curListScore / length
		scoreForEach[fileName] = curListScore
		score += curListScore
score = score / numberOfLists

print "Total Score: " + str(score)
print "Number of Words in input list: " + str(numberIncluded)
print "Number of Words not in input list: " + str(numberNotIncluded)
print("-----------------------------------")
print("-----------------------------------")
print("List scores------------------------")
print("-----------------------------------")
for score in scoreForEach:
	print("For " + score + ": " + str(scoreForEach[score]))
	
res = "word" #Temp container of output text
for list in listsWords:
	res += ", " + list
res += "\n"

for word in wordsIncluded:
	res += word
	for list in listsWords:
		if word in listsWords[list]:
			res +=  ", " + str(listsWords[list][word])
		else:
			res += ", 0"
	res += "\r\n"

with codecs.open("included.csv", 'w', "utf8") as file:
	file.write(res)

res = "word"
for list in listsWords:
	res += ", " + list
res += "\n"

for word in wordsNotIncluded:
	res += word
	for list in listsWords:
		if word in listsWords[list]:
			res +=  ", " + str(listsWords[list][word])
		else:
			res += ", 0"
	res += "\r\n"

with codecs.open("notincluded.csv", 'w', "utf8") as file:
	file.write(res)
	
res = ""
for word in input:
	if(not(word in wordsNotIncluded or word in wordsIncluded)):
		res += word + "\r\n"

with codecs.open("includedandnotfoundinlists.csv", 'w', "utf8") as file:
	file.write(res)