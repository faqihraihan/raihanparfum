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

document.getElementById('item-response').addEventListener('change', function() {
  var items = document.querySelectorAll('.item');

  items.forEach(function(item) {
      item.style.display = 'none';

      var requiredInputs = item.querySelectorAll('select.required');
      requiredInputs.forEach(function(input) {
        input.removeAttribute('required');
      });
  });

  var selectedValue = this.value;

  if (selectedValue) {
      var itemToShow = document.getElementById('item' + selectedValue);
      if (itemToShow) {
          itemToShow.style.display = 'block';

          var requiredInputsToShow = itemToShow.querySelectorAll('select.required');
          requiredInputsToShow.forEach(function(input) {
            input.setAttribute('required', 'required');
          });
      }
  }
});

$('#item-response').click(function() {
    var barangResponse = $(this).val();
    var $parent = $(this).closest('.parent-response-class');

    $.ajax({
        type: "POST",
        url: "/database/barang/live-search",
        data: {
            'barang_response' : barangResponse
        },
        success: function(data){
            $parent.find('.barang-response').html(data);
            $parent.find('.barang-response').append(data.htmlresponse);
        },
    });
});