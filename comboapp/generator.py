import random
import pandas as pd
import os
from pathlib import Path

base_path = Path(__file__).parent
loc = (base_path / "tricks_master.xlsx").resolve()
stances = {
    'complete_lb': ['punch', 'pop', 'backside', 'vanish_r', 'redirect_l', 'swing', 'reversal_l'],
    'complete_lf': ['punch', 'pop', 'backside', 'vanish_r', 'redirect_l', 'reversal_l'],
    'complete_r': ['punch', 'pop', 'backside', 'vanish_l', 'redirect_r', 'reversal_r'],
    'hyper': ['pop', 'backside', 'vanish_l', 'redirect_r', 'wrap', 'missleg_r', 'reversal_r'],
    'hyper_k': ['pop', 'backside', 'vanish_r', 'redirect_l', 'swing', 'missleg_l', 'reversal_l'],
    'mega': ['pop', 'backside', 'vanish_r', 'redirect_l', 'frontswing_l', 'missleg_l', 'reversal_l'],
    'semi': ['pop', 'backside', 'vanish_l', 'redirect_r', 'frontswing_r', 'reversal_r']

}
transitions = {
    'punch': [],
    'pop': [],
    'vanish_l': [],
    'vanish_r': [],
    'redirect_l': [],
    'redirect_r': [],
    'reversal_l': [],
    'reversal_r': [],
    'swing': [],
    'wrap': [],
    'frontswing_l': [],
    'frontswing_r': [],
    'missleg_l': [],
    'missleg_r': [],
    'backside': [],
}
tricks = {}
start = {'start': []}
all_stances = list(stances.keys())
all_transitions = list(transitions.keys())
land_right_nohook = []
scissor = []
common = []
challenge = []
spins = [
    ['zero'],
    ['one'],
    ['two'],
    ['three'],
    ['four']
]
types = ['vert', 'flatspin', 'backward', 'forward', 'outside', 'inside', 'other']
tricks_by_type = {
    'vert': [],
    'flatspin': [],
    'backward': [],
    'forward': [],
    'outside': [],
    'inside': [],
    'other': []
}
common_tricks_by_type = {
    'vert': [],
    'flatspin': [],
    'backward': [],
    'forward': [],
    'outside': [],
    'inside': [],
    'other': []
}

for j in range(7):
    df = pd.read_excel(loc, engine='openpyxl', sheet_name=j).to_numpy()
    for row in df:
        if row[1] == 1 or row[1] == 0:
            start['start'].append(str(row[0]))
            tricks_by_type[types[j]].append(str(row[0]))
            trick_stances = []
            for i in range(len(row)):
                if 1 <= i <= 7:
                    if row[i] == 1:
                        trick_stances.append(all_stances[i - 1])
                if 8 <= i <= 21:
                    if row[i] == 1:
                        transitions[all_transitions[i - 8]].append(str(row[0]))
                if i == 22:
                    if row[i] == 1:
                        land_right_nohook.append(str(row[0]))
                if i == 23:
                    if row[i] == 1:
                        scissor.append(str(row[0]))
                if i == 24:
                    if row[i] == 1:
                        common.append(str(row[0]))
                        common_tricks_by_type[types[j]].append(str(row[0]))
                    else:
                        challenge.append(str(row[0]))
                if i == 25:
                    spins[int(row[i])].append(str(row[0]))
                if i == 26:
                    if row[i] == 1:
                        transitions['backside'].append(str(row[0]))
            tricks[str(row[0])] = trick_stances

total = stances
total.update(transitions)
total.update(tricks)
total.update(start)

lk_funds = ['cartwheel', 'tornado', 'scoot', 'skip hook', 'butterfly kick', 'aerial', 'front tuck', 'gainer', 'raiz',
            'back tuck']
vert_kicks = ['roundhouse', 'hook', 'skip hook', 'tornado', 'flick flack', 'feilong', 'crowd awakener', 'parafuso',
              'wackknife', '540', '720', 'jackknife', '900', '1080', '1260']

