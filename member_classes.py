import pygame
import random
import world_map_info
import map_objects as mo
import factions

greenfood = mo.GreenFood()
g_food = greenfood.name


class Person:
    def __init__(self, x, y, wh, max_hp, faction):
        self.x = x
        self.y = y
        self.wh = wh
        self.center = [((wh / 2) + self.x), ((wh / 2) + self.y)]
        self.max_hp = max_hp
        self.hp = self.max_hp
        self.lvl = 1
        self.max_exp = 3
        self.exp = 0
        self.faction = faction
        self.inventory = []

    def lvl_up(self):
        if self.exp >= self.max_exp:
            self.lvl += 1
            self.exp -= self.max_exp
            self.max_exp *= 2
            self.wh += 1 / 3
            self.max_hp += 1
            self.hp = self.max_hp
            print(f'Now object is level {self.lvl}')

    def go(self, vel, x, y):
        if (self.x + (self.wh / 2)) > x:
            self.x -= vel
        if (self.x + (self.wh / 2)) < x:
            self.x += vel
        if (self.y + (self.wh / 2)) > y:
            self.y -= vel
        if (self.y + (self.wh / 2)) < y:
            self.y += vel


class Prophet(Person):
    def __init__(self, x, y, wh, max_hp, team_base):
        super().__init__(x, y, wh, max_hp, team_base)
        self.self_control = 9 + self.lvl
        self.vel = 0
        self.prophet_rgb = 51
        self.aura = True
        self.char_colour = [(self.prophet_rgb, self.prophet_rgb, self.prophet_rgb), (0, 0, 0)]

    def draw(self, window):
        if self.char_colour[0] == (self.prophet_rgb, self.prophet_rgb, self.prophet_rgb):
            if self.prophet_rgb < 255 and self.aura:
                self.prophet_rgb += 1
            elif self.prophet_rgb == 255:
                self.aura = False
                self.prophet_rgb -= 1
            elif self.prophet_rgb > 50 and not self.aura:
                self.prophet_rgb -= 1
            elif self.prophet_rgb == 50:
                self.aura = True
            del self.char_colour[0]
            self.char_colour.insert(0, tuple((self.prophet_rgb, self.prophet_rgb, self.prophet_rgb)))
        pygame.draw.rect(window, (self.char_colour[0]), (self.x, self.y, round(self.wh), round(self.wh)))
        self.center = [((self.wh / 2) + self.x), ((self.wh / 2) + self.y)]

    def gather(self):
        g_food_loc = greenfood.g_food_loc
        way_lenght = []
        for way in range(len(g_food_loc)):
            way_lenght.append(abs(self.center[0] - int(g_food_loc[way][0])) +
                              (abs(self.center[1] - int(g_food_loc[way][1]))))
        way_lenght_min = min(way_lenght)
        way_lenght_index = way_lenght.index(way_lenght_min)
        # print(way_lenght)
        # print('{}. {}   '.format(way_lenght_index, way_lenght_min) + str(self.x) + '. ' + str(self.y))
        short_x = int(g_food_loc[way_lenght_index][0]) - 1
        short_y = int(g_food_loc[way_lenght_index][1]) - 1
        Person.go(self, self.vel, short_x, short_y)

    def change_colour(self):
        global rand_dir

        if self.char_colour[0] == (self.prophet_rgb, self.prophet_rgb, self.prophet_rgb):
            self.vel = 3
            rand_dir = random.randrange(1, self.self_control)
        else:
            self.vel = 6
            rand_dir = 0

    def controls(self):
        self.change_colour()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_r]:
            print(self.center)
            if self.char_colour[0]:
                self.char_colour.append(self.char_colour[0])
                del self.char_colour[0]

        if keys[pygame.K_g] or self.char_colour[0] == (0, 0, 0):
            self.gather()

        if keys[pygame.K_x]:
            if 'Green Food' in self.inventory:
                mo.GreenFood.g_food_loc.append((random.randrange(self.x - 27, self.x + 27),
                                                random.randrange(self.y - 27, self.y + 27)))
                self.inventory.remove('Green Food')

        if keys[pygame.K_LEFT] and self.x > self.vel or rand_dir == 1 and self.x > self.vel:
            self.x -= self.vel

        if keys[pygame.K_RIGHT] and self.x < world_map_info.screenWidth - self.wh - self.vel \
                or rand_dir == 2 and self.x < world_map_info.screenWidth - self.wh - self.vel:
            self.x += self.vel

        if keys[pygame.K_UP] and self.y > self.vel or rand_dir == 3 and self.y > self.vel:
            self.y -= self.vel

        if keys[pygame.K_DOWN] and self.y < world_map_info.screenHeight - self.wh - self.vel \
                or rand_dir == 4 and self.y < world_map_info.screenHeight - self.wh - self.vel:
            self.y += self.vel

        if keys[pygame.K_k]:
            for fac in factions.all_factions:
                try:
                    fac[5].pop(0)
                except IndexError:
                    pass  # visi villagers killed


class Villager(Person):
    def __init__(self, x, y, wh, max_hp, faction):
        super().__init__(x, y, wh, max_hp, faction)
        self.vel = random.randrange(1, 4)
        self.char_colour = faction[1].copy()
        self.go_gather = True
        self.faction = faction
        self.faction_inventory = self.faction[3]
        self.rand_dir = 0

    def draw(self, window):
        self.char_colour[self.faction[2]] = 180
        pygame.draw.circle(window, self.char_colour, (self.x, self.y), round(self.wh))
        self.center = [((self.wh / 2) + self.x), ((self.wh / 2) + self.y)]

    def go(self, vel, x, y):
        self.rand_dir = random.randrange(1, 15)
        if self.rand_dir in range(5, 12):
            Person.go(self, self.vel, x, y)
        elif self.rand_dir in range(1, 5):
            if self.rand_dir == 1:
                self.x -= vel
            if self.rand_dir == 2:
                self.x += vel
            if self.rand_dir == 3:
                self.y -= vel
            if self.rand_dir == 4:
                self.y += vel

    def put_in_base(self, material):
        all_same_item = self.inventory.count(material)
        for one_same_item in range(all_same_item):
            self.faction_inventory.append(material)
            self.inventory.remove(material)
            factions.store_in(material, self.faction)

    def go_base(self):
        global faction_base

        faction_base = self.faction[0]
        self.go(self.vel, faction_base[0], faction_base[1])
        if self.x == faction_base[0] and self.y == faction_base[1]:
            self.put_in_base(g_food)
            if g_food not in self.inventory:
                self.go_gather = True

    def gather(self):
        g_food_loc = greenfood.g_food_loc
        if g_food in self.inventory:
            self.go_gather = False
            self.go_base()
        elif self.go_gather:
            way_lenght_villager = []
            for way in range(len(g_food_loc)):
                way_lenght_villager.append(abs(self.center[0] - int(g_food_loc[way][0])) +
                                           (abs(self.center[1] - int(g_food_loc[way][1]))))
            try:
                way_lenght_min = min(way_lenght_villager)
                way_lenght_index = way_lenght_villager.index(way_lenght_min)
                short_x = int(g_food_loc[way_lenght_index][0]) - 1
                short_y = int(g_food_loc[way_lenght_index][1]) - 1
                self.go(self.vel, short_x, short_y)
            except ValueError:
                pass
