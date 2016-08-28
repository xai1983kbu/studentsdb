
$(document).ready( function() {
$("#button-load-more-students").click( function(event) {
$.ajax({
    type: "POST",
    url: "/ajax_students_load_more/",  /* http://localhost:8000 не вказую бо цей запит відсилається на той же хост  */
    data: { csrfmiddlewaretoken: CSRF_TOKEN,
          page:page,
          },
    success: success
})
function success(response) 
{ 
 if (page<=paginator_num_pages) { page = page+1;    $('#tbody-from-table-for-students').append(response);}
 if (page>paginator_num_pages) { $('#button-load-more-students').hide();}
}
});
});

/*$(document).ready( function() {
    $("#button-load-more-students").click( function(event) {
        alert("Load More");

        var p = $("#trtb").clone().appendTo("#tb");
            p.children()[0].innerHTML = "111"
            p.children()[1].innerHTML = "222"
            p.children()[2].innerHTML = "333"
            p.children()[3].innerHTML = "444"
            p.children()[4].innerHTML = "555"
            //p.children()[5]
            $(".dropdown:last").children('.dropdown-menu').children()[0].innerHTML = "<a href='http://127.0.0.1:8000/students/16/edit'>Редагувати</a>"
            $(".dropdown:last").children('.dropdown-menu').children()[1].innerHTML = "<a href='http://127.0.0.1:8000/students/16/edit'>Відвідування</a>"
            $(".dropdown:last").children('.dropdown-menu').children()[2].innerHTML = "<a href='http://127.0.0.1:8000/students/16/edit'>Видалити</a>"
         
            

    });
});*/

