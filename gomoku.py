import random
import json
BOARD_SIZE=20
MINIMAX_INFINITY=999
MAX_DEPTH=6
class GomokuPos:
    def __init__(self, x=-1, y=-1,threatening=0):
        self.x = x
        self.y = y
        self.threatening = threatening

    def serialize(self):
        return json.dumps({'x': self.x, 'y': self.y, 'threatening': self.threatening})
    @classmethod
    def deserialize(cls, data):
        data=json.loads(data)
        return cls(x=data['x'],y=data['y'],threatening=data['threatening'])
    def valid_pos(self):
        return 0 <=self.x<BOARD_SIZE and 0 <=self.y < BOARD_SIZE
    @staticmethod
    def distance_between(pos_a,pos_b):
        x1,y1=pos_a.x,pos_a.y
        x2,y2=pos_b.x,pos_b.y   
        distance=((x2-x1)**2+(y2-y1)**2)**0.5
        return distance
    def to_standard_pos(self):
        return self.x+1,chr(65+self.y)
    @staticmethod
    def to_gomoku_pos(row_number,col_letter):
        return GomokuPos(row_number-1,ord(col_letter)-ord('A'))
    def __eq__(self,other):
        return (self.x,self.y)==(other.x,other.y) 
    def __hash__(self):
        return hash((self.x,self.y))
    def __str__(self):
        return hash((self.x,self.y))
class Gomoku:
    def __init__(self,other=None):
        if other is None:
            self.board= [['N' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
            self.active_turn='X'
        else:
            self.board=[row[:]for row in other.board]
            self.active_turn=other.active_turn

    def serialize(self):
        return json.dumps({
            'board': self.board, 
        'active_turn': self.active_turn,
        })
    @classmethod
    def deserialize(cls, json_str):
        data=json.loads(json_str)
        instance=cls()
        instance.board=data['board']
        instance.active_turn=data['active_turn']
        return instance
    def win(self):
        def check_sequence(seq):
            for i in range(len(seq)-4):
                if seq[i:i+5]==['X']*5:
                    return 'X'
                elif seq[i:i+5]==['O']*5:
                    return 'O'
            return None
        
        for i in range(BOARD_SIZE):
            row_winner=check_sequence(self.board[i])
            if row_winner:
                return row_winner
            column=[self.board[j][i] for j in range(BOARD_SIZE)]
            column_winner=check_sequence(column)
            if column_winner:
                return column_winner
        for i in range(BOARD_SIZE-4):
            for j in range(BOARD_SIZE):
                if j<=BOARD_SIZE-5:
                   diag1=[self.board[i+k][j+k]for k in range(5)]
                   diag1_winner=check_sequence(diag1)
                   if diag1_winner:
                       return diag1_winner
                if j>=4:
                   diag2=[self.board[i+k][j-k] for k in range(5)]
                   diag2_winner=check_sequence(diag2)
                   if diag2_winner:
                       return diag2_winner
        if all(cell!='N' for row in self.board for cell in row):
            return 'T'
        return 'N'
    def over(self):
            return self.win()!='N'
    def move(self,pos):
            if self.board[pos.x][pos.y]=='N':
                self.board[pos.x][pos.y]=self.active_turn
                self.active_turn='O' if self.active_turn=='X' else 'X'
            else:
                raise ValueError("Invalid move: position already occupied")
    def have_occupied(self,pos):
        return self.board[pos.x][pos.y]!='N'
    def get_new_state(self,pos):
        new_state= Gomoku(self)
        new_state.move
        return new_state      
    def get_threatening_positions(self,opponent):
        me='X' if opponent=='O' else 'O'
        threatening_patterns = ["{1}{0}{0}{0}{0}N".format(opponent, me), "N{0}{0}{0}{0}{1}".format(opponent, me), "{0}{0}{0}{0}N".format(opponent, me), "N{0}{0}{0}{0}".format(opponent, me), "{0}{0}{0}N{0}".format(opponent), "{0}N{0}{0}{0}".format(opponent), "{0}{0}N{0}{0}".format(opponent), \
                    "N{0}N{0}{0}N".format(opponent), "N{0}{0}N{0}N".format(opponent), "N{0}{0}{0}N".format(opponent), "{1}N{0}{0}{0}NN".format(opponent, me), "NN{0}{0}{0}N{1}".format(opponent, me), "{1}{0}{0}{0}NN".format(opponent, me), "NN{0}{0}{0}{1}".format(opponent, me), "{0}N{0}N{0}".format(opponent),\
                        "N{0}{0}NN".format(opponent), "NN{0}{0}N".format(opponent), "N{0}N{0}N".format(opponent)]
        EXTRA_THREATENING_PATTERNS=0.5