import pygame
import sys

from flags import F
from pygame.locals import *
from ui import GenUI

class Controller(object):
    """
    this is the flow controller of the game, 
    when to main screen, when to game over, etc
    it has the application status (var game_status)
    """
    game_status_dict = {
        0: 'initial',
        1: 'main_menu',
        5: 'starting_board',
        2: 'playing',
        21: 'blocks_moving',
        3: 'option',
        4: 'game_over',
        6: 'game_beat'
    }

    def __init__(self, DISPLAYSUR):
        self.game_status = 0 
        self.DISPLAYSUR = DISPLAYSUR
        self.title_counter = 0
        self.title_color = 0

    def start_application(self):
        self.game_status = 1

    def quit_game(self):
        self.big_print("QUITTING THE GAME. 3Q4 PLAYING")
        pygame.quit()
        sys.exit()

    def reset_game(self):
        self.big_print("(re-) Starting the game...")
        self.game_status = 5

    def call_option(self):
        print("bringing up the pop up option window....")
        self.game_status = 3

    def resume_game(self):
        print("going back to the game...")        
        self.game_status = 2

    def lose_game(self):
        self.game_status = 4
        self.big_print("GAME OVER")

    def win_game(self):
        self.game_status = 6
        self.big_print("GAME FINISHED! AMAZING!")

    def draw_pop_up_menu_bg_rect(self, color, size, show_ver = True):
        menu_rect = F.menu_rect
        if size is not None:
            menu_rect = (F.center_x-size, F.center_y-size, 2*size, 2*size)   
        pygame.draw.rect(self.DISPLAYSUR, color, menu_rect)
        if show_ver:
            ver_str_1 = "ver."+F.game_ver
            ver_str_2 = " by whoji"
            FONT_s = pygame.font.Font('freesansbold.ttf', 15)
            text_obj_1 = FONT_s.render(ver_str_1, True, F.white, None)
            text_obj_2 = FONT_s.render(ver_str_2, True, F.white, None)
            px_pad = 5
            pos_x = menu_rect[0] + menu_rect[2] - text_obj_1.get_size()[0] - px_pad
            pos_y = menu_rect[1] + menu_rect[3] - text_obj_1.get_size()[1] - px_pad
            self.DISPLAYSUR.blit(text_obj_1,(pos_x, pos_y))
            pos_x = menu_rect[0] + menu_rect[2] - text_obj_2.get_size()[0] - px_pad
            self.DISPLAYSUR.blit(text_obj_2,(pos_x, pos_y-text_obj_1.get_size()[1]))

    def show_game_over(self):
        #self.game_status = 4
        #pass
        GFONT_b = pygame.font.Font('freesansbold.ttf', 100)
        GFONT_s = pygame.font.Font('freesansbold.ttf', 25)

        text_obj_0 = GFONT_b.render("GAME OVER", True, F.white, None)
        text_obj_0_bg = GFONT_b.render("GAME OVER", True, F.red, None)
        text_obj_1 = GFONT_s.render("Press <ENTER> to start a new game !  ", 
            True, F.white, F.red + (255,))
        text_obj_2 = GFONT_s.render("Press <Q> to quit ...  ", 
            True, F.white, F.red + (255,))

        pos_0 = (F.center_x - int(text_obj_0.get_size()[0] / 2),  F.center_y - 100)
        pos_1 = (F.center_x - int(text_obj_1.get_size()[0] / 2),  F.center_y + 50)
        pos_2 = (F.center_x - int(text_obj_1.get_size()[0] / 2),  F.center_y + 75)

        self.DISPLAYSUR.blit(text_obj_0_bg,(pos_0[0]-6, pos_0[1])) #for outline
        self.DISPLAYSUR.blit(text_obj_0_bg,(pos_0[0]+6, pos_0[1])) #for outline
        self.DISPLAYSUR.blit(text_obj_0_bg,(pos_0[0], pos_0[1]-6)) #for outline
        self.DISPLAYSUR.blit(text_obj_0_bg,(pos_0[0], pos_0[1]+6)) #for outline
        self.DISPLAYSUR.blit(text_obj_0,pos_0)
        self.DISPLAYSUR.blit(text_obj_1,pos_1)
        self.DISPLAYSUR.blit(text_obj_2,pos_2)

        # pos_0 = (F.center_x - int(text_obj_0.get_size()[0] / 2),  F.center_y - 100)
        # pos_1 = (F.center_x - int(text_obj_1.get_size()[0] / 2),  F.center_y + 50)
        # pos_2 = (F.center_x - int(text_obj_1.get_size()[0] / 2),  F.center_y + 75)
        # GenUI.draw_text_with_outline(self.DISPLAYSUR, GFONT_b, "GAME OVER", F.white, F.red, 10, pos_0)
        # GenUI.draw_text_with_outline(self.DISPLAYSUR, GFONT_s, "Press <ENTER> to start a new game !  ", F.white, F.red, 5, pos_1)
        # GenUI.draw_text_with_outline(self.DISPLAYSUR, GFONT_s, "Press <Q> or <ESC> to quit ...  ", F.white, F.red, 5, pos_2)
        # pygame.display.update()

        #GenUI.draw_text_with_outline(self.DISPLAYSUR, GFONT_b, "Test Text String", 
        #    F.orange, F.blue, 10, (200,200) , if8=True, if_center=True)

        for event in pygame.event.get():
            if event.type == QUIT:
                self.quit_game()
            elif  event.type == KEYDOWN: 
                #if event.key == pygame.K_ESCAPE or event.unicode == 'q':
                if event.unicode == 'q':
                    self.quit_game()
                if event.key == pygame.K_RETURN:
                    self.reset_game()
            else:
                pass


    def show_main_menu(self):
        #self.game_status = 1
        #pass
        FONT_m = pygame.font.Font('freesansbold.ttf', 20)
        FONT_l = pygame.font.Font('freesansbold.ttf', 100)
        text_obj_0 = FONT_m.render("Press <ENTER> to start", True, F.white, None) 
        text_obj_1 = FONT_m.render("Press <Q> to quit.", True, F.white, None)

        #pygame.draw.rect(self.DISPLAYSUR, F.red, F.menu_rect)
        self.draw_pop_up_menu_bg_rect(F.red, size= F.menu_size)

        y_offset = 200
        self.DISPLAYSUR.blit(text_obj_0,(F.center_x-F.menu_size+20, F.center_y-F.menu_size+y_offset+20))
        self.DISPLAYSUR.blit(text_obj_1,(F.center_x-F.menu_size+20, F.center_y-F.menu_size+y_offset+50))

        # Game Tile
        fg_color = F.white
        bg_color = F.orange
        if F.blink_title:
            if self.title_counter >= 10000:
                self.title_counter = 0
            color_idx = int(self.title_counter / F.blink_tile_fps) % 10
            fg_color = [F.black, F.grey1, F.blue, F.red, F.white, F.green, F.blue2, F.grey2, F.yellow, F.blue][color_idx]
            self.title_counter += 1

        GenUI.draw_text_with_outline(self.DISPLAYSUR, FONT_l, F.game_name, 
            fg_color, bg_color, 5, (F.center_x, F.center_y-100) , if8=True, if_center=True)
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                self.quit_game()
            elif  event.type == KEYDOWN: 
                #if event.key == pygame.K_ESCAPE or event.unicode == 'q':
                if event.unicode == 'q':
                    self.quit_game()
                if event.key == pygame.K_RETURN:
                    self.reset_game()
            else:
                pass


    def show_option(self):

        FONT_s = pygame.font.Font('freesansbold.ttf', 15)
        FONT_m = pygame.font.Font('freesansbold.ttf', 20)
        FONT_l = pygame.font.Font('freesansbold.ttf', 65)

        text_obj_0 = FONT_m.render(" ", True, F.white, None) 
        text_obj_1 = FONT_s.render("Press <F1> or <ESC> to resume the game.", True, F.white, None)
        text_obj_2 = FONT_s.render("Press <Q> to quit the game.", True, F.white, None)
        text_obj_3 = FONT_s.render("Press <R> to start over the game.", True, F.white, None)
        text_obj_4 = FONT_s.render("To play: ", True, F.white, None)
        text_obj_4a = FONT_s.render("   Arrow Key / W,A,S,D / H,J,K,L to move ", True, F.white, None)
        text_obj_4b = FONT_s.render("   * LEFT board: merge two blocks of opposite signs,  ", True, F.white, None)
        text_obj_4c = FONT_s.render("      with same values to cancel them and move them  ", True, F.white, None)
        text_obj_4d = FONT_s.render("      to the RIGHT board.  ", True, F.white, None)
        text_obj_4e = FONT_s.render("   * RIGHT board: play like a normal 2048 game.  ", True, F.white, None)
        text_obj_4f = FONT_s.render("      creat a 2048 tile on RIGHT to win.  ", True, F.white, None)

        self.draw_pop_up_menu_bg_rect(F.green, size= F.menu_size+10)

        y_offset = 90
        self.DISPLAYSUR.blit(text_obj_0,(F.center_x-F.menu_size+20, F.center_y-F.menu_size+y_offset+20))
        self.DISPLAYSUR.blit(text_obj_1,(F.center_x-F.menu_size+20, F.center_y-F.menu_size+y_offset+20))
        self.DISPLAYSUR.blit(text_obj_2,(F.center_x-F.menu_size+20, F.center_y-F.menu_size+y_offset+40))
        self.DISPLAYSUR.blit(text_obj_3,(F.center_x-F.menu_size+20, F.center_y-F.menu_size+y_offset+60))
        self.DISPLAYSUR.blit(text_obj_4,(F.center_x-F.menu_size+20, F.center_y-F.menu_size+y_offset+110))
        self.DISPLAYSUR.blit(text_obj_4a,(F.center_x-F.menu_size+20, F.center_y-F.menu_size+y_offset+130))
        self.DISPLAYSUR.blit(text_obj_4b,(F.center_x-F.menu_size+20, F.center_y-F.menu_size+y_offset+150))
        self.DISPLAYSUR.blit(text_obj_4c,(F.center_x-F.menu_size+20, F.center_y-F.menu_size+y_offset+170))
        self.DISPLAYSUR.blit(text_obj_4d,(F.center_x-F.menu_size+20, F.center_y-F.menu_size+y_offset+190))
        self.DISPLAYSUR.blit(text_obj_4e,(F.center_x-F.menu_size+20, F.center_y-F.menu_size+y_offset+210))
        self.DISPLAYSUR.blit(text_obj_4f,(F.center_x-F.menu_size+20, F.center_y-F.menu_size+y_offset+230))
        GenUI.draw_text_with_outline(self.DISPLAYSUR, FONT_l, "OPTION MENU", 
            F.white, F.orange, 5, (F.center_x, F.center_y-170) , if8=True, if_center=True)
        
        pygame.display.update()


        for event in pygame.event.get():
            if event.type == QUIT:
                self.quit_game()
            elif  event.type == KEYDOWN: 
                if event.unicode == 'r':
                    self.reset_game()
                if event.unicode == 'q':
                    self.quit_game()
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_F1:
                    self.resume_game()
            else:
                pass

    def show_game_finished(self, milestone = None):

        FONT_s = pygame.font.Font('freesansbold.ttf', 15)
        FONT_m = pygame.font.Font('freesansbold.ttf', 20)
        FONT_l = pygame.font.Font('freesansbold.ttf', 80)

        text_obj_0 = FONT_m.render("CONGRATULATIONS!! YOU WON !!", True, F.white, None) 
        text_obj_1 = FONT_s.render("Press <ENTER> to continue the INFINITE mode", True, F.white, None) 
        text_obj_2 = FONT_s.render("Press <Q>to quit the game.", True, F.white, None)         
        text_obj_3 = FONT_s.render("Press <R> to start over the game.", True, F.white, None)         

        if milestone is not None:
            text_obj_0 = INvFONT.render("MILESTONE [%d] REACHED" % milestone,
                True, F.white, None)
            text_obj_1 = GFONT.render("Press <ENTER> to continue.", True, 
                F.white, F.black)
            text_obj_2 = GFONT.render("", True, F.white, F.black) 
        
        #pygame.draw.rect(self.DISPLAYSUR, F.blue, F.menu_rect)
        self.draw_pop_up_menu_bg_rect(F.blue2, size= F.menu_size+20)

        y_offset = 150

        self.DISPLAYSUR.blit(text_obj_0,(F.center_x-F.menu_size+20, F.center_y-F.menu_size+y_offset+20))
        self.DISPLAYSUR.blit(text_obj_1,(F.center_x-F.menu_size+20, F.center_y-F.menu_size+y_offset+60))
        self.DISPLAYSUR.blit(text_obj_2,(F.center_x-F.menu_size+20, F.center_y-F.menu_size+y_offset+90))
        self.DISPLAYSUR.blit(text_obj_3,(F.center_x-F.menu_size+20, F.center_y-F.menu_size+y_offset+120))
        GenUI.draw_text_with_outline(self.DISPLAYSUR, FONT_l, "YOU WIN", 
            F.orange, F.red, 5, (F.center_x, F.center_y-150) , if8=True, if_center=True)
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                self.quit_game()
            elif  event.type == KEYDOWN: 
                if event.unicode == 'r':
                    self.reset_game()
                if event.unicode == 'q':
                    self.quit_game()                    
                if event.key == pygame.K_RETURN:
                    self.resume_game()
            else:
                pass

    def render_pop_window(self):
        if self.game_status == 1:
            self.show_main_menu()
        elif self.game_status == 3:
            self.show_option()
        elif self.game_status == 4:
            self.show_game_over()
        elif self.game_status == 6:
            self.show_game_finished()
        else:
            pass

    @staticmethod        
    def big_print(str1):
        print()
        print("========================================")
        print("  " + str(str1))
        print("========================================")
        print()


    def show_help(self):
        raise NotImplementedError
        '''
        Enter: start        : start the game / confirm
        asdw / hjkl / arrow : play the game
        F1                  : call the option menu
        ESC / q             : quit the game
        '''
