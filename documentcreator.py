from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys



def getwords():

    #getting data from website 
    r = requests.get('https://www.ef.edu/english-resources/english-vocabulary/top-3000-words/')

    #making soup object
    soup = BeautifulSoup(r.text, features="html.parser")


    #finding div
    div = soup.find('div', class_ = 'field-item even')

    #finding p tag with word list
    uF = div.find('p').findNext('p').getText()

    #making words string into list of string
    filt = uF.split()

    #make file with all words
    wordlist = open("words.txt", 'w')
    #convert all strings to lowercase
    for word in filt:
        word = word.lower()
        wordlist.write(word +'\n')

    wordlist.close()

    return filt




def getdefin(word,doc):
    print(word)
   
    #get definitions
    wordurl= requests.get("https://www.lexico.com/en/definition/" + word)
    soupword = BeautifulSoup(wordurl.text, features="html.parser")


    div = soupword.find_all('ul', class_ = 'semb')

    if len(div) < 3:
        num = len(div)
    else:
        num = 3
    
    
    meaninglist = set()
    for element in div[0:num]:
        
        
        #if meaning has no example sentences we dont need it
        if len(element.find_all('li', class_ = 'ex')) == 0:
            print(len(element.find_all('li', class_ = 'ex')))
            continue
        else:
            #get meaning
            meaning = element.find('p').getText()


            #some words show two of the same meaning for some reason
            #this is to not add a meaning if it was already written to file

            if(meaning in meaninglist):
                print("SKIPPED")
                continue
                
            else:
                print('false')
                meaninglist.add(meaning)



            #indicate that we are about to write a meaning to file
            print("--meaning")
            doc.write("--meaning"+'\n')


            #get rid of unnecessary numbers in meaning
            if(meaning[0].isdigit()):
                meaning = meaning.replace(meaning[0],'')

            #change meaning to all lowercase, there are unnecessary capitalizations sometimes
                meaning = meaning.lower()

            #write meaning to file
            doc.write(meaning+'\n')
            


            #get sentences
            doc.write("--sentences"+'\n')
            if len(element.find_all('li', class_ = 'ex')) < 6:
                num = len(element.find_all('li', class_ = 'ex'))
            else:
                num = 6

            for sentence in element.find_all('li', class_ = 'ex')[0:num]:
                print(sentence)
                # wordin = ' ' + word + ' '

                try:
                    doc.write(sentence.getText()+'\n')
                # block raising an exception
                except:
                    pass # doing nothing on exception
                    
                #print(sentence.getText())

        
    #get synonyms
    doc.write("--synonyms"+'\n')
    synonymurl= requests.get("https://thesaurus.yourdictionary.com/" + word)
    sdoc = BeautifulSoup(synonymurl.text, features="html.parser")
    synonyms = sdoc.find_all('div', class_ = 'synonym')

    if(len(synonyms) < 4):
        for element in synonyms:
            try:
                doc.write(element.getText()+'\n')
            # block raising an exception
            except:
                pass # doing nothing on exception
    else:
        for element in synonyms[:4]:
            try:
                doc.write(element.getText()+'\n')
            # block raising an exception
            except:
                pass # doing nothing on exception

#driver to make the txt files
def maketxt():

    
    
    #make txt file for every word
    for word in getwords():
        
        #if txt file already has data, then skip and move on to next word
        doc = open(word +".txt", 'r',encoding='utf-8')
        file = doc.read()
        if("--meaning" in file):
            print("meaning in doc")
            doc.close()
            continue
        doc.close()
        
        #if no data in file, add relevant data to file
        doc = open(word +".txt", 'w',encoding='utf-8')
        

        doc.write(word+'\n')
        getdefin(word, doc)
        doc.close()
        
    

       



maketxt()
#doc = open('a' +".txt", 'r',encoding='utf-8')
#doc =doc.read()
#print(("--meaning" in doc))
#getdefin('conclude', doc)
#getwords()
