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
    
def wordToArray(word):
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
    guessList = validAnswerList.tolist()
    answer = wordToArray(word)
    guessesEval = []
    guesses = []
    turn = 0
    win = False
    
    for i in range(0,6):
        turn += 1
        solver = findBestGuess(guesses, guessesEval, turn, guessList, startingWord)
        guessList = solver[1]
        guesses.append(wordToArray(solver[0]))
        guessesEval.append(evaluateGuess(guesses[i], answer))
        if np.array_equal(guesses[i], answer):
            win = True
            break
        
    #handle game ending
    if win == True:

        return(turn)
    else: 
        return(turn*1.5)
    main()
    
    
    
    pass
    
def findBestGuess(guesses, guessesEval, turn, guessList, startingWord):
    
    if turn != 1:
        greens = []
        yellows = []
        for i in range(0,5):
            if guessesEval[turn-2][i] == 2:
                greens.append(guesses[turn-2][i])
                for j in guessList[:]:
                    if j[i] != guesses[turn-2][i]:
                        guessList.remove(j)
             
            if guessesEval[turn-2][i] == 1:
                yellows.append(guesses[turn-2][i])
                for j in guessList[:]:
                    if j[i] == guesses[turn-2][i]:
                        guessList.remove(j)   
        
        for i in range(0,5): 
            if guessesEval[turn-2][i] == 1:
                for j in guessList[:]:
                    if not guesses[turn-2][i] in j:
                        guessList.remove(j)
                
            if guessesEval[turn-2][i] == 0:
                for j in guessList[:]:
                    if guesses[turn-2][i] in j and not guesses[turn-2][i] in greens and not guesses[turn-2][i] in yellows:
                        guessList.remove(j)
                    elif j[i] == guesses[turn-2][i]:
                        guessList.remove(j)
    else:
        guess = startingWord
                        
    guess = guessList[np.random.randint(0,len(guessList))]
    return(guess, guessList)
    pass



main()