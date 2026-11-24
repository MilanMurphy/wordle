"""
Created on Mon Sep 28 13:11:00 2026

@author: melon
"""
"""WordleV1 by Milan Murphy mjmurph1@ualberta.ca"""
"Intended for the ENCMP 100 fall 2026 competition"

import numpy as np
import random
validWordList = np.char.lower(np.genfromtxt('wordlist.csv', dtype=str))

def main():
    #Manages starting and exiting the program, also generates the word
    word = random.choice(validWordList)
    start = input("Type EXIT to close the program, or START to start the game: ")
    
    if start.lower() == "exit":
        pass
    elif start.lower() == "start":
        game(word)
    else: main()


def game(word): 
    #Takes the game answer as input Word
    #manages the flow of the game (ex guesses, evaluating wins)
    
    answer = wordToArray(word)
    turn = 0
    
    while turn <= 6:
        guess = askGuess()
        guess = evaluateGuess(guess, answer)
        if np.all(guess == 2):
            print("WIN")
            break
        print(guess)
    
    print("Word was:", word)
    
    pass

def askGuess():
    #Gets and validates the guess the user inputs
    #Returns the guess when it is valid
    #Invokes itself if a guess is invalid
    guess = input("Guess: ")
    if (type(guess) == str and len(guess) == 5 
        and np.any(validWordList == guess.lower())):
        return wordToArray(guess)
    else: 
        print("Invalid Guess!")
        return(askGuess())

def evaluateGuess(guess, answer):
    #Evaluates a guess, taking the users guess, and the game answer as its 
    #parameters
    #Returns an array in the form of [x,y,z,j,k], where each letter is a
    #number between 0-2, with 0 being not in the word, 1 being in the word
    #in the wrong place, and 2 being the correct letter in the
    #correct place
    if np.array_equal(guess, answer):
        return np.full(5,2)
    
    else:
        correct = np.full(5, 0)
        answerTemp = answer.copy()
        for i in range(0,5):
            if answerTemp[i] == guess[i]:
                correct[i] = 2
                answerTemp[i] = "."
        for i in range(0,5):
            if correct[i] == 2:
                continue
            if np.any(answerTemp == guess[i]):
                correct[i] = 1
                for j in range(0,5):
                    if answerTemp[j] == guess[i]:
                        answerTemp[j] = "."
                        break
        
        return[correct]
    
    pass
    
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

main()

