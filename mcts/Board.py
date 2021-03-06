class Board(object):
    DEFAULT_BOARD_SIZE = 8
    IN_PROGRESS        = -1
    EMPTY              = 0
    DRAW               = 0
    AVAILABLE_ONE_MOVES    = [[-1,0] , [0,1], [1,0], [0,-1]]
    AVAILABLE_CROSS_MOVES  = [[-2,0] , [0,2], [2,0], [0,-2]]

    def __init__(self):
        # Create the initialized state and initialized board
        # Example
        # boardValues = [[0,1,1,0,0,0,0,0],
        #                [0,1,1,0,0,2,2,2],
        #                [0,1,1,0,0,2,2,2],
        #                [0,1,1,0,0,2,2,2],
        #                [0,1,1,0,0,2,2,2],
        #                [0,1,1,0,0,2,2,2],
        #                [0,1,1,0,0,2,2,2],
        #                [0,1,1,0,0,2,2,2]]
        self.boardValues    = []
        self.blackMovesNum  = 0
        self.whiteMovesNum  = 0

    def moveOneStep(self,playerNo,oneMove):
        """
        @param      playerNo : 1 代表黑色 2 代表白色   oneMove: 一個 list 從 a 移動到 b  [a,b]
        @return     如果是一個合法的移動，會移動該步並回傳True，如果是一個不合法的移動，不移動該步並回傳False
        """
        #oneMove = oneMove.astype(int)
        opponent = 3 - playerNo
        initialRow = oneMove[0][0]
        initialCol = oneMove[0][1]
        finalRow   = oneMove[1][0]
        finalCol   = oneMove[1][1]
        if self.boardValues[initialRow][initialCol] == playerNo and self.boardValues[finalRow][finalCol] == self.EMPTY:
            if [initialRow-finalRow, initialCol-finalCol] in self.AVAILABLE_ONE_MOVES:
                # 上下左右動一步
                self.boardValues[initialRow][initialCol] = self.EMPTY
                self.boardValues[finalRow][finalCol] = playerNo
                return True
            elif [initialRow-finalRow, initialCol-finalCol] in self.AVAILABLE_CROSS_MOVES and \
                self.boardValues[initialRow - int((initialRow-finalRow)/2) ][ initialCol - int((initialCol-finalCol)/2)] == opponent:
                # 跨一步吃掉對手
                self.boardValues[initialRow][initialCol] = self.EMPTY
                self.boardValues[initialRow - int((initialRow-finalRow)/2) ][ initialCol - int((initialCol-finalCol)/2)] = self.EMPTY
                self.boardValues[finalRow][finalCol] = playerNo
                return True
            elif [initialRow-finalRow, initialCol-finalCol] in self.AVAILABLE_CROSS_MOVES and \
                self.boardValues[initialRow - int((initialRow-finalRow)/2) ][ initialCol - int((initialCol-finalCol)/2)] == playerNo:
                # 跨一步自己
                self.boardValues[initialRow][initialCol] = self.EMPTY
                self.boardValues[finalRow][finalCol] = playerNo
                return True
            return False
        
        return False         

    def performMove(self,playerNo, moveList):
        """
        @param    playerNo : 1 代表黑色 2 代表白色 moveList: 從第一個位置移動到最後一個位置的一連串位置
        @return   如果這一連串的移動是合法的話就成功移動並且return True，如果這是一個不合法的移動，就會return False
        """
        # Example 
        # player     : 1 
        # moveList   : [[3,4] , [3,6] , [3,8]]
        #print( moveList)
        tempBoardValues = self.boardValues
        legal = True
        if len(moveList) == 0:
            return legal
        
        for index in range(len(moveList)-1):
            legal = self.moveOneStep(playerNo,[moveList[index],moveList[index+1]])
            if legal == False:
                break
        
        if legal:
            if playerNo == 1:
                self.blackMovesNum += 1
            else:
                self.whiteMovesNum += 1
            return True
        else:
            # 還原
            self.boardValues = tempBoardValues
            return False

    def getBoardValues(self):
        return self.boardValues
    
    def setBoardValues(self,boardValues):
        self.boardValues = boardValues

    def checkInRegion(self):
        """
        @return 
        黑棋全部都在區域內且白棋都被吃光 1 ， 黑棋全部都在區域內且白棋還有  2 ， 白棋都在區域內且黑棋被吃光 3 ，白棋都在區域內且黑棋還有 4 ， 黑或白棋都沒全到區域內 -1 
        如果黑棋全部都被吃掉，白棋會繼續玩到直到全部白子皆到達目標區域or完成200回合才會結束遊戲 (問助教的)
        """
        # check for black
        blackwin = 0
        blackNum = 0
        whitewin = 0
        whiteNum = 0
        for i in range(8):
            for j in range(8):
                if self.boardValues[i][j] == 1 and ( j != 6 and j != 7 ):
                    blackwin = -1
                    break
                if ( j == 6 or j == 7) and self.boardValues[i][j] == 1:
                    blackNum += 1
            
            if blackwin == -1:
                break
        
        for i in range(8):
            for j in range(8):
                if self.boardValues[i][j] == 2 and ( j != 0 and j != 1):
                    whitewin = -1
                    break
                if ( j == 0 or j == 1) and self.boardValues[i][j] == 2:
                    whiteNum += 1
            if whitewin == -1:
                break
        
        if blackwin == 0:
            return 1,blackNum,whiteNum
        if whitewin == 0:
            return 2,blackNum,whiteNum

        return -1,blackNum,whiteNum
                    
    def checkStatus(self,step):
        """
        @param
        @return  如果是黑子獲勝 回傳 1 如果是白子獲勝 回傳 2 如果還在進行中 回傳 IN_PROGRESS (-1) 平手 DRAW (0)
        """
        if self.whiteMovesNum >= step and self.blackMovesNum >= step :    
            allInRegion,blackNum,whiteNum = self.checkInRegion()
            if allInRegion != -1:
                if blackNum > whiteNum:
                    return 1
                elif blackNum < whiteNum:
                    return 2
                else:
                    return self.DRAW
        return -1
    


    
    

    