"""
Created on Mon Sep 28 13:11:00 2026

@author: melon
"""
"""2 by Milan Murphy mjmurph1@ualberta.ca"""
"Intended for the ENCMP 100 fall 2026 competition"

import numpy as np
import csv
validWordList = np.char.lower(np.genfromtxt('wordlist.csv', dtype=str))
validAnswerList = np.char.lower(np.genfromtxt('wordbank.csv', dtype=str))
turnData = {}
wordPriority = dict(np.genfromtxt('wordPriority.csv', dtype=str, delimiter=","))
for i in wordPriority:
    wordPriority[i] = float(wordPriority[i])


def main():
    
    #Manages starting and exiting the program
    start = input("Type EXIT to close the program, SOLVE to use the solver.")
    
    if start.lower() == "exit":
        pass
    elif start.lower() == "solve":
        divvy = len(validAnswerList)
        for i in validAnswerList:
            turnData[i] = 0
            for j in validAnswerList:
                turnData[i] += solve(i, j)
            turnData[i] /= divvy
            print("")
            print("words complete:", len(turnData))
            print("word:", i, "Average Guesses:", turnData[i])
         
        #the below code is code slightly edited from the solution on 
        #https://stackoverflow.com/questions/24769600/write-python-
        #dictionary-to-csv-columns-keys-to-first-column-values-to-second
        #via user zsquare
        with open('startingWordResults.csv', 'w') as f:
            writer = csv.writer(f)
            for row in turnData.items():
                writer.writerow(row)
            print("done")
        
                
    else: main()

def evaluateGuess(guess, answer):
    #Evaluates a guess, taking the users guess, and the game answer as its 
    #parameters
    #Returns an array in the form of [x,y,z,j,k], where each letter is a
    #number between 0-2, with 0 being not in the word, 1 being in the word
    #in the wrong place, and 2 being the correct letter in the
    #correct place
    
    guessTemp = np.copy(guess)
    answerTemp = np.copy(answer)
    
    #shorcut for winning guesses
    if np.array_equal(guess, answer):
        return np.full(5,2)
    
    else:
        
        correct = np.full(5, 0)
        
        #start by evaluating green squares
        for i in range(0,5):
            if answerTemp[i] == guessTemp[i]:
                correct[i] = 2
                #ensures these squares are not considered when calculating
                #yellows
                answerTemp[i] = ","
                guessTemp[i] = "."
                
        #get the count of each letter for yellows
        letterCount = {}
        for i in answerTemp:
            if i in letterCount:
                letterCount[i] += 1
            else: letterCount[i] = 1
        
        #evaluate yellows
        for i in range(0,5):
            if guessTemp[i] in letterCount and letterCount[guessTemp[i]] >= 1:
                letterCount[guessTemp[i]] -= 1
                correct[i] = 1
    
        return(correct)
    
def wordToList(word):
    #Convers a string to a one dimentional list where each
    #Item is each letter of the string
    #Returns a list
    j = 0
    arr = np.full(5, '')
    for i in word:
        arr[j] = i
        j += 1
    return(arr)

def solve(startingWord, word):
    greens = []
    yellows = []
    guessList = validAnswerList.copy()
    answer = wordToList(word)
    guessesEval = []
    guesses = []
    turn = 0
    win = False
    
    for i in range(0,6):
        turn += 1
        solver = findBestGuess(guesses, guessesEval, turn, guessList, greens, yellows, startingWord)
        guessList = solver[1].copy()
        guesses.append(wordToList(solver[0]))
        guessesEval.append(evaluateGuess(list(guesses[i]), answer))
        greens = solver[2]
        yellows = solver[3]
        
        if np.array_equal(guesses[i], answer):
            win = True
            break
        
    #handle game ending
    if win == True:

        return(turn)
    else: 
        return(turn*1.5)
    main()
    
    
    

    

def findBestGuess(guesses, guessesEval, turn, guessList, greens, yellows, startingWord):
   
    if turn != 1:
    
        #solve loop 1
        for i in range(0,5):
            letter = guesses[turn-2][i]
            
            #Green square loop
            if guessesEval[turn-2][i] == 2:
                greens.append(letter)
                
                x = np.where(np.array([word[i] != letter for word in guessList]))
                guessList = filterX(x, guessList).copy()
             
            #Yellow square loop part one
            if guessesEval[turn-2][i] == 1:
                yellows.append(letter)
                x = np.where(np.array([word[i] == letter for word in guessList]))
                guessList = filterX(x, guessList).copy()
                
        for i in range(0,5):
            letter = guesses[turn-2][i]
            
            #second yellow suqare loop
            for j in yellows:
                x = np.where(np.array([j not in word for word in guessList]))
                guessList = filterX(x, guessList).copy()         
            
            #deal with the grays
            if guessesEval[turn-2][i] == 0:
                x = np.where(np.array([letter in word and letter not in greens and letter not in yellows for word in guessList]))
                guessList = filterX(x, guessList).copy()
                
                
            
        guess = evaluatePriority(guessList)
        
    else:
        #deal with the starting word
        guess = startingWord
        
        x = np.where(np.array([word == startingWord for word in guessList]))
        guessList = filterX(x, guessList).copy()
    
        
    
    return(guess, guessList, greens, yellows)
    pass

    #Filters the list based on a filter variable, and replaces the list
    #Helps with effeciency when running a large number of games
def filterX(x, guessList):
    filter = np.full(len(guessList), True)
    filter[x] = False
    newGuessList = guessList[filter]
    return(newGuessList)

    #picks words based on what has the highest priority
def evaluatePriority(guessList):
    priority = 9
    word = ""
    for i in guessList:
        x = wordPriority[i]
        if x < priority:
            priority = x
            word = i
    return(word)
            


main()