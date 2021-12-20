def checkKing(kRow, kCol, PositionList, horVerList, crossList, oppPawn, oppKnight):

    for up in range(kRow + 1, 8):
        if PositionList[up][kCol] is None:
            continue
        else:
            if PositionList[up][kCol] in horVerList:
                return False
            else:
                break

    for down in range(kRow - 1, -1, -1):
        if PositionList[down][kCol] is None:
            continue
        else:
            if PositionList[down][kCol] in horVerList:
                return False
            else:
                break

    for right in range(kCol + 1, 8):
        if PositionList[kRow][right] is None:
            continue
        else:
            if PositionList[kRow][right] in horVerList:
                return False
            else:
                break

    for left in range(kCol - 1, -1, -1):
        if PositionList[kRow][left] is None:
            continue
        else:
            if PositionList[kRow][left] in horVerList:
                return False
            else:
                break

    # topRight
    ext = 1
    while ext <= 7:
        if kRow+ext in range(8) and kCol+ext in range(8):
            if PositionList[kRow+ext][kCol+ext] is not None:
                if PositionList[kRow+ext][kCol+ext] in crossList:
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
            if PositionList[kRow - ext][kCol + ext] is not None:
                if PositionList[kRow - ext][kCol + ext] in crossList:
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
            if PositionList[kRow - ext][kCol - ext] is not None:
                if PositionList[kRow - ext][kCol - ext] in crossList:
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
            if PositionList[kRow + ext][kCol - ext] is not None:
                if PositionList[kRow + ext][kCol - ext] in crossList:
                    return False
                else:
                    break
        else:
            break
        ext += 1

    # checking pawn for whiteKing
    if oppPawn == 'p':
        if kRow+1 in range(8) and kCol-1 in range(8):
            if PositionList[kRow+1][kCol-1] == oppPawn:
                return False
        if kRow+1 in range(8) and kCol+1 in range(8):
            if PositionList[kRow+1][kCol+1] == oppPawn:
                return False
    else:
        if kRow-1 in range(8) and kCol-1 in range(8):
            if PositionList[kRow-1][kCol-1] == oppPawn:
                return False
        if kRow-1 in range(8) and kCol+1 in range(8):
            if PositionList[kRow-1][kCol+1] == oppPawn:
                return False

    # checking knight for whiteKing
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
    if oppKnight[0] == 'n1':
        for x, y in knightPositions:
            if x in range(8) and y in range(8):
                if PositionList[x][y] in oppKnight:
                    return False

    return True
