import os.path
import sys
from word_forms.word_forms import get_word_forms

#this is a method to switch the synonym with
#the word in its example sentence

save_path = 'C:/Users/Milan Trivedi/Desktop/Python/Research/Dataset1Synonymswitch'


def createsentence(word):
	word = word[0]
	print(word)

	#open file for specific word
	doc = open(word + '.txt', 'r',encoding='utf-8')
	file = doc.read()


	# if(not("--meaning" in file)):
 #            print("no meanings")
 #            doc.close()
 #            return

	lines = file.split("\n")
	
	
	synonyms = []
	condition = False

	

	#go through file and make list of synoynms

	for line in lines:
		

		if(line == '--synonyms'):
		 	condition = True


		if(condition):
			if(len(line.split('    '))>1):
				synonym = line.split('    ')[0]
				synonyms.append(synonym)
	print(synonyms)


	file_name = word + ".txt"

	completeName = os.path.join(save_path, file_name)
	file = open(completeName,"w", encoding = 'utf-8' )

	file.write(word + '\n')

	#go line by line and add relevant information to new txt file

	
	condition2 = False
	condition3 = False

	for line in lines:

		# print(line)
		
		if(line == '--sentences'):
		 	condition2 = True
		 	condition3 = False
		 	
		if(line == '--meaning'):
			condition2 = False
			condition3 = True

		if(line == '--synonyms'):
			condition2 = False
			condition3 = False

		if(condition2):
			if(line != '--sentences'):
				for synonym in synonyms:
					file.write(line + '\n')
					file.write(sentenceswap(word,synonym,line) + '\n')
					
	 				
				

				

		if(condition3):
			
			file.write(line + '\n')
			
		

	
	doc.close()



#this method will switch the synonym and the word	
def sentenceswap(word,synonym,sentence):


	wordlist = get_word_forms(word)


	#get list of forms that the word is in
	formlist = []
	for form in wordlist.items():
		if(word in form[1]):
			formlist.append(form[0])

	#get list of words from all the different type of forms
	dforms = []
	for i in formlist:
		for x in wordlist[i]:
			dforms.append(x)

	#if any of the forms are found in sentence, change word, and then break
	for newword in dforms:
		newword = " " + newword + " "
		if(newword in sentence):
	 		word  = newword
	 		break

	synonym = " " + synonym + " "
	

	#make the new sentence
	newsent = sentence.replace(word,synonym)
	return newsent


def synonymswitch():

	
	file = open("words.txt", 'r',encoding='utf-8') 

	counter = 0
	for line in file:
		# if(counter == 30):
		# 	return
		counter = counter + 1
		print(counter)
		createsentence(line.split())

#print(sentenceswap("acquire", "obtain", "I acquired the gold medal"))
#print(get_word_forms("acquire"))
synonymswitch()



