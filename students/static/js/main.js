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
});
