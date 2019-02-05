import pygame
from flags import F

class SoundPlayer(object):
    """docstring for SoundPlayer"""
    def __init__(self, pygame):
        self.pygame = pygame
        self.__load_sound()
        self.is_playing = False
    
    def __load_sound(self):
        self.sounds = {
            'move'   : self.pygame.mixer.Sound(F.proj_path + 'asset/sound/Coin_1.wav'), 
            'merge'  : self.pygame.mixer.Sound(F.proj_path + 'asset/sound/Coin_2.wav'), 
            'castle' : self.pygame.mixer.Sound(F.proj_path + 'asset/sound/Coin_3.wav'),
            'main_menu' : self.pygame.mixer.Sound(F.proj_path + 'asset/sound/sfx_sounds_powerup2.wav'),
            'game_over' : self.pygame.mixer.Sound(F.proj_path + 'asset/sound/Explosion_1.wav'),
            'game_finish' : self.pygame.mixer.Sound(F.proj_path + 'asset/sound/Explosion_1.wav'),
        }
        self.sounds['move'].set_volume(0.3)
        self.sounds['main_menu'].set_volume(0.5)
        self.sounds['game_over'].set_volume(0.3)
        self.sounds['game_finish'].set_volume(0.3)

    def play_sound_effect(self, event, game_status):
        if game_status == 1: # main menu
            if not self.is_playing:
                self.sounds['main_menu'].play()
                self.is_playing = True
            return
        elif game_status == 4:
            if not self.is_playing:
                self.sounds['game_over'].play()
                self.is_playing = True 
            return
        elif game_status == 6:
            if not self.is_playing:
                self.sounds['game_finish'].play()
                self.is_playing = True 
            return
        else:
            if event[2]:
                self.sounds['castle'].play()
                return
            #elif event[1]:
            #    self.sounds['merge'].play()
            #elif event[0]:
            #    self.sounds['move'].play()


    def play_action_sound(self):
        self.sounds['move'].play()


