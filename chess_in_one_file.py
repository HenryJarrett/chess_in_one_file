import random


# establish constants
FILES = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
RANKS = {1:7, 2:6, 3:5, 4:4, 5:3, 6:2, 7:1, 8:0}

# establish game functions
def display_board(board):
    print('\n')
    for i in range(8):
        print(board[i])
0
def establish_board():
    # 0,0 of board = h8
    # board = [row, col]

    # create 2-d array
    board = [['  ' for col in range(8)] for row in range(8)]

    # initialize pieces
    black_pieces = ['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br']
    white_pieces = ['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr']
    for col in range(8):
        board[1][col] = 'bp'
        board[6][col] = 'wp'
        board[0][col] = black_pieces[col]
        board[7][col] = white_pieces[col]
    
    return board

def copy_board(board):
    copied_board = [[]for i in range(8)]
    for i in range(8):
        copied_board[i] = board[i][:]
    return copied_board


def convert_to_square(rank, file):
    numtorank = {0:'8', 1:'7', 2:'6', 3:'5', 4:'4', 5:'3', 6:'2', 7:'1'}
    numtofile = {0: 'a', 1:'b', 2:'c', 3:'d', 4:'e',5:'f',6:'g',7:'h'}
    return numtofile[file] + numtorank[rank] 
# determine if king is in check functions

def pawn_check(board, enemies, enemiepawn, kingcol, kingrow):
    # check if there is room for pawns
    if kingrow + enemiepawn < 8 and kingrow + enemiepawn >= 0:
        # check if there is an enemie pawn to the board's right
        if kingcol + 1 < 8:
            if board[kingrow+enemiepawn][kingcol+1] == enemies[0]: return True
        # check if there is an enemie pawn to the board's left
        if kingcol -1 > -1:
            if board[kingrow+enemiepawn][kingcol-1] == enemies[0]: return True
    return False

def bishop_check(board, enemies, kingcol, kingrow):
    def _bishop_check(rowdir, coldir):
        piecefound = False
        row = kingrow
        col = kingcol
        while(row+rowdir < 8 and row+rowdir > -1 and col+coldir < 8 and col+coldir > -1 and piecefound == False):
            row += rowdir
            col += coldir
            if board[row][col] == enemies[2] or board[row][col] == enemies[4]: return True
            if board[row][col] != '  ': piecefound = True

    # go down the +/+, -/-, +/-, and -/+ diagonals until end of board or non enemy bishop/queen
    if _bishop_check(1,1) or _bishop_check(-1, -1) or _bishop_check(-1, 1) or _bishop_check(1, -1): return True
    return False

def rook_check(board, enemies, kingcol, kingrow):
    # helper func to avoid repetitive code, checks the specified direction
    def _rook_check(coldir, rowdir):
        piecefound = False
        row = kingrow
        col = kingcol
        while(row+rowdir < 8 and row+rowdir > -1 and col+coldir < 8 and col+coldir > -1 and piecefound == False):
            row+=rowdir
            col+=coldir
            if board[row][col] == enemies[4] or board[row][col] == enemies[3]: return True
            if board[row][col] != '  ': piecefound = True

    #check the +/0, -/0, 0/+, 0/- directions for enemie rook or queen
    if _rook_check(1,0) or _rook_check(-1, 0) or _rook_check(0, 1) or _rook_check(0, -1): return True
    return False
    
def knight_check(board, enemies, kingcol, kingrow):
    def _knight_check(rowdir, coldir):
        row = kingrow + rowdir
        col = kingcol + coldir
        if row < 8 and row > -1 and col < 8 and col > -1:
            if board[row][col] == enemies[1]: return True
    if _knight_check(2,-1) or _knight_check(2, 1) or _knight_check(-2, 1) or _knight_check(-2, -1) or _knight_check(1,2) or _knight_check(-1, 2) or _knight_check(1, -2) or _knight_check(-1, -2): return True    
    return False

def king_check(board, enemies, kingcol, kingrow):
    def _king_check(rowdir, coldir):
        row = kingrow + rowdir
        col = kingcol + coldir
        if row < 8 and row > -1 and col < 8 and col > -1:
            if board[row][col] == enemies[5]:return True
    if _king_check(1, 1) or _king_check(1, -1) or _king_check(1, 0) or \
        _king_check(-1, 1) or _king_check(-1, 0) or _king_check(-1, -1) or \
        _king_check(0, 1) or _king_check(0, -1):return True
    return False

