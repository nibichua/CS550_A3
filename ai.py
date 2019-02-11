'''
Shawn Nehemiah Chua
CS550-Assignment 3
817662151
ai.py
'''
"""
ai - search & strategy module

implement a concrete Strategy class and AlphaBetaSearch
"""

from copy import deepcopy
import abstractstrategy

class Strategy(abstractstrategy.Strategy):
    def __init__(self, player, game, maxplies):
        self.player = player
        self.game = game
        self.maxplies = maxplies
        super(Strategy,self).__init__(self.player, self.game, self.maxplies)
    
    """Determining the utility in different ways""" 
    def utility(self, board_state):
        #edges tiles
        edges = [[0,1],[0,3],[0,5],[0,7],[1,0],[3,0],[5,0],[2,7],[4,7],[6,7],[7,0],[7,2],[7,4],[7,6]]
        temp = deepcopy(board_state)
        #update pawn and king count
        temp.update_counts()
        utility = 0
        """Utility - Number of pawns and kings"""
        num_P = temp.get_pawnsN()[1] - temp.get_pawnsN()[0]
        #If the opponent has more pawns
        if temp.get_pawnsN()[0] >= temp.get_pawnsN()[1]: 
            utility += num_P*3
        else:
            utility -= num_P*3
        num_K = temp.get_kingsN()[1] - temp.get_kingsN()[0]
        #If the opponent has more kings
        if temp.get_kingsN()[0] >= temp.get_kingsN()[1]:
            utility += num_K*5
        else:
            utility -= num_K*5
        """Utility - Distance to king"""       
        for r in range (8):
            for c in range (8):
                if self.maxplayer is temp.get(r,c):
                    if board_state.disttoking(self.player,r) == 1:
                        utility += 4
                    elif board_state.disttoking(self.player,r) == 2:
                        utility += 3
                elif self.minplayer is temp.get(r,c):
                    if board_state.disttoking(self.minplayer,r) == 1:
                        utility -= 5
                    elif board_state.disttoking(self.minplayer,r) == 2:
                        utility -= 4
        """Utility - based on edges"""
        for r in range (8):
            for c in range (8):
                #Edges gives an advantage in the game        
                if self.maxplayer is temp.get(r,c):
                    if edges.__contains__([r,c]):
                        utility += 4
                elif self.minplayer is temp.get(r,c):
                    if edges.__contains__([r,c]):
                        utility -= 6            
        """Utility - Actions of the ai, if got captured or not"""
        for player in temp.get_actions(self.maxplayer): 
            if len(player[1]) == 3: #player captures opponent
                cappiece = temp.get(player[1][2][0], player[1][2][1])
                if temp.ispawn(cappiece):
                    utility += 5
                elif temp.isking(cappiece):
                    utility += 10
            nextboard = temp.move(player)
            #look at board as a result of our moves
            #determine if the opponent can capture a piece
            for opponent in nextboard.get_actions(self.minplayer):
                if len(opponent) == 3: #indicates multiple capture
                    utility -= 20
        return utility
    
    
    def play(self, board, hints=True):
        board.update_counts()
        if board.is_terminal()[0]:
            return (board,0)
        s = Strategy(self.player,self.game,self.maxplies)
    
        temp= AlphaBetaSearch(s,self.maxplayer,self.minplayer,maxplies=self.maxplies)
        v = temp.alphabeta(board,self.maxplies)
        action = board.move(v[1])
        return (action,v[1])
        
class AlphaBetaSearch:
    def __init__(self, strategy, maxplayer, minplayer, maxplies = 3, verbose = False):
        self.strategy = strategy
        self.maxplayer = maxplayer
        self.minplayer = minplayer
        
    def alphabeta(self, state, maxplies):
        #alpha is -inf beta is inf
        v = self.max_value(state,float('-inf'),float('inf'), maxplies, [])
        print (v)
        return v #where v is a tuple of(utility, action)
    
    def max_value(self, state, alpha, beta, plies, action):
        new_action = action
        if state.is_terminal()[0] or plies <= 0:
            v = self.strategy.utility(state)
        else:
            v = float('-inf')
            for action in state.get_actions(self.maxplayer):
                new_action = action   
                new_plies = plies - 1             
                v = max(v, self.min_value(state.move(action), alpha, beta, new_plies, new_action)[0])
                if isinstance(v,int) or isinstance(v,float):
                    if v >= beta:
                        break
                    else:
                        alpha = max(alpha,v)
                else:
                    if v[0] >= beta:
                        break
                    else:
                        alpha = max(alpha, v[0])
        return (v, new_action)
    
    def min_value(self, state, alpha, beta, plies, action):
        new_action = action
        if state.is_terminal()[0] or plies <= 0:
            v = self.strategy.utility(state)
        else:
            v = float('inf')
            for action in state.get_actions(self.minplayer):
                new_action = action    
                new_plies = plies - 1            
                v = min(v, self.max_value(state.move(action), alpha, beta, new_plies, new_action)[0])
                if isinstance(v,int) or isinstance(v,float):
                    if v <= alpha:
                        break
                    else:
                        beta = min(beta,v)
                else:
                    if v[0] <= alpha:
                        break
                    else:
                        beta = min(beta, v[0])
        return (v, new_action)
