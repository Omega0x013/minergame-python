class BlockType:
    def __init__(self, top_color, side_color, health, value):
        self.top_color = top_color
        self.side_color = side_color
        self.health = health / 10
        self.max_health = health / 10
        self.value = value
class GroundType:
    def __init__(self, color):
        self.color = color
stone_block = BlockType((0x80, 0x80, 0x80), (0x40, 0x40, 0x40), health=30, value=0)
emerald_block = BlockType((54, 206, 68), (54 / 2, 206 / 2, 68 / 2), health=90, value=50)
sapphire_block = BlockType((0, 0, 200), (0, 0, 100), health=60, value=30)
ruby_block = BlockType((200, 0, 0), (100, 0, 0), health=50, value=20)
coal_block = BlockType((40, 40, 40), (20, 20, 20), health=40, value=10)
air_block = BlockType((0, 0, 0, 0), (0, 0, 0, 0), health=0, value=0)
shopkeeper_block = BlockType((101, 28, 130), (53, 14, 68), health=0, value=0)
block_types = [stone_block, air_block, emerald_block, sapphire_block, ruby_block, coal_block, shopkeeper_block]
dirt_ground = GroundType((0x95, 0x4B, 0x33))
stone_ground = GroundType((77, 77, 77))
spawn_ground = GroundType((128, 204, 255))
ground_types = [dirt_ground, stone_ground, spawn_ground]
rings = [
    [
        (0.2, air_block),
        (0.05, coal_block)
    ],
    [
        (0.15, air_block),
        (0.01, ruby_block),
        (0.05, coal_block)
    ],
    [
        (0.10, air_block),
        (0.02, ruby_block),
        (0.01, sapphire_block),
        (0.05, coal_block)
    ],
    [
        (0.05, air_block),
        (0.03, ruby_block),
        (0.02, sapphire_block),
        (0.05, coal_block)
    ],
    [
        (0.02, ruby_block),
        (0.03, sapphire_block),
        (0.05, coal_block)
    ],
    [
        (0.01, ruby_block),
        (0.03, coal_block),
        (0.05, sapphire_block),
        (0.005, emerald_block)
    ],
    [
        (0.02, ruby_block),
        (0.03, sapphire_block),
        (0.01, emerald_block)
    ],
    [
        (0.01, ruby_block),
        (0.02, sapphire_block),
        (0.02, emerald_block)
    ],
    [
        (0.01, sapphire_block),
        (0.03, emerald_block)
    ],
    [
        (0.005, sapphire_block),
        (0.04, emerald_block),
    ],
    [
        (0.05, emerald_block)
    ],
    [
        (0.06, emerald_block)
    ],
    [
        (0.07, emerald_block)
    ],
    [
        (0.08, emerald_block)
    ],
    [
        (0.1, emerald_block),
        (0.05, sapphire_block),
        (0.03, ruby_block),
        (0.01, coal_block)
    ],
    [
        (0.125, emerald_block),
        (0.075, sapphire_block),
        (0.05, ruby_block),
        (0.025, coal_block)
    ],
    [
        (0.15, emerald_block),
        (0.1, sapphire_block),
        (0.075, ruby_block),
        (0.05, coal_block)
    ],
    [
        (0.175, emerald_block),
        (0.125, sapphire_block),
        (0.1, ruby_block),
        (0.075, coal_block)
    ],
    [
        (0.2, emerald_block),
        (0.15, sapphire_block),
        (0.125, ruby_block),
        (0.1, coal_block)
    ],
    [
        (0.2, emerald_block),
        (0.175, sapphire_block),
        (0.15, ruby_block),
        (0.125, coal_block)
    ],
    [
        (0.2, emerald_block),
        (0.2, sapphire_block),
        (0.175, ruby_block),
        (0.15, coal_block)
    ],
    [
        (0.2, emerald_block),
        (0.2, sapphire_block),
        (0.2, ruby_block),
        (0.175, coal_block)
    ],
    [
        (0.2, emerald_block),
        (0.2, sapphire_block),
        (0.2, ruby_block),
        (0.2, coal_block)
    ],
    [
        (0.25, emerald_block),
        (0.25, sapphire_block),
        (0.25, ruby_block),
        (0.25, coal_block)
    ],
    [
        (0.33, emerald_block),
        (0.33, sapphire_block),
        (0.33, ruby_block)
    ],
    [
        (0.5, emerald_block),
        (0.5, sapphire_block)
    ],
    [
        (1, emerald_block)
    ]
]