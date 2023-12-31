
import java.util.Random;

public class MCTS {

    static int row = 6;
    static int column = 7;
    // Numero maximo de iteracoes
    static long startTime;
    static double limit_millis = 1000;
    static int num_itera;
    static int player;
    static int position_row;


    // array para armazenar movimentos possiveis e quantidade total de movimentos possiveis num estado
    static int possible_moves[] = new int[column +1];



    //criar lista de movimentos possiveris e qauntidae e retornar um deles aleatoriamente
    public static int getPossibleMoves(int array[][]) {
        int remaining_moves[] = new int[column];
        int amount_moves = 0;
        int random_move=0;
    
        // lista de colunas disponiveis
        for (int j = 0; j < column; j++) {
            if (array[row - 1][j] == 0) {
                possible_moves[j] = 1;
                remaining_moves[amount_moves] = j;
                amount_moves++;
            } else {
                possible_moves[j] = 0;
            }
        }
    
        // Quantidade total de movimentos possiveis
        possible_moves[7] = amount_moves;
        //escolher um numero aleatoriamente de uma lista de movimentos possiveis
        if (amount_moves > 0) {
            Random rand = new Random();
            //escolher um numero, aleatoriamente, de uma lista das colunas disponiveis
            random_move = remaining_moves[rand.nextInt(amount_moves)];
            //random_move = remaining_moves[rand() % amount_moves];
        }
    
        return random_move;
    }

    // jogar na proxima posicao disponivel 
    public static int setMove(int array[][], int pl, int move) {
        int pos_row=0;
        //verificar posicoes disponiveis na coluna selecionada
        for (int i = 0; i < row; i++) {
            if (array[i][move] == 0) {
                array[i][move] = pl;
                pos_row = i;
                break;
            }
        }
        //retornar a linha
        return pos_row;
    }

    public static int switchPlayer(int pl) {
        if (pl == 1) {
            pl = 2;
        } else {
            pl = 1;
        }

        return pl;
    }


    // Verificar fim de jogo
    public static int checkWin(int array[][], int player, int move, int position_row) {

        int temp_column;
        int temp_position_row;

        // vertical 
        for (int i = 0; i < row - 3; i++) {
            if (array[i][move] == player && array[i + 1][move] == player && array[i + 2][move] == player &&
                array[i + 3][move] == player) {
                return player;
            }
        }

        // horizontal 
        for (int j = 0; j < column - 3; j++) {
            if (array[position_row][j] == player && array[position_row][j + 1] == player &&
                array[position_row][j + 2] == player &&
                array[position_row][j + 3] == player) {
                return player;
            }
        }

        // diagonal direita
        if (move > position_row) {
            temp_column = move - position_row;
            temp_position_row = 0;
        } else {
            temp_column = 0;
            temp_position_row = position_row - move;
        }
        for (; temp_position_row < row - 3 && temp_column < column - 3; temp_position_row++, temp_column++) {
            if (array[temp_position_row][temp_column] == player &&
                array[temp_position_row + 1][temp_column + 1] == player &&
                array[temp_position_row + 2][temp_column + 2] == player &&
                array[temp_position_row + 3][temp_column + 3] == player) {
                return player;
            }
        }

        // diagonal esquerda
        if (((column - 1) - move) > position_row) {
            temp_column = position_row + move;
            temp_position_row = 0;
        } else {
            temp_column = (column - 1);
            temp_position_row = position_row - ((column - 1) - move);
        }
        for (; temp_position_row < row - 3 && temp_column > 2; temp_position_row++, temp_column--) {
            if (array[temp_position_row][temp_column] == player &&
                array[temp_position_row + 1][temp_column - 1] == player &&
                array[temp_position_row + 2][temp_column - 2] == player &&
                array[temp_position_row + 3][temp_column - 3] == player) {
                return player;
            }
        }

        // empate
        if (array[row - 1][0] != 0 && array[row - 1][1] != 0 && array[row - 1][2] != 0 &&
            array[row - 1][3] != 0 && array[row - 1][4] != 0 && array[row - 1][5] != 0 &&
            array[row - 1][6] != 0) {
            return 3;
        }

        // retornar 0 se nao for estado final
        return 0;
    }


    //simular o jogo com movimentos aleatorios até que alguém ganhe
    public static int simulate(int array[][], int player, int move, int pos_row) {
        // lEnquanto nao for estado final
        while (true) {
            // verificar se acabou
            if (checkWin(array, player, move, pos_row) != 0) {
                return checkWin(array, player, move, pos_row);
            }

            player = switchPlayer(player);

            //executar jogada aleatoria entre as possiveis
            move = getPossibleMoves(array);
            pos_row = setMove(array, player, move);
        }
    }

    // actualizar os nos da arvore com o resultado da simulacao
    public static void update(int win, Node node_pt) {
        //iterar sobre todos os nos do ramo utilizado
        while (true) {
            //actualizar o no com vitoria ou derrota, dependendo de quem foi o movimento
            if (win == node_pt.player) {
                node_pt.wins = node_pt.wins + 1;
            } else if (win != 0) {
                node_pt.wins = node_pt.wins - 1;
            }

            //Aumentar o numero de nos vistados para ambos jogadores
            node_pt.visits += 1;

            // selecionar o pai
            if (node_pt.parent_node != null) {
                node_pt = node_pt.parent_node;
            } else {
                break;
            }
        }
    }

