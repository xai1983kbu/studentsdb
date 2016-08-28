$(document).ready( function() {
    $(window).scroll(function() {
if (page<=paginator_num_pages)
    { 
      
        if ($(window).scrollTop() == $(document).height() - $(window).height())
           {  
            $.ajax({
                type: "POST",
                url: "/ajax_students_scroll/",  /* http://localhost:8000 не вказую бо цей запит відсилається на той же хост  */
                data: { csrfmiddlewaretoken: CSRF_TOKEN,
                        page:page++,
                      },
                success: success
              });

                function success(response) { $('#tbody-from-table-for-students').append(response);   }
                                }
    }
});

/*Заповнюю window данними поки не з'явиться scroll */
$(window).scroll(); 
$(window).scroll(); 
$(window).scroll(); 
$(window).scroll();  

});



