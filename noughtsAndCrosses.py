#ohamilton79
#Noughts and crosses game tree
#21/12/2020

class Player:
    def __init__(self, character):
        self.character = character

#Board configuration in tree
class Node:
    def __init__(self, boardSize):
        self.boardSize = boardSize
        #Create initial empty board configuration
        self.board = [[" " for i in range(boardSize)] for j in range(boardSize)]

        #Stores a list of the children of this node in the tree
        self.children = []

        #Stores the 'score' of this node
        self.score = None

    #Check if the board configuration was won by the player
    def isWon(self, player):

        #The number of player characters in a line
        playerCharCount = 0

        positionsToCheck = [(0, 0), (1, 0), (2, 0), (0, 0), (0, 1), (0, 2), (0, 0), (0, 2)]
        vecsToCheck = [(0, 1), (0, 1), (0, 1), (1, 0), (1, 0), (1, 0), (1, 1), (1, -1)]
        playerChar = player.character

        #Check each position and its corresponding vector
        for i in range(len(positionsToCheck)):
            currentPos = positionsToCheck[i]
            currentVec = vecsToCheck[i]
            for x in range(self.boardSize):
                newPos = (currentPos[0] + x * currentVec[0], currentPos[1] + x * currentVec[1])
                #If the player's character is at that position
                if self.board[newPos[0]][newPos[1]] == playerChar:
                    playerCharCount += 1

            #If enough consecutive tokens are found
            if playerCharCount == self.boardSize:
                return True

            playerCharCount = 0

        return False

    #Check if the board configuration is a draw (no free spaces in board)
    def isDraw(self):
        #Count the number of empty characters (if draw, there will be zero)
        spacesCount = 0
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                if self.board[i][j] == " ":
                    spacesCount += 1

        #If there are no spaces, the game is a draw (no more spaces available)
        if spacesCount == 0:
            return True

        else:
            return False

    def nOfChars(self, n, player):
        positionsToCheck = [(0, 0), (1, 0), (2, 0), (0, 0), (0, 1), (0, 2), (0, 0), (0, 2)]
        vecsToCheck = [(0, 1), (0, 1), (0, 1), (1, 0), (1, 0), (1, 0), (1, 1), (1, -1)]
        playerChar = player.character
        
        totalScore = 0

        #Check each position and its corresponding vector
        for i in range(len(positionsToCheck)):
            currentPos = positionsToCheck[i]
            currentVec = vecsToCheck[i]
            currentScore = 0
            for x in range(self.boardSize):
                newPos = (currentPos[0] + x * currentVec[0], currentPos[1] + x * currentVec[1])
                #If the player's character is at that position
                if self.board[newPos[0]][newPos[1]] == playerChar:
                    currentScore += 1

                #If the other player's character is at that position
                elif self.board[newPos[0]][newPos[1]] != " ":
                    currentScore = 0
                    break

            #Add the current score to the total
            totalScore += currentScore

        #Return the total score
        return totalScore
                
        

    def evaluate(self, player1, player2):
        #Get the number of rows, columns and diagonals with 2 of a player's character, and none of the other's
        x2 = self.nOfChars(2, player1)
        x1 = self.nOfChars(1, player1)
        o2 = self.nOfChars(2, player2)
        o1 = self.nOfChars(1, player2)

        #Get the result of the linear evaluation function and return it
        self.score = 3*o2 + o1 - (3*x2 + x1)

