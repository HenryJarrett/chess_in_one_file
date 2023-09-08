# chess_in_one_file
Chess in one file. Written from scratch. The  only imported library is random. The program has a bot that plays random legal moves.

Requirements to run:
To run the game file "chess_in_one_file.py", only a working installation of python3 is required. The program can be run by entering its directory on your computer from the terminal and typing: "python3 chess_in_one_file.py"

Requirements to run tests.py:
tests.py uses the unittest framework to run tests. unittest should be installed by default with your python3.

The game functions like this:

User is asked if they want a bot to play either or both sides.

After this, the program initializes a chess board with pieces on their starting squares.

Then the program generates all legal moves. It does this by reviewing each piece of the color that is moving. For example, if it is white to move the program will find and evaluate all the white pieces. 

It will look at all the squares the piece could move to on an empty board. Then it will check if moving there would lead to its king being in check, or capturing a piece of its same color. If either of those cases is true, the program will not consider that move. If it can make the move without capturing its own piece or putting its own king into check, it will add that move to the dictionary of legal moves. 

Castling:
To determine if castling is legal, it will check if the king and either rook are on their starting square. If both of those are true, it will check the list of past moves for a king move or rook move. If the queenside rook has moved, it will stop considering long castling. If the kingside rook has moved, it will stop considering short castling. If a castling move has still not been ruled out, it will check if there are pieces between the rook and the king, if there are it will stop considering that castling move. If there are not any pieces in the way, it will check if castling moves the king through a check. If it does, it will stop considering that castling move. If a castling move passes through all these considerations, it will be appended to the legal moves list.

En Passant:
To determine if a pawn can capture in passing, it will check if the pawn is three squares removed from its starting square. If it is, it will check for an enemy pawn on either side of it. If there is an enemy pawn to either side it will check the previous board. If on the previous board, there was a pawn on the starting square of the enemy pawn, and if there were no pieces on the two squares ahead of it. If this is true, the program will check if en passant would put the pawn's king into check. If it won't en passant will be appended to the legal moves list.

Checking if the king is in check:
To check if the white king is in check, the program will find the white king, and then evaluate each square an enemy piece could attack it from. if any pieces are attacking it, it will return true.

Format of move dictionary:
The legal move dictionary is formatted like this: {(rank of piece, file of piece), [array of strings of legal moves in pgn format ("exd4", "e3")]} 

Selecting a random move for the computer:
The computer iterates through the keys of the legal moves dictionary and selects a random key. It then selects a random value in this key's array of moves.

Making a move:
The move is appended to the array of strings of moves, the program clones the current state of the board. Then, the move is sent to the make move function in this format: exd4. The program evaluates the number of characters in the move to determine what type of move it is. It then checks for a few more details to send the move to the proper helper function. This function then makes the move on the board. 

Evaluating if the game is over:
if the legal moves dictionary is empty after evaluating all legal moves, the game is over. If the king is in check the side whose move it is lost, the program will output this result. If their king is not in check, The program will output that the game is stalemated. Regardless of the result, the computer will ask the player if they would like to play again.

Note:
If the game is in a state where it is impossible for one side to be checkmated, the game will continue for ever. This is because there are still legal moves. The program does not care if the game goes on forever.

