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
hyper = Stance('hyper', [wrap, vanish, redirect, miss])
mega = Stance('mega', [front, vanish, redirect, miss])
semi = Stance('semi', [front])
all_transitions = [punch, pop, vanish, redirect, swing, wrap, front]
all_stances_dict = {'complete': complete, 'hyper': hyper, 'mega': mega, 'semi': semi}
all_stances = [complete, hyper, mega, semi]
all_tricks = []

round = [True, False, True]
hook = [True, True, False]
nokick = [False, False, False]

# vert kicks
all_tricks.append(Trick('tornado', [both, right], left, [punch, pop, vanish, redirect, wrap], [complete], round, True))
all_tricks.append(Trick('540', [both, right], right, [punch, pop, vanish, redirect, wrap], [complete, hyper, semi], round, True))
all_tricks.append(Trick('720', [both, right, left], right, [punch, pop, vanish, redirect, wrap, swing], [complete, hyper, semi], hook, True))
all_tricks.append(Trick('jackknife', [both, right], right, [punch, pop, vanish, redirect, wrap], [complete, hyper, semi], hook, True))
all_tricks.append(Trick('900', [both, right, left], left, [punch, pop, vanish, redirect, wrap, swing], [complete, hyper, semi], round, True))
all_tricks.append(Trick('1080', [both, right, left], right, [punch, pop, vanish, redirect, wrap, swing], [complete, hyper, semi], hook, True))

# flatspin flips
all_tricks.append(Trick('butterfly kick', left, right, [vanish, redirect, front], all_stances, nokick))

# flatspin twists
all_tricks.append(Trick('butterfly twist', left, left, [vanish, redirect, front], all_stances, nokick))

# backwards flips
all_tricks.append(Trick('back tuck', both, left, [punch, pop], all_stances, nokick))

# backwards twists
all_tricks.append(Trick('cork', left, left, [vanish, redirect, swing], all_stances, nokick))

# forward flips
all_tricks.append(Trick('front tuck', both, right, [punch, pop], all_stances, nokick))
all_tricks.append(Trick('webster', right, left, [vanish, redirect, front, miss], [complete, mega, semi], nokick))

# forward twists

# outside flips
all_tricks.append(Trick('raiz', right, left, [vanish, redirect, front], [complete], nokick))
all_tricks.append(Trick('touchdown raiz', right, left, [vanish, redirect, front], [complete], nokick))
all_tricks.append(Trick('gumbi', right, left, [vanish, redirect, front], [complete], nokick))
all_tricks.append(Trick('sideswipe', right, right, [vanish, redirect, front], [complete], round))

# outside twists
all_tricks.append(Trick('cheat 720 twist', right, left, [vanish, redirect, front], all_stances, nokick))

# inside flips
all_tricks.append(Trick('aerial', left, right, [vanish, redirect, front, miss], all_stances, nokick))
all_tricks.append(Trick('aerial hook', left, right, [vanish, redirect, front, miss], [complete, hyper, semi], hook))
all_tricks.append(Trick('cartwheel', left, right, [vanish, redirect, front, miss], all_stances, nokick))
all_tricks.append(Trick('scoot', right, left, [vanish, redirect], [complete, hyper], nokick))
all_tricks.append(Trick('masterscoot', right, left, [vanish, redirect], [complete, hyper], nokick))

# inside twists
all_tricks.append(Trick('tak full', right, left, [vanish, redirect], all_stances, nokick))