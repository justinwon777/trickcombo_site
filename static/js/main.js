function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

function copyCombo(element) {
    var $temp = $("<input>");
    $("body").append($temp);
    $temp.val($(element).text()).select();
    document.execCommand("copy");
    $temp.remove();
}

function updateStart(curr_set, custom_set) {
    $.ajax({
        url: '/get_set_tricks/',
        type: "POST",
        data: {
            set: curr_set,
            custom: custom_set
        },
        headers: {
        "X-CSRFToken": csrftoken,
        },
        success: function (data) {
            $(':radio[name=trick2]').each(function(){
                $(this).parent().remove()
            })
            data['vert'].forEach(function(item){
                $('.vertkicks_list').append('<div><input class="form-check-input text-primary" type="radio" name="trick2" style="margin-right: 5px" value="' + item + '" id="' + item + '"><label for="' + item + '">' + item + '</label><br></div>')
            })
            data['flatspin'].forEach(function(item){
                $('.flatspin_list').append('<div><input class="form-check-input text-primary" type="radio" name="trick2" style="margin-right: 5px" value="' + item + '" id="' + item + '"><label for="' + item + '">' + item + '</label><br></div>')
            })
            data['backward'].forEach(function(item){
                $('.backward_list').append('<div><input class="form-check-input text-primary" type="radio" name="trick2" style="margin-right: 5px" value="' + item + '" id="' + item + '"><label for="' + item + '">' + item + '</label><br></div>')
            })
            data['forward'].forEach(function(item){
                $('.forward_list').append('<div><input class="form-check-input text-primary" type="radio" name="trick2" style="margin-right: 5px" value="' + item + '" id="' + item + '"><label for="' + item + '">' + item + '</label><br></div>')
            })
            data['outside'].forEach(function(item){
                $('.outside_list').append('<div><input class="form-check-input text-primary" type="radio" name="trick2" style="margin-right: 5px" value="' + item + '" id="' + item + '"><label for="' + item + '">' + item + '</label><br></div>')
            })
            data['inside'].forEach(function(item){
                $('.inside_list').append('<div><input class="form-check-input text-primary" type="radio" name="trick2" style="margin-right: 5px" value="' + item + '" id="' + item + '"><label for="' + item + '">' + item + '</label><br></div>')
            })
            data['other'].forEach(function(item){
                $('.other_list').append('<div><input class="form-check-input text-primary" type="radio" name="trick2" style="margin-right: 5px" value="' + item + '" id="' + item + '"><label for="' + item + '">' + item + '</label><br></div>')
            })
        },
        error: function (error) {
            console.log(error);
        }
    });
}

