import pygame
import random
import member_classes
import map_objects as mo
import world_map_info
import buildings
import factions

pygame.init()

screenWidth = world_map_info.screenWidth
screenHeight = world_map_info.screenHeight
win = pygame.display.set_mode((screenWidth, (screenHeight + 120)))
pygame.display.set_caption("GSS")

run = True

ruby = factions.ruby
sapphire = factions.sapphire
emerald = factions.emerald

greenfood = mo.GreenFood()
g_food = greenfood.name


def redraw_display():
    win.fill((0, 18, 0))
    ui_colour = (18, 18, 18)
    ui_height = 600
    pygame.draw.rect(win, ui_colour, (0, ui_height, 900, 720))

    for fac in factions.all_factions:
        if fac[4][0] > 3: #and len(fac[5]) < 6:
            fac[5].append(member_classes.Villager(fac[0][0], fac[0][1], 3, 1, fac))
            fac[4][0] -= 3
            print('{}. {}'.format(fac[2], len(fac[5])))

    def g_food_remove(person, width):
        for loc_one in g_food_loc:
            if -width - person.wh < (person.x - int(loc_one[0])) < width and \
                    -width - person.wh < (person.y - int(loc_one[1])) < 6:
                try:
                    g_food_loc.remove(loc_one)
                    inventory = person.inventory
                    inventory.append(g_food)
                    if person.hp < person.max_hp:
                        person.hp += 1
                    person.exp += 1
                    person.lvl_up()
                    print(person.wh)
                except ValueError:
                    pass

    g_food_loc = greenfood.g_food_loc
    if len(g_food_loc) < 6:
        greenfood.draw(random.randrange(36, 72), screenWidth, screenHeight)
    else:
        for one_g in range(len(g_food_loc)):
            pygame.draw.circle(win, (0, 51, 0),
                               (int(g_food_loc[one_g][0]), int(g_food_loc[one_g][1])), 3)
    for fac in factions.all_factions:
        for vil in fac[5]:
            g_food_remove(vil, 3)
    g_food_remove(prophet, 6)
    # prophet.wh = prophet.wh + 1 (reikia lvl up sistemos, kad vel galeciau sita paleist)

    first_base.draw(win, ruby[1])
    second_base.draw(win, sapphire[1])
    third_base.draw(win, emerald[1])

    for fac in factions.all_factions:
        for vil in fac[5]:
            vil.draw(win)

    prophet.draw(win)

    pygame.display.update()


def duel(fp, sp):
    if fp.center[0] - fp.wh < sp.center[0] < fp.center[0] + fp.wh \
            and fp.center[1] - fp.wh < sp.center[1] < fp.center[1] + fp.wh:
        sp.hp -= random.randint(0, fp.lvl * 2)
        fp.hp -= random.randint(0, sp.lvl * 2)
        if sp.hp <= 0:
            try:
                fac[5].remove(sp)
            except ValueError:
                pass


game = True
while game:
    new_game = True

    if new_game:
        for _ in range(2):
            ruby[5].append(member_classes.Villager(450, 90, 3, 1, ruby))
            emerald[5].append(member_classes.Villager(180, 450, 3, 1, emerald))
            sapphire[5].append(member_classes.Villager(720, 450, 3, 1, sapphire))
        new_game = False

    prophet = member_classes.Prophet(450, 270, 6, 3, 9)

    first_base = buildings.Base(ruby)
    second_base = buildings.Base(sapphire)
    third_base = buildings.Base(emerald)

    while run:
        pygame.time.delay(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        prophet.controls()
        for fac in factions.all_factions:
            for vil in fac[5]:
                duel(prophet, vil)
                for another_fac in factions.all_factions:
                    for another_vil in another_fac[5]:
                        if fac != another_fac:
                            duel(another_vil, vil)
                vil.gather()
        redraw_display()
        if prophet.hp <= 0:
            print('You lost')
            run = False
        if len(factions.ruby[5]) == 0 and len(factions.sapphire[5]) == 0 and len(factions.emerald[5]) == 0:
            print('You won')
            run = False
    while not run:
        win.fill((0, 18, 0))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            run = True

pygame.quit()
