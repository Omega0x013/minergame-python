import pygame
import random
import math
import collections
from lib.spawn_probabilities import *

pygame.font.init()

empty_save = False
block_size = 60
wall_height = block_size // 3
player_size = block_size // 2
zone_size_in_blocks = 9
zone_size = block_size * zone_size_in_blocks
move_distance = 3
diagonal_move_distance = move_distance * math.cos(math.radians(45))
fnt = pygame.font.Font('./font.otf', 20)
screen_size = block_size * 14

zones_with_modifications = {}


def get_image(path, dimensions):
    return pygame.transform.scale(pygame.image.load(path), dimensions)


damage_levels = [get_image('/home/xander/Documents/openevening/minergame/graphics/break-1.png', (60, 60)),
                 get_image('/home/xander/Documents/openevening/minergame/graphics/break-2.png', (60, 60)),
                 get_image('/home/xander/Documents/openevening/minergame/graphics/break-3.png', (60, 60)),
                 get_image('/home/xander/Documents/openevening/minergame/graphics/break-4.png', (60, 60)),
                 get_image('/home/xander/Documents/openevening/minergame/graphics/break-5.png', (60, 60))
                 ]


# player_movement = [get_image()]

up = 0
left = 1
down = 2
right = 3

ticks = 0
gold = 0
inventory = collections.Counter()


class Modification:
    def __init__(self):
        self.last_damage_tick = ticks
        self.damage = 1


class Zone:
    def __init__(self, generate, zx=0, zy=0, blocks=None, ground=None):
        self.modifications = {}
        if generate:
            self.blocks = []
            self.ground = []
            pos = 0
            off_x = (zx - 0.5) * zone_size_in_blocks
            off_y = (zy - 0.5) * zone_size_in_blocks
            for x in range(zone_size_in_blocks):
                for y in range(zone_size_in_blocks):
                    bx = off_x + x
                    by = off_y + y
                    d = math.floor(math.sqrt(bx * bx + by * by) / 10)
                    if d >= len(rings):
                        ring = rings[-1]
                    else:
                        ring = rings[d]
                    r = random.random()
                    block = stone_block
                    for choice in ring:
                        r -= choice[0]
                        if r < 0:
                            block = choice[1]
                            break
                    self.blocks.append(block)
                    if block != air_block:
                        self.ground.append(stone_ground)
                    else:
                        self.ground.append(dirt_ground)
                    pos += 1
        else:
            self.blocks = blocks
            self.ground = ground

    def draw_floor_and_sides(self, zones, zx, zy, base_x, base_y):
        pos = 0
        for x in range(zone_size_in_blocks):
            for y in range(zone_size_in_blocks):
                block = self.blocks[pos]
                if y < zone_size_in_blocks - 1:
                    next_block = self.blocks[pos + 1]
                else:
                    next_zone = zones.get((zx, zy + 1), None)
                    if next_zone is None:
                        next_block = air_block
                    else:
                        next_block = next_zone.blocks[pos - 8]
                if block == air_block:
                    pygame.draw.rect(screen, self.ground[pos].color, (base_x + x * block_size, base_y + y * block_size, block_size, block_size))
                elif next_block == air_block:
                    pygame.draw.rect(screen, block.side_color, (base_x + x * block_size, base_y + y * block_size + block_size - wall_height, block_size, 20))
                pos += 1

    def draw_tops(self, base_x, base_y):
        pos = 0
        for x in range(zone_size_in_blocks):
            for y in range(zone_size_in_blocks):
                block = self.blocks[pos]
                pos += 1
                if block != air_block:
                    pygame.draw.rect(screen, block.top_color, (base_x + x * block_size, base_y + y * block_size - wall_height, block_size, block_size))

    def draw_damage(self, base_x, base_y):  # world_offset[0] + (zx * zone_size), world_offset[1] + (zy * zone_size)
        for position, modification in self.modifications.items():
            x = position // zone_size_in_blocks
            y = position % zone_size_in_blocks
            screen.blit(damage_levels[int((modification.damage / self.blocks[position].health) * len(damage_levels))], (base_x + x * block_size, base_y + y * block_size - wall_height))

    def damage(self, pos):
        global zones_with_modifications
        modification = self.modifications.get(pos, None)
        if modification is not None:
            modification.damage += 0.25
            modification.last_damage_tick = ticks
            if modification.damage == self.blocks[pos].health:
                del self.modifications[pos]
                if len(self.modifications) == 0:
                    del zones_with_modifications[self]
                return True
        else:
            self.modifications[pos] = Modification()
            zones_with_modifications[self] = True
        return False


