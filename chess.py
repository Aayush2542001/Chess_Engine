from chessboard import display
import time
import os

globalTerminalReached = 0
globalPrun = 0
globalPrunAtDepth = []
globalPossibleMovesReached = 0


class BoardData:
    PositionList = \
        [
            ['k', None, None, 'K', None, None, None, None],
            ['P', 'p', None, None, 'R1', None, None, None],
            [None, 'P', None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, 'P', None, None, None],
            ['R2', None, None, None, None, None, None, None],
            ['p', None, None, None, None, None, None, None],
            ['B1', None, None, None, None, 'b1', None, None]
        ]
    pieceRegister = {}

    nextMoveWhite = True
    canWhiteCastle = [True, False, False]  # King R1  R2
    canBlackCastle = [False, False, False]  # king r1  r2
    blackList = ['p', 'r1', 'r2', 'b1', 'b2', 'k', 'q', 'n1', 'n2']
    whiteList = ['P', 'R1', 'R2', 'B1', 'B2', 'K', 'Q', 'N1', 'N2']
    availableMoveList = []
    movement = []
    points = 0

    @staticmethod
    def changePoint(piece, isRemoved):

        pointTable = {
            'P': -1,
            'R1': -5,
            'R2': -5,
            'N1': -3,
            'N2': -3,
            'B1': -3,
            'B2': -3,
            'K': -41,
            'Q': -8,
            'p': 1,
            'r1': 5,
            'r2': 5,
            'n1': 3,
            'n2': 3,
            'b1': 3,
            'b2': 3,
            'k': 41,
            'q': 8,
        }
        x = pointTable.get(piece)
        if isRemoved:
            BoardData.points += x
        else:
            BoardData.points -= x

    @staticmethod
    def printData(List=True, Register=False, Castle=False, Points=False):
        if List:
            print()
            for row in range(len(BoardData.PositionList) - 1, -1, -1):
                for col in range(len(BoardData.PositionList[0])):
                    print("% 5s" % (BoardData.PositionList[row][col]), end=" ")
                print()
            print()
        if Register:
            print()
            for key, value in BoardData.pieceRegister.items():
                print(str(key), " ", str(value))
            print()
        if Castle:
            print()
            print(BoardData.canWhiteCastle)
            print(BoardData.canBlackCastle)
            print()
        if Points:
            print()
            print("Points " + str(BoardData.points))
            print()

    @staticmethod
    def pieceToFen(piece):
        dict = {
            'R1': 'R',
            'R2': 'R',
            'B1': 'B',
            'B2': 'B',
            'N1': 'N',
            'N2': 'N',
            'K': 'K',
            'Q': 'Q',
            'P': 'P',
            'r1': 'r',
            'r2': 'r',
            'b1': 'b',
            'b2': 'b',
            'n1': 'n',
            'n2': 'n',
            'k': 'k',
            'q': 'q',
            'p': 'p'
        }

        return dict.get(piece)

    @staticmethod
    def dataToFen():
        FEN = []

        for row in reversed(range(len(BoardData.PositionList))):
            num = 0
            for col in range(len(BoardData.PositionList[0])):
                cur = BoardData.PositionList[row][col]

                if cur is None:
                    num += 1
                else:
                    if num != 0:
                        FEN.append(str(num))
                        num = 0
                    FEN.append(BoardData.pieceToFen(cur))
                if col == 7 and num != 0:
                    FEN.append(str(num))
            if row != 0:
                FEN.append('/')

        FEN.append(' w ')

        oneOfFourIsTrue = False
        if BoardData.canWhiteCastle[0] and BoardData.canWhiteCastle[1]:
            oneOfFourIsTrue = True
            FEN.append('K')
        if BoardData.canWhiteCastle[0] and BoardData.canWhiteCastle[2]:
            oneOfFourIsTrue = True
            FEN.append('Q')
        if BoardData.canBlackCastle[0] and BoardData.canBlackCastle[1]:
            oneOfFourIsTrue = True
            FEN.append('k')
        if BoardData.canBlackCastle[0] and BoardData.canBlackCastle[1]:
            oneOfFourIsTrue = True
            FEN.append('q')

        if not oneOfFourIsTrue:
            FEN.append('-')
        FEN.append(' 0 1')

        return ''.join(FEN)

    @staticmethod
    def changePlayer():
        if BoardData.nextMoveWhite:
            BoardData.nextMoveWhite = False
        else:
            BoardData.nextMoveWhite = True

    @staticmethod
    def move(row, col, piece, newRow, newCol, castle=None):

        if piece in BoardData.whiteList:
            forWhite = True
        else:
            forWhite = False

        BoardData.PositionList[row][col] = None

        if piece in ['P', 'p']:
            for i, List in enumerate(BoardData.pieceRegister[piece]):
                if List is not None:
                    if BoardData.pieceRegister[piece][i] == [row, col]:
                        BoardData.pieceRegister[piece][i] = [newRow, newCol]
                        break

            tempPiece = BoardData.PositionList[newRow][newCol]
            BoardData.PositionList[newRow][newCol] = piece
        else:
            BoardData.pieceRegister[piece] = [newRow, newCol]
            tempPiece = BoardData.PositionList[newRow][newCol]
            BoardData.PositionList[newRow][newCol] = piece

            if castle is not None and len(castle) == 2:  # if it is castle then moving rook manually
                if forWhite:  # for white king
                    if castle[1] == 1:
                        BoardData.pieceRegister['R2'] = [0, 5]
                        BoardData.PositionList[0][7] = None
                        BoardData.PositionList[0][5] = 'R2'
                    else:
                        BoardData.pieceRegister['R1'] = [0, 3]
                        BoardData.PositionList[0][0] = None
                        BoardData.PositionList[0][3] = 'R1'
                else:  # for black king
                    if castle[1] == 1:
                        BoardData.pieceRegister['r2'] = [7, 5]
                        BoardData.PositionList[7][7] = None
                        BoardData.PositionList[7][5] = 'r2'
                    else:
                        BoardData.pieceRegister['r1'] = [7, 3]
                        BoardData.PositionList[7][0] = None
                        BoardData.PositionList[7][3] = 'r1'

        # if piece is captured then removing the location of it from pieceRegister
        if tempPiece is not None:
            BoardData.changePoint(tempPiece, True)
            if tempPiece in ['P', 'p']:
                for i, List in enumerate(BoardData.pieceRegister[tempPiece]):
                    if List is not None:
                        if BoardData.pieceRegister[tempPiece][i] == [newRow, newCol]:
                            BoardData.pieceRegister[tempPiece][i] = None
            else:
                BoardData.pieceRegister[tempPiece] = None

        # changing castle variable according to provided move
        if castle is not None:
            if forWhite:
                for i in castle:
                    BoardData.canWhiteCastle[i] = False
            else:
                for i in castle:
                    BoardData.canBlackCastle[i] = False

            # appending castle to movement
            BoardData.movement.append([newRow, newCol, piece, row, col, tempPiece, castle])
        else:
            BoardData.movement.append([newRow, newCol, piece, row, col, tempPiece])

        BoardData.changePlayer()

    @staticmethod
    def undoMove():

        popList = BoardData.movement.pop()

        if len(popList) == 6:
            row, col, piece, newRow, newCol, lastPiece = popList
        else:
            row, col, piece, newRow, newCol, lastPiece, castle = popList

        if piece in BoardData.whiteList:
            forWhite = True
        else:
            forWhite = False

        if piece in ['P', 'p']:
            for i, List in enumerate(BoardData.pieceRegister[piece]):
                if List is not None:
                    if BoardData.pieceRegister[piece][i] == [row, col]:
                        BoardData.pieceRegister[piece][i] = [newRow, newCol]

            BoardData.PositionList[newRow][newCol] = piece
        else:
            BoardData.pieceRegister[piece] = [newRow, newCol]
            BoardData.PositionList[newRow][newCol] = piece

        # setting lastPiece position on PositionList e.g. lastPiece = 'R1' or lastPiece = None
        BoardData.PositionList[row][col] = lastPiece
        if lastPiece is not None:
            if lastPiece in ['P', 'p']:
                if lastPiece in BoardData.pieceRegister:
                    BoardData.pieceRegister[lastPiece].append([row, col])
                else:
                    BoardData.pieceRegister[lastPiece] = [[row, col]]
            else:
                BoardData.pieceRegister[lastPiece] = [row, col]

            BoardData.changePoint(lastPiece, False)

        if 'castle' in locals():
            if forWhite:
                for i in castle:
                    BoardData.canWhiteCastle[i] = True

                if len(castle) == 2:
                    if castle[1] == 1:  # king side rook for white
                        BoardData.pieceRegister['R2'] = [0, 7]
                        BoardData.PositionList[0][7] = 'R2'
                        BoardData.PositionList[0][5] = None
                    else:  # queen side rook for white
                        BoardData.pieceRegister['R1'] = [0, 0]
                        BoardData.PositionList[0][0] = 'R1'
                        BoardData.PositionList[0][3] = None
            else:
                for i in castle:
                    BoardData.canBlackCastle[i] = True

                if len(castle) == 2:
                    if castle[1] == 1:  # king side rook for black
                        BoardData.pieceRegister['r2'] = [7, 7]
                        BoardData.PositionList[7][7] = 'r2'
                        BoardData.PositionList[7][5] = None
                    else:  # queen side rook for black
                        BoardData.pieceRegister['r1'] = [7, 0]
                        BoardData.PositionList[7][0] = 'r1'
                        BoardData.PositionList[7][3] = None

        BoardData.changePlayer()

    @staticmethod
    def horVer(piece, row, col, isWhite):
        if isWhite:
            castle = BoardData.canWhiteCastle
            oppositeList = BoardData.blackList
            if piece == 'R1':
                castleBreak = 1
            else:
                castleBreak = 2
        else:
            castle = BoardData.canBlackCastle
            oppositeList = BoardData.whiteList
            if piece == 'r1':
                castleBreak = 1
            else:
                castleBreak = 2

        ext = 1
        isTrue = [True, True, True, True]
        while ext <= 7:
            for exp1, exp2, index in [
                [row + ext, col, 0],
                [row, col + ext, 1],
                [row - ext, col, 2],
                [row, col - ext, 3]
            ]:
                if isTrue[index] and exp1 in range(8) and exp2 in range(8):
                    if BoardData.PositionList[exp1][exp2] is None:
                        if piece in ['R1', 'r1'] and castle[1] is True:
                            BoardData.availableMoveList.append([row, col, piece, exp1, exp2, [castleBreak]])
                        elif piece in ['R2', 'r2'] and castle[2] is True:
                            BoardData.availableMoveList.append([row, col, piece, exp1, exp2, [castleBreak]])
                        else:
                            BoardData.availableMoveList.append([row, col, piece, exp1, exp2])
                    elif BoardData.PositionList[exp1][exp2] in oppositeList:
                        if piece in ['R1', 'r1'] and castle[1] is True:
                            BoardData.availableMoveList.append([row, col, piece, exp1, exp2, [castleBreak]])
                        elif piece in ['R2', 'r2'] and castle[2] is True:
                            BoardData.availableMoveList.append([row, col, piece, exp1, exp2, [castleBreak]])
                        else:
                            BoardData.availableMoveList.append([row, col, piece, exp1, exp2])
                        isTrue[index] = False
                    else:
                        isTrue[index] = False
            ext += 1

    @staticmethod
    def cross(piece, row, col, isWhite):
        if isWhite:
            oppositeList = BoardData.blackList
        else:
            oppositeList = BoardData.whiteList

        ext = 1
        isTrue = [True, True, True, True]
        while ext <= 7:
            for exp1, exp2, index in [
                [row + ext, col + ext, 0],
                [row - ext, col + ext, 1],
                [row - ext, col - ext, 2],
                [row + ext, col - ext, 3]
            ]:
                if isTrue[index] and exp1 in range(8) and exp2 in range(8):
                    if BoardData.PositionList[exp1][exp2] is None:
                        BoardData.availableMoveList.append([row, col, piece, exp1, exp2])
                    elif BoardData.PositionList[exp1][exp2] in oppositeList:
                        BoardData.availableMoveList.append([row, col, piece, exp1, exp2])
                        isTrue[index] = False
                    else:
                        isTrue[index] = False
            ext += 1

    @staticmethod
    def kingCastling(forWhite, kRow, kCol, king):

        if forWhite:
            if BoardData.canWhiteCastle[0] and BoardData.canWhiteCastle[1]:  # king side castling
                if BoardData.PositionList[0][5] is None and BoardData.PositionList[0][6] is None and \
                        BoardData.PositionList[0][7] == 'R2':
                    # at here, move() king to in-between squares and check are those squares attacked by any piece or not?

                    isValid = BoardData.checkKing(forWhite)  # is king itself in check currently or not?

                    if isValid:
                        BoardData.move(0, 4, 'K', 0, 5, [0])  # is 0,5 position in check or not?
                        isValid = BoardData.checkKing(forWhite)
                        BoardData.undoMove()
                        if isValid:
                            BoardData.availableMoveList.append([kRow, kCol, king, 0, 6, [0, 1]])

            if BoardData.canWhiteCastle[0] and BoardData.canWhiteCastle[2]:  # queen side castling
                if BoardData.PositionList[0][3] is None and BoardData.PositionList[0][2] is None and \
                        BoardData.PositionList[0][1] is None and BoardData.PositionList[0][0] == 'R1':

                    isValid = BoardData.checkKing(forWhite)  # is king itself in check currently or not?

                    if isValid:
                        BoardData.move(0, 4, 'K', 0, 3)  # is 0,3 position in check or not?
                        isValid = BoardData.checkKing(forWhite)
                        BoardData.undoMove()
                        if isValid:
                            BoardData.availableMoveList.append([kRow, kCol, king, 0, 2, [0, 2]])

        else:  # casting for black king
            if BoardData.canBlackCastle[0] and BoardData.canBlackCastle[1]:  # king side castling
                if BoardData.PositionList[7][5] is None and BoardData.PositionList[7][6] is None and \
                        BoardData.PositionList[7][7] == 'r2':
                    # at here move() king to in-between squares and check are those squares attacked by any piece or not?
                    isValid = BoardData.checkKing(forWhite)

                    if isValid:
                        BoardData.move(7, 4, 'k', 7, 5)
                        isValid = BoardData.checkKing(forWhite)
                        BoardData.undoMove()
                        if isValid:
                            if isValid:
                                BoardData.availableMoveList.append([kRow, kCol, king, 7, 6, [0, 1]])
            if BoardData.canBlackCastle[0] and BoardData.canBlackCastle[2]:  # queen side castling
                if BoardData.PositionList[7][3] is None and BoardData.PositionList[7][2] is None and \
                        BoardData.PositionList[7][1] is None and BoardData.PositionList[7][0] == 'r1':

                    isValid = BoardData.checkKing(forWhite)
                    if isValid:
                        BoardData.move(7, 4, 'k', 7, 3)
                        isValid = BoardData.checkKing(forWhite)
                        BoardData.undoMove()
                        if isValid:
                            BoardData.availableMoveList.append([kRow, kCol, king, 7, 2, [0, 2]])

    @staticmethod
    def findPossibleMoves():
        BoardData.availableMoveList.clear()
        if BoardData.nextMoveWhite:
            forWhite = True
            pawnChar = 'P'
            rookChar = 'R'
            kingChar = 'K'
            queenChar = 'Q'
            knightChar = 'N'
            bishopChar = 'B'
            castle = BoardData.canWhiteCastle
            oppositeList = BoardData.blackList
        else:
            forWhite = False
            pawnChar = 'p'
            rookChar = 'r'
            kingChar = 'k'
            queenChar = 'q'
            knightChar = 'n'
            bishopChar = 'b'
            castle = BoardData.canBlackCastle
            oppositeList = BoardData.whiteList

        if pawnChar == 'P':  # for white pawns
            for i, List in enumerate(BoardData.pieceRegister[pawnChar]):  # for all pawns
                if List is not None:
                    # front move for pawn
                    row = List[0]
                    col = List[1]
                    if BoardData.PositionList[row + 1][col] is None:
                        BoardData.availableMoveList.append([row, col, pawnChar, row + 1, col])
                        # two moves for pawn
                        if row == 1 and BoardData.PositionList[row + 2][col] is None:
                            BoardData.availableMoveList.append([row, col, pawnChar, row + 2, col])
                    # cross capturing moves
                    if col - 1 in range(8) and BoardData.PositionList[row + 1][col - 1] in oppositeList:
                        BoardData.availableMoveList.append([row, col, pawnChar, row + 1, col - 1])
                    if col + 1 in range(8) and BoardData.PositionList[row + 1][col + 1] in oppositeList:
                        BoardData.availableMoveList.append([row, col, pawnChar, row + 1, col + 1])

        else:  # for black pawns
            for i, List in enumerate(BoardData.pieceRegister[pawnChar]):  # for all pawns
                if List is not None:
                    row = List[0]
                    col = List[1]
                    if BoardData.PositionList[row - 1][col] is None:
                        BoardData.availableMoveList.append([row, col, pawnChar, row - 1, col])
                        if row == 6 and BoardData.PositionList[row - 2][col] is None:
                            BoardData.availableMoveList.append([row, col, pawnChar, row - 2, col])
                    # cross capturing moves
                    if col - 1 in range(8) and BoardData.PositionList[row - 1][col - 1] in oppositeList:
                        BoardData.availableMoveList.append([row, col, pawnChar, row - 1, col - 1])
                    if col + 1 in range(8) and BoardData.PositionList[row - 1][col + 1] in oppositeList:
                        BoardData.availableMoveList.append([row, col, pawnChar, row - 1, col + 1])

        for key, value in BoardData.pieceRegister.items():  # for rook
            if value is not None and key.startswith(rookChar):
                rook = key
                rRow, rCol = value[0], value[1]
                BoardData.horVer(rook, rRow, rCol, forWhite)

        kRow, kCol = BoardData.pieceRegister[kingChar]  # for king
        # kRow, kCol  = value[0], value[1]  # clockwise starts from top
        for newRow, newCol in [
            [kRow + 1, kCol],
            [kRow + 1, kCol + 1],
            [kRow, kCol + 1],
            [kRow - 1, kCol + 1],
            [kRow - 1, kCol],
            [kRow - 1, kCol - 1],
            [kRow, kCol - 1],
            [kRow + 1, kCol - 1]
        ]:
            if newRow in range(8) and newCol in range(8):
                if BoardData.PositionList[newRow][newCol] is None:
                    if castle[0]:  # boolean value itself
                        BoardData.availableMoveList.append([kRow, kCol, kingChar, newRow, newCol, [0]])
                    else:
                        BoardData.availableMoveList.append([kRow, kCol, kingChar, newRow, newCol])
                elif BoardData.PositionList[newRow][newCol] in oppositeList:
                    if castle[0]:  # boolean value itself
                        BoardData.availableMoveList.append([kRow, kCol, kingChar, newRow, newCol, [0]])
                    else:
                        BoardData.availableMoveList.append([kRow, kCol, kingChar, newRow, newCol])

        BoardData.kingCastling(forWhite, kRow, kCol, kingChar)  # castling move appending

        for key, value in BoardData.pieceRegister.items():  # for knight
            if value is not None and key.startswith(knightChar):
                knight = key
                nRow, nCol = value[0], value[1]  # clockwise starts from top-right
                for newRow, newCol in [
                    [nRow + 2, nCol + 1],
                    [nRow + 1, nCol + 2],
                    [nRow - 1, nCol + 2],
                    [nRow - 2, nCol + 1],
                    [nRow - 2, nCol - 1],
                    [nRow - 1, nCol - 2],
                    [nRow + 1, nCol - 2],
                    [nRow + 2, nCol - 1],
                ]:
                    if newRow in range(8) and newCol in range(8):
                        if BoardData.PositionList[newRow][newCol] is None:
                            BoardData.availableMoveList.append([nRow, nCol, knight, newRow, newCol])
                        elif BoardData.PositionList[newRow][newCol] in oppositeList:
                            BoardData.availableMoveList.append([nRow, nCol, knight, newRow, newCol])

        for key, value in BoardData.pieceRegister.items():  # for bishop
            if value is not None and key.startswith(bishopChar):
                bishop = key
                bRow, bCol = value[0], value[1]
                BoardData.cross(bishop, bRow, bCol, forWhite)

        for key, value in BoardData.pieceRegister.items():  # for queen
            if value is not None and key == queenChar:
                queen = key
                qRow, qCol = value[0], value[1]
                BoardData.horVer(queen, qRow, qCol, forWhite)
                BoardData.cross(queen, qRow, qCol, forWhite)

        BoardData.verifyMoves()
        return BoardData.availableMoveList.copy()

    @staticmethod
    def printMoves():
        for x in BoardData.availableMoveList:
            print(x)

    @staticmethod
    def verifyMoves():
        if BoardData.nextMoveWhite:
            forWhite = True
        else:
            forWhite = False

        illegalMoveIndex = []
        for moveIndex in range(len(BoardData.availableMoveList)):

            BoardData.move(*BoardData.availableMoveList[moveIndex])

            isValid = BoardData.checkKing(forWhite)

            if not isValid:
                illegalMoveIndex.append(moveIndex)

            BoardData.undoMove()

        for index in reversed(illegalMoveIndex):
            BoardData.availableMoveList.pop(index)

    @staticmethod
    def checkKing(forWhite):

        if forWhite:
            oppPawn = 'p'
            oppKing = 'k'
            kRow = BoardData.pieceRegister['K'][0]
            kCol = BoardData.pieceRegister['K'][1]
            oppKnight = ['n1', 'n2']
            horVerList = ['r1', 'r2', 'q']
            crossList = ['b1', 'b2', 'q']
        else:
            oppPawn = 'P'
            oppKing = 'K'
            oppKnight = ['N1', 'N2']
            kRow = BoardData.pieceRegister['k'][0]
            kCol = BoardData.pieceRegister['k'][1]
            horVerList = ['R1', 'R2', 'Q']
            crossList = ['B1', 'B2', 'Q']

        for up in range(kRow + 1, 8):
            if BoardData.PositionList[up][kCol] is None:
                continue
            else:
                if BoardData.PositionList[up][kCol] in horVerList:
                    return False
                else:
                    break

        for down in range(kRow - 1, -1, -1):
            if BoardData.PositionList[down][kCol] is None:
                continue
            else:
                if BoardData.PositionList[down][kCol] in horVerList:
                    return False
                else:
                    break

        for right in range(kCol + 1, 8):
            if BoardData.PositionList[kRow][right] is None:
                continue
            else:
                if BoardData.PositionList[kRow][right] in horVerList:
                    return False
                else:
                    break

        for left in range(kCol - 1, -1, -1):
            if BoardData.PositionList[kRow][left] is None:
                continue
            else:
                if BoardData.PositionList[kRow][left] in horVerList:
                    return False
                else:
                    break

        # topRight
        ext = 1
        while ext <= 7:
            if kRow + ext in range(8) and kCol + ext in range(8):
                if BoardData.PositionList[kRow + ext][kCol + ext] is not None:
                    if BoardData.PositionList[kRow + ext][kCol + ext] in crossList:
                        return False
                    else:
                        break
            else:
                break
            ext += 1

        # bottomRight
        ext = 1
        while ext <= 7:
            if kRow - ext in range(8) and kCol + ext in range(8):
                if BoardData.PositionList[kRow - ext][kCol + ext] is not None:
                    if BoardData.PositionList[kRow - ext][kCol + ext] in crossList:
                        return False
                    else:
                        break
            else:
                break
            ext += 1

        # bottomLeft
        ext = 1
        while ext <= 7:
            if kRow - ext in range(8) and kCol - ext in range(8):
                if BoardData.PositionList[kRow - ext][kCol - ext] is not None:
                    if BoardData.PositionList[kRow - ext][kCol - ext] in crossList:
                        return False
                    else:
                        break
            else:
                break
            ext += 1

        # bottomRight
        ext = 1
        while ext <= 7:
            if kRow + ext in range(8) and kCol - ext in range(8):
                if BoardData.PositionList[kRow + ext][kCol - ext] is not None:
                    if BoardData.PositionList[kRow + ext][kCol - ext] in crossList:
                        return False
                    else:
                        break
            else:
                break
            ext += 1

        # checking oppPawn
        if oppPawn == 'p':
            if kRow + 1 in range(8) and kCol - 1 in range(8):
                if BoardData.PositionList[kRow + 1][kCol - 1] == oppPawn:
                    return False
            if kRow + 1 in range(8) and kCol + 1 in range(8):
                if BoardData.PositionList[kRow + 1][kCol + 1] == oppPawn:
                    return False
        else:
            if kRow - 1 in range(8) and kCol - 1 in range(8):
                if BoardData.PositionList[kRow - 1][kCol - 1] == oppPawn:
                    return False
            if kRow - 1 in range(8) and kCol + 1 in range(8):
                if BoardData.PositionList[kRow - 1][kCol + 1] == oppPawn:
                    return False

        # checking oppKnight
        knightPositions = [
            [kRow + 2, kCol + 1],
            [kRow + 1, kCol + 2],
            [kRow - 1, kCol + 2],
            [kRow - 2, kCol + 1],
            [kRow - 2, kCol - 1],
            [kRow - 1, kCol - 2],
            [kRow + 1, kCol - 2],
            [kRow + 2, kCol - 1]
        ]
        for x, y in knightPositions:
            if x in range(8) and y in range(8):
                if BoardData.PositionList[x][y] in oppKnight:
                    return False

        # checking oppKing for king
        oppKingPositions = [
            [kRow + 1, kCol],
            [kRow + 1, kCol + 1],
            [kRow, kCol + 1],
            [kRow - 1, kCol + 1],
            [kRow - 1, kCol],
            [kRow - 1, kCol - 1],
            [kRow, kCol - 1],
            [kRow + 1, kCol - 1]
        ]
        for x, y in oppKingPositions:
            if x in range(8) and y in range(8):
                if BoardData.PositionList[x][y] == oppKing:
                    return False

        return True

    @staticmethod
    def positionListToPieceRegister():

        # convert positionList to reverse
        BoardData.PositionList.reverse()

        for row in range(len(BoardData.PositionList)):
            for col in range(len(BoardData.PositionList[0])):
                curPiece = BoardData.PositionList[row][col]
                if curPiece is not None:
                    BoardData.changePoint(curPiece, False)
                    if curPiece in ['P', 'p']:
                        if curPiece in BoardData.pieceRegister:
                            BoardData.pieceRegister[curPiece].append([row, col])
                        else:
                            BoardData.pieceRegister[curPiece] = [[row, col]]
                    else:
                        BoardData.pieceRegister[curPiece] = [row, col]

        for x in ['P', 'R1', 'R2', 'B1', 'B2', 'K', 'Q', 'N1', 'N2', 'p', 'r1', 'r2', 'b1', 'b2', 'k', 'q', 'n1', 'n2']:
            if x not in BoardData.pieceRegister:
                if x in ['P', 'p']:
                    BoardData.pieceRegister[x] = []
                else:
                    BoardData.pieceRegister[x] = None

