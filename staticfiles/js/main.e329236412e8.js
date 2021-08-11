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


$(document).ready(function(){
    $('#trickset').on('change', function(){
        if ($('input[name=radioName]:checked', '#trickset').val() == 'custom') {
            $('#pick_tricks').prop('disabled', false)
        }
        else {
            open = $('#custom_collapse').is( ":visible" )
            if (open) {
                $('#pick_tricks').trigger('click')
            }
            $('#pick_tricks').attr('disabled', true)
        }
    })
    $('#generate').click(function(){
        var tricks = $('input[name=radioName]:checked', '#trickset').val();
        var length = $('#length').val();
        var stances = [];
        var custom_set = []
        $("input[name='stance']:checked").each(function(){
            stances.push(this.value);
        });
        var transitions = [];
        $("input[name='transition']:checked").each(function(){
            transitions.push(this.value);
        });
        if (tricks == 'custom') {
            $("input[name='trick']:checked").each(function(){
                custom_set.push(this.value);
            });
        }
        $.ajax({
            url: '/getcombo/',
            type: "POST",
            data: {
                trickset: tricks,
                stanceset: stances,
                transitionset: transitions,
                length: length,
                custom: custom_set
            },
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function (data) {
                $('#combo').text(data['combo']);
                $('#full').text(data['full']);
            },
            error: function (error) {
                console.log(error);
            }
        });
    });
});