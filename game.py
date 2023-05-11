"""
ULTIMATE TIC TAC TOE
Class Board contenant les méthodes et attributs nécessaires à la création d'un plateau de jeu

Programme réalisé par :
- Elias TOURNEUX

ESILV A3 - TD I S6 - PROMO 2025
"""

from art import *
from pick import pick
import os
import random

DEBUG = False

def init():
    tprint("Ultimate Tic Tac Toe")
    print("Appuyez sur une touche pour continuer...")
    input()

    title = 'Bienvenue ! Veuillez sélectionner combien de joueurs vont jouer :'
    options = ['0 - IA vs IA', '1 - Joueur vs IA', '2 - Joueur vs Joueur']

    option, index = pick(options, title, indicator='>', default_index=0)
    main(index)
    
def main(choice):
    board = Board()
    player1 = Board.Joueur("Joueur 1", "X", False)
    player2 = Board.Joueur("Joueur 2", "O", False)

    if choice == 0:
        player1.isAI = True
        player2.isAI = True

    elif choice == 1:
        player1.name = input("Joueur 1, vous êtes les X. Veuillez entrer votre nom : ")
        player1.isAI = False
        player2.isAI = True

    elif choice == 2:
        player1.name = input("Joueur 1, vous êtes les X. Veuillez entrer votre nom : ")
        player2.name = input("Joueur 2, vous êtes les O. Veuillez entrer votre nom : ")

        player1.isAI = False
        player2.isAI = False
    
    os.system('cls')
    tprint("Ultimate Tic Tac Toe")
    print("La partie va commencer. Nous avons les joueurs suivants :")
    print(player1.name + " : " + player1.symbol+". Ce joueur est-il une IA ? " + str(player1.isAI))
    print(player2.name + " : " + player2.symbol+". Ce joueur est-il une IA ? " + str(player2.isAI))

    print("Appuyez sur une touche pour continuer...")
    os.system('cls')
    player = player1
    while(not board.terminal_test()):
        board.afficher_grille()
        if player.isAI:
            print("L'IA réfléchit...")
        else:
            print(player.name + ", c'est à vous de jouer !")
        board = player.jouer(board)
        player = player1 if player.symbol == player2.symbol else player2
        os.system('cls')

