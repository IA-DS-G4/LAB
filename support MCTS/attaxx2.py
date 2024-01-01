import tkinter as tk
from attaxx_ai_player import AttaxxAIPlayer  

class AttaxxGame:
    def __init__(self):
        self.board_size = 4
        self.board = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.players = ['X', 'O']
        self.current_player = 0  # Primeiro jogador//Red
        self.start_position = None  # Armazenar a posição de início para o movimento
        self.winner=-1
        # Posições iniciais
        self.board[0][0] = 'O' #Red
        self.board[self.board_size-1][self.board_size-1] = 'O' 
        self.board[0][self.board_size-1] = 'X' #Blue
        self.board[self.board_size-1][0] = 'X'
        
    def print_board(self):
        for row in self.board:
            print(' '.join(row))
        print()


###########################################################################################3
        #Verificar se existem movimentos possíveis
    def is_move_possible(self):
        for line in range(self.board_size):
            for column in range(self.board_size):
                if(self.players[self.current_player]==self.board[line][column]):
                    if self.is_valid_move((line,column),(line-2,column)):
                        return True;
                    if self.is_valid_move((line,column),(line-1,column)):
                        return True;
                    if self.is_valid_move((line,column),(line+1,column)):
                        return True;
                    if self.is_valid_move((line,column),(line+2,column)):
                        return True;
                    if self.is_valid_move((line,column),(line-2,column-2)):
                        return True;
                    if self.is_valid_move((line,column),(line-1,column-2)):
                        return True;
                    if self.is_valid_move((line,column),(line,column-2)):
                        return True;
                    if self.is_valid_move((line,column),(line+1,column-2)):
                        return True;
                    if self.is_valid_move((line,column),(line+2,column-2)):
                        return True;
                    if self.is_valid_move((line,column),(line-2,column-1)):
                        return True;
                    if self.is_valid_move((line,column),(line-1,column-1)):
                        return True;
                    if self.is_valid_move((line,column),(line,column-1)):
                        return True;
                    if self.is_valid_move((line,column),(line+1,column-1)):
                        return True;
                    if self.is_valid_move((line,column),(line+2,column-1)):
                        return True;
                    if self.is_valid_move((line,column),(line-2,column+1)):
                        return True;
                    if self.is_valid_move((line,column),(line-1,column+1)):
                        return True;
                    if self.is_valid_move((line,column),(line,column+1)):
                        return True;
                    if self.is_valid_move((line,column),(line+1,column+1)):
                        return True;
                    if self.is_valid_move((line,column),(line+2,column+1)):
                        return True;
                    if self.is_valid_move((line,column),(line-2,column+2)):
                        return True;
                    if self.is_valid_move((line,column),(line-1,column+2)):
                        return True;
                    if self.is_valid_move((line,column),(line,column+2)):
                        return True;
                    if self.is_valid_move((line,column),(line+1,column+2)):
                        return True;
                    if self.is_valid_move((line,column),(line+2,column+2)):
                        return True;
        return False;
###############################################################################################


    def is_valid_move(self, start, end):
        # Verificar se o movimento está dentro dos limites do tabuleiro
        if not (0 <= start[0] < self.board_size and 0 <= start[1] < self.board_size and
                0 <= end[0] < self.board_size and 0 <= end[1] < self.board_size):
            return False

        # Verificar se o destino está vazio
        if self.board[end[0]][end[1]] != ' ':
            return False

        # Verificar se o movimento é um salto válido (uma ou duas células de distância)
        row_diff = abs(start[0] - end[0])
        col_diff = abs(start[1] - end[1])
        return (1 <= row_diff <= 2 and col_diff == 0) or (1 <= col_diff <= 2 and row_diff == 0) or \
               (1 <= row_diff <= 2 and 1 <= col_diff <= 2)

    def make_move(self, end):
        finished=False
        if self.start_position and self.is_valid_move(self.start_position, end):
            # Se o destino é adjacente ao ponto de partida, cria uma nova peça
            if abs(self.start_position[0] - end[0]) <= 1 and abs(self.start_position[1] - end[1]) <= 1:
                self.board[end[0]][end[1]] = self.players[self.current_player]
                
            else:
                # Move a peça no ponto de partida para o destino
                self.board[end[0]][end[1]] = self.board[self.start_position[0]][self.start_position[1]]
                self.board[self.start_position[0]][self.start_position[1]] = ' '
                

            # Conquiste as células adjacentes
            self.conquer_adjacent(end)

            self.start_position = None  # Limpar a posição de início
            self.switch_player()
            #print(self.players[self.current_player])
            #print(self.is_move_possible());
            if(self.is_move_possible()==False):
                finished=True
                self.winner=self.check_winner()
            if finished:
                return self.winner
            return -1

    def make_move_ai(self,xi,yi,xf,yf):
        finished=False
        # Se o destino é adjacente ao ponto de partida, cria uma nova peça
        if abs(xi - xf) <= 1 and abs(yi - yf) <= 1:
            self.board[xf][yf] = self.players[self.current_player]
                
        else:
            # Move a peça no ponto de partida para o destino
            self.board[xf][yf] = self.board[xi][yi]
            self.board[xi][yi] = ' '
                

        # Conquiste as células adjacentes
        self.conquer_adjacent((xf,yf))
        self.print_board()

        self.switch_player()
        if(self.is_move_possible()==False):
            finished=True
            winner=self.check_winner()
        if finished:
            return winner
        return -1
            








    def switch_player(self):
        self.current_player = 1 - self.current_player  # Alternar entre jogadores


        #count pieces of the current player. The other has the rest of the board.
    def count_pieces(self):
        total=0;
        for line in range(self.board_size):
            for column in range(self.board_size):
                if(self.players[self.current_player]==self.board[line][column]):
                    total+=1;
        return total;



        
    def check_winner(self):
        if self.winner!=-1:
            return self.winner
        #print('ver vencedor')
        #self.print_board()
        if(self.count_pieces()<self.board_size*self.board_size/2):
            print('Ganhou o jogador ', 1-self.current_player, ' com ' , self.board_size*self.board_size-self.count_pieces(), ' peças.');
            return 1-self.current_player
        elif(self.count_pieces()==self.board_size*self.board_size/2):
            print('Houve empate')
            return 0
        else:
            print('Ganhou o jogador ', self.current_player, ' com ', self.count_pieces(), ' peças.');
        return self.current_player
        

   



   
      

    def conquer_adjacent(self, position):
        row, col = position

        for dr in range(-1, 2):
            for dc in range(-1, 2):
                new_row, new_col = row + dr, col + dc
                new_position = (new_row, new_col)

                if 0 <= new_row < self.board_size and 0 <= new_col < self.board_size \
                        and self.board[new_row][new_col] == self.players[1 - self.current_player]:
                    # Conquista a célula adjacente
                    self.board[new_row][new_col] = self.players[self.current_player]

