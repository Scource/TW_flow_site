jQuery(document).ready(function() {
    $(".clickable-row").click(function () {
    	let url = $("#url").attr("data-url");
    	let id = $(this).attr('data-id');

       document.location.href = url.replace('123', id);
    });

    $(".clickable-row_task").click(function () {
    	let url = $("#url").attr("data-url");
    	let id = $(this).attr('data-id');

       document.location.href = url.replace('123', id);
    });


    $("#toggle_filter").click(function(){
    $(".adv_filter").toggle();
    });


    $("#cor_template").click(function(){
    $(".cor_template").toggle();
    });


    $("#cor_template_new").click(function(){
    $(".cor_template_new").toggle();
    });
});
