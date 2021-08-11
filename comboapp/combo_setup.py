# not being used

class Trick:
    def __init__(self, name, takeoff, landing, transitions, stances, kick, vert=False):
        self.name = name
        self.takeoff = takeoff
        self.landing = landing
        self.transitions = transitions
        self.stances = stances
        self.kick = kick[0]
        self.hook = kick[1]
        self.round = kick[2]
        self.vert = vert

class Transition:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        if self.name == other.name:
            return True
        else:
            return False

class Stance:
    def __init__(self, name, transitions):
        self.name = name
        self.transitions = transitions

    def __eq__(self, other):
        if self.name == other.name:
            return True
        else:
            return False

right = 'right'
left = 'left'
both = 'both'

punch = Transition('punch')
pop = Transition('pop')
vanish = Transition('vanish')
redirect = Transition('redirect')
swing = Transition('swing')
wrap = Transition('wrap')
front = Transition('frontswing')
miss = Transition('missleg')
complete = Stance('complete', [punch, pop, vanish, redirect, swing])
hyper = Stance('hyper', [wrap, vanish, redirect, miss, swing])
mega = Stance('mega', [front, vanish, redirect, miss])
semi = Stance('semi', [front])
all_tricks = {}

#transition sets
all_transitions = [punch, pop, vanish, redirect, swing, wrap, front, miss]
vert_transitions = [pop, vanish, redirect, swing, wrap, front, miss]
lk_transitions = [punch, pop, vanish, redirect, swing, wrap, front]
transition_sets = {'all': all_transitions, 'lk_funds': lk_transitions, 'vert': vert_transitions}

#stance sets
all_stances_dict = {'complete': complete, 'hyper': hyper, 'mega': mega, 'semi': semi}
all_stances = [complete, hyper, mega, semi]

round = [True, False, True]
hook = [True, True, False]
nokick = [False, False, False]

# vert kicks
all_tricks['hook'] = Trick('hook', right, right, [vanish, redirect, miss], [complete, semi], hook, True)
all_tricks['skip hook'] = Trick('skip hook', left, right, [vanish, redirect, miss, swing], [complete, hyper, semi], hook, True)
all_tricks['tornado'] = Trick('tornado', [both, right], left, [punch, pop, vanish, redirect, wrap], [complete], round, True)
all_tricks['540'] = Trick('540', [both, right], right, [punch, pop, vanish, redirect, wrap], [complete, hyper, semi], round, True)
all_tricks['720'] = Trick('720', [both, right, left], right, [punch, pop, vanish, redirect, wrap, swing], [complete, hyper, semi], hook, True)
all_tricks['jackknife'] = Trick('jackknife', [both, right], right, [punch, pop, vanish, redirect, wrap], [complete, hyper, semi], hook, True)
all_tricks['900'] = Trick('900', [both, right, left], left, [punch, pop, vanish, redirect, wrap, swing], [complete, hyper, semi], round, True)
all_tricks['1080'] = Trick('1080', [both, right, left], right, [punch, pop, vanish, redirect, wrap, swing], [complete, hyper, semi], hook, True)

# flatspin flips
all_tricks['butterfly kick'] = Trick('butterfly kick', left, right, [vanish, redirect, front], all_stances, nokick)
all_tricks['butter knife'] = Trick('butter knife', left, right, [vanish, redirect, front], [complete, hyper, semi], hook)
all_tricks['spyder'] = Trick('spyder', right, left, [vanish, redirect, front], all_stances, nokick)
all_tricks['janitor'] = Trick('janitor', both, left, [punch, pop], all_stances, nokick)

# flatspin twists
all_tricks['butterfly twist'] = Trick('butterfly twist', left, left, [vanish, redirect, front], all_stances, nokick)

# backwards flips
all_tricks['back tuck'] = Trick('back tuck', both, left, [punch, pop], all_stances, nokick)
all_tricks['back handspring'] = Trick('back handspring', both, left, [punch, pop], all_stances, nokick)
all_tricks['arabian'] = Trick('arabian', both, right, [punch, pop], all_stances, nokick)
all_tricks['gainer'] = Trick('gainer', left, right, [vanish, redirect, swing], all_stances, nokick)
all_tricks['gainer switch'] = Trick('gainer switch', left, left, [vanish, redirect, swing], [complete], nokick)
all_tricks['moonkick'] = Trick('moonkick', left, right, [vanish, redirect, swing], [complete, hyper, semi], hook)
all_tricks['flashkick'] = Trick('flashkick', both, right, [punch, pop], all_stances, nokick)

# backwards twists
all_tricks['cork'] = Trick('cork', left, left, [vanish, redirect, swing], all_stances, nokick)

# forward flips
all_tricks['front tuck'] = Trick('front tuck', both, right, [punch, pop], all_stances, nokick)
all_tricks['webster'] = Trick('webster', right, left, [vanish, redirect, front, miss], [complete, mega, semi], nokick)

# forward twists

# outside flips
all_tricks['raiz'] = Trick('raiz', right, left, [vanish, redirect, front], [complete], nokick)
all_tricks['touchdown raiz'] = Trick('touchdown raiz', right, left, [vanish, redirect, front], [complete], nokick)
all_tricks['gumbi'] = Trick('gumbi', right, left, [vanish, redirect, front], [complete], nokick)
all_tricks['sideswipe'] = Trick('sideswipe', right, right, [vanish, redirect, front], [complete], round)

# outside twists
all_tricks['cheat 720 twist'] = Trick('cheat 720 twist', right, left, [vanish, redirect, front], all_stances, nokick)

# inside flips
all_tricks['aerial'] = Trick('aerial', left, right, [vanish, redirect, front, miss], all_stances, nokick)
all_tricks['aerial hook'] = Trick('aerial hook', left, right, [vanish, redirect, front, miss], [complete, hyper, semi], hook)
all_tricks['cartwheel'] = Trick('cartwheel', left, right, [vanish, redirect, front, miss], all_stances, nokick)
all_tricks['scoot'] = Trick('scoot', right, left, [vanish, redirect, miss], [complete, hyper], nokick)
all_tricks['masterscoot'] = Trick('masterscoot', right, left, [vanish, redirect, miss], [complete, hyper], nokick)

# inside twists
all_tricks['tak full'] = Trick('tak full', right, left, [vanish, redirect], all_stances, nokick)

#other
all_tricks['side flip'] = Trick('side flip', both, right, [punch, pop], all_stances, nokick)

#trick sets
lk_funds = ['cartwheel', 'tornado', 'scoot', 'skip hook', 'butterfly kick', 'aerial', 'front tuck', 'gainer', 'raiz', 'back tuck']
vert_kicks = ['hook', 'skip hook', 'tornado', '540', '720', 'jackknife', '900', '1080']
all_tricks_list = list(all_tricks.keys())
trick_sets = {'all': all_tricks_list, 'lk_funds': lk_funds, 'vert': vert_kicks}