$(document).ready(function(){
    $('#trick_set').on('change', function(){
        var curr_set = $('input[name=set_name]:checked', '#trick_set').val()
        var custom_set = [];
        $("#custom_collapse input[name='trick']:checked").each(function(){
            custom_set.push(this.value);
        });
        if ( curr_set== 'custom') {
            $('#pick_tricks').prop('disabled', false)
        }
        else {
            open = $('#custom_collapse').is( ":visible" )
            if (open) {
                $('#pick_tricks').trigger('click')
            }
            $('#pick_tricks').attr('disabled', true)
        }
        updateStart(curr_set, custom_set)
    })
    $('#trickset').on('change', function(){
        var curr_set = $('input[name=set_name]:checked', '#trick_set').val()
        var custom_set = [];
        $("#custom_collapse input[name='trick']:checked").each(function(){
            custom_set.push(this.value);
        });
        updateStart(curr_set, custom_set)
    })
    $('#reset_start').click(function(){
        if ($('#start_modal input[name=trick2]').is(':checked')) {
            $('#start_modal input[name=trick2]:checked').prop('checked', false)
        }
    })
    $('#reset_finish').click(function(){
        if ($('#finish_modal input[name=trick2]').is(':checked')) {
            $('#finish_modal input[name=trick2]:checked').prop('checked', false)
        }
    })
    $('#generate').click(function(){
        var tricks = $('input[name=set_name]:checked', '#trick_set').val();
        var length = $('#length').val();
        var spin_limit = $('#spin_limit').val();
        var stances = [];
        var custom_set = [];
        var start_set = [];
        var finish_set = [];
        $("input[name='stance']:checked").each(function(){
            stances.push(this.value);
        });
        var transitions = [];
        $("input[name='transition']:checked").each(function(){
            transitions.push(this.value);
        });
        if (tricks == 'custom') {
            $("#custom_collapse input[name='trick']:checked").each(function(){
                custom_set.push(this.value);
            });
        }
        $("#start_modal input[name='trick2']:checked").each(function(){
                start_set.push(this.value);
        });
        $("#finish_modal input[name='trick2']:checked").each(function(){
                finish_set.push(this.value);
        });
        $.ajax({
            url: '/getcombo/',
            type: "POST",
            data: {
                trickset: tricks,
                stanceset: stances,
                transitionset: transitions,
                length: length,
                custom: custom_set,
                start: start_set,
                finish: finish_set,
                spin_limit: spin_limit
            },
            headers: {
            "X-CSRFToken": csrftoken,
            },
            success: function (data) {
                if (data['result'] == 'success') {
                    $('#combo').text(data['combo']);
                    $('#include_fail').prop('hidden', true)
                    $('#start_fail').prop('hidden', true)
                    if (data['full_list'][0] == 'No valid combos') {
                        $('#full').empty()
                        $('#full').append('<h3>No valid combos</h3>')
                    }
                    else {
                        $('#full').empty()
                        data['full_list'].forEach(function(item){
                            $('#full').append('<div class="ck-button"><label><input class="full_part" type="checkbox" hidden value="' + item + '"><span>' + item + '</span></label></div>')
                        })
                    }
                }
                else {
                    $('#start_fail').prop('hidden', false)
                }
            },
            error: function (error) {
                console.log(error);
            }
        });
    });
    $('#regenerate').click(function(){
        if ($('input.full_part').is(':checked')) {
            var tricks = $('input[name=set_name]:checked', '#trick_set').val();
            var spin_limit = $('#spin_limit').val();
            var stances = [];
            var transitions = [];
            var custom_set = [];
            $("input[name='stance']:checked").each(function(){
                stances.push(this.value);
            });
            $("input[name='transition']:checked").each(function(){
                transitions.push(this.value);
            });
            if (tricks == 'custom') {
                $("#custom_collapse input[name='trick']:checked").each(function(){
                    custom_set.push(this.value);
                });
            }
            var full_list = [];
            $("input.full_part").each(function(){
                full_list.push(this.value);
            });
            var change_idxs = [];
            $("input.full_part:checked").each(function(){
                change_idxs.push($(this).parent().parent().index())
            })
            $('#regenerate_error').prop('hidden', true)
            $.ajax({
                url: '/regenerate/',
                type: "POST",
                data: {
                    trickset: tricks,
                    stanceset: stances,
                    transitionset: transitions,
                    custom: custom_set,
                    spin_limit: spin_limit,
                    full_list: full_list,
                    change_idxs: change_idxs
                },
                headers: {
                "X-CSRFToken": csrftoken,
                },
                success: function (data) {
                    $('#combo').text(data['new_combo']);
                    for (i = 0; i < data['replacements'].length; i++) {
                        index = data['indexes'][i]
                        $('div.ck-button').eq(index).find("span").text(data['replacements'][i])
                        $('div.ck-button').eq(index).find("input").val(data['replacements'][i])
                    }
                },
                error: function (error) {
                    console.log(error);
                }
            });
        }
        else {
            $('#regenerate_error').prop('hidden', false)
        }
    })
    $('#add_trick').click(function(){
        var trick = $('input[name=trick2]:checked', '#trickset2').val();
        var stance = $('input[name=stance2]:checked', '#stanceset2').val();
        if (!$("input[name='stance2']:checked").val() || !$("input[name='trick2']:checked").val()) {
           $('#trick_error').prop('hidden', false)
        }
        else {
            $("#trickset2 input").prop("disabled", true);
            $("#stanceset2 input").prop("disabled", true);
            $('#trick_error').prop('hidden', true);
            $('#add_trans').prop('disabled', false);
            $('#add_trick').prop('disabled', true);
            $('#made_combo').append(' ' + trick + ' ' + stance);
            $.ajax({
                url: '/shorten/',
                type: "POST",
                data: {
                    curr_combo: $('#made_combo').text()
                },
                beforeSend: function (xhr) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                },
                success: function (data) {
                    $('#short').text(data['short'])
                },
                error: function (error) {
                    console.log(error);
                }
            });
        }
    })
    $('#add_trans').click(function(){
        var selected_trick = $('input[name=trick2]:checked', '#trickset2').val();
        var transition = $('input[name=transition2]:checked', '#transitionset2').val();
        var selected_stance = $('input[name=stance2]:checked', '#stanceset2').val();
        if(!$("input[name='transition2']:checked").val()) {
            $('#trans_error').prop('hidden', false);
        }
        else {
            $('#trans_error').prop('hidden', true);
            $('#add_trick').prop('disabled', false);
            $('#add_trans').prop('disabled', true);
            $('#made_combo').append(' ' + transition);
            $("#trickset2 input").prop("checked", false);
            $("#stanceset2 input").prop("checked", false);
            $("#transitionset2 input").prop("checked", false);
            $.ajax({
                url: '/gettricks/',
                type: "POST",
                data: {
                    select_trans: transition,
                    select_stance: selected_stance,
                    select_trick: selected_trick,
                    curr_combo: $('#made_combo').text()
                },
                beforeSend: function (xhr) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                },
                success: function (data) {
                    $('#short').text(data['short'])
                    allowed = data['tricks']
                    $('#trickset2 *').filter(':input').each(function(){
                        if (allowed.includes($(this).val())) {
                            $(this).prop('disabled', false)
                        }
                        else {
                            $(this).prop('disabled', true)
                        }
                    });
                },
                error: function (error) {
                    console.log(error);
                }
            });
        }
    })
    $('#reset').click(function(){
        $('#short').text('')
        $('#made_combo').text('')
        $("#trickset2 input").prop("disabled", false);
        $("#trickset2 input").prop("checked", false);
        $("#stanceset2 input").prop("disabled", true);
        $("#stanceset2 input").prop("checked", false);
        $("#transitionset2 input").prop("disabled", true);
        $("#transitionset2 input").prop("checked", false);
        $('#trans_error').prop('hidden', true);
        $('#trick_error').prop('hidden', true);
        $('#add_trick').prop('disabled', false);
        $('#add_trans').prop('disabled', true);
    })
    $('#trickset2').on('change', function() {
        var selected_trick = $('input[name=trick2]:checked', '#trickset2').val();
        $("#stanceset2 input").prop("checked", false);
        $.ajax({
            url: '/getstances/',
            type: "POST",
            data: {
                selected: selected_trick
            },
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function (data) {
                allowed = data['stances']
                $('#complete2').prop('disabled', false)
                if (allowed.includes('hyper') || allowed.includes('hyper_k')) {
                    $('#hyper2').prop('disabled', false)
                }
                else {
                    $('#hyper2').prop('disabled', true)
                }
                if (allowed.includes('mega')) {
                    $('#mega2').prop('disabled', false)
                }
                else {
                    $('#mega2').prop('disabled', true)
                }
                if (allowed.includes('semi')) {
                    $('#semi2').prop('disabled', false)
                }
                else {
                    $('#semi2').prop('disabled', true)
                }
            },
            error: function (error) {
                console.log(error);
            }
        });
    })
    $('#stanceset2').on('change', function() {
        var selected_stance = $('input[name=stance2]:checked', '#stanceset2').val();
        var selected_trick = $('input[name=trick2]:checked', '#trickset2').val();
        $("#transitionset2 input").prop("checked", false);
        $.ajax({
            url: '/gettransitions/',
            type: "POST",
            data: {
                select_trick: selected_trick,
                select_stance: selected_stance
            },
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function (data) {
                allowed = data['transitions']
                if (allowed.includes('punch')) {
                    $('#punch2').prop('disabled', false)
                }
                else {
                    $('#punch2').prop('disabled', true)
                }
                if (allowed.includes('pop')) {
                    $('#pop2').prop('disabled', false)
                }
                else {
                    $('#pop2').prop('disabled', true)
                }
                if (allowed.includes('vanish_r') || allowed.includes('vanish_l')) {
                    $('#vanish2').prop('disabled', false)
                }
                else {
                    $('#vanish2').prop('disabled', true)
                }
                if (allowed.includes('redirect_r') || allowed.includes('redirect_l')) {
                    $('#redirect2').prop('disabled', false)
                }
                else {
                    $('#redirect2').prop('disabled', true)
                }
                if (allowed.includes('reversal_r') || allowed.includes('reversal_l')) {
                    $('#reversal2').prop('disabled', false)
                }
                else {
                    $('#redirect2').prop('disabled', true)
                }
                if (allowed.includes('swing')) {
                    $('#swing2').prop('disabled', false)
                }
                else {
                    $('#swing2').prop('disabled', true)
                }
                if (allowed.includes('wrap')) {
                    $('#wrap2').prop('disabled', false)
                }
                else {
                    $('#wrap2').prop('disabled', true)
                }
                if (allowed.includes('frontswing')) {
                    $('#frontswing2').prop('disabled', false)
                }
                else {
                    $('#frontswing2').prop('disabled', true)
                }
                if (allowed.includes('missleg')) {
                    $('#missleg2').prop('disabled', false)
                }
                else {
                    $('#missleg2').prop('disabled', true)
                }
                if (allowed.includes('backside')) {
                    $('#backside2').prop('disabled', false)
                }
                else {
                    $('#backside2').prop('disabled', true)
                }
            },
            error: function (error) {
                console.log(error);
            }
        });
    })
    $('#set_list').on('change', function() {
        var isChecked = $('input[name=set_name]').is(':checked');
        if (isChecked) {
            $('#edit_set').prop('disabled', false)
            $('#delete_set').prop('disabled', false)
            $('#create_set').prop('disabled', true)
        }
        else {
            $('#create_set').prop('disabled', true)
            $('#edit_set').prop('disabled', true)
            $('#delete_set').prop('disabled', true)
            $('#create_set').prop('disabled', false)
        }
    })
    $('#create_set').click(function(){
        if ($('#create_collapse').is(':visible')) {
            $('#create_collapse').hide()
        }
        else {
            $('#edit_collapse').hide()
            $('#create_collapse').show()
        }
    })
    $('#create_save_set').click(function(){
        var tricks = [];
        var name = $('#create_set_name').val()
        $("input[name='trick']:checked").each(function(){
                tricks.push(this.value);
            })
        $.ajax({
            url: '/create_set/',
            type: "POST",
            data: {
                trickset: tricks,
                set_name: name
            },
            headers: {
            "X-CSRFToken": csrftoken,
            },
            success: function (data) {
                if (data['result'] == 'success') {
                    if (data['trick_count'] == 1) {
                        $('#set_list').append('<li class="list-group-item"><input class="form-check-input me-1" name="set_name" type="checkbox" value="' + data['new_set_name'] + '"><span>' + data['new_set_name'] + '</span><span style="float: right" class="text-secondary">' + data['trick_count'] +' trick</span></li>')
                    }
                    else {
                        $('#set_list').append('<li class="list-group-item"><input class="form-check-input me-1" name="set_name" type="checkbox" value="' + data['new_set_name'] + '"><span>' + data['new_set_name'] + '</span><span style="float: right" class="text-secondary">' + data['trick_count'] +' tricks</span></li>')
                    }
                    $('#create_success').prop('hidden', false)
                    $('#create_fail').prop('hidden', true)
                    $('#create_max').prop('hidden', true)
                }
                else if (data['result'] == 'max') {
                    $('#create_success').prop('hidden', true)
                    $('#create_fail').prop('hidden', true)
                    $('#create_max').prop('hidden', false)
                }
                else {
                    $('#create_success').prop('hidden', true)
                    $('#create_fail').prop('hidden', false)
                    $('#create_max').prop('hidden', true)
                }
            },
            error: function (error) {
                console.log(error);
            }
        });
    });
    $('#edit_set').click(function(){
        var checkTotal = $('#set_list').find('input[name=set_name]:checked').length
        if (checkTotal > 1) {
            $('#select_fail').prop('hidden', false)
        }
        else {
            $('#create_collapse').hide()
            $('#edit_collapse').show()
            $('#select_fail').prop('hidden', true)
            var selected_set = $('input[name=set_name]:checked', '#set_list').val();
            var str1 = 'Editing set: '
            $('#curr_set').text(str1.concat(selected_set))
            $.ajax({
                url: '/edit_set/',
                type: "POST",
                data: {
                    set_name: selected_set
                },
                headers: {
                "X-CSRFToken": csrftoken,
                },
                success: function (data) {
                    in_set = data['tricks']
                    $('#trickset2 *').filter(':input').each(function(){
                        if (in_set.includes($(this).val())) {
                            $(this).prop('checked', true)
                        }
                        else {
                            $(this).prop('checked', false)
                        }
                    });
                    $('#edit_set_name').val(data['name'])
                },
                error: function (error) {
                    console.log(error);
                }
            });
        }
    });
    $('#edit_save_set').click(function(){
        var tricks = [];
        var new_name = $('#edit_set_name').val()
        var old_name = $('#curr_set').text().substr(13)
        $("input[name='trick2']:checked").each(function(){
                tricks.push(this.value);
            })
        $.ajax({
            url: '/edit_save_set/',
            type: "POST",
            data: {
                trickset: tricks,
                old_name: old_name,
                new_name: new_name
            },
            headers: {
            "X-CSRFToken": csrftoken,
            },
            success: function (data) {
                if (data['result'] == 'success') {
                    console.log($('#set_list :checkbox[value=' + data['old_name'] + ']').next().text(data['new_name']))
                    $('#set_list :checkbox[value=' + data['old_name'] + ']').val(data['new_name'])
                    $('#edit_success').prop('hidden', false)
                    $('#edit_fail').prop('hidden', true)
                }
                else {
                    $('#edit_success').prop('hidden', true)
                    $('#edit_fail').prop('hidden', false)
                }
            },
            error: function (error) {
                console.log(error);
            }
        });
    });
    $('#delete_set').click(function(){
        var myModal = new bootstrap.Modal(document.getElementById('exampleModal'), {
          keyboard: false
        })
        myModal.show()
    })
    $('#confirm_delete').click(function(){
        var selected_set = []
        $("#set_list input[name=set_name]:checked").each(function(){
            selected_set.push(this.value);
        });
        $.ajax({
            url: '/delete_set/',
            type: "POST",
            data: {
                set_name: selected_set
            },
            headers: {
            "X-CSRFToken": csrftoken,
            },
            success: function (data) {
                if (data['result'] == 'success') {
                    data['set_del'].forEach(function(item){
                        $('#set_list :checkbox[value=' + item + ']').parent().remove();
                    })
                    $('#delete_success').prop('hidden', false)
                }
                else {
                    $('#delete_success').prop('hidden', true)
                }
            },
            error: function (error) {
                console.log(error);
            }
        });
    });
    $('#save').click(function(){
        if ($('#combo').is(':empty')) {
        }
        else {
            combo_to_save = $('#combo').text()
            $.ajax({
                url: '/save_combo/',
                type: "POST",
                data: {
                    combo_save: combo_to_save
                },
                headers: {
                "X-CSRFToken": csrftoken,
                },
                success: function (data) {
                    if (data['result'] == 'max') {
                        $('#save_max').prop('hidden', false)
                    }
                    else {
                        $('#save_max').prop('hidden', true)
                    }
                },
                error: function (error) {
                    console.log(error);
                }
            });
        }
    })
    $('#save_build').click(function(){
        if ($('#made_combo').is(':empty')) {
        }
        else {
            combo_to_save = $('#short').text()
            $.ajax({
                url: '/save_combo/',
                type: "POST",
                data: {
                    combo_save: combo_to_save
                },
                headers: {
                "X-CSRFToken": csrftoken,
                },
                success: function (data) {
                    if (data['result'] == 'max') {
                        $('#save_max').prop('hidden', false)
                    }
                    else {
                        $('#save_max').prop('hidden', true)
                    }
                },
                error: function (error) {
                    console.log(error);
                }
            });
        }
    })
    $('#delete_combo').click(function(){
        var myModal = new bootstrap.Modal(document.getElementById('exampleModal2'), {
          keyboard: false
        })
        myModal.show()
    })
    $('#confirm_delete_combo').click(function(){
        var selected_combo = []
        $("#combo_list input[name=combo_name]:checked").each(function(){
            selected_combo.push(this.value);
        });
        $.ajax({
            url: '/delete_combo/',
            type: "POST",
            data: {
                combo: selected_combo
            },
            headers: {
            "X-CSRFToken": csrftoken,
            },
            success: function (data) {
                if (data['result'] == 'success') {
                    data['combo'].forEach(function(item) {
                        $('#combo_list :checkbox[value="' + item + '"]').parent().remove();
                    })
                    $('#delete_combo_success').prop('hidden', false)
                }
                else {
                    $('#delete_combo_success').prop('hidden', true)
                }
            },
            error: function (error) {
                console.log(error);
            }
        });
    });
    $('#combo_list').on('change', function() {
        var isChecked = $('input[name=combo_name]').is(':checked');
        if (isChecked) {
            $('#delete_combo').prop('disabled', false)
        }
        else {
            $('#delete_combo').prop('disabled', true)
        }
    })
    $('#save_new_combo').click(function(){
        combo_to_save = $('#new_combo').val()
        $.ajax({
            url: '/save_new_combo/',
            type: "POST",
            data: {
                combo_save: combo_to_save
            },
            headers: {
            "X-CSRFToken": csrftoken,
            },
            success: function (data) {
                if (data['result'] == 'success') {
                    $('#combo_list').append('<li class="list-group-item"><input class="form-check-input me-1" name="combo_name" type="checkbox" value="' + data['new_combo'] + '">' + data['new_combo'] + '</li>')
                    $('#save_max').prop('hidden', true)
                    $('#add_fail').prop('hidden', true)
                    $('#add_success').prop('hidden', false)
                }
                else if (data['result'] == 'max') {
                    $('#save_max').prop('hidden', false)
                    $('#add_fail').prop('hidden', true)
                    $('#add_success').prop('hidden', true)
                }
                else {
                    $('#save_max').prop('hidden', true)
                    $('#add_fail').prop('hidden', false)
                    $('#add_success').prop('hidden', true)
                }
            },
            error: function (error) {
                console.log(error);
            }
        });

    })
    $('#delete_trick_wish').click(function(){
        var myModal = new bootstrap.Modal(document.getElementById('exampleModal3'), {
          keyboard: false
        })
        myModal.show()
    })
    $('#confirm_delete_trick').click(function(){
        var selected_tricks = []
        $("#trick_wishlist input[name=trick_name]:checked").each(function(){
            selected_tricks.push(this.value);
        });
        $.ajax({
            url: '/delete_trick/',
            type: "POST",
            data: {
                tricks: selected_tricks
            },
            headers: {
            "X-CSRFToken": csrftoken,
            },
            success: function (data) {
                if (data['result'] == 'success') {
                    data['trick'].forEach(function(item) {
                        $('#trick_wishlist :checkbox[value="' + item + '"]').parent().remove();
                    })
                    $('#delete_trick_success').prop('hidden', false)
                }
                else {
                    $('#delete_trick_success').prop('hidden', true)
                }
            },
            error: function (error) {
                console.log(error);
            }
        });
    });
    $('#trick_wishlist').on('change', function() {
        var isChecked = $('input[name=trick_name]').is(':checked');
        if (isChecked) {
            $('#delete_trick_wish').prop('disabled', false)
        }
        else {
            $('#delete_trick_wish').prop('disabled', true)
        }
    })
    $('#save_new_trick').click(function(){
        trick_to_save = $('#new_trick').val()
        $.ajax({
            url: '/save_new_trick/',
            type: "POST",
            data: {
                trick_save: trick_to_save
            },
            headers: {
            "X-CSRFToken": csrftoken,
            },
            success: function (data) {
                if (data['result'] == 'success') {
                    $('#trick_wishlist').append('<li class="list-group-item"><input class="form-check-input me-1" name="trick_name" type="checkbox" value="' + data['new_trick'] + '">' + data['new_trick'] + '</li>')
                    $('#save_trick_max').prop('hidden', true)
                    $('#add_trick_fail').prop('hidden', true)
                    $('#add_trick_success').prop('hidden', false)
                }
                else if (data['result'] == 'max') {
                    $('#save_trick_max').prop('hidden', false)
                    $('#add_trick_fail').prop('hidden', true)
                    $('#add_trick_success').prop('hidden', true)
                }
                else {
                    $('#save_trick_max').prop('hidden', true)
                    $('#add_trick_fail').prop('hidden', false)
                    $('#add_trick_success').prop('hidden', true)
                }
            },
            error: function (error) {
                console.log(error);
            }
        });
    })
