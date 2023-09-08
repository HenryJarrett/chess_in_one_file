import chess_in_one_file as chess
import unittest

class ChessFuncsTests(unittest.TestCase):
    """Set up empty board"""
    def setUp(self):
        self.board = [['  ' for i in range(8)] for j in range(8)]
        self.blankboard = [['  ' for i in range(8)] for j in range(8)]

    """Verifies that a white king in check by a black pawn to its right returns true"""
    def test_in_check1(self):
        self.board[7][4] = 'wk'
        self.board[6][5] = 'bp'
        self.assertTrue(chess.in_check('w', self.board))
    
    """verifies that a white king in check by a black pawn to its left returns true""" 
    def test_in_check2(self):
        self.board[7][4] = 'wk'
        self.board[6][3] = 'bp'
        self.assertTrue(chess.in_check('w', self.board))
    
    """verifies that a black king in check by a white pawn to its right returns true"""
    def test_in_check3(self):
        self.board[0][4] = 'bk'
        self.board[1][3] = 'wp'
        self.assertTrue(chess.in_check('b', self.board))
    
    """verifies that a black king in check by a white pawn to its left returns true"""
    def test_in_check4(self):
        self.board[0][4] = 'bk'
        self.board[1][5] = 'wp'
        self.assertTrue(chess.in_check('b', self.board))
    
    """verifies that a king in check by an enemy bishop on the +/+ diagonal returns true"""
    def test_in_check5(self):
        self.board[0][4] = 'bk'
        self.board[3][7] = 'wb'
        self.assertTrue(chess.in_check('b', self.board))

    """verifies that a king in check by an enemy queen on the -/- diagonal returns true"""
    def test_in_check6(self):
        self.board[7][4] = 'wk'
        self.board[3][0] = 'bq'
        self.assertTrue(chess.in_check('w', self.board))

    """verifies that a king with a pinned piece preventing a check on the -/- diagonal returns false"""
    def test_in_check7(self):
        self.board[7][4] = 'wk'
        self.board[3][0] = 'bb'
        self.board[4][1] = 'wr'
        self.assertFalse(chess.in_check('w', self.board))
    
    """verifies that a king in check from a + row returns True"""
    def test_in_check8(self):
        self.board[0][4] = 'bk'
        self.board[5][4] = 'wr'
        self.assertTrue(chess.in_check('b', self.board))

    """verifies that a king with a pinned piece preventing check returns False"""
    def test_in_check9(self):
        self.board[7][4] = 'wk'
        self.board[0][4] = 'br'
        self.assertTrue(chess.in_check('w', self.board))
        self.board[5][4] = 'bb'
        self.assertFalse(chess.in_check('w', self.board))

    """verifies that a king in check by a knight returns True"""
    def test_in_check10(self):
        self.board[5][4] = 'bk'
        self.board[7][3] = 'wn'
        self.assertTrue(chess.in_check('b', self.board))
        self.board[7][3] = '  '
        self.board[4][2] = 'wn'
        self.assertTrue(chess.in_check('b', self.board))
    
    """In Check Functions properly!!!"""

    """test if ablack pawn can move forward 2 square from its starting square"""
    def test_nvp1(self):
        self.board[1][4] = 'bp'
        self.blankboard[3][4] = 'bp'
        self.assertEqual(chess.make_move(self.board, 'e5', 'b'), self.blankboard)

    """test if a white pawn can move forward 2 square's from its starting square"""
    def test_nvp2(self):
        self.board[6][2] = 'wp'
        self.blankboard[4][2] = 'wp'
        self.assertEqual(chess.make_move(self.board, 'c4', 'w'), self.blankboard) 
    
    """test if a white pawn can advance one square (not into promotion yet)"""
    def test_nvp3(self):
        self.board[6][2] = 'wp'
        self.blankboard[5][2] = 'wp'
        self.assertEqual(chess.make_move(self.board, 'c3', 'w'), self.blankboard)
    
    """test if a black pawn can advance one square (not into promotion yet)"""
    def test_nvp4(self):
        self.board[1][2] = 'bp'
        self.blankboard[2][2] = 'bp'
        self.assertEqual(chess.make_move(self.board, 'c6', 'b'), self.blankboard)  

    """test if a white pawn can advance and promote to another piece"""
    def test_promotion1(self):
        self.board[1][2] = 'wp'
        self.blankboard[0][2]='wq'
        self.assertEqual(chess.make_move(self.board, 'c8=Q', 'w'), self.blankboard)
        
    """test if a black pawn can advance and promote to another piece"""
    def test_promotion2(self):
        self.board[6][2] = 'bp'
        self.blankboard[7][2]='bq'
        self.assertEqual(chess.make_move(self.board, 'c1=Q', 'b'), self.blankboard)

    """Peaceful pawn and advances are functional"""

    """test if a white king can move peacefully from c2 to b3 """
    def test_king1(self):
        self.board[6][2] = 'wk'
        self.blankboard[5][1] = 'wk'
        self.assertEqual(chess.make_move(self.board, 'Kc2b3', 'w'), self.blankboard)
     
    """test if a white king can move peacefully from c2 to d1 """
    def test_king2(self):
        self.board[6][2] = 'wk'
        self.blankboard[7][3] = 'wk'
        self.assertEqual(chess.make_move(self.board, 'Kc2d1', 'w'), self.blankboard)

    """test if a white king can move peacefully from c2 to d2 """
    def test_king3(self):
        self.board[6][2] = 'wk'
        self.blankboard[6][3] = 'wk'
        self.assertEqual(chess.make_move(self.board, 'Kc2d2', 'w'), self.blankboard)

    """test if a white king can move peacefully from c2 to b1 """
    def test_king3(self):
        self.board[6][2] = 'wk'
        self.blankboard[7][1] = 'wk'
        self.assertEqual(chess.make_move(self.board, 'Kc2b1', 'w'), self.blankboard)

    """test if a white king can short castle"""
    def test_00(self):
        self.board[7][4] = 'wk'
        
        self.board[7][7] = 'wr'
        self.blankboard[7][6] = 'wk'
        self.blankboard[7][5] = 'wr'
        self.assertEqual(chess.make_move(self.board, '0-0', 'w'), self.blankboard) 
     
    """test if a black king can long castle"""
    def test_000(self):
        self.board[0][4] = 'bk'
        self.board[0][7] = 'br'
        self.blankboard[0][2] = 'bk'
        self.blankboard[0][3] = 'br'
        self.assertEqual(chess.make_move(self.board, '0-0-0', 'b'), self.blankboard)
    
    """Castling works, so do other peaceful king moves"""

    """Peaceful Knight move testing"""
    def test_knight(self):
        self.board[4][2] = 'wn'
        self.blankboard[6][1] = 'wn'
        #self.assertEqual(chess.make_move(self.board, 'Nb2', 'w'), self.blankboard)

    """Peaceful Bishop move testing"""
    def test_bishop(self):
        self.board[5][2] = 'wb'
        self.blankboard[7][0] = 'wb'
        #self.assertEqual(chess.make_move(self.board, 'Ba1', 'w'), self.blankboard)
    """Peaceful Rook move testing"""
    def test_rook(self):
        self.board[0][0] = 'wr'
        self.blankboard[0][7] = 'wr'
        self.assertEqual(chess.make_move(self.board, 'Ra8h8', 'w'), self.blankboard)
    """Peaceful Queen move testing"""
    def test_queen1(self):
        self.board[0][0] = 'wq'
        self.blankboard[7][7] = 'wq'
        self.assertEqual(chess.make_move(self.board, 'Qa8h1', 'w'), self.blankboard)
    def test_queen2(self):
        self.board[0][0] = 'wq'
        self.blankboard[0][7] = 'wq'
        self.assertEqual(chess.make_move(self.board, 'Qa8h8', 'w'), self.blankboard)

    """Peaceful moves complete"""
    
    """test piece capture"""
    def test_capture(self):
        self.board[6][1] = 'wb'
        self.board[7][0] = 'br'
        self.blankboard[7][0] = 'wb'
        self.assertEqual(chess.make_move(self.board, 'Bb2xa1', 'w'), self.blankboard)

    """White pawn capture"""
    def test_pawn_capture_w(self):
        self.board[3][4] = 'wp'
        self.board[2][3] = 'bp'
        self.blankboard[2][3] = 'wp'
        self.assertEqual(chess.make_move(self.board, 'exd6', 'w'), self.blankboard)
        #chess.display_board(chess.make_move(self.board, 'exd6', 'w'))

    """White pawn en passant"""
    def test_en_passant_w(self):
        self.board[3][4] = 'wp'
        self.board[3][3]= 'bp'
        self.blankboard[2][3] = 'wp'
        self.assertEqual(chess.make_move(self.board, 'exd6', 'w'), self.blankboard)

    """black pawn capture"""
    def test_pawn_capture_b(self):
        self.board[4][4] = 'bp'
        self.board[5][3] = 'wp'
        self.blankboard[5][3] = 'bp'
        self.assertEqual(chess.make_move(self.board, 'exd3', 'b'), self.blankboard)

    """black pawn en passant"""
    def test_en_passant_b(self):
        self.board[4][4] = 'bp'
        self.board[4][3]= 'wp'
        self.blankboard[5][3] = 'bp'
        #
        self.assertEqual(chess.make_move(self.board, 'exd3', 'b'), self.blankboard)

    """white Capturing into promotion"""
    def test_white_capture_promote(self):
        self.board[1][1] = 'wp'
        self.board[0][0] = 'bb'
        self.blankboard[0][0] = 'wq'
        self.assertEqual(chess.make_move(self.board, 'bxa8=Q', 'w'), self.blankboard)
    
    """black capturing into promotion"""
    def test_white_capture_promote(self):
        self.board[6][4] = 'bp'
        self.board[7][3] = 'wq'
        self.blankboard[7][3] = 'bn'
        self.assertEqual(chess.make_move(self.board, 'exd1=N', 'b'), self.blankboard)
    
    """Captures and making moves complete"""

    """Detecting legal moves"""
    """Testing if a pawn advancing with its two starting squares empty, also check if it can detect capturing to the right and left is detected as a legal move"""
    def test_advance2_detection(self):
        self.board[6][4] = 'wp'
        self.board[5][3] = 'bb'
        self.board[5][5] = 'bb'
        self.board[7][4] = 'wk'
        self.assertEqual(chess.all_legal('w', self.board)[6,4], ['e4', 'e3','exd3','exf3'])
    
    def test_pawns_save(self):
        self.board[6][4] = 'wp'
        self.board[5][3] = 'bb'
        self.board[5][5] = 'bn'
        self.board[7][4] = 'wk'
        self.assertEqual(chess.all_legal('w', self.board)[6,4], ['exf3'])

    """Test legal knight move detection"""
    def test_legal_knight(self):
        self.board[1][2] = 'bn'
        self.board[0][7] = 'bk'
        self.board[0][0] = 'wb'
        self.assertEqual(chess.all_legal('b', self.board)[1,2], ['Nc7b5','Nc7d5','Nc7a6','Nc7e6','Nc7e8','Nc7xa8'])
        self.board[0][0] = 'wr'
        self.assertEqual(chess.all_legal('b', self.board)[1,2], ['Nc7e8','Nc7xa8'])

    """Test legal Bishop move detection"""
    def test_legal_bishop(self):
        self.board[2][5] = 'bb'
        self.board[0][7] = 'bk'
        self.board[4][3] = 'wp'
        self.assertEqual(len(chess.all_legal('b', self.board)[2,5]), 7)
        # test its understangind of pins
        self.board[4][3] = 'wb'
        self.assertEqual(chess.all_legal('b', self.board)[2,5], ['Bf6g7', 'Bf6e5', 'Bf6xd4'])
    
    """Test legal Rook move detection"""
    def test_legal_Rook(self):
        # test its understangind of forced captures
        self.board[0][5] = 'wr'
        self.board[0][7] = 'bk'
        self.board[0][3] = 'br'
        self.assertEqual(len(chess.all_legal('b', self.board)[0,3]), 1)
        # test its general manuevarability
        self.board[0][5] = '  '
        self.assertEqual(len(chess.all_legal('b', self.board)[0,3]), 13)
    """Test legal Queen move detection"""
    def test_legal_queen(self):
        self.board[4][3] = 'wq'
        self.board[3][5] = 'wk'
        self.assertEqual(len(chess.all_legal('w', self.board)[4,3]), 27)
    """test copy board function"""
    def test_copy_board(self):
        self.board = chess.establish_board()
        self.blankboard = chess.copy_board(self.board)
        self.assertEqual(self.board, self.blankboard)
    
    """test that pawn won't move into check"""
    def test_move_into_check(self):
        self.board[7][4] = 'wk'
        self.board[6][3] = 'wp'
        self.board[3][0] = 'bq'
        self.assertEqual(chess.all_legal('w', self.board), {(7, 4): ['Ke1e2', 'Ke1f2', 'Ke1f1', 'Ke1d1']})
    """Test pawn promotions"""
    def test_peace_promotions(self):
        self.board[1][1] = 'wp'
        self.board[7][7] = 'wk'
        self.assertEqual(len(chess.all_legal('w', self.board)[1,1]), 4)
    """max possible promotions"""
    def test_maxpossible_promotions(self):
        self.board[1][1]= 'wp'
        self.board[7][7] = 'wk'
        self.board[0][0] = 'bn'
        self.board[0][2] = 'bn'
        self.assertEqual((len(chess.all_legal('w', self.board)[1,1])), 12)
    def test_promote_outof_check(self):
        self.board[1][1] = 'wp'
        self.board[0][7] = 'wk'
        self.board[0][0] = 'br'
        self.board[0][2] = 'br'
        self.assertEqual((len(chess.all_legal('w', self.board)[1,1])),4)
    """Detect all legal king moves"""
    def test_basic_king(self):
        self.board[4][4] = 'wk'
        self.assertEqual((len(chess.all_legal('w', self.board)[4,4])), 8)
    """Detect if castling is legal"""
    def test_legal_castling(self):
        self.board[7][4] = 'wk'
        self.board[7][7] = 'wr'
        self.board[7][0] = 'wr'
        self.assertEqual((len(chess.all_legal('w', self.board)[7,4])), 7)
    """Detect if a past king move shuts off castling"""
    def test_past_king_move(self):
        self.board[7][4] = 'wk'
        self.board[7][7] = 'wr'
        self.board[7][0] = 'wr'
        self.assertEqual((len(chess.all_legal('w', self.board, ['Ked1', '  ', 'Kde1'])[7,4])), 5)

    """Detect if a past queenrook move shuts off long castling"""
    def test_past_queens_rook(self):
        self.board[7][4] = 'wk'
        self.board[7][7] = 'wr'
        self.board[7][0] = 'wr'
        self.assertEqual((len(chess.all_legal('w', self.board, ['Rh7h6', '  ', 'Rh6h7'])[7,4])), 6)
    """Detect if a piece pointing at a square castling through is required shuts off castling"""
    def test_through_check(self):
        self.board[7][4] = 'wk'
        self.board[7][7] = 'wr'
        self.board[7][0] = 'wr'
        self.board[5][6] = 'br'
        self.assertEqual((len(chess.all_legal('w', self.board)[7,4])), 6)
    """Detect if a missing rook shuts off castling"""
    def missing_rook(self):
        self.board[7][4] = 'wk'
        self.board[7][7] = 'wr'
        self.assertEqual((len(chess.all_legal('w', self.board)[7,4])), 6)
    
    """Detect if will try to castle out of check"""
    def test_legal_castling(self):
        self.board[7][4] = 'wk'
        self.board[7][7] = 'wr'
        self.board[7][0] = 'wr'
        self.board[5][4] = 'br'
        self.assertEqual((len(chess.all_legal('w', self.board)[7,4])), 4)
      

    """Detect if white en passant is legal"""
    def test_legal_enpassent_w(self):
        self.board[3][4] = 'wp'
        self.board[3][5] = 'bp'
        self.board[7][7] = 'wk'
        self.blankboard[3][4] = 'wp'
        self.blankboard[1][5] = 'bp'
        self.assertEqual((len(chess.all_legal('w', self.board,last_board=self.blankboard)[3,4])), 2)
    """Detect if black en passant is legal"""
    def test_legal_enpassent_b(self):
        self.board[4][5] = 'wp'
        self.board[4][4] = 'bp'
        self.board[7][7] = 'bk'
        self.blankboard[6][5] = 'wp'
        self.blankboard[4][4] = 'bp'
        self.assertEqual((len(chess.all_legal('b', self.board,last_board=self.blankboard)[4,4])), 2)
    def test_bot(self):
        self.board[7][4] = 'wk'
        self.board[7][7] = 'wr'
        self.board[7][0] = 'wr'
        #print(chess.get_move_computer(chess.all_legal('w', self.board)))
    def test_check_King(self):
        self.board[7][4] = 'wk'
        self.board[7][5] = 'bk'
        self.assertTrue(chess.in_check('w', self.board))
        self.assertTrue(chess.in_check('b', self.board))

if __name__ == '__main__':
   unittest.main()