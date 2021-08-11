from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .generator import generate, trick_sets, tricks_by_type, start, tricks, transitions, stances, short_name, string_to_list, spins, regenerate_combo, short_to_full, common_tricks_by_type
from .models import TrickSet


def test(request):
    return render(request, 'comboapp/test.html')

def game(request):
    return render(request, 'comboapp/game_home.html')


def home(request):
    set_names = []
    saved_combos = []
    if request.user.is_authenticated:
        for set in request.user.trickset_set.all():
            set_names.append(set.name)
        for combo in request.user.combo_set.all():
            saved_combos.append(combo.combo_name)
    context = {
        'vertkick': common_tricks_by_type['vert'],
        'flat': common_tricks_by_type['flatspin'],
        'back': common_tricks_by_type['backward'],
        'forward': common_tricks_by_type['forward'],
        'outside': common_tricks_by_type['outside'],
        'inside': common_tricks_by_type['inside'],
        'other': common_tricks_by_type['other'],
        'set_names': set_names,
        'saved_combos': saved_combos
    }
    return render(request, 'comboapp/home.html', context)


def builder(request):
    set_names = []
    if request.user.is_authenticated:
        for set in request.user.trickset_set.all():
            set_names.append(set.name)
    context = {
        'vertkick': tricks_by_type['vert'],
        'flat': tricks_by_type['flatspin'],
        'back': tricks_by_type['backward'],
        'forward': tricks_by_type['forward'],
        'outside': tricks_by_type['outside'],
        'inside': tricks_by_type['inside'],
        'other': tricks_by_type['other'],
        'set_names': set_names
    }
    return render(request, 'comboapp/builder.html', context)


def editor(request):
    set_names = []
    saved_combos = []
    if request.user.is_authenticated:
        for set in request.user.trickset_set.all():
            set_names.append(set.name)
        for combo in request.user.combo_set.all():
            saved_combos.append(combo.combo_name)
    context = {
        'vertkick': tricks_by_type['vert'],
        'flat': tricks_by_type['flatspin'],
        'back': tricks_by_type['backward'],
        'forward': tricks_by_type['forward'],
        'outside': tricks_by_type['outside'],
        'inside': tricks_by_type['inside'],
        'other': tricks_by_type['other'],
        'set_names': set_names,
        'saved_combos': saved_combos
    }
    return render(request, 'comboapp/editor.html', context)


def about(request):
    return render(request, 'comboapp/about.html')


def blog(request):
    return render(request, 'comboapp/blog.html')


def guide(request):
    context = {
        'count': len(start['start'])
    }
    return render(request, 'comboapp/guide.html', context)


def get_combo(request):
    if request.method == 'POST':
        set_name = request.POST['trickset']
        if set_name in list(trick_sets.keys()):
            set = trick_sets[set_name]
        elif set_name == 'custom':
            set = request.POST.getlist('custom[]')
        else:
            set = TrickSet.objects.get(name=set_name, author=request.user).tricks
        stance_set = request.POST.getlist('stanceset[]')
        length = int(request.POST['length'])
        transition_set = request.POST.getlist('transitionset[]')
        start_trick = request.POST.getlist('start[]')
        finish_trick = request.POST.getlist('finish[]')
        spin_limit = request.POST['spin_limit']
        final_set = set.copy()
        if spin_limit != 'none':
            set_copy = set.copy()
            for trick in set_copy:
                remove = True
                for i in range(int(spin_limit) + 1):
                    if trick in spins[i]:
                        remove = False
                if remove:
                    final_set.remove(trick)
        if start_trick:
            if start_trick[0] in final_set:
                combo, full_list = generate(length, final_set, stance_set, transition_set, start_trick, finish_trick)
                data = {'combo': combo, 'result': 'success', 'full_list': full_list}
                return JsonResponse(data)
            else:
                return HttpResponse('fail')
        else:
            combo, full_list = generate(length, final_set, stance_set, transition_set, start_trick, finish_trick)
            data = {'combo': combo, 'result': 'success', 'full_list': full_list}
            return JsonResponse(data)


