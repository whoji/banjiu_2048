import pygame
import random

from pygame.locals import *
from flags import F

class Block():
    def __init__(self, x, y, val, dest_i, dest_j, if_disappear):
        self.x = x
        self.y = y
        self.val = val
        self.dest_i = dest_i
        self.dest_j = dest_j
        self.if_disappear = if_disappear
        self.speed_x, self.speed_y = self.get_speed()

    def get_speed(self):
        #import pdb; pdb.set_trace()
        #print("[%d,%d] to ..." % (self.x,self.y))
        print("[%d,%d] to [%d,%d]" % (self.x,self.y,self.dest_i,self.dest_j))
        speed_x = (self.dest_i - self.x) * 1.0 / F.move_frame
        speed_y = (self.dest_j - self.y) * 1.0 / F.move_frame
        return speed_x, speed_y

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def __repr__(self):
        return "%d@(%d,%d)" % (self.val, self.x, self.y)

class Mover(object):
    """docstring for Mover"""
    def __init__(self, b, action):
        self.board = [r[:] for r in b]
        self.action = action
        self.total_moving_frames = F.move_frame
        self.remain_moving_frames = self.total_moving_frames
        self.blocks = self.get_all_blocks_destination(self.board, self.action)

    def render(self, DISPLAYSUR):
        pass

    def move_all(self):
        assert self.remain_moving_frames > 0
        m = F.map_rows
        n = F.map_cols
        for i in range(m):
            for j in range(n):
                if isinstance(self.blocks[i][j], Block):
                    self.blocks[i][j].move()
        self.remain_moving_frames -= 1

    def get_all_blocks_destination(self, b, action):
        m = F.map_rows
        n = F.map_cols
        dest = [[0 for w in range(F.map_rows)] for h in range (F.map_cols)]
        if action == 'up':
            for i in range(m):
                for j in range(n):
                    dest_i, dest_j, if_disappear = self.get_block_destination(b,i,j,action)
                    if dest_i is None: continue
                    dest[i][j] = Block(i,j,b[i][j],dest_i, dest_j, if_disappear)
                    v = b[i][j]
                    b[i][j] = 0
                    b[dest_i][dest_j] = v
        elif action == 'down':
            for i in reversed(range(m)):
                for j in range(n):
                    dest_i, dest_j, if_disappear = self.get_block_destination(b,i,j,action)
                    if dest_i is None: continue
                    dest[i][j] = Block(i,j,b[i][j],dest_i, dest_j, if_disappear)
                    v = b[i][j]
                    b[i][j] = 0
                    b[dest_i][dest_j] = v
        elif action == 'right':
            for i in range(m):
                for j in reversed(range(n)):
                    dest_i, dest_j, if_disappear = self.get_block_destination(b,i,j,action)
                    if dest_i is None: continue
                    dest[i][j] = Block(i,j,b[i][j],dest_i, dest_j, if_disappear)
                    v = b[i][j]
                    b[i][j] = 0
                    b[dest_i][dest_j] = v
        elif action == 'left':
            for i in range(m):
                for j in range(n):
                    dest_i, dest_j, if_disappear = self.get_block_destination(b,i,j,action)
                    if dest_i is None: continue                    
                    dest[i][j] = Block(i,j,b[i][j],dest_i, dest_j, if_disappear)
                    v = b[i][j]
                    b[i][j] = 0
                    b[dest_i][dest_j] = v
        else:
            raise Exception("WTF is this action: %s" % str(action))

        return dest

    def get_block_destination(self, b, i, j, action):
        '''
        return: dest_i
        return: dest_j
        return: if_disappear
        '''
        assert 0 <= i < F.map_rows
        assert 0 <= j < F.map_rows
    
        if b[i][j] == 0:
            return None, None, None
        else:
            v = b[i][j]
            if_disappear = False

            if action == 'up':
                while i >= 1:
                    if b[i-1][j] == 0: 
                        if_disappear = False
                        i -= 1
                    elif abs(b[i-1][j]) == abs(v):
                        if_disappear = True
                        i -= 1
                        break
                    else:
                        return i, j, False
                return i, j, if_disappear

            elif action == 'down':
                while i < F.map_rows - 1:
                    if b[i+1][j] == 0: 
                        if_disappear = False
                        i += 1
                    elif abs(b[i+1][j]) == abs(v):
                        if_disappear = True
                        i += 1
                        break
                    else:
                        return i, j, False
                return i, j, if_disappear

            elif action == 'left':
                while j >= 1:
                    if b[i][j-1] == 0: 
                        if_disappear = False
                        j -= 1
                    elif  abs(b[i][j-1]) ==  abs(v):
                        if_disappear = True
                        j -= 1
                        break
                    else:
                        return i, j, False
                return i, j, if_disappear

            elif action == 'right':
                while j < F.map_cols - 1:
                    if b[i][j+1] == 0: 
                        if_disappear = False
                        j += 1
                    elif  abs(b[i][j+1]) ==  abs(v):
                        if_disappear = True
                        j += 1
                        break
                    else:
                        return i, j, False
                return i, j, if_disappear

            else:
                raise Exception("invalid actoin.")


    def get_coordinates(self):
        pass

    @staticmethod
    def center_text(text_obj, moving_tile_pos):
        """
        return the postion (x,y) for the centered text, (center relative to block/tile)
        """
        x_adj = int((F.tile_size - text_obj.get_size()[0])/2)
        y_adj = int((F.tile_size - text_obj.get_size()[1])/2)
        new_pos = (moving_tile_pos[0]+x_adj, moving_tile_pos[1]+y_adj)
        return new_pos