class Board:
    
    def __init__(self):
        self.board = ['*' for i in range(9)]
        self.x = -1
        self.y = -1
        for i in range(9):
            self.board[i] = ['*' for i in range(9)]

    def terminal_test(self):
        if self.coups_possible() == False:
            tprint("Match nul !")
            self.afficher_grille()
            return True
        if self.winnerBigGrid() == '*':
            return False
        else:
            tprint("Partie terminee !")
            print("Le joueur " + self.winnerBigGrid() + " a gagné !")
            self.afficher_grille()

            if DEBUG:
                for i in range(3):
                    for j in range(3):
                        print()
                        print("Winner of grid (" + str(i) + "," + str(j) + ") : " + self.winnerGrid(i,j))

            return True
           
    def coups_possible(self):
        possibleMoves = []
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == '*':
                    possibleMoves.append((i,j))
            
        if(possibleMoves == []):
            return False
        return True
        
    def get_possible_moves(self):
        possible_moves = []
        if self.x == -1 and self.y == -1:
            for i in range(9):
                for j in range(9):
                    if self.board[i][j] == '*':
                        possible_moves.append((i, j))
        else:
            x_start = (self.x // 3) * 3
            y_start = (self.y // 3) * 3
            x_end = x_start + 3
            y_end = y_start + 3
            for i in range(x_start, x_end):
                for j in range(y_start, y_end):
                    if self.board[i][j] == '*':
                        possible_moves.append((i, j))
        return possible_moves

    def get_possible_moves_in_grid(self, grid_x, grid_y):
        """
        Retourne les coordonnées des cases vides dans la grande case (grid_x, grid_y).
        """
        possible_moves = []
        for i in range(3):
            for j in range(3):
                if self.board[grid_x * 3 + i][grid_y * 3 + j] == '*':
                    possible_moves.append((grid_x * 3 + i, grid_y * 3 + j))
        return possible_moves

    def afficher_grille(self):
        for i in range(9):
            for j in range(9):
                print(self.board[i][j], end = " ")
                if j == 2 or j == 5:
                    print("|", end = " ")
            print()
            if i == 2 or i == 5:
                print("---------------------")

    """
    Cette fonction permet de dire au joueur où il peut jouer. En effet, dans le ultimate tic tac toe, le joueur ne peut pas jouer où il veut. Si le joueur précédent a décidé de jouer en haut à droite par exemple dans la sous-grille, alors le joueur doit jouer dans la grille en haut à droite.
    """
    def gridToPlay(self):
        if self.x == -1 and self.y == -1:
            return (-1,-1)
        xToPlay = self.x%3
        yToPlay = self.y%3
        if self.winnerGrid(xToPlay,yToPlay) == '*':
            return (xToPlay,yToPlay)
        else:
            return (-1,-1)
        
    def otherPlayer(self, player):
        if player == "X":
            return "O"
        else:
            return "X"

    def winnerGrid(self, x,y):
        x = x*3
        y = y*3
        if DEBUG:
            print('Current grid : ('+str(x)+','+str(y)+')')
        for i in range(3):
            # check horizontal
            if self.board[x+i][y+0] == self.board[x+i][y+1] == self.board[i][y+2] and self.board[x+i][y+0] != '*':
                if DEBUG:
                    print('Horizontal line x: '+str(x+i))
                self.fillSmallGrid(x,y, self.board[x+i][y+0])
                return self.board[x+i][y+0]
            # check vertical
            elif self.board[x+0][y+i] == self.board[x+1][y+i] == self.board[x+2][y+i] and self.board[x+0][y+i] != '*':
                if DEBUG:
                    print('Vertical line y: '+str(y+i))
                self.fillSmallGrid(x,y, self.board[x+0][y+i])
                return self.board[x+0][y+i]
        # check diagonal
        if self.board[x+0][y+0] == self.board[x+1][y+1] == self.board[x+2][y+2] and self.board[x+0][y+0] != '*':
            if DEBUG:
                print('Diagonal line 1')
            self.fillSmallGrid(x,y, self.board[x+0][y+0])
            return self.board[x+0][y+0]
        elif self.board[x+0][y+2] == self.board[x+1][y+1] == self.board[x+2][y+0] and self.board[x+0][y+2] != '*':
            if DEBUG:
                print('Diagonal line 2')
            self.fillSmallGrid(x,y, self.board[x+0][y+2])
            return self.board[x+0][y+2]
        else:
            if DEBUG:
                print('No winner')
            return '*'

    def winnerBigGrid(self):
        for i in range(3):
            # check horizontal
            if self.winnerGrid(i,0) == self.winnerGrid(i,1) == self.winnerGrid(i,2) and self.winnerGrid(i,0) != '*':
                return self.winnerGrid(i,0)
            # check vertical
            elif self.winnerGrid(0,i) == self.winnerGrid(1,i) == self.winnerGrid(2,i) and self.winnerGrid(0,i) != '*':
                return self.winnerGrid(0,i)
        # check diagonal
        if self.winnerGrid(0,0) == self.winnerGrid(1,1) == self.winnerGrid(2,2) and self.winnerGrid(0,0) != '*':
            return self.winnerGrid(0,0)
        elif self.winnerGrid(0,2) == self.winnerGrid(1,1) == self.winnerGrid(2,0) and self.winnerGrid(0,2) != '*':
            return self.winnerGrid(0,2)
        else:
            return '*'
        
    def fillSmallGrid(self, x, y, symbol):
        for i in range(3):
            for j in range(3):
                if DEBUG:
                    print('Filling ('+str(x+i)+','+str(y+j)+') with '+symbol)
                self.board[x+i][y+j] = symbol

    def evaluate(self, player):
        """
        Évaluer l'état du plateau en fonction des conditions de victoire et des positions des pions
        """

        # Vérifier si le joueur actuel a gagné
        symbolWinner = self.winnerBigGrid()
        if self.terminal_test() and symbolWinner == player.symbol:
            return 100  # Le joueur actuel a gagné, renvoyer une valeur élevée

        # Vérifier si l'adversaire a gagné
        if self.terminal_test() and symbolWinner != player.symbol:
            return -100  # L'adversaire a gagné, renvoyer une valeur basse

        # Évaluer le plateau en fonction des positions des pions
        score = 0

        # Parcourez chaque case du plateau et attribuez des valeurs en fonction de la position des pions
        for x in range(9):
            for y in range(9):
                piece = self.board[x][y]

                if piece == player.symbol:
                    # Le joueur actuel possède cette case
                    score += 1
                elif piece != '*':
                    # L'adversaire possède cette case
                    score -= 1
        return score

    class Joueur:
        def __init__(self, name, symbol, isAI):
            self.name = name
            self.symbol = symbol
            self.isAI = isAI

        def getPlayerBySymbol(self, symbol):
            if self.symbol == symbol:
                return self
        
        def jouer(self, board):
            if self.isAI:
                return self.jouerIA(board)
            else:
                return self.jouerHumain(board)
            
        def jouerHumain(self, board):
            print("Veuillez entrer les coordonnées de votre coup : ")
            x = -1
            y = -1
            # TODO : Vérifier que les coordonnées sont valides. Le joueur joue dans la case 
            (xToPlay, yToPlay) = board.gridToPlay()
            if xToPlay == -1:
                print("Vous pouvez jouer où vous voulez !")
                x = int(input("x : "))
                y = int(input("y : "))
                while board.winnerGrid(xToPlay,yToPlay) != '*':
                    print("Cette grille n'est pas jouable.")
                    x = int(input("x : "))
                    y = int(input("y : "))

            else:
                print("Vous devez jouer dans la grille " + str(xToPlay) + " " + str(yToPlay) + ".")
                x = int(input("x : "))
                y = int(input("y : "))
                
                #Check if the player plays in the right grid
                while x < xToPlay*3 or x > xToPlay*3+2 or y < yToPlay*3 or y > yToPlay*3+2 or board.winnerGrid(xToPlay,yToPlay) != '*':
                    print("Vous devez jouer dans la grille " + str(xToPlay) + " " + str(yToPlay) + ".")
                    x = int(input("x : "))
                    y = int(input("y : "))

            board.board[x][y] = self.symbol
            board.x = x
            board.y = y
            return board
        
        """
        Cette fonction permet de jouer un coup aléatoire.
        Elle est à modifier pour utiliser l'algorithme MinMax avec élagage Alpha-Beta.
        TODO : Implémenter l'algorithme MinMax avec élagage Alpha-Beta. Commenter cette fonction.
        """
        def jouerIAAleatoire(self, board):
            # Joue un coup aléatoire.

            # On récupère les coups possibles
            possibleMoves = []
            for i in range(9):
                for j in range(9):
                    if board.board[i][j] == '*':
                        possibleMoves.append((i,j))
            
            x = -1
            y = -1
            (xToPlay, yToPlay) = board.gridToPlay()
            if xToPlay == -1:
                (x,y) = random.choice(possibleMoves)
            else:
                possibleMoves = []
                for i in range(xToPlay*3, xToPlay*3+3):
                    for j in range(yToPlay*3, yToPlay*3+3):
                        if board.board[i][j] == '*':
                            possibleMoves.append((i,j))
                if possibleMoves == []:
                    return board
                (x,y) = random.choice(possibleMoves)

            board.board[x][y] = self.symbol
            board.x = x
            board.y = y
            return board

        def jouerIA(self, board):
            depth = 4  # Profondeur de l'algorithme Minimax
            player = self  # Joueur actuel
        
            def minimax(board, depth, alpha, beta, maximizing_player):
                if depth == 0 or board.terminal_test():
                    return board.evaluate(player), None

                if maximizing_player:
                    max_score = float('-inf')
                    best_move = None
                    moves = []

                    x_grid, y_grid = board.gridToPlay()
                    if x_grid == -1:
                        moves = board.get_possible_moves()
                    else:
                        moves = board.get_possible_moves_in_grid(x_grid, y_grid)
                        if not moves:
                            moves = board.get_possible_moves()
                    for move in moves:
                        x, y = move
                        new_board = Board()  # Crée une nouvelle instance de Board
                        new_board.board[x][y] = player.symbol
                        score, _ = minimax(new_board, depth - 1, alpha, beta, False)
                        
                        if score > max_score:
                            max_score = score
                            best_move = move

                        alpha = max(alpha, max_score)
                        if alpha >= beta:
                            break

                    return max_score, best_move
                else:
                    min_score = float('inf')
                    best_move = None

                    x_grid, y_grid = board.gridToPlay()
                    moves = board.get_possible_moves_in_grid(x_grid, y_grid)
                    if not moves:
                        moves = board.get_possible_moves()

                    for move in moves:
                        x, y = move
                        new_board = Board()  # Crée une nouvelle instance de Board
                        new_board.board[x][y] = player.symbol
                        score, _ = minimax(new_board, depth - 1, alpha, beta, True)

                        if score < min_score:
                            min_score = score
                            best_move = move

                        beta = min(beta, min_score)
                        if alpha >= beta:
                            break
                    
                    return min_score, best_move

            _, best_move = minimax(board, depth, float('-inf'), float('inf'), True)
            x, y = best_move
            board.board[x][y] = self.symbol
            board.x = x
            board.y = y
            return board
    
if __name__ == "__main__":
    init()