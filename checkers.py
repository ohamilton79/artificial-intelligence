#ohamilton79
#Checkers game tree
#15/01/2021
import copy

class Player:
    def __init__(self, name, character, kingChar, kingRow, moves):
        self.name = name
        self.character = character
        self.kingChar = kingChar
        self.kingRow = kingRow
        self.moves = moves

#Represents a white or black checker
class Checker:
    #A king can move both forwards and backwards diagonally
    kingMoves = [(1,1), (1,-1), (-1,1), (-1,-1)]
    
    def __init__(self, player=None, isKing=False):
        #Identify the player who placed the Checker
        self.player = player
        #Save whether the Checker is a king
        self.isKing = isKing
        if player == None:
            self.moves = []
        else:
            self.moves = self.player.moves

    #Output the character representing the Checker
    def getCharacter(self):
        if self.player == None:
            return " "
        if self.isKing:
            return self.player.kingChar

        else:
            return self.player.character

    #Get the moves that the Checker can make, represented as vectors
    def getMoves(self):
        if self.isKing:
            return self.kingMoves
        else:
            return self.moves

#Board configuration in tree
class Node:

    #Generate the checkers on a board for a given player
    def generateCheckers(self, board, player, startRow=0):
        for row in range(startRow, startRow + 3):
            for col in range(8):
                if (col + row) % 2 == 0:
                    board[row][col] == Checker()

                else:
                    board[row][col] = Checker(player)

    #Return an 8x8 checkers board
    def createBoard(self, player1, player2):
        #Create an 8x8 array of blank spaces
        board = [[Checker() for row in range(8)] for col in range(8)]

        #Generate checkers for player 2 (at the top of the board)
        self.generateCheckers(board, player2)

        #Generate checkers for player 1 (at bottom of board)
        self.generateCheckers(board, player1, 5)

        #Return the final board
        return board
              
    def __init__(self, boardSize, player1, player2, movesSinceCapture):
        self.currentPlayer = None
        self.boardSize = boardSize
        self.player1 = player1
        self.player2 = player2
        #Generate the board configuration
        self.board = self.createBoard(player1, player2)

        #Stores a list of the children of this node in the tree
        self.children = []

        #Record the number of moves since a checker was captured
        self.movesSinceCapture = movesSinceCapture

        #Stores the 'score' of this node
        self.score = None

    #Check if the board configuration was won by the player
    def isWon(self, player, oppositePlayer):
        #The game is won if there are none of the other player's checkers on the board

        if self.getCheckers(oppositePlayer) == 0:
            return True

        else:
            return False

    #Check if the board configuration is a draw (more than 50 moves since last capture)
    def isDraw(self):
        if self.movesSinceCapture > 50:
            return True

        else:
            return False

    #Check if the current player can capture an opponent's piece, and return the start and end locations for the move, as well as the position where a checker needs to be removed.
    def canCaptureChecker(self, player, oppositePlayer):
        #Check each position on the board
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                currentChecker = self.board[i][j]
                #If there is a checker belonging to the current player at this position
                if currentChecker.player and currentChecker.player.character == player.character:
                    #If there is an empty space in the available directions two moves away 
                    for vec in currentChecker.getMoves():
                        newI = i + (2 * vec[0])
                        newJ = j + (2 * vec[1])

                        #If the move is valid
                        if self.validMove((i,j), (newI, newJ), player, oppositePlayer):
                            #A checker can be captured at this position
                            yield [(i, j), (newI, newJ)]

    def validMove(self, startPos, endPos, player, oppositePlayer):
        #Get position components
        startRow = startPos[0]
        startCol = startPos[1]

        endRow = endPos[0]
        endCol = endPos[1]

        #Each component must be within the boundaries of the board
        if startRow < 0 or startRow >= self.boardSize or startCol < 0 or startCol >= self.boardSize:
            return False

        if endRow < 0 or endRow >= self.boardSize or endCol < 0 or endCol >= self.boardSize:
            return False
        
        #The size of each of the components of the move must be the same
        if abs(endRow - startRow) != abs(endCol - startCol):
            return False

        #If the diagonal length of the move is not 1 or 2 (the square of the length isn't 8 or 2), the move isn't valid
        diagonalLength = (endRow - startRow)**2 + (endCol - startCol)**2
        if diagonalLength != 8 and diagonalLength != 2:
            return False

        #The end position must contain an empty space
        if self.board[endRow][endCol].getCharacter() != " ":
            return False

        #If the diagonal length of the move is 2, there must be a Checker of the opposite type in between
        midRow = (startRow + endRow) // 2
        midCol = (startCol + endCol) // 2
        #midpoint = "({},{})".format(midRow, midCol)
        if diagonalLength == 8 and not self.checkerExistsAt((midRow, midCol), oppositePlayer):
            return False

        #The move must be in the direction of one of the available vectors
        for vec in self.board[startRow][startCol].getMoves():
            if (endRow == startRow + vec[0] and endCol == startCol + vec[1]) or (endRow == startRow + 2*vec[0] and endCol == startCol + 2*vec[1]):
                return True

        return False

    def removeChecker(self, xPos, yPos):
        self.board[xPos][yPos] = Checker()

    def moveChecker(self, startPos, endPos, player, oppositePlayer):
        #endCoords = endPos.split(",")
        endRow = endPos[0]
        endCol = endPos[1]

        #startCoords = startPos.split(",")
        startRow = startPos[0]
        startCol = startPos[1]

        #If the end position specified is valid
        if self.validMove(startPos, endPos, player, oppositePlayer):
            #Create a new temporary node to perform operations on
            tempNode = Node(self.boardSize, self.player1, self.player2, self.movesSinceCapture)
            #Copy board from current board to new node
            for k in range(self.boardSize):
                for l in range(self.boardSize):
                    tempNode.board[k][l] = copy.deepcopy(self.board[k][l])

            
            #Place the checker
            tempNode.board[endRow][endCol] = Checker(player, self.board[startRow][startCol].isKing)
            #Remove the checker from the original position
            tempNode.removeChecker(startRow, startCol)

            #If the move length is 2, remove the checker in between as well
            if abs(endRow - startRow) == 2:
                tempNode.removeChecker((startRow + endRow) // 2, (startCol + endCol) // 2)
                #Reset the number of moves since the last capture
                tempNode.movesSinceCapture = 0

            else:
                #Increment the number of moves since the last capture
                tempNode.movesSinceCapture += 1

            #If a checker reaches the other end of the board, it has become a king
            if (player.kingRow == endRow):
                tempNode.board[endRow][endCol].isKing = True

            #Return the temporary node
            return tempNode

        #Otherwise, throw an error so an exception can be output
        else:
            raise Exception

    def checkerExistsAt(self, checkerPos, player):
        #posComponents = checkerPos.split(",")
        xPos = checkerPos[0]
        yPos = checkerPos[1]
        #If there is a checker here that belongs to the current player
        if self.board[xPos][yPos].getCharacter() != " " and self.board[xPos][yPos].getCharacter().lower() == player.character:
            return True

        #Otherwise, return false if there isn't a checker here
        else:
            return False

    #Get the number of checkers on the board that belong to the given player
    def getCheckers(self, player):
        count = 0
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                #print(self.board[i][j].player)
                if self.board[i][j].player and self.board[i][j].getCharacter().lower() == player.character:
                    count += 1

        return count

    #Get the number of kings on the board that belong to the given player
    def getKings(self, player):
        count = 0
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                if self.board[i][j].player == player and self.board[i][j].isKing == True:
                    count += 1

        return count

    #Get the number of ways in which a checker can be taken by a given player
    def checkersToTake(self, player, oppositePlayer):
        count = 0
        captureGenerator = self.canCaptureChecker(player, oppositePlayer)
        for i in captureGenerator:
            #Increment the number of checkers that can be taken
            count += 1
            
        return count

    def evaluate(self, player1, player2):
        #1. Get the number of checkers that the computer has
        c1 = self.getCheckers(player2)

        #2. Get the number of kings that the computer has
        c2 = self.getKings(player2)

        #3. Get the number of opportunities for the computer to take a checker
        c3 = self.checkersToTake(player2, player1)

        #4. Get the number of checkers that the current player has
        o1 = self.getCheckers(player1)

        #5. Get the number of kings that the current player has
        o2 = self.getKings(player1)

        #6. Get the number of opportunities for the current player to take a checker
        o3 = self.checkersToTake(player1, player2)
        
        #Get the result of the linear evaluation function and return it
        self.score = (10 * c1) + (20 * c2) + (600 * c3) - (10 * o1) - (20 * o2) - (1000 * o3)

    
    #Check if the board's belonging to this node and another node are identical
    def identicalTo(self, otherNode):
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                #If the player / character belonging to these board positions are not identical
                if not (self.board[i][j].player == otherNode.board[i][j].player or (self.board[i][j].player and otherNode.board[i][j].player and self.board[i][j].player.character == otherNode.board[i][j].player.character)):
                    #self.outputBoard()
                    return False

        return True

    #Output the current board state
    def outputBoard(self):
        firstRow = "-" + "----" * self.boardSize
        #Output the first row of characters
        print(firstRow)
        #Output each of the Checkers in the board
        for i in range(self.boardSize):
            currentRow = "|"
            for j in range(self.boardSize):
                if self.board[i][j] == " ":
                    currentRow += (" " + self.board[i][j] + " |")
                else:
                    currentRow += (" " + self.board[i][j].getCharacter() + " |")

            print(currentRow)

            #Output a separator row
            separatorRow = "-" + "----"*self.boardSize
            #Output the separator row of characters
            print(separatorRow)

class Game:
    def __init__(self, boardSize):
        self.boardSize = boardSize
        #Lowercase letters for normal checkers, uppercase for kings
        self.player1 = Player("Alice", "b", "B", 0, [(-1,-1), (-1,1)])  #Black checkers can move up
        self.player2 = Player("Bob", "r", "R", self.boardSize - 1, [(1,1), (1,-1)])    #Red checkers can move down

        #The root node is an empty board configuration
        self.rootNode = Node(boardSize, self.player1, self.player2, 0)
        self.rootNode.currentPlayer = self.player1

        self.updateGameTree(self.player1, False)

        #Generate all board configurations
        #self.generateBoardConfigurations(self.rootNode, self.player1, 1)

        #Define temporary parameters
        #alpha = -100000
        #beta = 100000

        #Get scores for board configurations
        #self.rootNode.score = self.minimax(self.rootNode, alpha, beta, False, 1)

    def generateBoardConfigurations(self, node, player, depth, captureMoves=[]):
        #Constants
        MAXDEPTH = 3

        #print("Depth: {}".format(depth))
        #print("Capture moves: {}".format(captureMoves))

        #If the maximum depth has been reached
        if depth > MAXDEPTH:
            return

        #If the current depth is equal to the maximum depth, and no score is set for the current node
        if depth >= MAXDEPTH and node.score == None:
            #Run an evaluation function to get the node's score
            node.evaluate(self.player1, self.player2)
            return

        #If the game is won by the first player, it is a loss for the second player (computer)
        if node.isWon(self.player1, self.player2):
            node.score = -5000

        #If the game is won by the second player (computer)
        elif node.isWon(self.player2, self.player1):
            node.score = 5000

        #If the board configuration is a draw
        elif node.isDraw():
            node.score = 0
            
        else:
            #Check which board configurations are possible
            for i in range(self.boardSize):
                for j in range(self.boardSize):
                    vecs = node.board[i][j].getMoves()
                    for vec in vecs:
                        #If a move one space away is valid, a new board configuration can be generated
                        endRow = i + vec[0]
                        endCol = j + vec[1]
                        if node.board[i][j].getCharacter().lower() == player.character and endRow >= 0 and endCol >= 0 and endRow < self.boardSize and endCol < self.boardSize and node.board[endRow][endCol].getCharacter() == " ":
                            #If a capture can be made, the move must be a capture move
                            if not captureMoves:
                                newNode = node.moveChecker((i,j), (endRow, endCol), player, self.getOppositePlayer(player))
                                newNode.currentPlayer = self.getOppositePlayer(player)
                                
                                #Add new node to previous node's children
                                node.children.append(newNode)

                                #Generate new board configurations for this new node
                                self.generateBoardConfigurations(newNode, self.getOppositePlayer(player), depth+1)

                        #If a move two spaces away is valid, a new board configuration can be generated
                        endRow = i + 2*vec[0]
                        endCol = j + 2*vec[1]
                        if node.board[i][j].getCharacter().lower() == player.character and endRow >= 0 and endCol >= 0 and endRow < self.boardSize and endCol < self.boardSize and node.board[endRow][endCol].getCharacter() == " " and node.validMove((i,j), (endRow, endCol), player, self.getOppositePlayer(player)):
                            #If a capture can be made, the move must be a capture move
                            if not captureMoves or (captureMoves and [(i,j), (endRow, endCol)] in captureMoves):
                                newNode = node.moveChecker((i,j), (endRow, endCol), player, self.getOppositePlayer(player))
                                
                                #Add new node to previous node's children
                                node.children.append(newNode)

                                newCaptureMoves = []
                                captureGenerator = newNode.canCaptureChecker(player, self.getOppositePlayer(player))
                                for move in captureGenerator:
                                    #Add to list of moves that result in a capture
                                    if move[0] == (endRow, endCol):
                                        newCaptureMoves.append(move)

                                #If a capture was previously made, and they still can be made
                                if captureMoves and newCaptureMoves:
                                    print(captureMoves)
                                    print(newCaptureMoves)
                                    #Generate a new board configuration for the current player
                                    newNode.currentPlayer = player
                                    self.generateBoardConfigurations(newNode, player, depth+1, newCaptureMoves)

                                else:
                                    #Generate new board configurations for the opposite player
                                    newNode.currentPlayer = self.getOppositePlayer(player)
                                    self.generateBoardConfigurations(newNode, self.getOppositePlayer(player), depth+1)

    def minimax(self, node, alpha, beta, isMax, depth):
        #Constants
        MAXDEPTH = 3
            
        #If the score is already set, return the score
        if node.score != None:
            return node.score

        if isMax:
            #The maximum score of the child nodes
            maxScore = -1000000 #Temp default (small) value
            #Otherwise, iterate over child nodes to find the maximum score of children
            for child in node.children:
                #Minimise scores of the children at the lower depth
                child.score = self.minimax(child, alpha, beta, False, depth+1)
                #print(child.score)
                if child.score > maxScore:
                    #Update max score
                    maxScore = child.score

                #Update alpha (max score for maximiser)
                if maxScore > alpha:
                    alpha = maxScore

                #If the score of this node is greater than beta, it doesn't need to be checked
                if maxScore >= beta:
                    break

            return maxScore

        else:
            #The minimum score of the child nodes
            minScore = 1000000 #Temp default (large) value
            #Otherwise, iterate over child nodes to find the minimum score of children
            for child in node.children:
                #Maximise scores of the children at the lower depth
                child.score = self.minimax(child, alpha, beta, True, depth+1)
                if child.score < minScore:
                    #Update min score
                    minScore = child.score

                #Update beta (min score for minimiser)
                if minScore < beta:
                    beta = minScore

                #If the score of this node is less than alpha, it doesn't need to be checked
                if minScore <= alpha:
                    break

            return minScore

    #Convert a position as a string to a tuple of integers
    def getPosTuple(self, posStr):
        #Split at comma to get two numbers
        posComponents = posStr.split(",")
        #Remove brackets next to the numbers
        rowPos = int(posComponents[0][1:])
        colPos = int(posComponents[1][:-1])

        return (rowPos, colPos)

    def playerMakeMove(self, player):
        valid = False
        #Repeat whilst inputs not validated
        while not valid:
            try:
                #Take an input from the user
                originalPos = input("Enter the board position (row,column) of the checker you want to move: ")

                #Check that there is a checker at the start position that belongs to the current player
                if not self.rootNode.checkerExistsAt(self.getPosTuple(originalPos), player):
                    print("Invalid move - please try again")

                else:
                    newPos = input("Enter the board position (row,column) where you want to move the checker to: ")
                    #Get the node representing the new board state
                    tempNode = self.rootNode.moveChecker(self.getPosTuple(originalPos), self.getPosTuple(newPos), player, self.getOppositePlayer(player))
                    #tempNode.outputBoard()
                    #If none of the children of the root node have a board in this state, it is not a valid move
                    newRoot = None
                    print(len(self.rootNode.children))
                    for child in self.rootNode.children:
                        print("Y")
                        #child.outputBoard()
                        #Check if the two nodes' boards are identical
                        if child.identicalTo(tempNode):
                            newRoot = child

                    print(newRoot)
                    if not newRoot:
                        raise ValueError("Invalid move - capture can be made")

                    #If a new root node has been found, set the root node to this node
                    self.rootNode = newRoot

                    #The inputs are valid if no exception is thrown
                    valid = True
                
            except Exception as e:
                print("Invalid move - please try again")
                print(e)
            
    def chooseBoardConfig(self):
        currentPlayer = self.rootNode.currentPlayer
        print(currentPlayer.name)
        #self.updateGameTree(currentPlayer
        if currentPlayer.name == self.player1.name:
            self.updateGameTree(self.player1, False)
            self.playerMakeMove(self.player1)
            

        else:
            self.updateGameTree(self.player2, True)
            self.computerMakeMove(self.player2)

    def resetNodeScores(self, node):
        node.score = None
        node.children = []
        for child in node.children:
            self.resetNodeScores(child)

    #Update the game tree once a move has been made
    def updateGameTree(self, player, isMax):
        captureMoves = []
        captureGenerator = self.rootNode.canCaptureChecker(player, self.getOppositePlayer(player))
        for move in captureGenerator:
            #Add to list of moves that result in a capture
            captureMoves.append(move)

        #Reset all node scores
        self.resetNodeScores(self.rootNode)
        #Generate all board configurations, based on the moves identified as capture moves
        self.generateBoardConfigurations(self.rootNode, player, 1, captureMoves)

        #Define temporary parameters
        alpha = -100000
        beta = 100000

        #Get scores for board configurations
        self.rootNode.score = self.minimax(self.rootNode, alpha, beta, isMax, 1)
        
    def computerMakeMove(self, player):           
        maxScoreNode = (None, -100000)
        for child in self.rootNode.children:
            if child.score != None and child.score > maxScoreNode[1]:
                #Update max score
                maxScoreNode = (child, child.score)

        #If there are no more nodes, the game has completed
        if maxScoreNode[0] == None:
            return
        #Move to the board configuration with the highest score
        print("Computer making move...")
        self.rootNode = maxScoreNode[0]

    #Get the opposite player to a given player
    def getOppositePlayer(self, player):
        if player == self.player1:
            return self.player2

        else:
            return self.player1

game = Game(8)

node = game.rootNode
#While the game hasn't been won or drawn
while not game.rootNode.isWon(game.player1, game.player2) and not game.rootNode.isWon(game.player2, game.player1) and not game.rootNode.isDraw():
    #Output current board state
    game.rootNode.outputBoard()
    #User chooses a board configuration
    game.chooseBoardConfig()

game.rootNode.outputBoard()
if game.rootNode.isWon(game.player1, game.player2):
    print("You win!")

elif game.rootNode.isWon(game.player2, game.player1):
    print("Computer wins!")

else:
    print("Draw!")