def regenerate(request):
    if request.method == 'POST':
        set_name = request.POST['trickset']
        if set_name in list(trick_sets.keys()):
            set = trick_sets[set_name]
        elif set_name == 'custom':
            set = request.POST.getlist('custom[]')
        else:
            set = TrickSet.objects.get(name=set_name, author=request.user).tricks
        stance_set = request.POST.getlist('stanceset[]')
        transition_set = request.POST.getlist('transitionset[]')
        spin_limit = request.POST['spin_limit']
        change_idxs = request.POST.getlist('change_idxs[]')
        full_list = request.POST.getlist('full_list[]')
        for i in range(len(change_idxs)):
            change_idxs[i] = int(change_idxs[i])
        final_set = set.copy()
        if spin_limit != 'none':
            set_copy = set.copy()
            for trick in set_copy:
                remove = True
                for i in range(int(spin_limit) + 1):
                    if trick in spins[i]:
                        remove = False
                if remove:
                    final_set.remove(trick)
        replacements = []
        new_combo = ''
        for idx in change_idxs:
            change = full_list[idx]
            if idx == 0:
                change_prev = 'start'
                change_prev2 = 'start'
                change_next = full_list[idx + 1]
            elif idx == 1:
                change_prev = full_list[0]
                change_prev2 = 'start'
                if 1 == len(full_list) - 1:
                    change_next = 'end'
                else:
                    change_next = full_list[idx + 1]
            elif idx == len(full_list) - 1:
                change_prev = full_list[idx - 1]
                if len(full_list) > 2:
                    change_prev2 = full_list[idx - 2]
                else:
                    change_prev2 =  'start'
                change_next = 'end'
            else:
                change_prev = full_list[idx - 1]
                change_prev2 = full_list[idx - 2]
                change_next = full_list[idx + 1]
            new_combo, replacement = regenerate_combo(change_prev2, change_prev, change, change_next, idx, final_set, stance_set, transition_set, full_list.copy())
            full_list[idx] = replacement
            replacements.append(replacement)
        data = {'new_combo': new_combo, 'replacements': replacements, 'indexes': change_idxs}
        return JsonResponse(data)


def get_stances(request):
    if request.method == 'POST':
        selected = request.POST['selected']
        allowed_stances = tricks[selected]
        return JsonResponse({'stances': allowed_stances})


def get_transitions(request):
    if request.method == 'POST':
        selected_trick = request.POST['select_trick']
        selected_stance = request.POST['select_stance']
        allowed_stances = tricks[selected_trick]
        allowed_transitions = []
        for i in range(len(allowed_stances)):
            if selected_stance in allowed_stances[i]:
                allowed_transitions = stances[allowed_stances[i]]
        return JsonResponse({'transitions': allowed_transitions})


def get_tricks(request):
    if request.method == 'POST':
        selected_trick = request.POST['select_trick']
        selected_transition = request.POST['select_trans']
        selected_stance = request.POST['select_stance']
        allowed_stances = tricks[selected_trick]
        allowed_transitions = []
        allowed_tricks = []
        for i in range(len(allowed_stances)):
            if selected_stance in allowed_stances[i]:
                allowed_transitions = stances[allowed_stances[i]]
        for i in range(len(allowed_transitions)):
            if selected_transition in allowed_transitions[i]:
                allowed_tricks = transitions[allowed_transitions[i]]
        shortened_combo_list = short_name(string_to_list(request.POST['curr_combo']))
        shortened_combo_str = ''
        for i in range(len(shortened_combo_list)):
            if i == 0:
                shortened_combo_str += shortened_combo_list[i]
            else:
                shortened_combo_str += ' ' + shortened_combo_list[i]
        return JsonResponse({'tricks': allowed_tricks, 'short': shortened_combo_str})


def shorten(request):
    if request.method == 'POST':
        shortened_combo_list = short_name(string_to_list(request.POST['curr_combo']))
        shortened_combo_str = ''
        for i in range(len(shortened_combo_list)):
            if i == 0:
                shortened_combo_str += shortened_combo_list[i]
            else:
                shortened_combo_str += ' ' + shortened_combo_list[i]
        return JsonResponse({'short': shortened_combo_str})


def get_set_tricks(request):
    if request.method == 'POST':
        set_name = request.POST['set']
        if set_name in list(trick_sets.keys()):
            set = trick_sets[set_name]
        elif set_name == 'custom':
            set = request.POST.getlist('custom[]')
        else:
           set = TrickSet.objects.get(name=set_name, author=request.user).tricks
        vert = []
        flat = []
        back = []
        forward = []
        outside = []
        inside = []
        other = []
        for trick in set:
            if trick in tricks_by_type['vert']:
                vert.append(trick)
            elif trick in tricks_by_type['flatspin']:
                flat.append(trick)
            elif trick in tricks_by_type['backward']:
                back.append(trick)
            elif trick in tricks_by_type['forward']:
                forward.append(trick)
            elif trick in tricks_by_type['outside']:
                outside.append(trick)
            elif trick in tricks_by_type['inside']:
                inside.append(trick)
            elif trick in tricks_by_type['other']:
                other.append(trick)
        return JsonResponse({'vert': vert, 'flatspin': flat, 'backward': back, 'forward': forward, 'outside': outside, 'inside': inside, 'other': other})


def load_combo(request):
    if request.method == 'POST':
        combo = request.POST['combo']
        short = (combo + '.')[:-1]
        full_list = short_to_full(short)
        data = {'short': short, 'full_list': full_list}
        return JsonResponse(data)