//    $('#full').on('change', 'input.full_part', function(){
//        $('input.full_part').not(this).prop('checked', false)
//    })
    $('#load_combo').click(function(){
        var myModal = new bootstrap.Modal(document.getElementById('combo_modal'), {
          keyboard: false
        })
        myModal.show()
    })
    $('#confirm_load_combo').click(function(){
        var combo = $('input[name=saved_combo]:checked').val()
        $.ajax({
            url: '/load_combo/',
            type: "POST",
            data: {
                combo: combo
            },
            headers: {
            "X-CSRFToken": csrftoken,
            },
            success: function (data) {
                $('#combo').text(data['short']);
                    $('#full').empty()
                    data['full_list'].forEach(function(item){
                        $('#full').append('<div class="ck-button"><label><input class="full_part" type="checkbox" hidden value="' + item + '"><span>' + item + '</span></label></div>')
                    })
            },
            error: function (error) {
                console.log(error);
            }
        });
    })
    $('#custom_search').on('input', function(){
        var text = $('#search_custom').val().toLowerCase()
        $('#trickset *').filter(':input[name=trick]').each(function(){
            if ($(this).val().includes(text)) {
                $(this).prop('hidden', false)
                $(this).next().prop('hidden', false)
                $(this).next().next().prop('hidden', false)
            }
            else {
                $(this).prop('hidden', true)
                $(this).next().prop('hidden', true)
                $(this).next().next().prop('hidden', true)
            }
        });
    })
    $('#starting_search').on('input', function(){
        var text = $('#search_starting').val().toLowerCase()
        $('#trickset2 *').filter(':input[name=trick2]').each(function(){
            if ($(this).val().includes(text)) {
                $(this).parent().prop('hidden', false)
            }
            else {
                $(this).parent().prop('hidden', true)
            }
        });
    })
    $('#finishing_search').on('input', function(){
        var text = $('#search_finishing').val().toLowerCase()
        $('#trickset3 *').filter(':input[name=trick2]').each(function(){
            if ($(this).val().includes(text)) {
                $(this).parent().prop('hidden', false)
            }
            else {
                $(this).parent().prop('hidden', true)
            }
        });
    })
    $('#create_search').on('input', function(){
        var text = $('#search_create').val().toLowerCase()
        $('#trickset_create *').filter(':input[name=trick]').each(function(){
            if ($(this).val().includes(text)) {
                $(this).prop('hidden', false)
                $(this).next().prop('hidden', false)
                $(this).next().next().prop('hidden', false)
            }
            else {
                $(this).prop('hidden', true)
                $(this).next().prop('hidden', true)
                $(this).next().next().prop('hidden', true)
            }
        });
    })
    $('#edit_search').on('input', function(){
        var text = $('#search_edit').val().toLowerCase()
        $('#trickset2 *').filter(':input[name=trick2]').each(function(){
            if ($(this).val().includes(text)) {
                $(this).prop('hidden', false)
                $(this).next().prop('hidden', false)
                $(this).next().next().prop('hidden', false)
            }
            else {
                $(this).prop('hidden', true)
                $(this).next().prop('hidden', true)
                $(this).next().next().prop('hidden', true)
            }
        });
    })
    $('#start').click(function(){
        var myModal = new bootstrap.Modal(document.getElementById('start_modal'), {
          keyboard: false
        })
        $('#reset_finish').trigger('click')
        myModal.show()
    })
    $('#finish').click(function(){
        var myModal = new bootstrap.Modal(document.getElementById('finish_modal'), {
          keyboard: false
        })
        $('#reset_start').trigger('click')
        myModal.show()
    })
    $('#animation').click(function(){
        console.log("hh")
        var myModal = new bootstrap.Modal(document.getElementById('animation_modal'), {
          keyboard: false
        })
        myModal.show()
    })
});