all_tricks_list = list(tricks.keys())
trick_sets = {'all': all_tricks_list, 'lk_funds': lk_funds, 'vert': vert_kicks, 'common': common,
              'challenge': challenge}


def find_all_paths(pool, start_move, length, paths, path=None):
    if path is None:
        path = []
    path = path + [start_move]
    if len(path) == length:
        paths.append(path)
        # print(path)
        if len(paths) % 1000000 == 0:
            print(len(paths) / 1000000)
    else:
        for node in total[start_move]:
            if node in pool:
                find_all_paths(pool, node, length, paths, path)


def find_path(pool, start_move, length, paths, path=None):
    if path is None:
        path = []
    path = path + [start_move]
    if len(path) == length:
        paths.append(path)
        return True
    else:
        options = []
        for node in total[start_move]:
            if node in pool:
                options.append(node)
        while options:
            next_move = options[random.randint(0, len(options) - 1)]
            options.remove(next_move)
            found = find_path(pool, next_move, length, paths, path)
            if found:
                return True


def find_path_backward(trick_set, transition_set, stance_set, finish, length, paths, path=None):
    if path is None:
        path = ['complete']
    path.insert(0, finish)
    if len(path) == length:
        paths.append(path)
        return True
    else:
        options = []
        if finish in all_tricks_list:
            for transition in transition_set:
                if finish in transitions[transition]:
                    options.append(transition)
        elif finish in all_transitions:
            for stance in stance_set:
                if finish in stances[stance]:
                    options.append(stance)
        elif finish in all_stances:
            for trick in trick_set:
                if finish in tricks[trick]:
                    options.append(trick)
        while options:
            next_move = options[random.randint(0, len(options) - 1)]
            options.remove(next_move)
            found = find_path_backward(trick_set, transition_set, stance_set, next_move, length, paths, path)
            if found:
                return True


def generate_all(length, trick_set, transition_set, stance_set):
    pool = trick_set + transition_set + stance_set
    paths = []
    find_all_paths(pool, 'start', length * 3, paths)
    print(len(paths))
    return


def generate(length, set, stance_set, transition_set, start_trick, finish_trick):
    if 'complete' in stance_set:
        stance_set.append('complete_lb')
        stance_set.append('complete_r')
        stance_set.append('complete_lf')
        stance_set.remove('complete')
    if 'hyper' in stance_set:
        stance_set.append('hyper_k')
    if 'vanish' in transition_set:
        transition_set.append('vanish_r')
        transition_set.append('vanish_l')
        transition_set.remove('vanish')
    if 'redirect' in transition_set:
        transition_set.append('redirect_r')
        transition_set.append('redirect_l')
        transition_set.remove('redirect')
    if 'reversal' in transition_set:
        transition_set.append('reversal_r')
        transition_set.append('reversal_l')
        transition_set.remove('reversal')
    if 'frontswing' in transition_set:
        transition_set.append('frontswing_r')
        transition_set.append('frontswing_l')
        transition_set.remove('frontswing')
    if 'missleg' in transition_set:
        transition_set.append('missleg_r')
        transition_set.append('missleg_l')
        transition_set.remove('missleg')
    pool = set + transition_set + stance_set
    paths = []
    combo = ''
    if start_trick:
        start_idx = 0
        find_path(pool, start_trick[0], length * 3 - 1, paths)
    else:
        start_idx = 1
        if finish_trick:
            for stance in stance_set:
                keep = False
                for trick in set:
                    if stance in tricks[trick]:
                        keep = True
                        break
                if not keep:
                    stance_set.remove(stance)
            for transition in transition_set:
                keep = False
                for stance in stance_set:
                    if transition in stances[stance]:
                        keep = True
                        break
                if not keep:
                    transition_set.remove(transition)
            for trick in set:
                keep = False
                for transition in transition_set:
                    if trick in transitions[transition]:
                        keep = True
                        break
                if not keep:
                    set.remove(trick)
            find_path_backward(set, transition_set, stance_set, finish_trick[0], length * 3 - 1, paths)
        else:
            find_path(pool, 'start', length * 3, paths)
    if len(paths) == 0:
        return 'No valid combos', 'No valid combos'
    if finish_trick:
        paths[0].insert(0, 'start')
    path = paths[0]
    long = full_name(path)
    long_copy = long.copy()
    short = short_name(long)
    for i in range(start_idx, len(short)):
        if i == start_idx:
            combo += short[i]
        else:
            combo += ' ' + short[i]
    if start_idx == 1:
        long_copy.remove('start')
    return combo, long_copy


