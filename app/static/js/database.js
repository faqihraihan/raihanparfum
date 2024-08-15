document.addEventListener('DOMContentLoaded', function() {
    var backToTopButton = document.getElementById('back-to-top');

    window.addEventListener('scroll', function() {
      if (window.scrollY > 100) {
        backToTopButton.style.display = 'block';
      } else {
        backToTopButton.style.display = 'none';
      }
    });

    backToTopButton.addEventListener('click', function(e) {
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
});

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