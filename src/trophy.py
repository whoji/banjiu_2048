import pygame
import pickle
from flags import F

class Trophy(object):
    """docstring for Trophy"""
    def __init__(self):
        self.trophy_file = F.save_path + 'trophy.pkl'
        self.trophy_dict = {
            "c256" : False,
            "c512" : False,
            "c1024" : False,
            "c2048" : False,
            "c4096" : False,
            "c8192" : False,
        }
        if F.debug_mod:
            self.trophy_dict["c4"] = False

        self.load_trophy()
        self.trophy_list = sorted([int(t[1:]) for t in self.trophy_dict.keys()])

    def trigger(self, name):
        self.trophy_dict[name] = True
        self.save_trophy()

    def load_trophy(self):
        try:
            with open(self.trophy_file, "rb") as f:
                self.trophy_dict = pickle.load(f)
        except FileNotFoundError as error:
            self.save_trophy()

    def save_trophy(self):
        with open(self.trophy_file, "wb") as f:
            pickle.dump(self.trophy_dict, f)

    def draw_trophy(self, DISPLAYSUR, pos):
        pos = (pos[0], pos[1])
        i = 0
        for t in self.trophy_list:
            t_name = "c"+str(t)
            trophy_pos = self.apply_offset(pos, 
                (0 +i*F.castle_icon_gap+i*F.castle_icon_px, 0))
            trophy_rect = (trophy_pos[0],trophy_pos[1],F.castle_icon_px, F.castle_icon_px)
            pygame.draw.rect(DISPLAYSUR, F.orange, trophy_rect)
            if self.trophy_dict[t_name]:
                c = F.castle_textures[t]
                cs = pygame.transform.scale(c, (F.castle_icon_px, F.castle_icon_px))
                DISPLAYSUR.blit(cs, trophy_pos)
            i += 1

    @staticmethod
    def apply_offset(pos,offset):
        return (pos[0]+offset[0], pos[1]+offset[1])