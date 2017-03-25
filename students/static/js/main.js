function initEditForm(modal, form){
    $(form).find('#submit-id-cancel_button').click(function(){
        modal.modal('hide');
        return false;
    });

    $(form).ajaxForm({
        'dataType': 'html',
        'error': function(){
            alert('Error on the server, please, try again a bit later');
        },
        'success': function(data, status, xhr){
            var html=$(data), form = html.find('#content-columns form');

            if (form.length > 0) {
                modal.find('.modal-body').html(html.find('#content-columns .alert'));
                modal.find('.modal-body').append(form);

                initEditForm(modal, form);

            } else {
                modal.find('.modal-body').html(html.find('#content-columns .alert'));
                setTimeout(function(){location.reload(true);}, 2000);

            }

        }
    });
}

function initEditPopup() {
    $('.editForm').click(function(){
        var modal = $('#myDialog');
        $.ajax({
            'url': $(this).attr('href'),
            'dataType': 'html',
            'error': function(xhr, status, error){
                alert('Error on the server, please try again a bit later.');
                //modal.modal('show');
            },
            'success': function(data, status, xhr){
                var html = $(data), form = html.find('#content-columns form');
                modal.find('.modal-title').html(html.find('#content-columns h2'));
                modal.find('.modal-body').html(form);
                console.log(form);
                initEditForm(modal, form);

                modal.modal('show');
            }
         });
        return false;
    });
}

function initGroups(){
    $('#group-select select').change(function(){
        var group =$(this).val();
        if (group) {
            $.cookie('current_group', group, { path: '/', expires: 365 });
        } else {
            $.removeCookie('current_group', { path: '/' });
        }

        location.reload(true);

        return true;

    });
}

function initJournal() {
    $('#journal-table input[type="checkbox"]').click(function(){
        // alert($(this).data('date'));
        var box = $(this);
        $.ajax(box.data('url'), {
            'method': 'post', 
            'async': true,
            'dataType': 'json',
            'data': {
                'student_id': box.data('student_id'),
                'date': box.data('date'),
                'present': box.is(':checked') ? '1' : '0',
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            'error': function(xhr, status, error){
                alert(error);
            },
            'success': function(data, status, xhr){
                // alert(data['status']);
            }
        });
    });
}


$(document).ready(function(){
    initJournal();
    initGroups();
    initEditPopup();
});
