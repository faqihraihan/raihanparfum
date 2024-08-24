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

document.getElementById('searchForm').onsubmit = function(e) {
    e.preventDefault();
    var id_pelanggan = document.getElementById('id_pelanggan').value;
    if(id_pelanggan) {
        this.action = 'purchase_history/' + id_pelanggan;
        this.submit();
    }
};