def move_into_check(board, color, move):
    #copy board
    copied_board = copy_board(board)

    #make move on copied board
    copied_board = make_move(copied_board, move, color)

    return in_check(color, copied_board)

def in_check(color, board):
    # establish enemies 
    king = 'wk' if color == 'w' else 'bk'
    enemies = ['bp', 'bn', 'bb', 'br',  'bq', 'bk'] if color == 'w' else ['wp', 'wn', 'wb', 'wr',  'wq', 'wk']
    enemiepawn = -1 if color == 'w' else 1
    
    # find the king
    for row in range(8):
        for col in range(8):
            if board[row][col] == king:
                kingcol, kingrow = col, row
                if pawn_check(board, enemies, enemiepawn, kingcol, kingrow) or \
                    bishop_check(board, enemies, kingcol, kingrow) or \
                        rook_check(board, enemies, kingcol, kingrow) or \
                            knight_check(board, enemies, kingcol, kingrow) or \
                                king_check(board, enemies, kingcol, kingrow): return True
    # check for pawns, bishops, rooks, queens, and knights checking
    
    
    # the king is not in check
    return False

# get all legal moves functions

def find_promotions(board, rank, file, piece):
    square = convert_to_square(rank, file)
    pawndir = -1 if piece[0] == 'w' else 1
    pawns_moves = []
    promotionrank = 0 if piece[0] == 'w' else 7
    options = ['Q', 'R', 'N', 'B']
    enemies = ['bp', 'bn', 'bb', 'br',  'bq'] if piece[0] == 'w' else ['wp', 'wn', 'wb', 'wr',  'wq']
    
    """all optional pieceful promotions. Get it? 
    pieceful, becuase this promotion doesn't involve captures and there are multiple piece options"""
    if board[promotionrank][file] == '  ':
        for option in options:
            move = convert_to_square(pawndir + rank, file) + '=' + option
            if move_into_check(board, piece[0], move) == False:
                pawns_moves.append(move)
    # capture into promotion, ie: axb4=B
    if file-1 > -1:
        if board[promotionrank][file-1] in enemies:
            for option in options:
                move = square[0] + 'x' + convert_to_square(pawndir + rank, file-1) + '=' + option
                if move_into_check(board, piece[0], move) == False:
                    pawns_moves.append(move)
    if file+1 < 8:
        if board[promotionrank][file+1] in enemies:
            for option in options:
                move = square[0] + 'x' + convert_to_square(pawndir + rank, file+1) + '=' + option
                if move_into_check(board, piece[0], move) == False:
                    pawns_moves.append(move)
    return pawns_moves

def legal_pawn(board, rank, file, piece, last_board=[]):
    square = convert_to_square(rank, file)
    pawndir = -1 if piece[0] == 'w' else 1
    pawns_moves = []
    promotionrank = 0 if piece[0] == 'w' else 7
    enprank = 3 if piece[0] == 'w' else 4
    enemies = ['bp', 'bn', 'bb', 'br',  'bq'] if piece[0] == 'w' else ['wp', 'wn', 'wb', 'wr',  'wq']
    #check if it's on it's starting square and can advance 2
    if (pawndir == -1 and rank == 6) or (pawndir == 1 and rank == 1):
        #its on its starting square
        if board[rank+pawndir][file] == '  ' and board[rank+2*pawndir][file] == '  ':
            #check if making this move would lead to the king being in check
            move = convert_to_square(2* pawndir+rank, file)
            if move_into_check(board, piece[0],move) == False:
                pawns_moves.append(move)
    # check if it can advance to the square in front without promoting
    if rank+pawndir != promotionrank:
        if board[rank+pawndir][file] == '  ':
            move = convert_to_square(pawndir + rank, file)
            if move_into_check(board, piece[0], move) == False:
                pawns_moves.append(move)
        # check if it can take to either or both side without promoting
        if file-1 > -1:
            if board[rank+pawndir][file-1] in enemies:
                # can capture to the left
                move = square[0] + 'x' + convert_to_square(rank+pawndir, file-1)
                if move_into_check(board, piece[0], move) == False:
                    pawns_moves.append(move)
        if file+1 < 8:
            if board[rank+pawndir][file+1] in enemies:
                # can capture to the left
                move = square[0] + 'x' + convert_to_square(rank+pawndir, file+1)
                if move_into_check(board, piece[0], move) == False:
                    pawns_moves.append(move)
    if rank == enprank:
        # en passent may be possible
        if file+1 < 8:
            if board[rank][file+1]== enemies[0]:
                #check last board for if pawn was two ranks back
                if last_board[rank+2*pawndir][file+1] == enemies[0] and last_board[rank][file+1] == '  ' and last_board[rank+pawndir][file+1] == '  ':
                    move = square[0] + 'x' + convert_to_square(rank+2*pawndir, file+1)
                    if move_into_check(board, piece[0], move) == False:
                        pawns_moves.append(move)
        if file-1 > -1:
            if board[rank][file-1]== enemies[0]:
                #check last board for if pawn was two ranks back
                if last_board[rank+2*pawndir][file-1] == enemies[0] and last_board[rank][file-1] == '  ' and last_board[rank+pawndir][file-1] == '  ':
                    move = square[0] + 'x' + convert_to_square(rank+2*pawndir, file-1)
                    if move_into_check(board, piece[0], move) == False:
                        pawns_moves.append(move)
    if rank+pawndir == promotionrank:
        return find_promotions(board, rank, file, piece)
    return pawns_moves