def printStatistics():
    two = 0
    three = 0
    four = 0

    for depth in globalPrunAtDepth:
        if depth == 2:
            two += 1
        elif depth == 3:
            three += 1
        else:
            four += 1

    print("Terminal")
    print(globalTerminalReached)

    print("Number of prun")
    print(globalPrun)

    print("Number of prun-method call")
    print(globalPossibleMovesReached)

    print("Depth 2 Prun")
    print(two)
    print("Depth 3 Prun")
    print(three)
    print("Depth 4 Prun")
    print(four)

def moveByIndex():
    possibleMoves = BoardData.findPossibleMoves()
    for i in range(len(possibleMoves)):
        print(str(i)+" ", end=" ")
        print(possibleMoves[i])
    moveIndex = int(input("Enter move Index:"))
    print(moveIndex)
    BoardData.move(*possibleMoves[moveIndex])

def pruning(alpha, beta, isMaximizer, curDepth, terminal):
    global globalPossibleMovesReached
    global globalTerminalReached
    global globalPrun
    global globalPrunAtDepth

    # display.start(BoardData.dataToFen())
    # time.sleep(0.3)

    globalPossibleMovesReached += 1
    if curDepth == terminal:
        globalTerminalReached += 1
        return BoardData.points

    if isMaximizer:
        bestValue = -1000
        possibleMoveList = BoardData.findPossibleMoves()

        if len(possibleMoveList) == 0:
            if not BoardData.checkKing(isMaximizer):
                return -41              # checkmate
            else:
                return 0                # stalemeate

        for moveIndex in range(len(possibleMoveList)):
            BoardData.move(*possibleMoveList[moveIndex])

            value = pruning(alpha, beta, False, curDepth + 1, terminal)
            if value == 41:
                BoardData.undoMove()
                return 41
            bestValue = max(bestValue, value)
            alpha = max(alpha, bestValue)
            BoardData.undoMove()
            if alpha >= beta:
                globalPrunAtDepth.append(curDepth)
                globalPrun += 1
                break

        return bestValue
    else:
        bestValue = 1000
        possibleMoveList = BoardData.findPossibleMoves()

        if len(possibleMoveList) == 0:
            if not BoardData.checkKing(isMaximizer):
                return 41
            else:
                return 0

        for moveIndex in range(len(possibleMoveList)):
            BoardData.move(*possibleMoveList[moveIndex])

            value = pruning(alpha, beta, True, curDepth + 1, terminal)
            if value == -41:
                BoardData.undoMove()
                return -41
            bestValue = min(bestValue, value)
            beta = min(beta, bestValue)
            BoardData.undoMove()
            if alpha >= beta:
                globalPrunAtDepth.append(curDepth)
                globalPrun += 1
                break

        return bestValue


