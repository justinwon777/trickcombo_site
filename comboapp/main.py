import random
from .combo_setup import *

dev = False

def calc_landing(trick, landing):
    if trick.landing == right:
        land_leg = right
        if trick.hook:
            if landing == hyper:
                land_leg = left
        else:
            if landing == mega:
                land_leg = left
    else:
        land_leg = left
        if landing == hyper:
            land_leg = right
        elif landing == semi:
            land_leg = right
    return land_leg

def pick_trick(transition, prev_trick, prev_landing, trick_set):
    if transition.name == None:
        return all_tricks[trick_set[random.randint(0, len(trick_set) - 1)]]
    if transition == punch or transition == pop:
        trick = all_tricks[trick_set[random.randint(0, len(trick_set) - 1)]]
        while both not in trick.takeoff:
            trick = all_tricks[trick_set[random.randint(0, len(trick_set) - 1)]]
        return trick
    land_leg = calc_landing(prev_trick, prev_landing)
    if land_leg == right:
        if transition == vanish:
            takeoff_leg = left
        else:
            takeoff_leg = right
    elif land_leg == left:
        if transition == vanish:
            takeoff_leg = right
        else:
            takeoff_leg = left
    # print(prev_trick.name, prev_landing.name, land_leg, transition.name, takeoff_leg)
    valid = False
    while not valid:
        trick = all_tricks[trick_set[random.randint(0, len(trick_set) - 1)]]
        if trick.vert:
            if takeoff_leg == left and transition == swing and transition in trick.transitions and takeoff_leg in trick.takeoff:
                valid = True
            elif takeoff_leg == right and transition != swing and transition in trick.transitions and takeoff_leg in trick.takeoff:
                valid = True
            elif takeoff_leg == left and trick.name == 'skip hook':
                valid = True
            else:
                valid = False
        else:
            if takeoff_leg in trick.takeoff and transition in trick.transitions:
                valid = True
            else:
                valid = False

    # print(prev_trick.name, prev_landing.name, land_leg, transition.name, takeoff_leg, trick.name)

    return trick

def pick_transition(prev_trick, prev_landing, trick_set, transition_set):
    # print(prev_trick.name, prev_landing.name)
    land_leg = calc_landing(prev_trick, prev_landing)
    options = all_stances_dict[prev_landing.name].transitions
    valid = False
    while not valid:
        transition = options[random.randint(0, len(options) - 1)]
        if transition in transition_set:
            if land_leg == right:
                if transition == swing:
                    valid = False
                else:
                    valid = True
            elif land_leg == left:
                if transition == wrap:
                    valid = False
                else:
                    valid = True
            elif prev_landing == complete:
                if transition == pop or transition == punch:
                    valid = True
                else:
                    valid = False
        else:
            valid = False
    return transition

def kick_label(trick, transition):
    if transition.name == None and trick.name != 'hook' and trick.name != 'skip hook':
        label = 'pop ' + trick.name
    elif transition == vanish or transition == redirect:
        if trick.name not in ['tornado', '540', 'hook', 'jackknife', 'skip hook']:
            label = 'cheat ' + trick.name
        else:
            label = trick.name
    else:
        label = trick.name
    return label

def generate(set_name, stances, length):
    trick_set = trick_sets[set_name]
    transition_set = transition_sets[set_name]
    stance_set = stances
    combo = ''
    full_combo = ''
    prev_landing = Stance(None, [])
    prev_trick = Trick(None, None, None, [], [], [False, False, False])
    transition = Transition(None)
    # trick = Trick(None, None, None, [], [], [False, False, False])
    # landing = Stance(None, [])

    for i in range(length):
        if i != 0:
            transition = pick_transition(prev_trick, prev_landing, trick_set, transition_set)
            combo += transition.name + ' '
            full_combo += transition.name + ' '
        trick = pick_trick(transition, prev_trick, prev_landing, trick_set)
        if trick.vert:
            combo += kick_label(trick, transition) + ' '
            full_combo += kick_label(trick, transition) + ' '
        else:
            combo += trick.name + ' '
            full_combo += trick.name + ' '
        landing = trick.stances[random.randint(0, len(trick.stances) - 1)]
        while landing.name not in stance_set:
            landing = trick.stances[random.randint(0, len(trick.stances) - 1)]
        land_leg = calc_landing(trick, landing)
        same = False
        if land_leg == right and trick.landing == right:
            same = True
        if landing != complete:
            if landing != hyper or not same:
                if trick.hook or not trick.kick:
                    if i == length - 1:
                        combo += landing.name
                    else:
                        combo += landing.name + ' '
                elif trick.round and landing == semi:
                    if i == length - 1:
                        combo += landing.name
                    else:
                        combo += landing.name + ' '
        if i == length - 1:
            full_combo += landing.name
        else:
            full_combo += landing.name + ' '
        # print(i, prev_landing.name, prev_trick.name, transition.name, trick.name, landing.name)
        prev_trick = trick
        prev_landing = landing
    return combo


if dev:
    all = 'all'
    lk = 'lk_funds'
    vert = 'vert'
    combo = generate(lk)
    print(combo)
    # print(full)