def legal_knight(board, rank, file, piece):
    # go a knights distance from each square, check if that move puts the king in check, return it\
    knight_moves = []
    friends = ['bp', 'bn', 'bb', 'br',  'bq', 'bk'] if piece[0] == 'b' else ['wp', 'wn', 'wb', 'wr',  'wq', 'wk']
    def _knightdistance(rowdir, coldir):
        row = rank + rowdir
        col = file + coldir
        if row < 8 and row > -1 and col < 8 and col > -1:
            if board[row][col] not in friends:
                #move is on the board
                move = 'N'+ convert_to_square(rank, file) + convert_to_square(row, col) if board[row][col] == '  ' \
                    else 'N'+ convert_to_square(rank, file)+ 'x' + convert_to_square(row, col)
                if move_into_check(board, piece[0], move) == False:
                    knight_moves.append(move)
                
    _knightdistance(2, -1)
    _knightdistance(2, 1)
    _knightdistance(-2, 1)
    _knightdistance(-2, -1)
    _knightdistance(1, -2)
    _knightdistance(1, 2)
    _knightdistance(-1, 2)
    _knightdistance(-1, -2)
    return knight_moves

def legal_bishop(board, rank, file, piece):
    friends = ['bp', 'bn', 'bb', 'br',  'bq'] if piece[0] == 'b' else ['wp', 'wn', 'wb', 'wr',  'wq']
    enemies = ['bp', 'bn', 'bb', 'br',  'bq'] if piece[0] == 'w' else ['wp', 'wn', 'wb', 'wr',  'wq']
    bishop_moves = []

    def _bishop_move(rowdir, coldir):
        row = rank
        col = file
        piecefound = False
        while(row+rowdir < 8 and row+rowdir > -1 and col+coldir < 8 and col+coldir > -1 and piecefound == False):
            row += rowdir
            col += coldir
            if board[row][col] in enemies or board[row][col] == '  ':
                move = 'B'+ convert_to_square(rank, file) + convert_to_square(row, col) if board[row][col] == '  ' \
                    else 'B'+ convert_to_square(rank, file)+ 'x' + convert_to_square(row, col)
                if move_into_check(board, piece[0], move) == False:
                    bishop_moves.append(move)
            if board[row][col] != '  ':
                piecefound = True

    # go down the +/+, -/-, +/-, and -/+ diagonals
    _bishop_move(1, 1)
    _bishop_move(-1, 1)
    _bishop_move(1, -1)
    _bishop_move(-1, -1)
    return bishop_moves

