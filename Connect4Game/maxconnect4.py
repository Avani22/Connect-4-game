#!/usr/bin/env python

# Written by Chris Conly based on C++
# code provided by Dr. Vassilis Athitsos
# Written to be Python 2.4 compatible for omega

import sys
from MaxConnect4Game import *
import time             
start = time.time()

def oneMoveGame(currentGame,depth):
    if currentGame.pieceCount == 42:    # Is the board full already? (6*7=42)
        print 'BOARD FULL\n\nGame Over!\n'
        sys.exit(0)

    move=currentGame.aiPlay(currentGame, depth) # Make a move
    result=currentGame.playPiece(move)
    operationsAfterMove(currentGame,move)
    currentGame.gameFile.close()                #close file after all the moves

def interactiveGame(currentGame,depth):
    while not currentGame.pieceCount==42:
        if currentGame.currentTurn==1:
            userMove=input("Enter the column number [1-7]:")        #user plays
            if not 0<userMove<8:
                print"Invalid column number!"
                continue
            if not currentGame.playPiece(userMove-1):
                print"This column is full!"
                continue
            try:
                currentGame.gameFile=open("human1.txt",'w')
            except:
                sys.exit("Error opening the output file!")

            operationsAfterMove(currentGame, userMove-1)

        elif not currentGame.pieceCount==42:
            move=currentGame.aiPlay(currentGame,depth)          #computer plays
            result=currentGame.playPiece(move)
            try:
                currentGame.gameFile=open("computer1.txt",'w')
            except:
                sys.exit("Error opening the output file!")

            operationsAfterMove(currentGame,move)

    currentGame.gameFile.close()

    if currentGame.player1Score>currentGame.player2Score:
        print "Player 1 wins!"
    elif currentGame.player2Score>currentGame.player1Score:
        print "Computer wins!"
    else:
        print"It is a draw!"

    print "Thank you for playing MaxConnect4Game!!!"

def operationsAfterMove(currentGame,move):
    print("\n\n Move no. %d: Player %d, column %d \n"% (currentGame.pieceCount, currentGame.currentTurn, move+1))
    if currentGame.currentTurn==1:
        currentGame.currentTurn=2
    elif currentGame.currentTurn==2:
        currentGame.currentTurn=1

    print'Game state after move:'
    currentGame.printGameBoard()

    currentGame.countScore()
    print('Score:Player 1= %d, Player 2= %d\n' % (currentGame.player1Score, currentGame.player2Score))

    currentGame.printGameBoardToFile()
    currentGame.gameFile.close()


def main(argv):
    # Make sure we have enough command-line arguments

    if len(argv) != 5:
        print 'Four command-line arguments are needed:'
        print('Usage: %s interactive [input_file] [computer-next/human-next] [depth]' % argv[0])
        print('or: %s one-move [input_file] [output_file] [depth]' % argv[0])
        sys.exit(2)

    game_mode, inFile = argv[1:3]

    if not game_mode == 'interactive' and not game_mode == 'one-move':
        print('%s is an unrecognized game mode' % game_mode)
        sys.exit(2)

    currentGame = maxConnect4Game() # Create a game

    # Try to open the input file
    try:
        currentGame.gameFile = open(inFile, 'r')
    except IOError:
        sys.exit("\nError opening input file.\nCheck file name.\n")

    # Read the initial game state from the file and save in a 2D list
    file_lines = currentGame.gameFile.readlines()
    currentGame.gameBoard = [[int(char) for char in line[0:7]] for line in file_lines[0:-1]]
    currentGame.currentTurn = int(file_lines[-1][0])
    currentGame.gameFile.close()

    print '\nMaxConnect-4 game\n'
    print 'Game state before move:'
    currentGame.printGameBoard()

    # Update a few game variables based on initial state and print the score
    currentGame.checkPieceCount()
    currentGame.countScore()
    print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))

    if game_mode == 'interactive':
        if argv[3]=='computer-next':
            currentGame.currentTurn=2
        else:
            currentGame.currentTurn=1
        interactiveGame(currentGame,argv[4]) # Be sure to pass whatever else you need from the command line
    else: # game_mode == 'one-move'
        # Set up the output file
        outFile = argv[3]
        try:
            currentGame.gameFile = open(outFile, 'w')
        except:
            sys.exit('Error opening output file.')
        oneMoveGame(currentGame,argv[4]) # Be sure to pass any other arguments from the command line you might need.
        end = time.time()
        total_time=(end - start)
        print "TIME:", total_time

if __name__ == '__main__':
    main(sys.argv)