class Game:
    def __init__(self, boardSize):
        self.boardSize = boardSize
        self.player1 = Player("X")
        self.player2 = Player("O")

        #The root node is an empty board configuration
        self.rootNode = Node(boardSize)

        #Generate all board configurations
        self.generateBoardConfigurations(self.rootNode, self.player1, 1)

        #Define temporary parameters
        alpha = -1000
        beta = 1000

        #Get scores for board configurations
        self.rootNode.score = self.minimax(self.rootNode, alpha, beta, False, 1)

    def generateBoardConfigurations(self, node, player, depth):
        #Constants
        MAXDEPTH = 6

        #If the maximum depth has been reached
        if depth > MAXDEPTH:
            return

        #If the current depth is equal to the maximum depth, and no score is set for the current node
        if depth >= MAXDEPTH and node.score == None:
            #Run an evaluation function to get the node's score
            node.evaluate(self.player1, self.player2)
            return

        #If the game is won by the first player, it is a loss for the second player (computer)
        if node.isWon(self.player1):
            node.score = -1

        #If the game is won by the second player (computer)
        elif node.isWon(self.player2):
            node.score = 1

        #If the board configuration is a draw
        elif node.isDraw():
            node.score = 0
            
        else:
            #print(node.board)
            #Check which board configurations are possible
            for i in range(self.boardSize):
                for j in range(self.boardSize):
                    #If the board space is free, a new board configuration can be generated
                    if node.board[i][j] == " ":                        
                        #Create new node with new board configuration
                        newNode = Node(self.boardSize)
                        
                        #Copy board from old node
                        for k in range(self.boardSize):
                            for l in range(self.boardSize):
                                newNode.board[k][l] = node.board[k][l]

                        #Add new player character to board 
                        newNode.board[i][j] = player.character
                        
                        #Add new node to previous node's children
                        node.children.append(newNode)

                        #Generate new board configurations for this new node
                        self.generateBoardConfigurations(newNode, self.getOppositePlayer(player), depth+1)

    def minimax(self, node, alpha, beta, isMax, depth):
        #Constants
        MAXDEPTH = 6
            
        #If the score is already set, return the score
        if node.score != None:
            return node.score

        if isMax:
            #The maximum score of the child nodes
            maxScore = -10000 #Temp default (small) value
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
            minScore = 10000 #Temp default (large) value
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

    def placeToken(self, position, token):
        coords = position.split(",")
        xCoord = int(coords[0][1:])
        yCoord = int(coords[1][:-1])

        #If the position specified is valid
        if xCoord != None and yCoord != None and self.rootNode.board[xCoord][yCoord] == " ":
            #Place the token
            self.rootNode.board[xCoord][yCoord] = token
            #Output the board
            print(self.rootNode.board)

        #Otherwise, throw an error so an exception can be output
        else:
             raise Exception
            
    def chooseBoardConfig(self):
        currentPlayer = self.player1
        #Take an input from the user
        newPos = input("Enter a board position (x,y) to insert a token")

        #Place the token in this position
        try:
            self.placeToken(newPos, currentPlayer.character)
        except:
            print("Invalid move - please try again")
            #Take an input from the user
            newPos = input("Enter a board position (x,y) to insert a token")
            self.placeToken(newPos, currentPlayer.character)

        #Find the child node of the root node with this board configuration
        for child in self.rootNode.children:
            if child.board == self.rootNode.board:
                #Change the root node
                self.rootNode = child

        #Reset all node scores
        self.resetNodeScores(self.rootNode)
        #Generate all board configurations
        self.generateBoardConfigurations(self.rootNode, self.player2, 1)

        #Define temporary parameters
        alpha = -1000
        beta = 1000

        #Get scores for board configurations
        self.rootNode.score = self.minimax(self.rootNode, alpha, beta, True, 1)
        #Make the computer make a move based on the scores of its children
        self.computerMakeMove(self.player2)

    def resetNodeScores(self, node):
        node.score = None
        node.children = []
        for child in node.children:
            self.resetNodeScores(child)

    def computerMakeMove(self, player):
        maxScoreNode = (None, -1000)
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

    #Output the current board state
    def outputBoard(self):
        firstRow = "-" + "----" * self.boardSize
        #Output the first row of characters
        print(firstRow)
        #Output each of the tokens in the board
        for i in range(self.boardSize):
            currentRow = "|"
            for j in range(self.boardSize):
                currentRow += " " + self.rootNode.board[j][i] + " |"

            print(currentRow)

            #Output a separator row
            separatorRow = "-" + "----"*self.boardSize
            #Output the separator row of characters
            print(separatorRow)

game = Game(3)

node = game.rootNode
#While the game hasn't been won or drawn
while not game.rootNode.isWon(game.player1) and not game.rootNode.isWon(game.player2) and not game.rootNode.isDraw():
    #Output current board state
    game.outputBoard()
    #User chooses a board configuration
    game.chooseBoardConfig()

game.outputBoard()
if game.rootNode.isWon(game.player1):
    print("You win!")

elif game.rootNode.isWon(game.player2):
    print("Computer wins!")

else:
    print("Draw!")