def legal_rook(board, rank, file, piece):
    friends = ['bp', 'bn', 'bb', 'br',  'bq'] if piece[0] == 'b' else ['wp', 'wn', 'wb', 'wr',  'wq']
    enemies = ['bp', 'bn', 'bb', 'br',  'bq'] if piece[0] == 'w' else ['wp', 'wn', 'wb', 'wr',  'wq']
    rook_moves = []
    def _rook_move(rowdir, coldir):
        row = rank
        col = file
        piecefound = False
        while(row+rowdir < 8 and row+rowdir > -1 and col+coldir < 8 and col+coldir > -1 and piecefound == False):
            row += rowdir
            col += coldir
            if board[row][col] in enemies or board[row][col] == '  ':
                move = 'R'+ convert_to_square(rank, file) + convert_to_square(row, col) if board[row][col] == '  ' \
                    else 'R'+ convert_to_square(rank, file)+ 'x' + convert_to_square(row, col)
                if move_into_check(board, piece[0], move) == False:
                    rook_moves.append(move)
            if board[row][col] != '  ':
                piecefound = True
    #check all legal rook moves
    _rook_move(1, 0)
    _rook_move(-1, 0)
    _rook_move(0, -1)
    _rook_move(0, 1)
    return rook_moves

def legal_queen(board, rank, file, piece):
    friends = ['bp', 'bn', 'bb', 'br',  'bq'] if piece[0] == 'b' else ['wp', 'wn', 'wb', 'wr',  'wq']
    enemies = ['bp', 'bn', 'bb', 'br',  'bq'] if piece[0] == 'w' else ['wp', 'wn', 'wb', 'wr',  'wq']
    queen_moves = []
    def _queen_move(rowdir, coldir):
        row = rank
        col = file
        piecefound = False
        while(row+rowdir < 8 and row+rowdir > -1 and col+coldir < 8 and col+coldir > -1 and piecefound == False):
            row += rowdir
            col += coldir
            if board[row][col] in enemies or board[row][col] == '  ':
                move = 'Q'+ convert_to_square(rank, file) + convert_to_square(row, col) if board[row][col] == '  ' \
                    else 'Q'+ convert_to_square(rank, file)+ 'x' + convert_to_square(row, col)
                if move_into_check(board, piece[0], move) == False:
                    queen_moves.append(move)
            if board[row][col] != '  ':
                piecefound = True
    #check all legal queen moves
    _queen_move(1, 0)
    _queen_move(-1, 0)
    _queen_move(0, -1)
    _queen_move(0, 1)
    _queen_move(1, 1)
    _queen_move(-1, 1)
    _queen_move(1, -1)
    _queen_move(-1, -1)
    return queen_moves

def legal_king(board, rank, file, piece, moves_made):
    friends = ['bp', 'bn', 'bb', 'br',  'bq'] if piece[0] == 'b' else ['wp', 'wn', 'wb', 'wr',  'wq']
    enemies = ['bp', 'bn', 'bb', 'br',  'bq'] if piece[0] == 'w' else ['wp', 'wn', 'wb', 'wr',  'wq']
    startingrank = 7 if piece[0] == 'w' else 0
    ourmoves = 'even' if piece[0] == 'w' else 'odd'
    shortcastle = True
    forbidden_castle = ['Ke', '0-']
    longcastle = True
    king_moves = []
    # basic king moves
    #-1, +1 in each direction
    # check if on board, no friendly pieces there, not moving into check, add move
    def _assess_king_move(newrank, newfile):
        if newrank > -1 and newrank < 8 and newfile > -1 and newfile < 8:
            if board[newrank][newfile] in enemies or board[newrank][newfile] == '  ':
                move = 'K'+ convert_to_square(rank, file) + convert_to_square(newrank, newfile) if board[newrank][newfile] == '  ' \
                        else 'K'+ convert_to_square(rank, file)+ 'x' + convert_to_square(newrank, newfile)
                if move_into_check(board, piece[0], move) == False:
                    king_moves.append(move)

    def _assess_castling(shortcastle, longcastle):
        if rank == startingrank and (shortcastle == True or longcastle == True):
            #not ruled out yet
            for move in range(len(moves_made)):
                if move % 2 == 0 and ourmoves == 'even':
                    #its whites move and we're looking at white
                    if moves_made[move][:2] in forbidden_castle:
                        longcastle = False
                        shortcastle = False
                    if moves_made[move][:2] == "Ra":
                        longcastle = False
                    if moves_made[move][:2] == "Rh":
                        longcastle = False
            if longcastle:
                #check if pieces are in the way dx, cx, bx
                if board[startingrank][0] == piece[0] + 'r' and board[startingrank][1] == '  ' and board[startingrank][2] == '  ' and board[startingrank][3] == '  ':
                    checkotwlong = copy_board(board)
                    checkotwlong[startingrank][1] = piece[0] + 'k'
                    checkotwlong[startingrank][2] = piece[0] + 'k'
                    checkotwlong[startingrank][3] = piece[0] + 'k'
                    # if not in check on the way to castling, castling is legal
                    if in_check(piece[0], checkotwlong) == False:
                        king_moves.append('0-0-0')
                    
            if shortcastle:
                if board[startingrank][7] == piece[0] + 'r' and board[startingrank][5] == '  ' and board[startingrank][6] == '  ':
                    checkotwshort = copy_board(board)
                    checkotwshort[startingrank][5] = piece[0] + 'k'
                    checkotwshort[startingrank][6] = piece[0] + 'k'
                    # if not in check on the way to castling, castling is legal
                    if in_check(piece[0], checkotwshort) == False:
                        king_moves.append('0-0')               


        
        

    _assess_king_move(rank+1, file)
    _assess_king_move(rank+1, file+1)
    _assess_king_move(rank+1, file-1)
    _assess_king_move(rank-1, file)
    _assess_king_move(rank-1, file+1)
    _assess_king_move(rank-1, file-1)
    _assess_king_move(rank, file+1)
    _assess_king_move(rank, file-1)
    _assess_castling(shortcastle, longcastle)
    return king_moves

    # castling
    # 0-0: Check that all those squares are empty, and that a king on each square would not be in check
    # check move order for moves by this king
    # check move order for the kingside rook
    # if any are false, cannot castle
    #0-0-0 is similar but for the queenside

