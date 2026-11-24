"""
Created on Mon Sep 28 13:11:00 2026

@author: melon
"""
"""2 by Milan Murphy mjmurph1@ualberta.ca"""
"Intended for the ENCMP 100 fall 2026 competition"

import numpy as np
import random
import matplotlib.pyplot as plt
validWordList = np.char.lower(np.genfromtxt('wordlist.csv', dtype=str))
validAnswerList = np.char.lower(np.genfromtxt('wordbank.csv', dtype=str))



def main():
    
    #Manages starting and exiting the program
    start = input("Type EXIT to close the program, GAME to play the game, or SOLVE to use the solver.")
    
    if start.lower() == "exit":
        pass
    elif start.lower() == "game": 
        game()
    elif start.lower() == "solve":
        solve()
    else: main()


def game(): 
    word = random.choice(validAnswerList)
    plotGame([], [])
    #Takes the game answer as input Word
    #manages the flow of the game (ex guesses, evaluating wins)
    answer = wordToArray(word)
    guessesEval = []
    guesses = []
    turn = 0
    win = False
    
    for i in range(0,6):
        turn += 1
        guesses.append(askGuess())
        guessesEval.append(evaluateGuess(guesses[i], answer))
        plotGame(guessesEval, guesses)
        if np.array_equal(guesses[i], answer):
            win = True
            break
        
    #handle game ending
    if win == True:
        print("You won in", str(turn), "guesses!")
    else: 
        print("You lost! The word was", word)
    main()
    pass

def askGuess():
    #Gets and validates the guess the user inputs
    #Returns the guess when it is valid
    #Invokes itself if a guess is invalid
    guess = input("Guess: ")
    if type(guess) == str and len(guess) == 5 and np.any(validWordList == guess.lower()):
        return wordToArray(guess)
    else: 
        print("Invalid Guess!")
        return(askGuess())
    
def askWord():
    #Gets and validates the word the user inputs
    #Returns the word when it is valid
    #Invokes itself if a guess is invalid
    guess = input("Word: ")
    if type(guess) == str and len(guess) == 5 and np.any(validAnswerList == guess.lower()):
        return wordToArray(guess)
    else: 
        print("Invalid Word!")
        return(askWord())

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

def plotGame(guessesEval, guesses):
    #Takes guessesEval and guesse as input
    #guessesEval is a 2d array with every current and past guess, as well
    #as their correctness, where guesses has every current and pass guess
    #as a wordToArray() array
    #plots the game to the plots window
        
    for i in range(0,6):
        for j in range(0,5):
         
            if i < len(guessesEval):
                if guessesEval[i][j] == 2:
                    plt.plot(j,6-i, "gs", markersize=25)
                elif guessesEval[i][j] == 1:
                    plt.plot(j,6-i, "ys", markersize=25)
                else: plt.plot(j, 6-i, color="gray",marker="s", markersize=25)
                plt.text(j-0.15,6-i-0.25,str(guesses[i][j]).upper(), color="white", fontsize=22)
            else:   plt.plot(j, 6-i, color="black",marker="s", markersize=25)

    plt.xlim(-1, 5)
    plt.ylim(0, 7)
    plt.axis("off")
    plt.show()
    pass

def solve():
    guessList = validAnswerList.tolist()
    word = askWord()
    plotGame([], [])
    answer = wordToArray(word)
    guessesEval = []
    guesses = []
    turn = 0
    win = False
    
    for i in range(0,6):
        turn += 1
        solver = findBestGuess(guesses, guessesEval, turn, guessList)
        guessList = solver[1]
        guesses.append(wordToArray(solver[0]))
        guessesEval.append(evaluateGuess(guesses[i], answer))
        plotGame(guessesEval, guesses)
        if np.array_equal(guesses[i], answer):
            win = True
            break
        
    #handle game ending
    if win == True:
        print("The computer won in in", str(turn), "guesses!")
    else: 
        print("It lost! The word was", word)
    main()
    
    
    
    pass
    
def findBestGuess(guesses, guessesEval, turn, guessList):
    input()
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
                        
    guess = guessList[np.random.randint(0,len(guessList))]
    return(guess, guessList)
    pass



main()