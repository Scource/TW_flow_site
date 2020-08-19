jQuery(document).ready(function() {
    $(".clickable-row").click(function () {
    	let url = $("#url").attr("data-url");
    	let id = $(this).attr('data-id');

       document.location.href = url.replace('123', id);
    });


    $(".clickable-row .td_btn").click(function () {
    });



/*    $('.addComm').click(function(){ 
	let id; 
	id = $(this).attr("data-postid"); 
	let str;
	str = $('#mesinput').val();
	let us ;
	us = "{{user.id}}";
	$.ajax({ 
	    type:"POST", 
	    url: "if_add_message",
	    data: { 
	             post_id: id,
	             text : str,
	             auth : us,
	             csrfmiddlewaretoken : '{{csrf_token}}',
	}, 
	success: function(data) 
	{ alert("A user with this username already exists.") }
	}) });
*/


	$("#addMess").submit(function (e) {
        // preventing from page reload and default actions
        e.preventDefault();
        var us;
		us = "{{post.id}}";
		var data = $(this).serializeArray(); // convert form to array
		data.push({name: "post_id", value: $(this).attr('data-postid')});

        // make POST ajax call
        $.ajax({
            type: 'POST',
            url: "if_add_message",
            data: data,
            success: function (response) {
                // on successfull creating object
                // 1. clear the form.
                $("#addMess").trigger('reset');}

        })
    })





});
