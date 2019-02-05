import pygame
from flags import F
from pygame.locals import *


class StatusBar(object):
    """docstring for StatusBar"""
    def __init__(self):
        #self.controller = None
        self.board = None
        self.top_score = 0
        self.cur_score = 0
        self.moves = 0
        self.pos = (0, F.window_h - F.status_bar_size)
        self.size = (F.window_w, F.status_bar_size)
        self.rect = (self.pos[0], self.pos[1], self.pos[0] + self.size[0], 
            self.pos[1]+self.size[1])

    def update_status(self):
        self.moves = self.board.total_moves
        self.cur_score = self.get_board_total_sum(self.board.board)
        if self.cur_score > self.top_score:
            self.top_score = self.cur_score

    def render(self, DISPLAYSUR):    
        #bg = pygame.image.load(F.option_bg_img_path)
        #bg = pygame.transform.scale(bg, self.size)
        #DISPLAYSUR.blit(bg,self.pos)
        pygame.draw.rect(DISPLAYSUR, F.blue2, self.rect)

        GFONT_s = pygame.font.Font('freesansbold.ttf', 15)
        GFONT_b = pygame.font.Font('freesansbold.ttf', 30)

        tot_moves = GFONT_s.render("moves", True, F.white, None)
        tot_score = GFONT_s.render("score", True, F.white, None)
        tot_top_score = GFONT_s.render("top score", True, F.white, None)

        tov_moves = GFONT_b.render(str(self.moves), True, F.white, None)
        tov_score = GFONT_b.render(str(self.cur_score), True, F.white, None)
        tov_top_score = GFONT_b.render(str(self.top_score), True, F.white, None)

        DISPLAYSUR.blit(tot_moves, self.apply_offset(self.pos, (10, 10)))
        DISPLAYSUR.blit(tov_moves, self.apply_offset(self.pos, (10, 25)))

        DISPLAYSUR.blit(tot_score, self.apply_offset(self.pos, (110, 10)))
        DISPLAYSUR.blit(tov_score, self.apply_offset(self.pos, (110, 25)))

        DISPLAYSUR.blit(tot_top_score, self.apply_offset(self.pos, (710, 10)))
        DISPLAYSUR.blit(tov_top_score, self.apply_offset(self.pos, (710, 25)))

    @staticmethod
    def get_board_total_sum(b):
        ret = sum([sum([abs(e) for e in r]) for r in b])
        return ret

    @staticmethod
    def apply_offset(pos,offset):
        return (pos[0]+offset[0], pos[1]+offset[1])

    def __draw_text_center():
        raise NotImplementedError
        # font = pygame.font.Font(None, 25)
        # text = font.render("You win!", True, BLACK)
        # text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        # screen.blit(text, text_rect)

class GenUI():
    """docstring for ClassName"""
    def __init__(self):
        self.GFONTS = None

    @staticmethod
    def shorten_block_text(n):
        if n > 1000000:
            return str(int(n / 1000000))+"m" # e.g. 1048576 -> 1m
        if n > 10000:
            return str(int(n / 1000))+"k" # e.g. 16384 -> 16k
        return str(n)

    #@staticmethod
    def generate_block_text_obj_obsolete(self, FONT, n):
        text_str = self.shorten_block_text(n)
        digits = len(text_str)        
        text_obj = FONT.render(text_str, True, F.block_text_fg, F.block_text_bg)
        text_obj_size = text_obj.get_rect().size
        text_obj_size = [int(s*F.block_font_size_perc[digits-1]) for s in text_obj_size]
        text_obj = pygame.transform.scale(text_obj, text_obj_size)
        return text_obj

    def generate_block_text_obj(self, FONTS, n):
        text_str = self.shorten_block_text(n)
        digits = len(text_str)
        FONT = FONTS[digits-1]
        text_obj = FONT.render(text_str, True, F.block_text_fg, F.block_text_bg)
        return text_obj

    @staticmethod
    def apply_offset(pos,offset):
        return (pos[0]+offset[0], pos[1]+offset[1])

    @staticmethod
    def draw_text_with_outline(SURF, FONT, text_str, fg_color, outline_color, 
        outline_px, pos_0, if8=True, if_center=True):
        text_obj_fg = FONT.render(text_str, True, fg_color, None)
        text_obj_bg = FONT.render(text_str, True, outline_color, None)
        if if_center:
            pos_0 = (
                pos_0[0] - int(text_obj_fg.get_size()[0] / 2),  
                pos_0[1] - int(text_obj_fg.get_size()[1] / 2)
            )
        SURF.blit(text_obj_bg,(pos_0[0]-outline_px, pos_0[1])) #for outline
        SURF.blit(text_obj_bg,(pos_0[0]+outline_px, pos_0[1])) #for outline
        SURF.blit(text_obj_bg,(pos_0[0], pos_0[1]-outline_px)) #for outline
        SURF.blit(text_obj_bg,(pos_0[0], pos_0[1]+outline_px)) #for outline
        if if8:
            SURF.blit(text_obj_bg,(pos_0[0]-outline_px, pos_0[1]-outline_px)) #for outline
            SURF.blit(text_obj_bg,(pos_0[0]+outline_px, pos_0[1]-outline_px)) #for outline
            SURF.blit(text_obj_bg,(pos_0[0]-outline_px, pos_0[1]+outline_px)) #for outline
            SURF.blit(text_obj_bg,(pos_0[0]+outline_px, pos_0[1]+outline_px)) #for outline
        SURF.blit(text_obj_fg, pos_0)        