def full_name(path):
    for i in range(len(path)):
        if 'complete' in path[i]:
            path[i] = 'complete'
        elif 'vanish' in path[i]:
            path[i] = 'vanish'
        elif 'redirect' in path[i]:
            path[i] = 'redirect'
        elif 'reversal' in path[i]:
            path[i] = 'reversal'
        elif 'frontswing' in path[i]:
            path[i] = 'frontswing'
        elif 'missleg' in path[i]:
            path[i] = 'missleg'
        elif 'hyper_k' in path[i]:
            path[i] = 'hyper'
    return path


def short_name(path):
    path[:] = [x for x in path if x != 'complete']
    for i in range(len(path)):
        if path[i] == 'hyper':
            if path[i - 1] in land_right_nohook:
                path[i] = 'remove'
        if path[i] == 'mega':
            if path[i - 1] in scissor:
                path[i] = 'remove'
    path[:] = [x for x in path if x != 'remove']
    return path


def string_to_list(combo_str):
    t = ['punch', 'pop', 'vanish', 'redirect', 'reversal', 'swing', 'wrap', 'frontswing', 'missleg', 'backside']
    s = ['complete', 'hyper', 'mega', 'semi']
    split_combo = combo_str.split()
    combo_list = []
    marked = 0
    for i in range(len(split_combo)):
        if split_combo[i] not in t and split_combo[i] not in s:
            marked += 1
        else:
            marked = 0
            combo_list.append(split_combo[i])
        if i != len(split_combo) - 1:
            if split_combo[i + 1] in t or split_combo[i + 1] in s:
                if marked != 0:
                    trick = ''
                    for j in range(marked, 0, -1):
                        if j == marked:
                            trick += split_combo[i - j + 1]
                        else:
                            trick += ' ' + split_combo[i - j + 1]
                    combo_list.append(trick)
        if i == len(split_combo) - 1:
            if split_combo[i] not in t and split_combo[i] not in s:
                if marked != 0:
                    trick = ''
                    for j in range(marked, 0, -1):
                        if j == marked:
                            trick += split_combo[i - j + 1]
                        else:
                            trick += ' ' + split_combo[i - j + 1]
                    combo_list.append(trick)
    combo_list[:] = [x for x in combo_list if x != '']

    return combo_list


