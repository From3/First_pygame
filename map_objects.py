import random


class GreenFood:
    g_food_loc = []
    name = 'Green Food'

    def __init__(self):
        pass

    def draw(self, quan, screen_x, screen_y):
        global g_food_loc_one

        for i in range(quan):
            g_food_loc_one = list([])
            g_food_loc_one.append(str(random.randrange(0, screen_x - 15)))
            g_food_loc_one.append(str(random.randrange(0, screen_y - 15)))
            self.g_food_loc.append(g_food_loc_one)