class AttaxxGUIPVP:
    def __init__(self, master, game):
        self.master = master
        self.game = game
        self.SQUARE_SIZE = 50  # Tamanho da célula

        # Configurar o tabuleiro
        self.canvas = tk.Canvas(master, width=self.game.board_size * self.SQUARE_SIZE,
                                height=self.game.board_size * self.SQUARE_SIZE)
        self.canvas.pack()

        # Desenhar o tabuleiro inicial
        self.draw_board()

        # Reconhecer as jogadas através do clique do rato
        self.canvas.bind("<Button-1>", self.handle_click)

    def draw_board(self):
        for row in range(self.game.board_size):
            for col in range(self.game.board_size):
                player = self.game.board[row][col]
                color = "white" if player == ' ' else "red" if player == 'X' else "blue"  # Definir cores
                self.canvas.create_rectangle(col * self.SQUARE_SIZE, row * self.SQUARE_SIZE,
                                             (col + 1) * self.SQUARE_SIZE, (row + 1) * self.SQUARE_SIZE,
                                             fill=color, outline="black")

    def handle_click(self, event):
        col = event.x // self.SQUARE_SIZE
        row = event.y // self.SQUARE_SIZE
        piece = self.game.board[row][col]

        if piece != ' ' and piece == self.game.players[self.game.current_player]:
            self.game.start_position = (row, col)
        else:
            end_position = (row, col)
            self.game.make_move(end_position)

        self.draw_board()


class AttaxxGUIPVC:
    def __init__(self, master, game):
        self.master = master
        self.game = game
        self.SQUARE_SIZE = 50  # Tamanho da célula

        # Configurar o tabuleiro
        self.canvas = tk.Canvas(master, width=self.game.board_size * self.SQUARE_SIZE,
                                height=self.game.board_size * self.SQUARE_SIZE)
        self.canvas.pack()

        # Desenhar o tabuleiro inicial
        self.draw_board()

        # Reconhecer as jogadas através do clique do rato
        self.canvas.bind("<Button-1>", self.handle_click)

    def draw_board(self):
        for row in range(self.game.board_size):
            for col in range(self.game.board_size):
                player = self.game.board[row][col]
                color = "white" if player == ' ' else "red" if player == 'X' else "blue"  # Definir cores
                self.canvas.create_rectangle(col * self.SQUARE_SIZE, row * self.SQUARE_SIZE,
                                             (col + 1) * self.SQUARE_SIZE, (row + 1) * self.SQUARE_SIZE,
                                             fill=color, outline="black")

    def handle_click(self, event):
        if self.game.current_player == self.game.players.index('X'):
            col = event.x // self.SQUARE_SIZE
            row = event.y // self.SQUARE_SIZE
            piece = self.game.board[row][col]

            if piece != ' ' and piece == self.game.players[self.game.current_player]:
                self.game.start_position = (row, col)
            else:
                end_position = (row, col)
                self.game.make_move(end_position)

            self.draw_board()
            if self.game.is_move_possible():
                self.handle_ai_move()

    def handle_ai_move(self):
        # Example: Assume AI player is player 'O'
        if self.game.current_player == self.game.players.index('O'):

            ai_player = AttaxxAIPlayer(self.game, player_number=self.game.players.index('O'))
            #xi, yi = ai_player.rand_choose()
            #xf, yf = ai_player.rand_choose()
            xi, yi, xf, yf =ai_player.mcts()
            #while((self.game.board[xi][yi]!='O') or (self.game.is_valid_move((xi,yi),(xf,yf))==False)):
                #xi, yi = ai_player.rand_choose()
                #xf, yf = ai_player.rand_choose()
                
            print('melhor jogada', xi,yi,xf,yf)
            self.game.make_move_ai(xi,yi,xf,yf)
            self.draw_board()
           
    
    


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Attaxx Game")
    game = AttaxxGame()
    option='PVC'
    if(option=='PVP'):
        gui_PVP = AttaxxGUIPVP(root, game)
    else:
        gui_PVC=AttaxxGUIPVC(root, game)
    root.mainloop()
