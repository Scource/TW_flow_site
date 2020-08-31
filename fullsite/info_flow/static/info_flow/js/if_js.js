jQuery(document).ready(function() {
    $(".clickable-row").click(function () {
    	let url = $("#url").attr("data-url");
    	let id = $(this).attr('data-id');

       document.location.href = url.replace('123', id);
    });


    $(".clickable-row .td_btn").click(function () {
    });




});
