$(document).ready(function(){
    
    $(".clickable-row").click(function () {
        let url = $("#url").attr("data-url");
        let id = $(this).attr('data-id');

       document.location.href = url.replace('123', id);
    });

    $(".clickable-row_task").click(function () {
        let url = $("#url-task").attr("data-url");
        let id = $(this).attr('data-id');

       document.location.href = url.replace('123', id);
    });


    $("#toggle_filter").click(function(){
    $(".adv_filter").toggle();
    });

    $("#toggle_filter_tasks").click(function(){
    $(".adv_filter_tasks").toggle();
    });

    $("#cor_template").click(function(){
    $(".cor_template").toggle();
    });


    $("#osdn_template").click(function(){
    $(".osdn_template").toggle();
    });


    $(document).ready(function(){
      $(".del").click(function(){
        if (!confirm("Czy na pewno usuąnć?")){
              return false;
            }
          });
        });


$("ul.dropdown li").hover(function(){
    
        $(this).addClass("hover");
        $('ul:first',this).css('visibility', 'visible');
    
    }, function(){
    
        $(this).removeClass("hover");
        $('ul:first',this).css('visibility', 'hidden');
    
    });

 jQuery(function ($) {
    var datepickerDict = {};
    var isBootstrap4 = $.fn.collapse.Constructor.VERSION.split('.').shift() == "4";
    function fixMonthEndDate(e, picker) {
        e.date && picker.val().length && picker.val(e.date.endOf('month').format('YYYY-MM-DD'));
    }
    $("[dp_config]:not([disabled])").each(function (i, element) {
        var $element = $(element), data = {};
        try {
            data = JSON.parse($element.attr('dp_config'));
        }
        catch (x) { }
        if (data.id && data.options) {
            data.$element = $element.datetimepicker(data.options);
            data.datepickerdata = $element.data("DateTimePicker");
            datepickerDict[data.id] = data;
            data.$element.next('.input-group-addon').on('click', function(){
                data.datepickerdata.show();
            });
            if(isBootstrap4){
                data.$element.on("dp.show", function (e) {
                    $('.collapse.in').addClass('show');
                });
            }
        }
    });
    $.each(datepickerDict, function (id, to_picker) {
        if (to_picker.linked_to) {
            var from_picker = datepickerDict[to_picker.linked_to];
            from_picker.datepickerdata.maxDate(to_picker.datepickerdata.date() || false);
            to_picker.datepickerdata.minDate(from_picker.datepickerdata.date() || false);
            from_picker.$element.on("dp.change", function (e) {
                to_picker.datepickerdata.minDate(e.date || false);
            });
            to_picker.$element.on("dp.change", function (e) {
                if (to_picker.picker_type == 'MONTH') fixMonthEndDate(e, to_picker.$element);
                from_picker.datepickerdata.maxDate(e.date || false);
            });
            if (to_picker.picker_type == 'MONTH') {
                to_picker.$element.on("dp.hide", function (e) {
                    fixMonthEndDate(e, to_picker.$element);
                });
                fixMonthEndDate({ date: to_picker.datepickerdata.date() }, to_picker.$element);
            }
        }
    });
    if(isBootstrap4) {
        $('body').on('show.bs.collapse','.bootstrap-datetimepicker-widget .collapse',function(e){
            $(e.target).addClass('in');
        });
        $('body').on('hidden.bs.collapse','.bootstrap-datetimepicker-widget .collapse',function(e){
            $(e.target).removeClass('in');
        });
    }
});
    });

