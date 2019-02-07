import math
import pygame
from pygame.locals import *

class Flags(object):
    """docstring for Flags"""

    def __init__(self):
        # game general
        self.game_name = 'Banjiu 2048'
        self.game_ver = '0.0.1.apha.190203'
        self.proj_path = '/home/whoji/Desktop/ILC_2019/bw2048/'
        self.save_path = './save/'
        self.debug_mod = True
        self.game_fps = 60

        # colors
        self.grey1 = (28,32,38)
        self.grey2 = (14,22,14)
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.red = (250,50,50)
        self.blue = (50,50,250)
        self.blue2 = (2,39,99) # dark blue
        self.green = (50, 200, 100)
        self.yellow = (200,200,50)
        self.orange = (255, 153, 58)
        self.block_text_fg = self.white
        self.block_text_bg = None #self.black

        # size and pos conf (general and menu)
        self.window_w = 800
        self.window_h = 600
        self.tile_size = 70
        self.map_rows = 4
        self.map_cols = 4
        self.status_bar_size = 60
        self.text_offset_x = 10
        self.text_offset_y = 10
        self.text_offset = (10,10)
        self.menu_rect = (100, 100,
            self.map_cols*self.tile_size-100, self.map_rows*self.tile_size-100)
        self.menu_size = 200
        self.center_x  = round(self.window_w / 2)
        self.center_y  = round((self.window_h) / 2)
        self.blink_title = False
        self.blink_tile_fps = 20 # every 10 frames will change color

        # [Board] size and pos conf
        self.board_color = self.grey1
        self.board_frame_color = self.orange
        self.board_frame_px = 2
         #self.board_rect = (self.board_offset_x, self.board_offset_y,
         #    self.map_cols*self.tile_size, self.map_rows*self.tile_size)
         # self.board_offset_x, self.board_offset_y = self.__calculate_board_offset()
        self.board_rect_0, self.board_rect_1 = self.__calculate_two_board_rect()
        self.board_outer_rect_0 = (self.board_rect_0[0]-self.board_frame_px,
            self.board_rect_0[1]-self.board_frame_px, 
            self.board_rect_0[2]+2*self.board_frame_px, 
            self.board_rect_0[3]+2*self.board_frame_px)
        self.board_outer_rect_1 = (self.board_rect_1[0]-self.board_frame_px,
            self.board_rect_1[1]-self.board_frame_px, 
            self.board_rect_1[2]+2*self.board_frame_px,
            self.board_rect_1[3]+2*self.board_frame_px)
        self.board_origin_0 = self.board_rect_0[:2]
        self.board_origin_1 = self.board_rect_1[:2]
        self.init_board_blocks = 2
        self.block_font_center = True
        self.block_font_size = int(self.tile_size / 2)
        self.block_font_sizes = [int(self.tile_size / 2), # for 1 digit
            int(self.tile_size / 3), # for 2 digit
            int(self.tile_size / 4), # for 3 digit
            int(self.tile_size / 5) # for 4 digit
        ]
        self.block_font_size_perc = (1, 1, 0.9, 0.8, 0.5, 0.5, 0.5) 

        # status bar
        # self.display_castle = True
        # self.castle_icon_px  = 30
        # self.castle_icon_gap = 1
        # self.big_castle_icon = True
        # if self.big_castle_icon:
        #     self.castle_icon_px = 50
        #     self.castle_icon_gap = 3
        #     self.castle_list = [1,4,16, 64,256,1024,4096,16384]
        
        # game flow control
        self.win_condition_block = self.__calculate_win_block()
        #self.milestone_mode = True
        #self.milestone = [2**i for i in range(16)]

        # block moving effect
        self.if_movable = True
        self.move_frame = 10 # frames to finish the move

        # load texture
        #self.__get_textures()
        #self.__resize_texture()

        # load tile colors
        self.__get_tile_colors()

        # load sound effects
        #self.__get_sound()

        # run self check
        #self.__self_check():

    def __self_check():
        raise NotImplementedError
        #raise Exception("Bad set up logic")

    def __calculate_win_block(self):
        ret = 2 ** (int(math.sqrt(self.map_rows * self.map_cols))*3 - 1)
        ret = 2048

        if self.debug_mod:
            if self.map_rows == 3:
                ret = 8
            if self.map_rows == 4:
                ret = 16

        return ret

    def __calculate_board_offset(self):
        offset_x = round(self.window_w / 2 - self.map_cols * self.tile_size / 2)
        offset_y = round((self.window_h - self.status_bar_size) / 2 - 
            self.map_rows * self.tile_size / 2)
        return offset_x, offset_y

    def __calculate_two_board_rect(self):
        offset_x0 = round(self.window_w / 4     - self.map_cols * self.tile_size / 2)
        offset_x1 = round(self.window_w / 4 * 3 - self.map_cols * self.tile_size / 2)
        offset_y0 = round((self.window_h - self.status_bar_size) / 2 - 
            self.map_rows * self.tile_size / 2)
        offset_y1 = offset_y0
        l = self.map_cols * self.tile_size
        return (offset_x0, offset_y0, l, l), (offset_x1, offset_y1, l, l)

    def __get_tile_colors(self):
        self.tile_color = {
            0   : self.white,
            1   : (250,120,120),
            2   : (250,110,110),
            4   : (250,100,100),
            8   : (250,90,90),
            16  : (250,80,80),
            32  : (250,70,70),
            64  : (250,60,60),
            128 : (250,50,50),
            256 : (250,40,40),
            512 : (250,30,30),
            1024: (250,20,20),
            2048: (250,15,15),
            4096: (250,10,10),
            8192: (250, 5, 5),
            # now the negative ones
            -1   : (120,250,120),
            -2   : (110,250,110),
            -4   : (100,250,100),
            -8   : (90,250,90),
            -16  : (80,250,80),
            -32  : (70,250,70),
            -64  : (60,250,60),
            -128 : (50,250,50),
            -256 : (40,250,40),
            -512 : (30,250,30),
            -1024: (20,250,20),
            -2048: (15,250,15),
            -4096: (10,250,10),
            -8192: ( 5,250, 5)
        }

        self.tile_color_1 = {
            0   : self.white,
            1   : (150,150,90),
            2   : (220,180,45),
            4   : (250,220, 0),
            8   : (150,120, 0),
            16  : (150, 90, 0),
            32  : self.orange,
            64 : (250, 90, 0),
            128 : (250, 50, 0),
            256 : self.red,
            512: (250, 20,20),
            1024: self.blue,
            2048: self.blue2,
            4096: self.grey1,
            8192: self.grey2
        }

    # def __get_sound(self):
    #     self.sounds = {
    #         'move'   : pygame.mixer.Sound(self.proj_path + 'asset/sound/Coin_1.wav'), 
    #         'merge'  : pygame.mixer.Sound(self.proj_path + 'asset/sound/Coin_2.wav'), 
    #         'castle' : pygame.mixer.Sound(self.proj_path + 'asset/sound/Coin_3.wav')
    #     }

F = Flags()

