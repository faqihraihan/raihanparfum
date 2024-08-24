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

function formatRupiah(value) {
  const angka = parseFloat(value);
  if (angka >= 1e12) {
      return 'Rp ' + (angka / 1e12) + ' T';
  } else if (angka >= 1e9) {
      return 'Rp ' + (angka / 1e9) + ' M';
  } else if (angka >= 1e6) {
      return 'Rp ' + (angka / 1e6) + ' Jt';
  } else if (angka >= 1e3) {
      return 'Rp ' + (angka / 1e3) + ' Ribu';
  } else {
      return 'Rp ' + angka.toLocaleString();
  }
}

fetch('/api/penjualan-sebulan')
    .then(response => response.json())
    .then(data => {
        const dates = data.map(entry => entry.date);
        const salesThisMonth = data.map(entry => entry.sale_this_month);
        const salesLastMonth = data.map(entry => entry.sale_last_month);

        const ctx = document.getElementById('sales-chart').getContext('2d');
        const salesChart = new Chart(ctx, {
            type: 'line',
            data: {
              labels: dates,
              datasets: [{
                data: salesThisMonth,
                backgroundColor: 'transparent',
                borderColor: '#17a2b8',
                pointBorderColor: '#17a2b8',
                pointBackgroundColor: '#17a2b8',
                fill: false
              },
              {
                data: salesLastMonth,
                backgroundColor: 'tansparent',
                borderColor: '#ced4da',
                pointBorderColor: '#ced4da',
                pointBackgroundColor: '#ced4da',
                fill: false
              }]
            },
            options: {
                maintainAspectRatio: false,
                responsive: true,
                legend: {
                    display: false,
                },
                tooltips: {
                  mode: 'index',
                  intersect: true,
                  callbacks: {
                    label: function(tooltipItem, data) {
                        var datasetLabel = data.datasets[tooltipItem.datasetIndex].label || '';
                        var value = tooltipItem.yLabel;
                        return datasetLabel + ': Rp. ' + value.toLocaleString();
                    }
                  }
                },
                hover: {
                  mode: 'index',
                  intersect: true
                },
                scales: {
                    xAxes: [{
                      gridLines: {
                        display: false
                      },
                      ticks: {
                        fontColor: '#adb5bd',
                        callback: function(value, index) {
                            // Menampilkan hanya setiap 2 nilai
                            return index % 2 === 0 ? value : '';
                        }
                            }
                    }],
                    yAxes: [{
                      gridLines: {
                        display: false
                      },
                      ticks: {
                        fontColor: '#adb5bd',
                        callback: function(value) {
                          return formatRupiah(value);
                        }
                      }
                    }]
                },

            }
        });
    })