def findNextMove():
    global globalPossibleMovesReached
    MIN = -100
    MAX = 100
    startDepth = 1
    terminal = 5
    if BoardData.nextMoveWhite:
        bestValue = MIN
        isMaximize = False
    else:
        bestValue = MAX
        isMaximize = True

    possibleMoveList = BoardData.findPossibleMoves()

    lastGlobalPossibleMovesReachedValue = 0
    if len(possibleMoveList) == 0:
        print("No move available!!!")
    else:
        for moveIndex in range(len(possibleMoveList)):

            BoardData.move(*possibleMoveList[moveIndex])
            curMoveValue = pruning(MIN, MAX, isMaximize, startDepth, terminal)
            print(possibleMoveList[moveIndex], end=' ')
            print(curMoveValue, end=' ')
            print(globalPossibleMovesReached-lastGlobalPossibleMovesReachedValue)
            lastGlobalPossibleMovesReachedValue = globalPossibleMovesReached
            if not isMaximize:
                if curMoveValue > bestValue:  # if more than one move has same value as highest then 1st move will be selected
                    bestValue = curMoveValue
                    bestMoveIndex = moveIndex
            elif curMoveValue < bestValue:
                bestValue = curMoveValue
                bestMoveIndex = moveIndex
            BoardData.undoMove()

        BoardData.move(*possibleMoveList[bestMoveIndex])


if __name__ == '__main__':
    BoardData.positionListToPieceRegister()
    display.start(BoardData.dataToFen())
    findNextMove()
    display.start(BoardData.dataToFen())
    findNextMove()
    display.start(BoardData.dataToFen())
    findNextMove()
    display.start(BoardData.dataToFen())
    os.system("pause")

    printStatistics()

    # for i in range(5):
    #     moveByIndex()
    #     display.start(BoardData.dataToFen())
    #     findNextMove()
    #     display.start(BoardData.dataToFen())

    # for i in range(100):
    #     findNextMove()
    #     # BoardData.printData(True, False, False, False)  # List Register Castle Points
    #     display.start(BoardData.dataToFen())
    #     # time.sleep(0.5)

    # make possibleMove for promotion
    # en passant will be so difficult. Not going to implement at this time.
    # horVer and cross method has less code but it isn't efficient. Use 4 four loop searching
    # if multiple moves have same value of pruning(highest), then decrease the terminal for that moves and find again
