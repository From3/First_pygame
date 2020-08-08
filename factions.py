ruby = [(450, 90), [60, 0, 0], 0, [], [0], []]
emerald = [(180, 450), [0, 60, 0], 1, [], [0], []]
sapphire = [(720, 450), [0, 0, 60], 2, [], [0], []]
all_factions = (ruby, emerald, sapphire)


def store_in(material, faction_name):
    faction_inventory = faction_name[3]
    faction_storage = faction_name[4]
    items = faction_inventory.count(material)
    faction_storage[0] += items
    for item in range(items):
        faction_inventory.remove(material)


class Faction:
    def __init__(self, x, y, rgb, num):
        self.x = x
        self.y = y
        self.rgb = rgb
        self.num = num
        self.storage = []
        self.inventory = [0]
        self.unit_list = []
