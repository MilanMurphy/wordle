"""
Created on Mon Sep 28 13:11:00 2026

@author: melon
"""
"""WordleV4 by Milan Murphy mjmurph1@ualberta.ca"""
"Intended for the ENCMP 100 fall 2026 competition"

import numpy as np
import random
import matplotlib.pyplot as plt

#Setup three lists, 
validWordList = np.char.lower(np.genfromtxt('wordlist.csv', dtype=str))
validAnswerList = np.char.lower(np.genfromtxt('wordbank.csv', dtype=str))
wordPriority = dict(np.genfromtxt('wordPriority.csv', dtype=str, delimiter=","))
for i in wordPriority:
    wordPriority[i] = float(wordPriority[i])




def main():
    """Manages starting and exiting the program.
    Allows user to navigate the program through an input.\n
    Inputs: None \n
    Returns: None
    """
    
    start = input(""""Type EXIT to close the program, HELP for help, 
GAME to play the game, or SOLVE to use the solver.""")
    
    if start.lower() == "exit":
        pass
    elif start.lower() == "game": 
        game()
    elif start.lower() == "solve":
        solve()
    elif start.lower() == "help":
        print("""
Wordle is a word guessing game, where you input five letter words
and recieve hints based on how correct each letter is. A grey letter 
means that that letter is not in the final word. A yellow letter is 
included in the final word, but in a different collumn. A green letter 
is a correct letter in the correct column. Use these hints to form your 
guesses.
\n
In the solver, you may input any legal finishing word and the program 
will try to guess it in as little guesses as possible.
\n""")
        main()
    else: main()


def game(): 
    """Manages the game flow of Wordle.
    This includes generating words, plotting,
    and winning / losing. \n
    Inputs: None \n
    Returns: None
    """
    
    word = random.choice(validAnswerList)
    plotGame([], [], 0)
    answer = wordToArray(word)
    guessesEval = []
    guesses = []
    turn = 0
    win = False
    
    #game loop
    for i in range(0,6):
        turn += 1
        guesses.append(askGuess())
        guessesEval.append(evaluateGuess(guesses[i], answer))
        plotGame(guessesEval, guesses, turn)
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
    """Gets and validates the user guess inputs.
    Can invoke itself
    Inputs: None \n
    Returns: guess - 1d array of strings [x,y,z,i,j]"""
    
    guess = input("Guess: ")
    if type(guess) == str and len(guess) == 5 and np.any(validWordList == guess.lower()):
        return wordToArray(guess.lower())
    else: 
        print("Invalid Guess!")
        return(askGuess())
    
def askWord():
    """Gets and validates the user solver inputs.
    Can invoke itself.
    Inputs: None \n
    Returns: wordToSolve - 1d array of strings [x,y,z,i,j]"""
    #Gets and validates the word the user inputs
    #Returns the word when it is valid
    #Invokes itself if a guess is invalid
    wordToSolve = input("Word: ")
    if type(wordToSolve) == str and len(wordToSolve) == 5 and np.any(validAnswerList == wordToSolve.lower()):
        return wordToArray(wordToSolve.lower())
    else: 
        print("Invalid Word!")
        return(askWord())

def evaluateGuess(guess, answer):
    """Evaluates a guess for the 
    return hints. \n
    Inputs: guess - users guess \n
    answer - the game answer \n
    Returns: correct - an array of the hints
    
    
    """
    
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
    """Converts a string to a one dimentional array \n
    Inputs: word - string \n
    Returns: arr - array \n
    """
    j = 0
    arr = np.full(5, '')
    for i in word:
        arr[j] = i
        j += 1
    return(arr)

def plotGame(guessesEval, guesses, turns):
    """Creates a plot of the current game state \n
    Inputs: guessesEval - array of hints for every guess \n
    guesses - array of every guess \n
    turns - turn number \n
    Returns: None
    
    """
        
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
    turns = 6-turns
    plt.title(f"Turns left: {turns}")
    plt.xlim(-1, 5)
    plt.ylim(0, 7)
    plt.axis("off")
    plt.show()
    pass

