from npc import Enemy, Ally

locations = {
    'player_hideout': {
        'name': "Cramped Bolt-hole", 'description': "This cramped, easily overlooked space is your only sanctuary in The Shambles. The air is heavy with the scent of dust and damp stone. A single, rickety door offers a flimsy barrier to the dangers outside. It's not much, but it's yours to protect.",
        'description_level_1': "With some effort, you've reinforced the door and cleared away the worst of the grime. A small, somewhat cleaner space in one corner serves as a crude bed. It feels a little safer now, a proper bolt-hole against the threats of the city.",
        'exits': {'west': 'shambles_alley'}, 'items': [], 'npcs': [], 'is_hideout': True,
    },
    'old_sewer_tunnel': {
        'name': "Old Sewer Tunnel", 'description': "You descend into a damp, oppressive tunnel beneath The Shambles. The air is thick with the gagging stench of stagnant water, decay, and things best left unnamed. Rats skitter in the oppressive shadows, their tiny claws clicking on the slick stones. A constant, unnerving dripping echoes around you, each drop magnifying the suffocating silence.",
        'exits': {'up': 'shambles_square'}, 'items': ['sealed_package'],
        'npcs': [Enemy("Diseased Rat", 15, 6, 1, "Bloated, red-eyed rat.", loot=['rat_tail'])]
    },
    'shambles_square': {
        'name': "Shambles Square", 'description': "Shambles Square serves as the chaotic heart of this lawless district. The ground is a mess of mud and refuse, churned by countless feet. Dilapidated stalls, some empty, some hawking dubious goods like 'gently used' rags or skewers of 'mystery meat', crowd the edges. The air is a thick soup of smells: rotting vegetables, cheap ale, unwashed bodies, and the faint, metallic tang of desperation. Shouts of vendors, cries of beggars, and the din of occasional scuffles form a constant, unsettling symphony.",
        'exits': {'north': 'shambles_alley', 'east': 'shambles_gate_path', 'south': 'shambles_docks_approach', 'down': 'old_sewer_tunnel', 'west': 'murky_canal_bank'},
        'items': ['tattered_coin_pouch', 'discarded_rags'],
        'npcs': [Ally("Wary Informant", 50, 5, 5, "Shifty figure in rags.", dialogue="Need coin? Get package in sewer. Say 'accept package quest'.")]
    },
    'shambles_alley': {
        'name': "Shadowy Alleyway", 'description': "Narrow, refuse-strewn alley.",
        'exits': {'south': 'shambles_square', 'west': 'tenement_ruin', 'east': 'player_hideout', 'further west': 'shambles_alley_deeper', 'nook': 'shambles_hidden_nook'},
        'items': ['rusty_pipe'], 'npcs': []
    },
    'shambles_alley_deeper': {
        'name': "Deeper Into The Alley", 'description': "Narrow dead end. Stinks.",
        'exits': {'east': 'shambles_alley'}, 'items': [],
        'npcs': [Enemy("Scrawny Thug", 30, 8, 2, "Wiry thug with a knife.", loot=['5_coins', 'crude_shiv'])]
    },
    'tenement_ruin': {
        'name': "Crumbling Tenement Ruin", 'description': "Burnt-out tenement shell.",
        'exits': {'east': 'shambles_alley'}, 'items': ['charred_wood_plank'],
        'npcs': [Ally("Old Man Hemlock", 20, 1, 0, "Old man in rags.", dialogue="Watch your back.")],
        'features': {
            'wall': "The scorch mark on the wall seems relatively recent. Oddly, it almost resembles a crude, clawed handprint, much larger than any human's.",
            'marking': "The scorch mark on the wall seems relatively recent. Oddly, it almost resembles a crude, clawed handprint, much larger than any human's.",
            'rubble': "Piles of charred beams and broken masonry litter the floor. It looks unstable and dangerous to sift through without care."
        }
    },
    'murky_canal_bank': {
        'name': "Murky Canal Bank", 'description': "Slippery bank by polluted canal.",
        'exits': {'east': 'shambles_square'}, 'items': ['broken_bottle'], 'npcs': []
    },
    'shambles_hidden_nook': {
        'name': "Hidden Nook", 'description': "Concealed space behind crates.",
        'exits': {'south': 'shambles_alley'}, 'items': [],
        'npcs': [Ally("Old Hermit", 20, 2, 2, "Muttering old man.", dialogue="Rats whisper secrets.")]
    },
   'shambles_gate_path': {
        'name': "Path to Veridia Gate", 'description': "Muddy track towards city gate.",
        'exits': {'west': 'shambles_square'}, 'items': [], 'npcs': []
    },
    'shambles_docks_approach': {
        'name': "Approach to Shambles Docks", 'description': "Sodden ground, smells of fish.",
        'exits': {'north': 'shambles_square'}, 'items': ['broken_oar_fragment'], 'npcs': []
    }
}
if 'shambles_alley' in locations and 'shambles_hidden_nook' in locations:
    locations['shambles_alley']['exits']['nook'] = 'shambles_hidden_nook'

items_db = {
    'tattered_coin_pouch': {'name': "Tattered Pouch", 'description': "Empty pouch."},
    'discarded_rags': {'name': "Discarded Rags", 'description': "Filthy cloth."},
    'rusty_pipe': {'name': "Rusty Pipe", 'description': "Heavy pipe weapon."},
    'moldy_bread': {'name': "Moldy Bread", 'description': "Green bread."},
    'rusty_dagger': {'name': "Rusty Dagger", 'description': "Pitted dagger."},
    'broken_oar_fragment': {'name': "Broken Oar", 'description': "Splintered oar piece."},
    'shabby_coin': {'name': "Shabby Coin", 'description': "Worn coin."},
    '5_coins': {'name': "5 Coins", 'description': "Some coins."},
    'crude_shiv': {'name': "Crude Shiv", 'description': "Sharpened metal."},
    'rat_tail': {'name': "Rat Tail", 'description': "A rat tail."},
    'sealed_package': {'name': "Sealed Package", 'description': "Wax-sealed package."},
    'charred_wood_plank': {'name': "Charred Plank", 'description': "Burnt plank."},
    'broken_bottle': {'name': "Broken Bottle", 'description': "Jagged glass."}
}