    //selecionar o melhor no calculado com a formula uct
    public static int uctSelect(Node node_pt, Node root_pt) {
        double uct_result;
        double best_value = -5000;
        int selected_node=0;

        //iterar sobre os children
        for (int i = 0; i < column; i++) {

            // se o child existir 
            if (node_pt.child_nodes[i] != null) {

                // calcular ucb1 
                uct_result = (double) node_pt.child_nodes[i].wins / (double) node_pt.child_nodes[i].visits +
                            Math.sqrt(2) * Math.sqrt(Math.log((double) root_pt.visits) / (double) node_pt.child_nodes[i].visits);

                // guardar o melhor
                if (uct_result > best_value) {
                    best_value = uct_result;
                    selected_node = i;
                }
            }
        }
        // retornar o nó selecionado
        return selected_node;
    }

    //selecionar o no com mais visitas
    public static int visitsSelect(Node node_pt) {
        double best_value = -5000;
        int selected_node=0;

        //iterar sobre os filhos
        for (int i = 0; i < column; i++) {

            // se o child existir 
            if (node_pt.child_nodes[i] != null) {

                // guardar o melhor
                if (node_pt.child_nodes[i].visits > best_value) {
                    best_value = node_pt.child_nodes[i].visits;
                    selected_node = i;
                }
            }
        }

         // retornar o nó selecionado
        return selected_node;
    }

    public static int  runMCTS(int arr[][],int pl, double limit_millis,int max_itera) {
        int temp_array[][];
        int array[][];
        int temp_player;
        startTime= System.currentTimeMillis();
        num_itera =0;
        int move=0;
        int result;

        //INVERTER  AS LINHAS DO BOARD INICIAL
        array = new int[row][column];
        for (int i=0; i < row;i++){
            for(int j=0; j < column ; j++){
                array[row-i-1][j]= arr[i][j];
            }
        }
        //copiar array atual para temporario para simulacoes, obter lista de todos movimentos disponiveis
        temp_array = new int[row][column];

        player=pl;
        temp_player = player;

        for (int i=0; i < row;i++){
            for(int j=0; j < column ; j++){
                temp_array[i][j]= array[i][j];
            }
        }

        getPossibleMoves(temp_array);
       // System.out.println(" Possible moves" + Arrays.toString(possible_moves));

        //criar um root node e um ponteiro para ele - representa o estado actual
        Node root = new Node();
        root.setPossibleMoves(possible_moves);
        root.player = player;
        Node root_pt = root;

        //criar um pontero para gerir os nos durante o processo de construção da arvore
         Node node_pt = root;

        //criar uma arvore para manter todos os nos e apaga-los no fim de todas as simulacoes
        Tree tree= new Tree();

        //iterar sobre a arvore de procura para selecionar, expandir, simular e actualizar os seus nos
        while (true) {

            // Expandir  childs
            if (node_pt.possible_moves[7] > 0) {

                // obter um movimento aleatorio
                move = node_pt.getRandomMove();
                
                // fazer o movimento no array temporario
                position_row = setMove(temp_array, temp_player, move);

                //obter os movimentos possiveis para o estado do novo child
                getPossibleMoves(temp_array);

                //expandir o no usando o child apropriado para o movimento possivel
                node_pt.addChild(possible_moves, temp_player, move);

                //adicionar o no a arvore
                tree.addNode(node_pt.child_nodes[move]);

                //comecar a simulacao sobre o movimento actual
                result = simulate(temp_array, temp_player, move, position_row);
               
                //actualizar o no e todos os parent com o resultado da simulacao
                update(result, node_pt.child_nodes[move]);

                //repor o estado original e por o ponteiro de novo a apontar para o root
                temp_player = player;

                for (int i=0; i < row;i++){
                    for(int j=0; j < column ; j++){
                        temp_array[i][j]= array[i][j];
                    }
                }

                node_pt = root_pt;

            } else {

                //verificar se e estado final - um no folha que nao tem child nodes 
                if (checkWin(temp_array, switchPlayer(temp_player), move, position_row) != 0) {

                    //actualizar o no e todos parent nodes com o resultado deste estado final
                    result = checkWin(temp_array, switchPlayer(temp_player), move, position_row);
                    update(result, node_pt);

                    //repor o estado original e por o ponteiro de novo a apontar para o root
                    temp_player = player;

                    for (int i=0; i < row;i++){
                        for(int j=0; j < column ; j++){
                            temp_array[i][j]= array[i][j];
                        }
                    }
                    node_pt = root_pt;

                } else {
                    // selecionar o child com o melhor ratio calculado com a formula uct
                    move = uctSelect(node_pt, root_pt);

                    //fazer o movimento no array copia e trocar de jogador
                    position_row = setMove(temp_array, temp_player, move);
                    temp_player = switchPlayer(temp_player);

                    //selecionar no como proximo a ser processado
                    node_pt = node_pt.child_nodes[move];
                }
            }

            //Calcular tempo e numero de iteracoes e usar um deles como criterio de paragem
            
            long currTime=System.currentTimeMillis();
            long delay=(currTime - startTime);
            num_itera++;
            if (delay >= 2000) {
                break;
            }
        }

        // Numero total de simulacoes nesta pesquisa
        System.out.println( "Numero total de simulacoes MCTS: " + root_pt.visits);

        // obter o melhor movimento no root node, de acordo com o criterio de selecao 
        move = visitsSelect(root_pt);

        //apagar todos os nos criados na simulacao
        tree.deleteNodes();

        // retornar melhor movimento
        return move;
    }
}