def solve():
    """Controls the game flow for the computer solver \n
    Inputs: None \n
    Returns: None
    """
    
 
    greens = []
    yellows = []
    guessList = validAnswerList.copy()
    startingWord = "slant"
    word = askWord()
    plotGame([], [], 0)
    answer = wordToArray(word)
    guessesEval = []
    guesses = []
    turn = 0
    win = False
    
    #game loop
    for i in range(0,6):
        turn += 1
        solver = findBestGuess(guesses, guessesEval, turn, guessList, greens, yellows, startingWord)
        guessList = solver[1].copy()
        guesses.append(wordToArray(solver[0]))
        guessesEval.append(evaluateGuess(guesses[i], answer))
        greens = solver[2]
        yellows = solver[3]
        
        plotGame(guessesEval, guesses, turn)
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
    
def findBestGuess(guesses, guessesEval, turn, guessList, greens, yellows, startingWord):
    """Finds the best guess for the next word based on the current game state,
    and the list of word priorities. \n
    Inputs: guesses - all  guesses \n
    guessesEval - all  hints \n
    turn - turn number \n
    guessList - array of all possible gueses left\n
    greens - list of green letters \n
    yellows - list of all yellow letters \n
    startingWord - the starting word for the program\n
    Returns: guess - the best guess \n
    guessList - list of possible guesses \n
    greens - all green letters \n
    yellows - all yellow letters \n"""
   
    if turn != 1:
    
        #solve loop 1
        for i in range(0,5):
            letter = guesses[turn-2][i]
            
            #Green square loop
            if guessesEval[turn-2][i] == 2:
                greens.append(letter)
                
                x = np.where(np.array([word[i] != letter for word in guessList]))
                #the for loop logic in the above line was made with
                #ai assistance
                guessList = filterX(x, guessList).copy()
             
            #Yellow square loop part one
            if guessesEval[turn-2][i] == 1:
                yellows.append(letter)
                x = np.where(np.array([word[i] == letter for word in guessList]))
                #the for loop logic in the above line was made with
                #ai assistance
                guessList = filterX(x, guessList).copy()
            
           
                
        for i in range(0,5):
            letter = guesses[turn-2][i]
            
            #second yellow suqare loop
            for j in yellows:
                x = np.where(np.array([j not in word for word in guessList]))
                #the for loop logic in the above line was made with
                #ai assistance
                guessList = filterX(x, guessList).copy()         
            
            #deal with the grays
            if guessesEval[turn-2][i] == 0:
                x = np.where(np.array([letter in word and letter not in greens 
                            and letter not in yellows for word in guessList]))
                #the for loop logic in the above line was made with
                #ai assistance
                #im sure theres a better way to do this ^^^^
                guessList = filterX(x, guessList).copy()
                
            #gray square loop part one
            if guessesEval[turn-2][i] == 0:
                x = np.where(np.array([word[i] == letter for word in guessList]))
                #the for loop logic in the above line was made with
                #ai assistance
                guessList = filterX(x, guessList).copy()
                
                
                
            
        guess = evaluatePriority(guessList)
        
    else:
        #deal with the starting word
        guess = startingWord
        
        x = np.where(np.array([word == startingWord for word in guessList]))
        guessList = filterX(x, guessList).copy()
    
        
    
    return(guess, guessList, greens, yellows)
    pass

    
def filterX(x, guessList):
    """Filters the array based on a filter variable, and replaces the list
    with the filtered array \n
    Inputs: x - the filter array \n
    guessList - the list to filter \n
    Returns: newGuessList - the filtered list
    """
    filter = np.full(len(guessList), True)
    filter[x] = False
    newGuessList = guessList[filter]
    return(newGuessList)


def evaluatePriority(guessList):
    """Picks what word has the highest priority based on the 
    remaining guess list \n
    Inputs: guessList - remaining possible words \n
    Returns: word - picked word"""
    priority = 9
    word = ""
    for i in guessList:
        x = wordPriority[i]
        if x < priority:
            priority = x
            word = i
    return(word)
            

if __name__ == '__main__':
    main()