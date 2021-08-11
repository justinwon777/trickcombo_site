from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegister, UserUpdate, ProfileUpdate
from django.contrib.auth.decorators import login_required
from comboapp.v2 import tricks_by_type
from comboapp.models import TrickSet, Combo, Trick
from django.http import HttpResponse, JsonResponse


def register(request):
    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}.')
            return redirect('login')
    else:
        form = UserRegister()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdate(request.POST, instance=request.user)
        # p_form = ProfileUpdate(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid():
            u_form.save()
            # p_form.save()
            messages.success(request, f'Your account has been updated.')
            return redirect('profile')
    else:
        u_form = UserUpdate(instance=request.user)
        # p_form = ProfileUpdate(instance=request.user.profile)
    set_names = []
    set_counts = []
    for set in request.user.trickset_set.all():
        set_names.append([set.name, len(set.tricks)])
    saved_combos = []
    for combo in request.user.combo_set.all():
        saved_combos.append(combo.combo_name)

    wishlist = []
    for trick in request.user.trick_set.all():
        wishlist.append(trick.trick_name)
    context = {
        'u_form': u_form,
        'set_names': set_names,
        'set_counts': set_counts,
        'vertkick': tricks_by_type['vert'],
        'flat': tricks_by_type['flatspin'],
        'back': tricks_by_type['backward'],
        'forward': tricks_by_type['forward'],
        'outside': tricks_by_type['outside'],
        'inside': tricks_by_type['inside'],
        'other': tricks_by_type['other'],
        'combos': saved_combos,
        'trick_wishlist': wishlist
    }
    return render(request, 'users/profile.html', context)


def create_set(request):
    if request.method == 'POST':
        set_name = request.POST['set_name']
        new_tricks = request.POST.getlist('trickset[]')
        if request.user.trickset_set.all().count() < 5:
            if len(set_name) > 0 and len(new_tricks) > 0 and not request.user.trickset_set.all().filter(name=set_name).exists():
                new_set = TrickSet(name=set_name, tricks=new_tricks, author=request.user)
                new_set.save()
                return JsonResponse({'new_set_name': set_name, 'result': 'success', 'trick_count': len(new_tricks)})
        else:
            return JsonResponse({'result': 'max'})
    return HttpResponse('fail')


def edit_set(request):
    if request.method == 'POST':
        set_name = request.POST['set_name']
        set = TrickSet.objects.get(name=set_name, author=request.user)
        return JsonResponse({'tricks': set.tricks, 'name': set.name})


def edit_save_set(request):
    if request.method == 'POST':
        new_tricks = request.POST.getlist('trickset[]')
        new_name = request.POST['new_name']
        old_name = request.POST['old_name']
        if len(new_name) > 0 and len(new_tricks) > 0:
            set = TrickSet.objects.get(name=old_name, author=request.user)
            set.tricks = new_tricks
            set.name = new_name
            set.save()
            return JsonResponse({'result': 'success', 'new_name': new_name, 'old_name': old_name})
    return HttpResponse('fail')


def delete_set(request):
    if request.method == 'POST':
        set_names = request.POST.getlist('set_name[]')
        for set_name in set_names:
            set = TrickSet.objects.get(name=set_name, author=request.user)
            set.delete()
        return JsonResponse({'result': 'success', 'set_del': set_names})
    return HttpResponse('fail')

def save_combo(request):
    if request.method == 'POST':
        if request.user.combo_set.all().count() < 15:
            combo = request.POST['combo_save']
            if not request.user.combo_set.all().filter(combo_name=combo).exists():
                saved_combo = Combo(author=request.user, combo_name=combo)
                saved_combo.save()
                return HttpResponse('success')
        else:
            return JsonResponse({'result': 'max'})
    return HttpResponse('fail')

def delete_combo(request):
    if request.method == 'POST':
        combos_to_del = request.POST.getlist('combo[]')
        for combo_to_del in combos_to_del:
            combo = Combo.objects.get(combo_name=combo_to_del, author=request.user)
            combo.delete()
        return JsonResponse({'result': 'success', 'combo': combos_to_del})
    return HttpResponse('fail')

def save_new_combo(request):
    if request.method == 'POST':
        combo = request.POST['combo_save']
        if request.user.combo_set.all().count() < 15:
            if len(combo) > 0 and not request.user.combo_set.all().filter(combo_name=combo).exists():
                saved_combo = Combo(author=request.user, combo_name=combo)
                saved_combo.save()
                return JsonResponse({'result': 'success', 'new_combo': combo})
        else:
            return JsonResponse({'result': 'max'})
    return HttpResponse('fail')


def delete_trick(request):
    if request.method == 'POST':
        tricks_to_del = request.POST.getlist('tricks[]')
        for trick_to_del in tricks_to_del:
            trick = Trick.objects.get(trick_name=trick_to_del, author=request.user)
            trick.delete()
        return JsonResponse({'result': 'success', 'trick': tricks_to_del})
    return HttpResponse('fail')

def save_new_trick(request):
    if request.method == 'POST':
        trick = request.POST['trick_save']
        if request.user.trick_set.all().count() < 15:
            if len(trick) > 0 and not request.user.trick_set.all().filter(trick_name=trick).exists():
                saved_trick = Trick(author=request.user, trick_name=trick)
                saved_trick.save()
                return JsonResponse({'result': 'success', 'new_trick': trick})
        else:
            return JsonResponse({'result': 'max'})
    return HttpResponse('fail')