def pieces_legal_moves(board, rank, file, piece, moves_made=[], last_board=[]):
    if piece[1] == 'p':
        return legal_pawn(board, rank, file, piece, last_board)
    if piece[1] == 'n':
        return legal_knight(board, rank, file, piece)
    if piece[1] == 'b':
        return legal_bishop(board, rank, file, piece)
    if piece[1] == 'r':
        return legal_rook(board, rank, file, piece)
    if piece[1] == 'q':
        return legal_queen(board, rank, file, piece)
    if piece[1] == 'k':
        return legal_king(board, rank, file, piece, moves_made)
    
def all_legal(color, board, moves_made=[], last_board=[]):
    pieces = [color+'p', color+'b', color+'n', color+'k', color+'r',color+'q']
    #iterate throught the board, get all the legal moves for each piece
    legalmoves = {}
    for rank in range(8):
        for file in range(8):
            if board[rank][file] in pieces:
                #found a piece, get its legal moves
                tempmoves = pieces_legal_moves(board, rank, file, board[rank][file], moves_made, last_board)
                if tempmoves != [] and tempmoves != None:
                    square = (rank, file)
                    legalmoves[(rank, file)] = tempmoves
        
    return legalmoves
# make moves functions 
def non_violent_pawn(board, move, color):
    # handle pawns moving two from their starting square
    newrow = int(move[1])
    # files dictionary
    files = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
    col = files[move[0]]
    # white pawn on starting square
    if color == 'w' and newrow == 4:
        if board[6][col] == 'wp':
            board[6][col] = '  '
            board[4][col] = 'wp'
            return board
    
    # black pawn on starting square
    if color == 'b' and newrow == 5:
        if board[1][col] == 'bp':
            board[1][col] = '  '
            board[3][col] = 'bp'
            return board
    
    # handle pawns moving forward one
    pawndir = 1 if color == 'w' else -1 
    
    # invert newrow
    ranks = {2:6, 3:5, 4:4, 5:3, 6:2, 7:1}
    newrow = ranks[newrow]

    # erase the pawn, move it
    board[newrow+pawndir][col] = '  '
    board[newrow][col] = color+'p'
    return board
def peaceful_promotion(board, move, color):
    # get the piece the pawn is promoting to
    piece = color + move[3].lower()
    newrow = 7 if color == 'b' else 0
    oldrow = 6 if color == 'b' else 1

    # files dictionary
    files = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
    col = files[move[0]]

    # remove old pawn
    board[oldrow][col] = '  '

    # replace with new piece
    board[newrow][col] = piece
    return board
def castle(board, move, color):
    # find the rank
    rank = 7 if color == 'w' else 0
    # empty the kings spot and the rooks spot
    board[rank][4] = '  '
    board[rank][7] = '  '

    # place the king into the right spot
    # short castle
    if len(move) == 3:
        board[rank][6] = color+'k'
        board[rank][5] = color+'r'
    
    # long castle
    else:
        board[rank][2] = color+'k'
        board[rank][3] = color+'r'
    return board
