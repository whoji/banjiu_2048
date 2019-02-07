import pygame
import random

from pygame.locals import *
from flags import F
# TODO
# from combine import Combiner
# from move import Mover

class Board(object):

    """docstring for Board"""
    def __init__(self):
        self.board =[]
        self.prev_board = []
        self.prev_action = None
        self.total_moves = 0
        self.if_need_to_check_gg = False
        self.if_need_to_check_win = True
        self.if_gg = False
        self.if_win = False

        # for event monitor
        self.if_moved = False
        self.if_merged = False
        self.if_upgraded = False

        # pass to the right_board (board_1)
        self.cancelled = []

        self.init_board()
        print("init board:")
        print(self)

    def __repr__(self):
        for r in self.board:
            print(r)
        return ""

    def init_board(self):
        # initialize the map with all dirt
        self.board = [[0 for w in range(F.map_rows)] 
            for h in range (F.map_cols)]

        # spawn some random blocks
        for _ in range(F.init_board_blocks):
            self.spawn_block()

    def update_board(self, action = "up"):
        # 0. bak the old one
        new_board = [r[:] for r in self.board]

        # 1. move all the blocks
        self.move_all_to_direction(new_board, action)
        self.move_all_to_direction(new_board, action)
        self.move_all_to_direction(new_board, action)
        self.move_all_to_direction(new_board, action)
         # TODO three times? it should depends on the board size

        # 2. combine the blocks
        self.combine_blocks(new_board, action)
        self.move_all_to_direction(new_board, action)

        # 3. check if really updated. if yes update
        if self.check_if_same_board(new_board, self.board):
            return 0

        # 4. spawn another block
          #print("to spawn")
        self.total_moves += 1
        self.prev_action = action
        self.prev_board = self.board
        self.board = new_board
         # print("before spawn "+str(self))
        self.spawn_block()

        # 5. check GG condition
        if self.if_need_to_check_gg:
            if self.check_gg():
                self.if_gg = True
            else:
                self.if_need_to_check_gg = False

        # 6. check win condition
        if self.if_need_to_check_win:
            if self.check_win_condition():
                self.if_win = True
                self.if_need_to_check_win = False

        self.if_moved = True
        return 1

    @staticmethod
    def check_if_same_board(b1, b2):
        for i in range(F.map_rows):
            for j in range(F.map_cols):
                if b1[i][j] != b2[i][j]:
                    return False
        return True

    @staticmethod
    def move_all_to_direction(b, action):
        m = F.map_rows
        n = F.map_cols
        if action == 'up':
            for i in range(1,m):
                for j in range(n):
                    Board.move_block_to_direction(b,i,j,action)
        elif action == 'down':
            for i in reversed(range(m-1)):
                for j in range(n):
                    Board.move_block_to_direction(b,i,j,action)
        elif action == 'right':
            for i in range(m):
                for j in reversed(range(n-1)):
                    Board.move_block_to_direction(b,i,j,action)
        elif action == 'left':
            for i in range(m):
                for j in range(1,n):
                    Board .move_block_to_direction(b,i,j,action)
        else:
            raise Exception("WTF is this action: %s" % str(action))

        return b

    @staticmethod
    def move_block_to_direction(b,i,j,direction):
        assert 0 <= i < F.map_rows
        assert 0 <= j < F.map_rows
    
        if b[i][j] == 0:
            return 0
        else:
            if direction == 'up' and b[i-1][j] == 0:
                b[i-1][j] = b[i][j]
                b[i][j] = 0
                return 1
            elif direction == 'down' and b[i+1][j] == 0:
                b[i+1][j] = b[i][j]
                b[i][j] = 0
                return 1
            elif direction == 'left' and b[i][j-1] == 0:
                b[i][j-1] = b[i][j]
                b[i][j] = 0
                return 1
            elif direction == 'right' and b[i][j+1] == 0:
                b[i][j+1] = b[i][j]
                b[i][j] = 0
                return 1
            else:
                return 0 

    #@staticmethod
    def combine_blocks(self, b, action = 'up'):
        m = F.map_rows
        n = F.map_cols
        if action == 'up':
            for i in range(1,m):
                for j in range(n):
                    if self.if_block_mergable(b[i][j],b[i-1][j]):
                        #b[i-1][j] += b[i][j]
                        #b[i][j] = 0
                        self.merge_block(b, (i,j), (i-1,j) )
        elif action == 'down':
            for i in reversed(range(m-1)):
                for j in range(n):
                    if self.if_block_mergable(b[i][j],b[i+1][j]):
                        #b[i+1][j] += b[i][j]
                        #b[i][j] = 0                    
                        self.merge_block(b, (i,j), (i+1,j) )
        elif action == 'right':
            for i in range(m):
                for j in reversed(range(n-1)):
                    if self.if_block_mergable(b[i][j],b[i][j+1]):
                        #b[i][j+1] += b[i][j]
                        #b[i][j] = 0
                        self.merge_block(b, (i,j), (i,j+1) )
        elif action == 'left':
            for i in range(m):
                for j in range(1,n):
                    if self.if_block_mergable(b[i][j],b[i][j-1]):
                        #b[i][j-1] += b[i][j]
                        #b[i][j] = 0
                        self.merge_block(b, (i,j), (i,j-1) )                        
        else:
            raise Exception("WTF is this action: %s" % str(action))

        return b

    #@staticmethod
    def if_block_mergable(self, a,b):
        '''
        a: from
        b: to
        '''
        if a == b and a != 0:
            return True
        elif a == -1*b and a !=0:
            return True
        else:
            return False

    #@staticmethod
    def merge_block(self, b, from_pos, to_pos):
        temp_v = b[to_pos[0]][to_pos[1]]
        b[to_pos[0]][to_pos[1]] += b[from_pos[0]][from_pos[1]]
        b[from_pos[0]][from_pos[1]] = 0
        self.if_merged = True
        if b[to_pos[0]][to_pos[1]] == 0:
            self.cancelled.append(abs(temp_v))
            return 2
        else:
            return 1

    def add_to_board(self, pos, obj_type):
        self.board[pos[0]][pos[1]] = obj_type

    def remove_from_board(self, pos, obj_type):
        self.board[pos[0]][pos[1]] = None

    def spawn_block(self):
        valid_pos_candidates = self.get_valid_spawn_pos()
        #print(valid_pos_candidates)
        if len(valid_pos_candidates):
            self.if_need_to_check_gg = True
        spawn_pos = random.choice(valid_pos_candidates)
        spawn_type = random.choice(F.spawn_blocks)
        self.add_to_board(spawn_pos, spawn_type)
        return 1

    def get_valid_spawn_pos(self):
        m = F.map_rows
        n = F.map_cols
        return [(i,j) for i in range(m) for j in range(n) 
            if self.board[i][j] == 0 and (i == 0 or 
                j == 0 or i == m-1 or j == n-1)]

    def check_gg(self):
        # first backup sound monitor
        backup_sound_event_monitor = (self.if_moved, self.if_moved, self.if_upgraded)
        temp_board = [row[:] for row in self.board]
        for action in ['up','down','left','right']:
            Board.move_all_to_direction(temp_board, action)
            self.combine_blocks(temp_board, action)
            if not Board.check_if_same_board(self.board, temp_board):
                # restore from backup
                self.if_moved, self.if_moved, self.if_upgraded = backup_sound_event_monitor
                return False
        # restore from backup
        self.if_moved, self.if_moved, self.if_upgraded = backup_sound_event_monitor
        return True

    def check_win_condition(self):
        for r in self.board:
            if F.win_condition_block in r:
                return True
        return False

    def resest_event_monitor(self):
        self.if_moved = False
        self.if_merged = False
        self.if_upgraded = False
        self.cancelled = []

    @staticmethod
    def print_both_boards(b1, b2):
        n = len(b1)
        for i in range(n):
            r1 = [str(e).rjust(4) for e in b1[i]]
            r2 = [str(e).rjust(4) for e in b2[i]]
            r1 = "[" + "".join(r1) + "]"
            r2 = "[" + "".join(r2) + "]"
            print(r1, end="")
            print("\t", end="")
            print(r2)


class RightBoard(Board):
    """docstring for NewBoard"""
    def __init__(self):
        super(RightBoard, self).__init__()
        self.is_empty = True

    def spawn_block(self):
        print("xx")
        for b in self.cancelled_list:
            print("spawning b....")
            self.spawn_one_block(b)

    def spawn_one_block(self, spawn_type=1):
        valid_pos_candidates = self.get_valid_spawn_pos()
        #print(valid_pos_candidates)
        if len(valid_pos_candidates):
            self.if_need_to_check_gg = True
        spawn_pos = random.choice(valid_pos_candidates)
        self.add_to_board(spawn_pos, spawn_type)
        self.is_empty = False
        return 1        
        
    def init_board(self):
        # initialize the map with all dirt
        self.board = [[0 for w in range(F.map_rows)] 
            for h in range (F.map_cols)]

    def check_if_same_board(self, b1, b2):
        # start: added this handle the exception at the start of the board.
        if self.is_empty or len(self.cancelled_list) > 0:
            return False
        # end
        for i in range(F.map_rows):
            for j in range(F.map_cols):
                if b1[i][j] != b2[i][j]:
                    return False
        return True