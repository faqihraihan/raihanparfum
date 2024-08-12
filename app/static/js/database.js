$('.pabrik-response').click(function() {
    var pabrikResponse = $(this).val();
    var $parent = $(this).closest('.parent-response-class');

    $.ajax({
        type: "POST",
        url: "/database/aroma/live-search",
        data: {
            'pabrik_response' : pabrikResponse
        },
        success: function(data){
            $parent.find('.aroma-response').html(data);
            $parent.find('.aroma-response').append(data.htmlresponse);
        },
    });
});