#dead
def bishop_move(board, move, color):
    # create and place piece
    piece = color + move[0].lower()
    file = FILES[move[1]]
    rank = RANKS[int(move[2])]
    board[rank][file] = piece

    #find and delete old piece
    def _find_bishop(rowdir, coldir):
        row = rank
        col = file
        piecefound = False
        while(row+rowdir < 8 and row+rowdir > -1 and col+coldir < 8 and col+coldir > -1 and piecefound == False):
            row += rowdir
            col += coldir
            if board[row][col] == piece:
                board[row][col] = '  '
                piecefound = True
            if board[row][col] != '  ': piecefound = True

    # go down the +/+, -/-, +/-, and -/+ diagonals until end of board or bishop is found
    _find_bishop(1, 1)
    _find_bishop(-1, 1)
    _find_bishop(1, -1)
    _find_bishop(-1, -1)

    return board
#dead
def knight_move(board, move, color):
    # create and place piece
    piece = color + move[0].lower()
    file = FILES[move[1]]
    rank = RANKS[int(move[2])]
    board[rank][file] = piece
    #remove old piece
    #find old piece
    def _find_knight(rowdir, coldir):
        row = rank + rowdir
        col = file + coldir
        if row < 8 and row > -1 and col < 8 and col > -1:
            if board[row][col] == piece:
                board[row][col] = '  '
    _find_knight(2, -1)
    _find_knight(2, 1)
    _find_knight(-2, 1)
    _find_knight(-2, -1)
    _find_knight(1, -2)
    _find_knight(1, 2)
    _find_knight(-1, 2)
    _find_knight(-1, -2)
    return board
#dead
def rook_move(board, move, color):
    # create and place piece
    piece = color + move[0].lower()
    file = FILES[move[1]]
    rank = RANKS[int(move[2])]
    board[rank][file] = piece

    # find and delete piece
    def _find_rook(coldir, rowdir):
        piecefound = False
        row = rank
        col = file
        while(row+rowdir < 8 and row+rowdir > -1 and col+coldir < 8 and col+coldir > -1 and piecefound == False):
            row+=rowdir
            col+=coldir
            if board[row][col] == piece:
                board[row][col] = '  '
            if board[row][col] != '  ': piecefound = True

    #check the +/0, -/0, 0/+, 0/- directions for rook
    _find_rook(1, 0)
    _find_rook(-1, 0)
    _find_rook(0, 1)
    _find_rook(0, -1)
    return board
#dead
def queen_move(board, move, color):
    # create and place piece
    piece = color + move[0].lower()
    file = FILES[move[1]]
    rank = RANKS[int(move[2])]
    board[rank][file] = piece

    #find and delete old piece
    #find queen
    def _find_queen(coldir, rowdir):
        piecefound = False
        row = rank
        col = file
        while(row+rowdir < 8 and row+rowdir > -1 and col+coldir < 8 and col+coldir > -1 and piecefound == False):
            row+=rowdir
            col+=coldir
            if board[row][col] == piece:
                board[row][col] = '  '
            if board[row][col] != '  ': piecefound = True

    #check the +/0, -/0, 0/+, 0/- directions for queen
    _find_queen(1, 0)
    _find_queen(-1, 0)
    _find_queen(0, 1)
    _find_queen(0, -1)
    #find queen diagonally
    _find_queen(1, 1)
    _find_queen(-1, 1)
    _find_queen(1, -1)
    _find_queen(-1, -1)
    
    return board
#dead 
def king_move(board, move, color):
    # get the piece
    piece = color + move[0].lower()

    #get the pieces oiriginal location and empty it
    board[RANKS[int(move[2])]][FILES[move[1]]] = '  '

    # get the new piece location and put the piece in there
    board[RANKS[int(move[5])]][FILES[move[4]]] = piece

    return board

def piece_move(board, move, color):
    # get the piece
    piece = color + move[0].lower()

    #get the pieces oiriginal location and empty it
    board[RANKS[int(move[2])]][FILES[move[1]]] = '  '

    # get the new piece location and put the piece in there
    board[RANKS[int(move[4])]][FILES[move[3]]] = piece

    return board
    