class Character:
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.facing = up
        self.frame = 0

    def draw(self, w_o):
        x = self.x + w_o[0]
        y = self.y + w_o[1]
        if self.facing == up:
            pygame.draw.polygon(screen, (0x80, 0xFF, 0x80), [(x, y + player_size), (x + player_size / 2, y), (x + player_size, y + player_size)])
        elif self.facing == right:
            pygame.draw.polygon(screen, (0x80, 0xFF, 0x80), [(x, y + player_size), (x, y), (x + player_size, y + player_size / 2)])
        elif self.facing == down:
            pygame.draw.polygon(screen, (0x80, 0xFF, 0x80), [(x + player_size / 2, y + player_size), (x, y), (x + player_size, y)])
        else:
            pygame.draw.polygon(screen, (0x80, 0xFF, 0x80), [(x, y + player_size / 2), (x + player_size, y), (x + player_size, y + player_size)])


def is_empty(zones, px, py):
    zx = px // zone_size
    zy = py // zone_size
    z = zones.get((zx, zy), None)
    if z is None:
        return False
    return z.blocks[int(zone_size_in_blocks * ((px - (zx * zone_size)) // block_size) + ((py - (zy * zone_size)) // block_size))] == air_block


def test_move(zones, px, py):
    return is_empty(zones, px, py) and is_empty(zones, px, py + player_size) and is_empty(zones, px + player_size, py) and is_empty(zones, px + player_size, py + player_size)


def try_mine(zones, character):
    global inventory, gold
    if character.facing == up:
        px = character.x + player_size // 2
        py = character.y - 5
    elif character.facing == down:
        px = character.x + player_size // 2
        py = character.y + player_size + 5
    elif character.facing == left:
        px = character.x - 5
        py = character.y + player_size // 2
    else:
        px = character.x + player_size + 5
        py = character.y + player_size // 2
    zx = px // zone_size
    zy = py // zone_size
    z = zones.get((zx, zy), None)
    if z is None:
        return False
    pos = int(zone_size_in_blocks * ((px - (zx * zone_size)) // block_size) + ((py - (zy * zone_size)) // block_size))
    block = z.blocks[pos]
    # Cannot mine air
    if block == air_block:
        return
    # 'mining' a shop keeper sells blocks
    if block == shopkeeper_block:
        # Sell everything
        for block_type, count in inventory.items():
            gold += count * block_type.value
        # Reset inventory
        inventory = collections.Counter()
        return
    # Mine block
    if z.damage(pos):
        if block.value > 0:
            inventory[z.blocks[pos]] += 1
        z.blocks[pos] = air_block


def random_level():
    # Build random starting zones
    z = {}
    for zx in range(-3, 3):
        for zy in range(-3, 3):
            z[(zx, zy)] = Zone(True, zx, zy)
    # Create spawn area
    zone00 = z[(0, 0)]
    for x in range(3, 6):
        for y in range(3, 6):
            pos = zone_size_in_blocks * x + y
            zone00.blocks[pos] = air_block
            zone00.ground[pos] = spawn_ground
    zone00.blocks[39] = shopkeeper_block
    return z


def save_game(zones, player_x, player_y):
    if not empty_save:
        w = ''
        for i in zones:
            w += 'ZONE %s %s' % (i[0], i[1])
            for block in zones[i].blocks:
                w += ' %s' % block_types.index(block)
            for ground in zones[i].ground:
                w += ' %s' % ground_types.index(ground)
            w += '\n'
        w += 'PLAYER %s %s\n' % (player_x, player_y)
        w += 'GOLD %s' % gold
        q = '\nINVENTORY'
        for item in inventory:
            q += ' %s:%s' % (block_types.index(item), inventory[item])
        w += '%s\n' % q
        open('/home/xander/Documents/openevening/minergame/save-game.sav', 'w').write(w)


def load_game():
    global gold
    file = open('/home/xander/Documents/openevening/minergame/save-game.sav', 'r').read()
    plr = Character(((zone_size // 2) - .5 * player_size, (zone_size // 2) - .5 * player_size))
    if file != '':
        zns = {}
        for line in file.splitlines():
            line = line.split()
            initial = line[0]
            values = line[1:3]
            line = line[3:]
            if initial == 'ZONE':
                blocks = []
                ground = []
                for block in line[0:81]:
                    block = int(block)
                    blocks.append(block_types[block])
                for g in line[81:162]:
                    g = int(g)
                    ground.append(ground_types[g])
                zns[(int(values[0]), int(values[1]))] = Zone(False, blocks=blocks, ground=ground)
            elif initial == 'PLAYER':
                plr = Character((float(values[0]), float(values[1])))
            elif initial == 'GOLD':
                gold = int(values[0])
            elif initial == 'INVENTORY':
                for item in values+line:
                    item = item.split(':')
                    inventory[block_types[int(item[0])]] = int(item[1])
    else:
        zns = random_level()
    return zns, plr


def mainloop():
    global ticks
    zones, player = load_game()
    clock = pygame.time.Clock()
    done = False
    while not done:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        keys = pygame.key.get_pressed()
        # Work out which way the player wants to move based on the keys being held
        x_dir = 0
        y_dir = 0
        if keys[pygame.K_s]:
            player.facing = down
            y_dir += 1
        if keys[pygame.K_w]:
            player.facing = up
            y_dir -= 1
        if keys[pygame.K_d]:
            player.facing = right
            x_dir += 1
        if keys[pygame.K_a]:
            player.facing = left
            x_dir -= 1
        if keys[pygame.K_SPACE]:
            try_mine(zones, player)
        if x_dir != 0 or y_dir != 0:
            # Try mining the block being looked at
            # Work out how far the player can move in x and y
            active_move_distance = move_distance
            if x_dir != 0 and y_dir != 0:
                active_move_distance = diagonal_move_distance
            x_move = x_dir * active_move_distance
            y_move = y_dir * active_move_distance
            # Try and move the player
            if test_move(zones, player.x + x_move, player.y):
                player.x += x_move
            if test_move(zones, player.x, player.y + y_move):
                player.y += y_move
        # Heal damage
        for zone in list(zones_with_modifications.keys()):
            for pos, modification in list(zone.modifications.items()):
                if ticks - modification.last_damage_tick > 20:
                    modification.damage -= 2
                    if modification.damage <= 0:
                        del zone.modifications[pos]
            if len(zone.modifications) == 0:
                del zones_with_modifications[zone]
        # Calculate world offset
        world_offset = ((screen_size - player_size) // 2 - player.x, (screen_size - player_size) // 2 - player.y)
        # Work out which zones to render
        z_min = (math.floor(-world_offset[0] / zone_size), math.floor(-world_offset[1] / zone_size))
        z_max = (math.floor((-world_offset[0] + screen_size + wall_height) / zone_size), math.floor((-world_offset[1] + screen_size + wall_height) / zone_size))
        # Draw world
        for zx in range(z_min[0], z_max[0] + 1):
            for zy in range(z_min[1], z_max[1] + 1):
                zone = zones.get((zx, zy), None)
                if zone is None:
                    zone = Zone(True, zx, zy)
                    zones[(zx, zy)] = zone
                zone.draw_floor_and_sides(zones, zx, zy, world_offset[0] + (zx * zone_size), world_offset[1] + (zy * zone_size))
        player.draw(world_offset)
        for zx in range(z_min[0], z_max[0] + 1):
            for zy in range(z_min[1], z_max[1] + 1):
                zone = zones[zx, zy]
                zone.draw_tops(world_offset[0] + (zx * zone_size), world_offset[1] + (zy * zone_size))
                zone.draw_damage(world_offset[0] + (zx * zone_size), world_offset[1] + (zy * zone_size))
        # Draw UI
        # screen.blit(fnt.render(str(int(clock.get_fps())), False, (255, 255, 255)), (0, 0))
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, 150, 150))
        screen.blit(fnt.render("u " + str(gold), True, (255, 255, 0)), (0, 0))
        ui_y = 30
        for block_type in block_types:
            if block_type.value > 0:
                pygame.draw.rect(screen, block_type.top_color, (10, ui_y + 5, 10, 10))
                screen.blit(fnt.render(str(inventory[block_type]), True, (255, 255, 0)), (30, ui_y))
                ui_y += 30
        pygame.display.flip()
        clock.tick(60)
        ticks += 1
    save_game(zones, player.x, player.y)


pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((screen_size, screen_size))
pygame.display.set_caption('Mining Game')
pygame.display.set_icon(pygame.image.load('./icon.png'))
mainloop()
