import pygame
import sys
import random
from pygame.locals import *

from board import Board, RightBoard
from flags import F
from controller import Controller
from ui import StatusBar, GenUI
from mover import Mover
from sound import SoundPlayer

def eventkey_to_action(eventkey):
    action = None
    if eventkey in [K_RIGHT, K_l, K_d]:
        action = 'right'
    elif eventkey  in [K_LEFT, K_h, K_a]:
        action = 'left'
    elif eventkey in [K_DOWN, K_j, K_s]:
        action = 'down'
    elif eventkey in [K_UP, K_k, K_w]:
        action = 'up'
    else:
        #print("bad event key!!")
        pass
    return action

# Starting the game components
pygame.init()
pygame.display.set_caption(F.game_name)
board_0 = Board()
board_1 = RightBoard()
status_bar = StatusBar()
gen_ui = GenUI()
DISPLAYSUR = pygame.display.set_mode((F.window_w, F.window_h))
controller = Controller(DISPLAYSUR)
sound_player = SoundPlayer(pygame)
clock = pygame.time.Clock()

# setup a font for displaying block numbers
GFONT = pygame.font.Font('freesansbold.ttf', F.block_font_size)
GFONT_GG = pygame.font.Font('freesansbold.ttf', 66) 
GFONTS = [
            pygame.font.Font('freesansbold.ttf', int(F.block_font_size * F.block_font_size_perc[0])),
            pygame.font.Font('freesansbold.ttf', int(F.block_font_size * F.block_font_size_perc[1])),
            pygame.font.Font('freesansbold.ttf', int(F.block_font_size * F.block_font_size_perc[2])),
            pygame.font.Font('freesansbold.ttf', int(F.block_font_size * F.block_font_size_perc[3])),
            pygame.font.Font('freesansbold.ttf', int(F.block_font_size * F.block_font_size_perc[4])),
            pygame.font.Font('freesansbold.ttf', int(F.block_font_size * F.block_font_size_perc[5]))
        ]
gen_ui.GFONTS = GFONTS