def pawn_capture(board, move, color):
    #exd6 ed6 ed4
    original_file = FILES[move[0]] 
    new_file = FILES[move[1]] 
    new_rank = RANKS[int(move[2])]
    dir = 1 if color == 'w' else -1 
    #en passant
    if board[new_rank][new_file] == '  ':
        board[new_rank + dir][new_file] = '  '       

    #non en passant captures
    #delete original pawn
    board[new_rank + dir][original_file] = '  '
    #place new pawn
    board[new_rank][new_file] = color + 'p'
    return board

def capture_promote(board, move, color):
    newpiece = color + move[5].lower()
    originalfile = FILES[move[0]]
    newfile = FILES[move[2]]
    dir = 1 if color == 'w' else -1 
    board[RANKS[int(move[3])]+dir][originalfile] = '  '
    board[RANKS[int(move[3])]][newfile] = newpiece
    return board

def make_move(board, move, color):
    # figure out the type of move, send to its proper function
    
    #if length is 2, it must be a non violent pawn move
    if len(move) == 2: return non_violent_pawn(board, move, color)
    
    if len(move) == 3:
        # has to be short castle 0-0
        return castle(board, move, color)

    #if length is 4, must be a peaceful promotion, or pawn capture
    if len(move) == 4:
        if move[2] == "=": return peaceful_promotion(board, move, color)
        if move[1] == "x":
            if move[0].islower():
                return pawn_capture(board, move[0]+move[2]+move[3], color )
    #if length is 5, must be a long castle, or a peaceful peice move Ra4b4
    if len(move) == 5:
        if move[0] == '0':return castle(board, move, color)
        return piece_move(board, move, color)
    
    #if length is 6, must be a pawn capture leading to promotion, or a piece capturing
    if move[0].islower(): return capture_promote(board, move, color)
    # remove the x and send it to same function as before
    return piece_move(board, move[:3]+ move[4:], color)

def display_squares(moves):
    options = []
    for key in moves:
        options.append(convert_to_square(key[0], key[1]))
    ranks = {'1':7, '2':6, '3':5, '4':4, '5':3, '6':2, '7':1, '8':0}
    while True:
        print(options)
        choice = input("select a square:\n")
        if choice in options:
            #convert and return
            return (ranks[choice[1]], FILES[choice[0]])

def get_move_user(board, moves):
    propersquare = False
    square = display_squares(moves)
    while True:
        print(moves[square])
        answer = input("Enter your move")
        if answer in moves[square]:
            return answer

def get_move_computer(moves):
    #select a random square then a random move out of that square
    square = list(moves.keys())[random.randint(0, len(list(moves.keys()))-1)]
    return moves[square][random.randint(0,len(moves[square])-1)]

def player_turn(board, last_board, moves_made, color, bot):
    display_board(board)
    opposition = "black" if color == 'w' else "white"
    #get all legal moves
    moves = {}
    moves = all_legal(color, board, moves_made, last_board)
    if moves == {}:
        if in_check(color, board):
            print("Checkmate, "+opposition+" is victorious")
        else:
            print("GameDrawn by Stalemate")    
        print("Number of moves: " + str(len(moves_made)))
        print(moves_made)
        return False
    #game not mated, get whites move
    move = get_move_user(board, moves) if bot == False else get_move_computer(moves)
            
    # add move to moves list
    moves_made.append(move)

    #clone board before move
    last_board = copy_board(board)

    #make move
    board = make_move(board, move, color)

    return True

def game():
     #get bot decisions
    blackbot = False
    whitebot = False
    answer = input("Would you like white to be played by the computer?(y/n)")
    if answer == 'y':
        whitebot = True
    answer = input("Would you like black to be played by the computer?(y/n)")
    if answer == 'y':
        blackbot = True

        #establish local variables
    board = establish_board()
    last_board = establish_board()
    moves_made = []

    #game loop
    gameplay = True
    while gameplay:
        #whites turn
        gameplay = player_turn(board, last_board, moves_made, 'w', whitebot)
        if gameplay:
            gameplay = player_turn(board, last_board, moves_made, 'b', blackbot)
            
    #game is over
    again = input("Play again?(y/n)")
    if again == "n":
        return False
    return True


if __name__ == '__main__':
    playing_chess = True
    print("Welcome to Terminal Chess by Henry Jarrett")

    #general loop
    while playing_chess:
        playing_chess = game()
       
    #player is done playing
    print('Thanks for playing terminal chess by Henry Jarrett')