def regenerate_combo(prev2, prev, curr, next, idx, set, stances, transitions, full_list):
    if curr in all_tricks_list:
        if idx == 0:
            for stance in tricks[curr]:
                if next in stance:
                    next = stance
                    break
        else:
            for stance in total[curr]:
                if next in stance:
                    next = stance
                    break
            for transition in all_transitions:
                if prev in transition:
                    if curr in total[transition]:
                        prev = transition
                        break
    elif curr in ['complete', 'hyper', 'mega', 'semi']:
        if idx != len(full_list) - 1:
            for stance in tricks[prev]:
                if curr in stance:
                    curr = stance
                    break
            for transition in total[curr]:
                if next in transition:
                    next = transition
                    break
        else:
            for stance in tricks[prev]:
                if curr in stance:
                    curr = stance
                    break
    else:
        for transition in all_transitions:
            if curr in transition:
                if next in total[transition]:
                    curr = transition
                    break
        for stance in tricks[prev2]:
            if prev in stance:
                prev = stance
                break
    if 'complete' in stances:
        stances.append('complete_lb')
        stances.append('complete_r')
        stances.append('complete_lf')
        stances.remove('complete')
    if 'hyper' in stances:
        stances.append('hyper_k')
    if 'vanish' in transitions:
        transitions.append('vanish_r')
        transitions.append('vanish_l')
        transitions.remove('vanish')
    if 'redirect' in transitions:
        transitions.append('redirect_r')
        transitions.append('redirect_l')
        transitions.remove('redirect')
    if 'reversal' in transitions:
        transitions.append('reversal_r')
        transitions.append('reversal_l')
        transitions.remove('reversal')
    if 'frontswing' in transitions:
        transitions.append('frontswing_r')
        transitions.append('frontswing_l')
        transitions.remove('frontswing')
    if 'missleg' in transitions:
        transitions.append('missleg_r')
        transitions.append('missleg_l')
        transitions.remove('missleg')
    pool = set + transitions + stances
    new_part = ''
    if idx == 0:
        options = [curr]
        for option in total['start']:
            if option in pool and option not in options:
                options.append(option)
        found = False
        while not found:
            potential = options[random.randint(0, len(options) - 1)]
            if next in total[potential]:
                new_part = potential
                found = True
                if len(options) > 1:
                    if curr in potential:
                        found = False
            else:
                options.remove(potential)
    elif idx == len(full_list) - 1:
        options = [curr]
        for option in tricks[prev]:
            if option in stances and option not in options:
                options.append(option)
        if len(options) > 1:
            options.remove(curr)
        new_part = options[random.randint(0, len(options) - 1)]
    else:
        options = [curr]
        for option in total[prev]:
            if option in pool and option not in options:
                options.append(option)
        found = False
        while not found:
            potential = options[random.randint(0, len(options) - 1)]
            if next in total[potential]:
                new_part = potential
                found = True
                if len(options) > 1:
                    if curr in potential:
                        found = False
            else:
                options.remove(potential)
    full_list[idx] = new_part
    full_list = full_name(full_list)
    new_part = full_list[idx]
    short_list = short_name(full_list)
    new_combo = ''
    for i in range(len(short_list)):
        if i == 0:
            new_combo += short_list[i]
        else:
            new_combo += ' ' + short_list[i]
    return new_combo, new_part


def short_to_full(combo):
    t = ['punch', 'pop', 'vanish', 'redirect', 'reversal', 'swing', 'wrap', 'frontswing', 'missleg', 'backside']
    s = ['complete', 'hyper', 'mega', 'semi']
    combo_list = string_to_list(combo)
    full_list = []
    prev = 'start'
    for i in range(len(combo_list)):
        if combo_list[i] in all_tricks_list:
            full_list.append(combo_list[i])
            prev = combo_list[i]
        elif combo_list[i] in s:
            full_list.append(combo_list[i])
            prev = combo_list[i]
        elif combo_list[i] in t and prev in s:
            full_list.append(combo_list[i])
            prev = combo_list[i]
        else:
            options = []
            for option in tricks[prev]:
                for transition in total[option]:
                    if combo_list[i] in transition:
                        options.append(option)
            if 'semi' in options:
                options.remove('semi')
            if prev not in land_right_nohook:
                if 'hyper' in options:
                    options.remove('hyper')
            if prev not in scissor:
                if 'mega' in options:
                    options.remove('mega')
            stance = options[random.randint(0, len(options) - 1)]
            full_list.append(stance)
            full_list.append(combo_list[i])
    if combo_list[len(combo_list) - 1] in all_tricks_list:
        full_list.append('complete')
    full_list = full_name(full_list)
    return full_list


total_1 = 258
total_2 = 139359
total_3 = 75396572
# print(total_1 + total_2 + total_3)
# generate_all(1, ['540'], all_transitions, all_stances)
# combo, c_list = generate(3, all_tricks_list, all_stances, all_transitions, ['540'], [])
# print(combo)