while True:
    clock.tick(F.game_fps)

    # ===================================
    # part 1. Game flow control
    # ===================================

    DISPLAYSUR.fill(F.grey2)

    # when the app started
    if controller.game_status == 0:
        controller.start_application()
        continue

    # at main menu
    elif controller.game_status == 1:
        sound_player.play_sound_effect(None, controller.game_status)        
        controller.show_main_menu()
        continue

    # starting the board
    elif controller.game_status == 5:
        board_0 = Board()
        board_1 = RightBoard()
        controller.game_status = 2
        status_bar.board = board_1
        status_bar.update_status()
        #status_bar.controller = controller
        continue

    # playing the game (at board view)
    elif controller.game_status == 2:

        for event in pygame.event.get():
            if event.type == QUIT:
                controller.quit_game()
            elif event.type == KEYDOWN:
                action = eventkey_to_action(event.key)
                if action in ['up','down','right','left']:
                    sound_player.play_action_sound()
                    if_moved_0 = board_0.update_board(action)
                    board_1.cancelled_list = board_0.cancelled
                    if_moved_1 = board_1.update_board(action)
                    print(board_0.cancelled)
                    print(board_1.cancelled_list)

                    Board.print_both_boards(board_0.board, board_1.board)

                    if if_moved_0:
                        #print(board_0)
                        mover_0 = Mover(board_0.prev_board, action)
                        controller.game_status = 21
                        status_bar.update_status()

                    if if_moved_1:
                        #print(board_1)
                        mover_1 = Mover(board_1.prev_board, action)
                        controller.game_status = 21
                        status_bar.update_status()

                    # if if_moved_0 or if_moved_1:
                    #     if if_moved_0:
                    #         mover_0 = Mover(board_0.prev_board, action)
                    #     else:
                    #         mover_0 = Mover(board_0.board, action)

                    #     if if_moved_1:
                    #         mover_1 = Mover(board_1.prev_board, action)
                    #     else:
                    #         mover_1 = Mover(board_1.board, action)

                    #     controller.game_status = 21
                    #     status_bar.update_status()


                # can press q to exit the game only in debug_mode
                elif event.unicode == 'q' and F.debug_mod:
                    controller.quit_game()

                elif event.key == pygame.K_F1 or event.key == pygame.K_ESCAPE:
                    controller.call_option()

                elif F.debug_mod:
                    if event.key == pygame.K_F4: # Four for Die (si3)
                        board_0.if_gg = True
                        board_1.if_gg = True
                    elif event.key == pygame.K_F5: # Five (V) for Victory
                        board_1.if_win = True

                else:
                    print("Invalid key input: <" + str(event.key) +">; Doing nothing...")
            else:
                pass
                #print("other event.type: " + str(event.type))

        if board_0.if_gg or board_1.if_gg:
            controller.lose_game()
        elif board_1.if_win:
            controller.win_game()
            board_1.if_win = False

    else:
        pass

    # ===================================
    # part 2. render everything
    # ===================================

    # render the board bg
    pygame.draw.rect(DISPLAYSUR, F.board_frame_color, F.board_outer_rect_0)
    for row in range(F.map_cols):
        for col in range(F.map_rows):
            pygame.draw.rect(DISPLAYSUR, F.board_frame_color,
                (col*F.tile_size+F.board_origin_0[0], row*F.tile_size+
                    F.board_origin_0[1], F.tile_size, F.tile_size))
            pygame.draw.rect(DISPLAYSUR, F.board_color,(
                col*F.tile_size+F.board_origin_0[0]+F.board_frame_px,
                row*F.tile_size+F.board_origin_0[1]+F.board_frame_px, 
                F.tile_size-2*F.board_frame_px, 
                F.tile_size-2*F.board_frame_px))

    pygame.draw.rect(DISPLAYSUR, F.board_frame_color, F.board_outer_rect_1)
    for row in range(F.map_cols):
        for col in range(F.map_rows):
            pygame.draw.rect(DISPLAYSUR, F.board_frame_color,
                (col*F.tile_size+F.board_origin_1[0], row*F.tile_size+
                    F.board_origin_1[1], F.tile_size, F.tile_size))
            pygame.draw.rect(DISPLAYSUR, F.board_color,(
                col*F.tile_size+F.board_origin_1[0]+F.board_frame_px,
                row*F.tile_size+F.board_origin_1[1]+F.board_frame_px, 
                F.tile_size-2*F.board_frame_px, 
                F.tile_size-2*F.board_frame_px))

    # render the moving blocks
    if controller.game_status == 21:
        if mover_0.remain_moving_frames > 0 and if_moved_0:
            mover_0.move_all()
            for row in range(F.map_rows):
                for col in range(F.map_cols):
                    if mover_0.blocks[row][col]:
                        # the tile background
                        moving_tile_pos = (mover_0.blocks[row][col].y*F.tile_size+F.board_origin_0[0]+F.board_frame_px,
                            mover_0.blocks[row][col].x*F.tile_size+F.board_origin_0[1]+F.board_frame_px)
                        moving_tile_rect = moving_tile_pos + (F.tile_size-2*F.board_frame_px, 
                            F.tile_size -2*F.board_frame_px)
                        tile_color = F.tile_color[board_0.prev_board[row][col]]
                        pygame.draw.rect(DISPLAYSUR, tile_color, moving_tile_rect)
                        # the text (number)
                        text_obj = gen_ui.generate_block_text_obj(GFONTS, board_0.prev_board[row][col])
                        if F.block_font_center:
                            moving_tile_pos = Mover.center_text(text_obj,moving_tile_pos)
                        DISPLAYSUR.blit(text_obj,moving_tile_pos)

        if mover_1.remain_moving_frames > 0 and if_moved_1:
            mover_1.move_all()
            for row in range(F.map_rows):
                for col in range(F.map_cols):
                    if mover_1.blocks[row][col]:
                        # the tile background
                        moving_tile_pos = (mover_1.blocks[row][col].y*F.tile_size+F.board_origin_1[0]+F.board_frame_px,
                            mover_1.blocks[row][col].x*F.tile_size+F.board_origin_1[1]+F.board_frame_px)
                        moving_tile_rect = moving_tile_pos + (F.tile_size-2*F.board_frame_px, 
                            F.tile_size -2*F.board_frame_px)
                        tile_color = F.tile_color_1[board_1.prev_board[row][col]]
                        pygame.draw.rect(DISPLAYSUR, tile_color, moving_tile_rect)
                        # the text (number)
                        text_obj = gen_ui.generate_block_text_obj(GFONTS, board_1.prev_board[row][col])
                        if F.block_font_center:
                            moving_tile_pos = Mover.center_text(text_obj,moving_tile_pos)
                        DISPLAYSUR.blit(text_obj,moving_tile_pos)
        else:
            controller.game_status = 2

    # render the board
    if controller.game_status != 21:
        for row in range(F.map_cols):
            for col in range(F.map_rows):
                if board_0.board[row][col]:
                    block_rect = (col*F.tile_size+F.board_origin_0[0]+F.board_frame_px, 
                        row*F.tile_size+F.board_origin_0[1]+F.board_frame_px, 
                        F.tile_size-F.board_frame_px*2,F.tile_size-F.board_frame_px*2)
                    tile_color = F.tile_color[board_0.board[row][col]]
                    pygame.draw.rect(DISPLAYSUR, tile_color, block_rect)
    
    if controller.game_status != 21:
        for row in range(F.map_cols):
            for col in range(F.map_rows):
                if board_1.board[row][col]:
                    block_rect = (col*F.tile_size+F.board_origin_1[0]+F.board_frame_px, 
                        row*F.tile_size+F.board_origin_1[1]+F.board_frame_px, 
                        F.tile_size-F.board_frame_px*2,F.tile_size-F.board_frame_px*2)
                    tile_color = F.tile_color_1[board_1.board[row][col]]
                    pygame.draw.rect(DISPLAYSUR, tile_color, block_rect)

    # render the text
    if controller.game_status != 21:
        for row in range(F.map_cols):
            for col in range(F.map_rows):
                if board_0.board[row][col]:
                    text_obj = gen_ui.generate_block_text_obj(FONTS=GFONTS, n=board_0.board[row][col])
                    tile_pos = (col*F.tile_size+F.board_origin_0[0]+F.board_frame_px, 
                        row*F.tile_size+F.board_origin_0[1]+F.board_frame_px)
                    if F.block_font_center:
                        tile_pos = Mover.center_text(text_obj, tile_pos)
                    DISPLAYSUR.blit(text_obj, tile_pos)

    if controller.game_status != 21:
        for row in range(F.map_cols):
            for col in range(F.map_rows):
                if board_1.board[row][col]:
                    text_obj = gen_ui.generate_block_text_obj(FONTS=GFONTS, n=board_1.board[row][col])
                    tile_pos = (col*F.tile_size+F.board_origin_1[0]+F.board_frame_px, 
                        row*F.tile_size+F.board_origin_1[1]+F.board_frame_px)
                    if F.block_font_center:
                        tile_pos = Mover.center_text(text_obj, tile_pos)
                    DISPLAYSUR.blit(text_obj, tile_pos)

    # render the status bar
    status_bar.render(DISPLAYSUR)

    # render the pop up window (option menu / game over / etc)
    controller.render_pop_window()

    pygame.display.update()


    # ===================================
    # part 3. play sound effect
    # ===================================


    sound_event_monitor = [board_0.if_moved, board_0.if_merged, board_0.if_upgraded]
    sound_event_monitor.append(len(board_0.cancelled)>0)
    sound_player.play_sound_effect(sound_event_monitor, controller.game_status)
    board_0.resest_event_monitor()


    # ===================================
    # end of each frame
    # ===================================



