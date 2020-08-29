jQuery(document).ready(function() {
    $(".clickable-row").click(function () {
    	let url = $("#url").attr("data-url");
    	let id = $(this).attr('data-id');

       document.location.href = url.replace('123', id);
    });


    $(".clickable-row .td_btn").click(function () {
    });


/*	$("#delID").onclick(function (e) {
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
            	console.log(data);
                // on successfull creating object
                // 1. clear the form.
                $("#addMess").trigger('reset');

                var instance = JSON.parse(response["newMes"]);
                var fields = instance[0]["fields"];


                }
        })
    })*/





});
